#-*- encoding:utf-8 -*-

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
from django.utils import simplejson

import logging
import time
import datetime
import subprocess
import os
from models import *
#import access_server

COMMIT_USER_LIST = ["王一","战广月","袁芳芳"]


CUR_YEAR = time.strftime("%Y")
TEMP_FILE = "/Users/DVDFab/goland_gitstats/product.txt"
LOG_FILENAME = "/Users/DVDFab/goland_gitstats/log.txt"
#记录log的函数，参数是log信息
def log(info):
    logging.basicConfig(filename = LOG_FILENAME, level = logging.NOTSET, filemode = 'a', format = '%(asctime)s : %(message)s')
    logging.info(info)


def format_date_time(src_date):
    from_list_time = src_date.split("-")  
    if len(from_list_time[1]) == 1:
        month = "0" + from_list_time[1]
    else:
        month = from_list_time[1]
    if len(from_list_time[2]) == 1:
        day = "0" + from_list_time[2]
    else:
        day = from_list_time[2]
    format_date = from_list_time[0] + "-" + month + "-" + day
    return format_date

def get_git_log(request):
    product = request.POST.get("product", "").strip()
    fp = open(TEMP_FILE, "w")
    fp.write(product)
    fp.close()
    return HttpResponse(product) 
    result = access_server()
    return render_to_response("get_git_log_success.html")


def show_project(request):
    product = request.POST.get("product", "")
    product_obj = Product.objects.get(name = product)
    project_list = product_obj.project_name.split(";")
    results = ''
    num = 0
    for each_project in sorted(project_list):
        if each_project:
            each_format_project = each_project.split(":")[1].split(".git")[0]
        num += 1
        #if num % 2 == 0:
        record = "<label><input type = 'checkbox' name = 'checkbox' value = '" + each_project + "' checked = 'checked' />" + each_format_project + "</label><br />"
        #else: 
        #    record = "<label><input type = 'checkbox' name = 'checkbox' value = '" + each_project + "' checked = 'checked' />" + each_format_project + "</label>" + "&nbsp;"*10
        results += record
    #results = "</table>"
    return HttpResponse(results, content_type = 'application/json')
    return HttpResponse(simplejson.dumps(results), content_type = 'application/json')

