#-*- encoding:utf-8 -*-

#standard lib
import os
import json
import time
import subprocess
import sys
reload(sys)
sys.setdefaultencoding("utf8")

#django lib
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.contrib.auth.models import User
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import resolve, reverse
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied
#3rd lib
from dwebsocket import require_websocket
import dwebsocket
from dwebsocket import *
import MySQLdb

#local lib
from models import *
from local_settings import *
import send_mail
#sys.path.append("/usr/local/lib/python2.7/dist-packages/django/contrib/admin/templates")

class RestfulApi(object):
    """ api接口函数 """
    def __init__(self, host, user, passwd, db):
        """ 初始化变量 """
        self.host = host
        self.user = user
        self.passwd = passwd
        self.db = db

    def connect_db(self):
        """ 连接数据库 """
        self.conn = MySQLdb.connect(host = self.host,
                                    user = self.user,
                                    passwd = self.passwd,
                                    db = self.db,
                                    charset = "utf8")
        self.cursor = self.conn.cursor()

    def get_product_id(self, product_name):
        """ 获得产品的id """
        select_sql = "select id from %s where name = '%s'" % ("publish_product", product_name)
        self.cursor.execute(select_sql)
        res = self.cursor.fetchone()
        if not res:
            return ""
        return res[0]

    def get_master_imagename(self, product_id):
        """ 回滚时获得master_imagename字段 """
        sql = "select master_imagename from %s where product_id = '%s' and pub_flag = '%s'" % ("publish_publish", product_id, "1") 
        self.cursor.execute(sql)
        res = self.cursor.fetchone()
        if not res:
            return ""
        return res[0]

    def update_master_imagename(self, master_imagename, product_id):
        """ 更新master_imagename字段 """
        sql = "update %s set master_imagename = '%s' where master_imagename = '' and product_id = '%s' and pub_status = '1' order by id DESC limit 1" % ("publish_publish", master_imagename, product_id) 
        self.cursor.execute(sql)

    def update_pub_flag(self, pub_flag, pub_status, product_id):
        """ 更新pub_flag字段 """
        pub_date = time.strftime("%Y-%m-%d %H:%M:%S")
        sql1 = "update %s set pub_flag = '%s' where product_id = '%s' and pub_flag = '%s'" % ("publish_publish", "0", product_id, "2")
        sql2 = "update %s set pub_flag = '%s', pub_status = '%s', pub_date = '%s' where product_id = '%s' and pub_flag = '1'" % ("publish_publish", pub_flag, pub_status, pub_date, product_id) 
        print "pub_flag is ", pub_flag, "pub_status is ", pub_status
        print sql1
        print sql2
        """ pub_status为3，表示发布成功; 4表示失败 """
        if pub_status == "3":
            self.cursor.execute(sql1)
        self.cursor.execute(sql2)

    def update_pre_imagename(self, pre_imagename, test_flag, product_id):
        """ 更新pre_imagename字段 """
        pub_date = time.strftime("%Y-%m-%d %H:%M:%S")
        sql = "update %s set pre_imagename = '%s', test_flag = '%s', pub_date = '%s', pub_status = '%s' where product_id = '%s' and pub_status = '0'" % ("publish_publish", pre_imagename, test_flag, pub_date, "1", product_id) 
        print sql
        self.cursor.execute(sql)

    def commit(self):
        """ 提交数据 """
        self.conn.commit()

    def rollback(self):
        """ 关闭 """
        self.conn.rollback()

    def close_db(self):
        """ 关闭数据库 """
        self.cursor.close()
        self.conn.close()

def check_params(standard_params_list, check_params_list):
    """ 检测参数, standard_params_list是标准的参数列表， check_params_list是待检测的版本"""
    for res in standard_params_list:
        if res not in check_params_list:
            return False
    return True


def update_db(rfa, func,  params, *args):
    """ 更新数据库操作 """
    product_id = rfa.get_product_id(params["product_name"])
    if product_id:
	try:
	    func(*args + (product_id,))
	    rfa.commit()
	    ret = {"result": "success"}
	except Exception, e:
	    rfa.rollback()
	    ret = {"reason": "update db error : %s" % str(e)}
    else:
	ret = {"season": "can not find the given product in table"}
    return ret

