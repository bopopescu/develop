#-*- coding:utf-8 -*-
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.paginator import Paginator,InvalidPage, EmptyPage,PageNotAnInteger


#用分页类分页显示
def fenye(request):
    sessions = Session.objects.all()
    after_range_num = 5      #当前页面之前显示5页
    befor_range_num = 4      #当前页面之后显示4页
    #如果请求的页码少于1或者类型错误，则跳转至第1页
    try:              
        page = int(request.GET.get("page",1))
        if page < 1:
            page = 1
    except ValueError:
        page = 1
    paginator = Paginator(sessions,50)   #设置sessions在每页显示的数量，这里为50

    #跳转至请求页面，如果该页不存在或者超过则跳转到尾页
    try:
        session_list = paginator.page(page)
    except (EmptyPage,InvalidPage,PageNotAnInteger):
        page = paginator.num_pages
        session_list = paginator.page(page)

    if page >= after_range_num:
        page_range = paginator.page_range[page - after_range_num : page + befor_range_num]
    else:
        page_range = paginator.page_range[0: page + befor_range_num]
    return render_to_response("test.html",locals())
	
	