def index(request):
    context = {}
    context["CUR_YEAR"] = CUR_YEAR
    page_title = "查询中心"
    context["page_title"] = page_title
    authors = Author.objects.all().order_by("name")
    products = Product.objects.all()
    projects = Project.objects.all()
    context["authors"] = authors
    context["products"] = products
    context["projects"] = projects
    
    author = request.GET.get("author", "").strip()
    product = request.GET.get("product", "").strip()
    project = request.GET.get("project", "").strip()
    start_time = request.GET.get("start_time", "").strip()
    end_time = request.GET.get("end_time", "").strip()
    #如果所有条件为空，则只限定日期
    if not(author or product or start_time or end_time):
        end_time = time.strftime("%Y-%m-%d %H:%M:%S")
        #默认情况下只显示2天以内的log
        days = 2
        start_time = get_time(days)
        qs = Commit_Record.objects.filter(commit_time__gte = start_time).order_by("-commit_time")
        commit_record = qs.filter(commit_time__lte = end_time)
        if not commit_record:
            commit_record = ""
            empty_message = "Sorry, but there is no result in default %d days!" % days
            context["empty_message"] = empty_message
            
    #只要有一个条件不为空
    else:
        if product:
            checkbox_list = request.GET.getlist("checkbox")
            format_project_list = []
            for each_project in checkbox_list:
                each_format_project = each_project.split(":")[1].split(".git")[0]
                format_project_list.append(each_format_project)
            checkbox_url = ""
            for record in checkbox_list:
                checkbox_url += "checkbox="+record + "&"
            selected_project_list = request.GET.getlist("selected_project")
            #return HttpResponse(selected_project_list)
            url = request.get_full_path()
            if "&page=" in url:
                pass
            else:
                #cmd = "python /Users/DVDFab/goland_gitstats/analyze_log/webpage/run_git_log.py " + ";".join(checkbox_list)
                cmd = "python /Users/DVDFab/goland_gitstats/analyze_log/webpage/run_git_log.py " + product
                subprocess.call(cmd, cwd = "/Users/DVDFab/goland_gitstats/analyze_log/webpage", shell = True)
                #p = subprocess.Popen(cmd, cwd = "/Users/DVDFab/goland_gitstats/analyze_log/webpage",stdout = subprocess.PIPE, shell = True)
                #content = p.stdout.read()
                #fp = open("/Volumes/qqq.txt", "w")
                #fp.write(content)
                #fp.close()
        if start_time:
            start_time = format_date_time(start_time)
        if end_time:
            end_time = format_date_time(end_time)
        else:
            end_time = time.strftime("%Y-%m-%d %H:%M:%S")
            
        try:
            author_obj = Author.objects.get(name = author)
        except Author.DoesNotExist:
            author_obj = ""
            
        try:
            product_obj = Product.objects.get(name = product)
            qs0 = product_obj.commit_record.all().order_by("-commit_time")
            package_nas_path = product_obj.package_nas_path
        except Product.DoesNotExist:
            product_obj = ""
            qs0 = Commit_Record.objects.all().order_by("-commit_time")
            package_nas_path = ""
            
        try:
            project_obj = Project.objects.get(name = project)
        except Project.DoesNotExist:
            project_obj = ""
            
        search_dict = {}
        if author_obj:
            search_dict["author"] = author_obj
        if project_obj:
            search_dict["project"] = project_obj
        qs1 = qs0.filter(**search_dict)

        if start_time:
            if len(start_time) == 10:
                start_time += " 00:00:00"
            qs2 = qs1.filter(commit_time__gte = start_time)
        else:
            qs2 = qs1
                       
        if end_time:
            if len(end_time) == 10:
                end_time += " 23:59:59"
            commit_record = qs2.filter(commit_time__lte = end_time)
        else:
            commit_record = qs2
        #commit_record= qs1
        if not commit_record:
            commit_record = ""
            empty_message = "Sorry, but your search does not contain any result!"
            context["empty_message"] = empty_message
        context["author"] = author
        context["product"] = product
        context["project"] = project
        context["start_time"] = start_time
        context["end_time"] = end_time
        context["package_nas_path"] = package_nas_path
    if product and checkbox_list:   
        context["checkbox_list"] = checkbox_list
        commit_record_list, project_id_list = filter_commit_record(commit_record, checkbox_list) 
        if commit_record:
            commit_record = commit_record.filter(project_id__in = project_id_list)
        #commit_record = commit_record_list
        #context["selected_project_list"] = selected_project_list
        context["format_project_list"] = format_project_list
        context["checkbox_url"] = checkbox_url
    context["all_length"] = len(commit_record)
    if commit_record:
        page, paginator, page_range, commit_record = fenye(request,commit_record)
        sort, new_list_record_order = order_sort(request, commit_record)
        context["page"] = page
        context["paginator"] = paginator
        context["page_range"] = page_range
        context["sort"] = sort
        context["commit_record_order"] = new_list_record_order
        
    #无论commit_record是否为空，都需要将值传到模板里面去    
    context["commit_record"] = commit_record
    return render_to_response("index.html", context)