@csrf_exempt
def update_pre_imagename(request):
    if request.method == "POST":
        params = json.loads(request.POST.keys()[0])
        ret = check_params(["pre_imagename", "test_flag", "product_name"], params.keys())
        rfa = RestfulApi(DB_HOST, DB_USER, DB_PASSWD, DB_NAME)
        rfa.connect_db()
        if not ret:
            ret = {"season": "params are not right"}
        else:
            ret = update_db(rfa, rfa.update_pre_imagename,  params, *(params["pre_imagename"], params["test_flag"]))
        rfa.close_db()
        return HttpResponse(json.dumps(ret))
    return HttpResponse("request method must be POST; Your method is %s" % request.method)

@csrf_exempt
def update_pub_flag(request):
    if request.method == "POST":
        params = json.loads(request.POST.keys()[0])
        ret = check_params(["pub_flag", "pub_status", "product_name"], params.keys())
        rfa = RestfulApi(DB_HOST, DB_USER, DB_PASSWD, DB_NAME)
        rfa.connect_db()
        if not ret:
            ret = {"season": "params are not right"}
        else:
            ret = update_db(rfa, rfa.update_pub_flag,  params, *(params["pub_flag"], params["pub_status"]))
        rfa.close_db()
        return HttpResponse(json.dumps(ret))
    return HttpResponse("request method must be POST; Your method is %s" % request.method)

@csrf_exempt
def update_master_imagename(request):
    if request.method == "POST":
        params = json.loads(request.POST.keys()[0])
        ret = check_params(["master_imagename", "product_name"], params.keys())
        rfa = RestfulApi(DB_HOST, DB_USER, DB_PASSWD, DB_NAME)
        rfa.connect_db()
        if not ret:
            ret = {"season": "params are not right"}
        else:
            ret = update_db(rfa, rfa.update_master_imagename,  params, *(params["master_imagename"],))
        rfa.close_db()
        return HttpResponse(json.dumps(ret))
    return HttpResponse("request method must be POST; Your method is %s" % request.method)

"""
@csrf_exempt
def update_pre_imagename_old(request):
    if request.method == "POST":
        params = json.loads(request.POST.keys()[0])
        ret = check_params(["pre_imagename", "test_flag", "product_name"], params.keys())
        if not ret:
            ret = {"season": "params are not right"}
        else:
            rfa = RestfulApi(DB_HOST, DB_USER, DB_PASSWD, DB_NAME)
            rfa.connect_db()
            product_id = rfa.get_product_id(params["product_name"])
            if product_id:
                try:
                    rfa.update_pre_imagename(params["pre_imagename"], params["test_flag"], product_id)
                    rfa.commit()
                    ret = {"result": "success"}
                except Exception, e:
                    rfa.rollback()
                    ret = {"reason": "update db error : %s" % str(e)}
            else:
                ret = {"season": "can not find the given product in table"}
            rfa.close_db()
        return HttpResponse(json.dumps(ret))
    return HttpResponse("request method must be POST; Your method is %s" % request.method)

@csrf_exempt
def update_pub_flag_old(request):
    if request.method == "POST":
        params = json.loads(request.POST.keys()[0])
        ret = check_params(["pub_flag", "product_name"], params.keys())
        if not ret:
            ret = {"season": "params are not right"}
        else:
            rfa = RestfulApi(DB_HOST, DB_USER, DB_PASSWD, DB_NAME)
            rfa.connect_db()
            product_id = rfa.get_product_id(params["product_name"])
            if product_id:
                try:
                    rfa.update_pub_flag(params["pub_flag"], product_id)
                    rfa.commit()
                    ret = {"result": "success"}
                except Exception, e:
                    rfa.rollback()
                    ret = {"reason": "update db error : %s" % str(e)}
            else:
                ret = {"season": "can not find the given product in table"}
            rfa.close_db()
        return HttpResponse(json.dumps(ret))
    return HttpResponse("request method must be POST; Your method is %s" % request.method)

@csrf_exempt
def update_master_imagename_old(request):
    if request.method == "POST":
        params = json.loads(request.POST.keys()[0])
        ret = check_params(["master_imagename", "product_name"], params.keys())
        if not ret:
            ret = {"season": "params are not right"}
        else:
            rfa = RestfulApi(DB_HOST, DB_USER, DB_PASSWD, DB_NAME)
            rfa.connect_db()
            product_id = rfa.get_product_id(params["product_name"])
            if product_id:
                try:
                    rfa.update_master_imagename(params["master_imagename"], product_id)
                    rfa.commit()
                    ret = {"result": "success"}
                except Exception, e:
                    rfa.rollback()
                    ret = {"reason": "update db error : %s" % str(e)}
            else:
                ret = {"season": "can not find the given product in table"}
            rfa.close_db()
        return HttpResponse(json.dumps(ret))
    return HttpResponse("request method must be POST; Your method is %s" % request.method)
"""

