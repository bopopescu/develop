#-*- encoding:utf-8 -*-

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
import time
import datetime

from models import *

CUR_YEAR = time.strftime("%Y")


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


def index(request):
    context = {}
    context["CUR_YEAR"] = CUR_YEAR
    page_title = "查询中心"
    context["page_title"] = page_title
    authors = Author.objects.all()
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
        qs = Commit_Record.objects.filter(commit_time__gte = start_time).order_by("commit_time")
        commit_record = qs.filter(commit_time__lte = end_time)
        if not commit_record:
            commit_record = ""
            empty_message = "Sorry, but there is no result in default %d days!" % days
            context["empty_message"] = empty_message
            
    #只要有一个条件不为空
    else:
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
            qs0 = product_obj.commit_record.all().order_by("commit_time")
            package_nas_path = product_obj.package_nas_path
        except Product.DoesNotExist:
            product_obj = ""
            qs0 = Commit_Record.objects.all().order_by("commit_time")
            package_nas_path = ""
            
        try:
            project_obj = Project.objects.get(name = project)
        except Project.DoesNotExist:
            project_obj = ""
            
        search_dict = {}
        if author_obj:
            search_dict["author"] = author_obj
        #if product_obj:
        #    search_dict["product"] = product_obj
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
 
    if commit_record:
        #page, paginator, page_range, commit_record = fenye(request,commit_record)
        #使用分页类显示分页
        after_range_num = 5
        befor_range_num = 4
        try:
            page = int(request.GET.get("page", 1))
        except ValueError:
            page = 1
        paginator = Paginator(commit_record, 5)

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
        context["page"] = page
        context["paginator"] = paginator
        context["page_range"] = page_range
        
    #无论commit_record是否为空，都需要将值传到模板里面去    
    context["commit_record"] = commit_record
    return render_to_response("index.html", context)

                              
def fenye(request, commit_record):
    #使用分页类显示分页
    after_range_num = 5
    befor_range_num = 4
    try:
        page = int(request.GET.get("page", 1))
    except ValueError:
        page = 1
    paginator = Paginator(commit_record, 5)

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
    context = {}
    context["CUR_YEAR"] = CUR_YEAR
    page_title = "显示产品与工程对应列表"
    context["page_title"] = page_title
    products = Product.objects.all()
    context["products"] = products
    return render_to_response("display_product_project.html", context)


#添加产品与对应的工程
def add_product_project(request):
    context = {}
    context["CUR_YEAR"] = CUR_YEAR
    page_title = "添加产品与对应工程"
    context["page_title"] = page_title
    if request.method == "POST":
        product_name = request.POST.get("product_name", "").strip()
        builder_name = request.POST.get("builder_name", "").strip()
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
        
        if product_name and builder_name and project_name and package_nas_path:
            product = Product(name = product_name, builder_name = builder_name, \
                              project_name = project_name,package_nas_path = package_nas_path)
            product.save()

            if "," in project_name:
                project_name = project_name.replace(",", ";")
             
            #去除两边的空白符     
            project_name_list = [i.strip() for i in project_name.split(";")]
        
            for each_project in project_name_list:
                if each_project:
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
        builder_name = request.POST.get("builder_name", "").strip()
        project_name = request.POST.get("project_name", "").strip()
        package_nas_path = request.POST.get("package_nas_path", "").strip()
        product_record.update(name = product_name, builder_name = builder_name, project_name = project_name, package_nas_path = package_nas_path)
        return render_to_response("update_success.html", context)
        
    return render_to_response("update_product_project.html", context)