def order_sort(request, commit_record):
    ziduan = request.GET.get("ziduan", "").strip()
    sort = request.GET.get("sort", "").strip()
    new_list_param = []
    new_list_record = []
    new_list_record_order = []
    if ziduan:
        if ziduan == "id":
            for each_record in commit_record:
                new_list_record.append((each_record.id, each_record))
                new_list_param.append(each_record.id)
        elif ziduan == "author":
            for each_record in commit_record:
                author_obj = Author.objects.get(id=each_record.author_id)
                #new_list_record.append((each_record.author_id, each_record))
                new_list_record.append((author_obj.name, each_record))
                new_list_param.append(author_obj.name)
        elif ziduan == "project":
            for each_record in commit_record:
                project_obj = Project.objects.get(id=each_record.project_id)
                #new_list_record.append((each_record.project_id, each_record))
                new_list_record.append((project_obj.name, each_record))
                new_list_param.append(project_obj.name)
        elif ziduan == "branch_name":
            for each_record in commit_record:
                new_list_record.append((each_record.branch_name, each_record))
                new_list_param.append(each_record.branch_name)
        elif ziduan == "commit_time":
            for each_record in commit_record:
                new_list_record.append((each_record.commit_time, each_record))
                new_list_param.append(each_record.commit_time)
        elif ziduan == "commit_version":
            for each_record in commit_record:
                new_list_record.append((each_record.commit_version, each_record))
                new_list_param.append(each_record.commit_version)
        elif ziduan == "commit_message":
            for each_record in commit_record:
                new_list_record.append((each_record.commit_message, each_record))
                new_list_param.append(each_record.commit_message)
        new_list_param1 = sorted([i for i in set(new_list_param)])
        for i in new_list_param1:
            for j in new_list_record:
                if i in j:
                    new_list_record_order.append(j[1])
        if sort == "2":
            new_list_record_order = new_list_record_order[::-1]
            sort = "1"
        else:
            new_list_record_order = new_list_record_order
            sort = "2"
    else:
        new_list_record_order = commit_record
    return sort,new_list_record_order 
    


def filter_commit_record(commit_record, checkbox_list):
    commit_record_list = []
    project_id_list = []
    for each_record in checkbox_list:
        try:
            project_obj = Project.objects.get(name=each_record)
            project_id = project_obj.id
            project_id_list.append(project_id)
            if commit_record:
                commit_record_list.extend(commit_record.filter(project_id = project_id))
        except Project.DoesNotExist:
            pass
    return commit_record_list, project_id_list

                              
def fenye(request, commit_record):
    #使用分页类显示分页
    after_range_num = 5
    befor_range_num = 4
    try:
        page = int(request.GET.get("page", 1))
    except ValueError:
        page = 1
    paginator = Paginator(commit_record, 50)

    #跳转至请求页面，如果该页面不存在或者超过则跳转至尾页
    try:
        commit_record = paginator.page(page)
    except (EmptyPage, InvalidPage, PageNotAnInteger):
        page = paginator.num_pages
        commit_record = paginator.page(page)
    if page >= after_range_num:
        page_range = paginator.page_range[page - after_range_num: page + befor_range_num]
    else:
        page_range = paginator.page_range[0: page + befor_range_num]
    return page, paginator, page_range, commit_record


#获得时间
def get_time(days):
    t1 = time.localtime()#current date
    t2=datetime.datetime(t1[0],t1[1],t1[2],t1[3],t1[4],t1[5])   
    t3=t2-datetime.timedelta(days=days)
    t3=str(t3)
    return t3


#显示所有的作者
def display_author(request):
    context = {}
    context["CUR_YEAR"] = CUR_YEAR
    page_title = "显示所有作者"
    context["page_title"] = page_title
    authors = Author.objects.all()
    context["authors"] = authors
    return render_to_response("display_author.html", context)


#显示所有的工程
def display_project(request):
    context = {}
    context["CUR_YEAR"] = CUR_YEAR
    page_title = "显示所有工程"
    context["page_title"] = page_title
    projects = Project.objects.all()
    context["projects"] = projects
    return render_to_response("display_project.html", context)


#显示所有的产品与工程对应列表
def display_product_project(request):
    product_list = []
    context_all = {}
    context_all["CUR_YEAR"] = CUR_YEAR
    page_title = "显示产品与工程对应列表"
    context_all["page_title"] = page_title
    products = Product.objects.all()
    for each_product in products:
        context = {}
        product_id = each_product.id
        product_name = each_product.name
        product_project_name = each_product.project_name
        product_package_nas_path = each_product.package_nas_path
        product_project_name = " ; ".join([i.split(":")[1].split(".git")[0] for i in product_project_name.split(";") if i.strip()])
        context["product_id"] = product_id
        context["product_name"] = product_name
        context["product_project_name"] = product_project_name
        context["product_package_nas_path"] = product_package_nas_path
        product_list.append(context)
    context_all["product_list"] = product_list
    return render_to_response("display_product_project.html", context_all)