@csrf_exempt
def get_master_imagename(request):
    if request.method == "POST":
        params = json.loads(request.POST.keys()[0])
        ret = check_params(["product_name"], params.keys())
        if not ret:
            ret = {"season": "params are not right"}
        else:
            rfa = RestfulApi(DB_HOST, DB_USER, DB_PASSWD, DB_NAME)
            rfa.connect_db()
            product_id = rfa.get_product_id(params["product_name"])
            if product_id:
                master_imagename = rfa.get_master_imagename(product_id)
                ret = {"master_imagename": master_imagename}
            else:
                ret = {"season": "can not find the given product in table"}
            rfa.close_db()
        return HttpResponse(ret[ret.keys()[0]])
        #return HttpResponse(json.dumps(ret))
    return HttpResponse("request method must be POST; Your method is %s" % request.method)

def list_dir(path):
    """ 列出当前目录中的子目录 """
    return [os.path.join(path, i) for i in os.listdir(path) if os.path.isdir(os.path.join(path, i))]

def sort_list(the_list):
    """ 二维列表，根据每个元素的第一个数值进行排序，返回以第二个数值组成的列表 """
    tmp_list = [i[0] for i in the_list]
    sorted_list = [the_list[tmp_list.index(i)][1] for i in sorted(tmp_list)[::-1]]
    return sorted_list

def start_jenkins(url, username = "jenkins", password = "123.com"):
    """ 启动jenkins自动流程 """
    cmd = "curl -u%s:%s %s" % (username, password, url)
    os.system(cmd)

def superuser_required(user, login_url = None, raise_exception = False):
    """ 判断是否是超级用户 """
    if user.is_superuser:
        return True
    return False

def forbidden(request):
    return HttpResponse("Forbidden", status = 403)

@login_required
@csrf_exempt
def index(request):
    """ 首页 """
    print request.COOKIES
    publish_list = []
    pub_user = request.user.last_name + request.user.first_name
    if not pub_user:
        pub_user = request.user.username
    if request.user.is_superuser:
        product_list = [i.name for i in Product.objects.all()]
    else:
        product_list = [i.product.name for i in Product_Management.objects.filter(username = pub_user)]
    product_list = [i for i in set(product_list)]
    for each_product in product_list:
       record_list = Publish.objects.filter(product__name = each_product)#, pub_user = pub_user)
       if not request.user.is_superuser:
           record_list = record_list.filter(pub_user = pub_user)
       if record_list:
           record = record_list[0]
           #publish_list.append((record.pub_date, record))
           publish_list.append((int(record.id), record))
    publish_list = sort_list(publish_list)
    if request.method == "POST":
        product = request.POST.get("product", "").strip()
        pub_date = time.strftime("%Y-%m-%d %H:%M:%S")
        if product:
            product_obj = Product.objects.get(name = product)
            jenkins_test_url = product_obj.jenkins_test_url
            publish_obj = Publish(product = product_obj, pub_user = pub_user, pub_date = pub_date, pub_status = 0)
            publish_obj.save()
            start_jenkins(jenkins_test_url)
            #send_mail.main("更新代码", "亲爱的%s，您已成功更新 %s 代码" % (pub_user.encode("utf-8"), product.encode("utf-8")), [request.user.email])
            return HttpResponseRedirect("/")
    context = {"request": request, "inner_failed_user_list": inner_failed_user_list, "pub_user": pub_user, "publish_list": publish_list, "product_list": product_list}
    return render_to_response("index.html", context)


@login_required
@user_passes_test(superuser_required, login_url = "/forbidden/")
@csrf_exempt
def add_product(request):
    context = {"request": request}
    if request.method == "POST":
        product = request.POST.get("product", "").strip()
        jenkins_test_url = request.POST.get("jenkins_test_url", "").strip()
        jenkins_publish_url = request.POST.get("jenkins_publish_url", "").strip()
        if product and jenkins_test_url and jenkins_publish_url:
            pro_obj = Product.objects.filter(name = product)
            context["product"] = product
            context["jenkins_test_url"] = jenkins_test_url
            context["jenkins_publish_url"] = jenkins_publish_url
            if not pro_obj:
                product_obj = Product(name = product, jenkins_test_url = jenkins_test_url, jenkins_publish_url=jenkins_publish_url)
                product_obj.save()
                return HttpResponseRedirect("/show_product/")
            else:
                prompt = "该产品已存在"
                context["prompt"] = prompt
    return render_to_response("add_product.html", context)

@login_required
@user_passes_test(superuser_required, login_url = "/forbidden/")
@csrf_exempt
def add_product_management(request):
    """ 添加产品与人员的对应关系 """
    user_obj = User.objects.all()
    user_list = set([(i.last_name + i.first_name) for i in user_obj if (i.last_name + i.first_name)])
    product_list = [i.name for i in Product.objects.all()]
    context = {"request": request, "product_list": product_list, "user_list": user_list}
    if request.method == "POST":
        user = request.POST.get("user", "").strip()    
        product = request.POST.get("product", "").strip()   
        if user and product:
            #if not Product_Management.objects.filter(username = user, product = product):
            if Product_Management.objects.filter(username = user, product__name = product).count() == 0:
                pro_obj = Product.objects.get(name = product)
                pm_obj = Product_Management(username = user, product = pro_obj)
                pm_obj.save()
                return HttpResponseRedirect("/add_product_management/")
            else:
                return HttpResponse("已存在")
    return render_to_response("add_product_management.html", context)

@login_required
@csrf_exempt
def search_product_management(request):
    """ 查询对应关系 """
    current_user = request.user.last_name + request.user.first_name
    user_obj = User.objects.all()
    user_list = set([(i.last_name + i.first_name) for i in user_obj if (i.last_name + i.first_name)])
    context = {"request": request, "user_list": user_list}
    if request.method == "POST":
        search_user = request.POST.get("user", "").strip()
        last_name = search_user[:1]
        first_name = search_user[1:]
        search_user_obj = User.objects.filter(last_name = last_name, first_name = first_name)
        if any([obj.is_superuser for obj in search_user_obj]):
        #if search_user_obj.is_superuser:
            pro_obj = Product.objects.all()
            product_list = [i.name for i in pro_obj]
        else:
            pm_obj = Product_Management.objects.filter(username = search_user)
            product_list = [i.product.name for i in pm_obj]
        context["product_list"] = product_list
        context["search_user"] = search_user 
    return render_to_response("search_product_management.html", context)

def fenye(request, record_list, after_range_num = 5, befor_range_num = 4, each_page_num = 20):
    """ 分页 """
    try:
        page = int(request.GET.get("page", "1").strip())
    except ValueError:
        page = 1
    paginator = Paginator(record_list, each_page_num)
    try:
        record_list = paginator.page(page)
    except (EmptyPage, InvalidPage, PageNotAnInteger):
        page = paginator.num_pages
        record_list = paginator.page(page)
    if page >= after_range_num:
        page_range = paginator.page_range[page - after_range_num: page + befor_range_num]
    else:
        page_range = paginator.page_range[0: page + befor_range_num]
    return page, paginator, page_range, record_list

@login_required
@user_passes_test(superuser_required, login_url = "/forbidden/")
def show_product(request):
    """ 展示产品列表 """
    product_list = Product.objects.all()
    #product_list = Product.objects.get_query_set()
    context = {"request": request, "product_list": product_list}
    return render_to_response("show_product.html", context)

@login_required
@user_passes_test(superuser_required, login_url = "/forbidden/")
@csrf_exempt
def update_product(request, params):
    """ 修改产品 """
    pro_obj = Product.objects.get(id = params)
    context = {"request": request, "pro_obj": pro_obj}
    if request.method == "POST":
        product = request.POST.get("product", "").strip()
        jenkins_test_url = request.POST.get("jenkins_test_url", "").strip()
        jenkins_publish_url = request.POST.get("jenkins_publish_url", "").strip()
        if product and jenkins_test_url and jenkins_publish_url:
            pro_obj.name = product
            pro_obj.jenkins_test_url = jenkins_test_url
            pro_obj.jenkins_publish_url = jenkins_publish_url
            pro_obj.save()
            return HttpResponseRedirect("/show_product/")
    return render_to_response("update_product.html", context)