#添加产品与对应的工程
def add_product_project(request):
    context = {}
    context["CUR_YEAR"] = CUR_YEAR
    page_title = "添加产品与对应工程"
    context["page_title"] = page_title
    if request.method == "POST":
        product_name = request.POST.get("product_name", "").strip()
        #builder_name = request.POST.get("builder_name", "").strip()
        builder_name = ""
        project_name = request.POST.get("project_name", "").strip()
        package_nas_path = request.POST.get("package_nas_path", "").strip()

        try:
            product_record = Product.objects.get(name=product_name)
            product_id = product_record.id
            context["product_id"] = product_id
            page_title = "已经存在"
            context["page_title"] = page_title
            return render_to_response("exist.html", context)
        except Product.DoesNotExist:
            pass
        #product_record = Product.objects.filter(name=product_name)
        #if product_record:
        #    return render_to_response("exist.html", locals())
        
        #if product_name and builder_name and project_name and package_nas_path:
        if product_name and project_name and package_nas_path:
            if "," in project_name:
                project_name = project_name.replace(",", ";")
             
            product = Product(name = product_name, builder_name = builder_name, \
                              project_name = project_name,package_nas_path = package_nas_path)
            product.save()

            #去除两边的空白符     
            project_name_list = [i.strip() for i in project_name.split(";")]
        
            for each_project in project_name_list:
                if "@" in each_project and ":" in each_project and ".git" in each_project:
                    project = Project.objects.filter(name = each_project)
                    if not project:
                        project = Project(name = each_project)
                        project.save()
            return HttpResponseRedirect('/add_product_project/')
    return render_to_response("add_product_project.html", context)


#修改产品与对应的工程
def update_product_project(request, param):
    context = {}
    context["CUR_YEAR"] = CUR_YEAR
    context["param"] = param
    page_title = "修改产品与对应工程"
    context["page_title"] = page_title
    try:
        product_record = Product.objects.get(id = param)
        product_name = product_record.name
        builder_name = product_record.builder_name
        project_name = product_record.project_name
        package_nas_path = product_record.package_nas_path
    except Product.DoesNotExist:
        product_name = ""
        builder_name = ""
        project_name = ""
        package_nas_path = ""

    context["product_name"] = product_name
    context["builder_name"] = builder_name
    context["project_name"] = project_name
    context["package_nas_path"] = package_nas_path
        
    if request.method == "POST":
        context["CUR_YEAR"] = CUR_YEAR
        page_title = "修改成功"
        context["page_title"] = page_title
        product_record = Product.objects.filter(id = param)
        product_name = request.POST.get("product_name", "").strip()
        #builder_name = request.POST.get("builder_name", "").strip()
        project_name = request.POST.get("project_name", "").strip()
        package_nas_path = request.POST.get("package_nas_path", "").strip()
        if "," in project_name:
            project_name = project_name.replace(",", ";")
             
        product_record.update(name = product_name, builder_name = builder_name, project_name = project_name, package_nas_path = package_nas_path)
            

        #去除两边的空白符     
        project_name_list = [i.strip() for i in project_name.split(";")]
        
        for each_project in project_name_list:
            if "@" in each_project and ":" in each_project and ".git" in each_project:
                project = Project.objects.filter(name = each_project)
                if not project:
                    project = Project(name = each_project)
                    project.save()
        context["success_url"] = "display_product_project"
        return render_to_response("update_success.html", context)
        
    return render_to_response("update_product_project.html", context)




#显示所有测试结果
def display_test_result(request):
    context = {}
    context["CUR_YEAR"] = CUR_YEAR
    page_title = "显示所有测试结果"
    context["page_title"] = page_title
    test_results = Test_Result.objects.all()
    context["test_results"] = test_results
    return render_to_response("display_test_result.html", context)