@login_required
@user_passes_test(superuser_required, login_url = "/forbidden/")
@csrf_exempt
def delete_product(request, params):
    """ 删除产品 """
    pro_obj = Product.objects.get(id = params)
    pro_obj.delete()
    return HttpResponseRedirect("/show_product/")

@login_required
@user_passes_test(superuser_required, login_url = "/forbidden/")
@csrf_exempt
def delete_product_management(request):
    """ 删除产品 """
    product = request.GET.get("product", "").strip()
    user = request.GET.get("user", "").strip()
    prom_obj = Product_Management.objects.filter(username = user, product__name = product)
    prom_obj.delete()
    return HttpResponseRedirect("/search_product_management/")

@login_required
def show_history(request):
    """ 展示指定产品的历史记录 """
    pub_user = request.user.last_name + request.user.first_name
    uid = request.user.id
    pub_user = request.user.last_name + request.user.first_name
    product = request.GET.get("product", "").strip()
    publish_list = Publish.objects.filter(product__name = product)
    if not request.user.is_superuser:
        publish_list = publish_list.filter(pub_user = pub_user)
    page, paginator, page_range, publish_list = fenye(request, publish_list)
    context = {"request": request, "pub_user": pub_user, "inner_failed_user_list": inner_failed_user_list,"product": product, "publish_list": publish_list, "page": page, "paginator": paginator, "page_range": page_range}
    return render_to_response("show_history.html", context)

def create_link(ip, src, dst):
    """ 创建链接 """
    cmd = "ln -s %s %s" % (src, dst)
    exec_ansible_cmd(ip, cmd)

@login_required
@csrf_exempt
def publish_revert(request, params):
    """ 发布或者回滚代码 """
    """ 更新发布状态，完成发布:这里只修改pub_flag为1，然后满潇就可以操作这条记录了，将其他的记录的pub_flag置为0，然后该条记录的pub_flag置为2 """
    publish_obj = Publish.objects.get(id = params)
    product = publish_obj.product.name
    changelog1 = request.POST.get("changelog", "").strip()
    changelog2 = request.GET.get("changelog", "").strip()
    changelog = changelog1 if changelog1 else changelog2
    jenkins_publish_url = publish_obj.product.jenkins_publish_url
    pub_user = request.user.last_name + request.user.first_name
    if not pub_user:
        pub_user = request.user.username
    publish_obj.pub_user = pub_user
    publish_obj.pub_date = time.strftime("%Y-%m-%d %H:%M:%S")
    publish_obj.pub_status = 2
    publish_obj.pub_flag = 1
    publish_obj.changelog = changelog
    publish_obj.save()
    start_jenkins(jenkins_publish_url)
    #send_mail.main("发布代码", "亲爱的%s，您已成功发布 %s 的代码" % (pub_user.encode("utf-8"), product.encode("utf-8")), [request.user.email])
    return HttpResponseRedirect("/show_history/?product=%s" % product)


def defend_attack(func):
    """ 装饰器，session不过期的前提下，登录页面访问次数超过1000，则禁止访问 """
    def _deco(request, *args, **kwargs):
        if request.session.get("visit", 1) > 1000:
            return HttpResponse("<h1>Forbidden</h1>", status = 403)
        request.session.set_expiry(0)   #设置为0，表示session会在浏览器关闭时过期
        request.session["visit"] = request.session.get("visit", 0) + 1
        return func(request, *args, **kwargs)
    return _deco

@csrf_exempt
@defend_attack
def login(request, template_name = "login.html"):
    """ 登录 """
    if request.session.has_key("username"):
        return HttpResponseRedirect("/")
    context = {}
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()
        user = auth.authenticate(username = username, password = password)
        if user is not None:
            auth.login(request, user)
            request.session["username"] = username
            return HttpResponseRedirect("/")
        else:
            failed_prompt = "用户名和密码不匹配!"
            context = {"username": username, "password": password, "failed_prompt": failed_prompt}
    return render_to_response(template_name, context) 

def logout(request):
    """ 登出 """
    auth.logout(request)
    return HttpResponseRedirect(reverse("login_name"))