#display details
def display_details(request, param):
    context = {}
    context["CUR_YEAR"] = CUR_YEAR
    page_title = "显示详细测试结果"
    context["page_title"] = page_title
    test_result = Test_Result.objects.get(id = param)
    context["test_result"] = test_result
    return render_to_response("display_details.html", context)
    

#add test result
def add_test_result(request):
    context = {}
    context["CUR_YEAR"] = CUR_YEAR
    context["commit_user_list"] = COMMIT_USER_LIST
    page_title = "添加新的测试结果"
    context["page_title"] = page_title
    products = Product.objects.all()
    context["products"] = products
    if request.method == "POST":
        commit_user = request.POST.get("commit_user", "")#.strip()
        product = request.POST.get("product", "")#.strip()
        package_name = request.POST.get("package_name", "")#.strip()
        package_path = request.POST.get("package_path", "")#.strip()
        plcore_branch = request.POST.get("plcore_branch", "")#.strip()
        changelog = request.POST.get("changelog", "")#.strip()
        verification_result = request.POST.get("verification_result", "")#.strip()
        remark_explantion = request.POST.get("remark_explantion", "")#.strip()
        supplement_explantion = request.POST.get("supplement_explantion", "")#.strip()
        if commit_user and product and package_name:
            test_result = Test_Result(commit_user = commit_user, product = product, package_name = package_name, package_path = package_path, \
                                      plcore_branch = plcore_branch, changelog = changelog, verification_result = verification_result, \
                                      remark_explantion = remark_explantion, supplement_explantion = supplement_explantion)
            test_result.save()
            return HttpResponseRedirect("/display_test_result/")
    return render_to_response("add_test_result.html", context)


#修改测试结果
def update_test_result(request, param):
    context = {}
    context["CUR_YEAR"] = CUR_YEAR
    context["param"] = param
    page_title = "修改测试结果"
    context["page_title"] = page_title
    test_result = Test_Result.objects.get(id = int(param))
    commit_user = test_result.commit_user
    product = test_result.product
    package_name = test_result.package_name
    package_path = test_result.package_path
    plcore_branch = test_result.plcore_branch
    changelog = test_result.changelog
    verification_result = test_result.verification_result
    remark_explantion = test_result.remark_explantion
    supplement_explantion = test_result.supplement_explantion

    context["commit_user"] = commit_user
    context["product"] = product
    context["package_name"] = package_name
    context["package_path"] = package_path
    context["plcore_branch"] = plcore_branch
    context["changelog"] = changelog
    context["verification_result"] = verification_result
    context["remark_explantion"] = remark_explantion
    context["supplement_explantion"] = supplement_explantion
    
    if request.method == "POST":
        page_title = "修改成功"
        context["page_title"] = page_title
        test_result_obj = Test_Result.objects.filter(id = param)
        commit_user = request.POST.get("commit_user", "")#.strip()
        product = request.POST.get("product", "")#.strip()
        package_name = request.POST.get("package_name", "")#.strip()
        package_path = request.POST.get("package_path", "")#.strip()
        plcore_branch = request.POST.get("plcore_branch", "")#.strip()
        changelog = request.POST.get("changelog", "")#.strip()
        verification_result = request.POST.get("verification_result", "")#.strip()
        remark_explantion = request.POST.get("remark_explantion", "")#.strip()
        supplement_explantion = request.POST.get("supplement_explantion", "")#.strip()
        if commit_user and product and package_name:
            test_result_obj.update(commit_user = commit_user, product = product, package_name = package_name, package_path = package_path, \
                                   plcore_branch = plcore_branch, changelog = changelog, verification_result = verification_result, \
                                   remark_explantion = remark_explantion, supplement_explantion = supplement_explantion)
            context["success_url"] = "display_test_result"
            return render_to_response("update_success.html", context)
    return render_to_response("update_test_result.html", context)
