#-*- coding:utf-8 -*-
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from models import Session
from django.core.paginator import Paginator,InvalidPage, EmptyPage,PageNotAnInteger



"""
    用分页类分页显示，并点击标题进行排序，只不过有一个bug，就是点击标题链接时，无论之前sort值是多少，最后都会变成2，
    虽然说这个2是自己指定的，如果不指定的话,第一次点击标题链接没有反应。本意是想着sort值不变的
	这两个功能加在一个页面上，牵强的说也算是实现了。但是里面有一些自认为不可饶恕的bug，主要是逻辑问题。
	受限于脑力不足，暂时只能到这一步，以后继续优化.
"""
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

    ziduan = request.GET.get("ziduan","").strip()
    sort = request.GET.get("sort","").strip()
          
    paginator = Paginator(sessions,10)   #设置session在每页显示的数量，这里为10

    #跳转至请求页面，如果该页不存在或者超过则跳转到尾页
    try:
        session_list = paginator.page(page)     
    except (EmptyPage,InvalidPage,PageNotAnInteger):
        page = paginator.num_pages
        session_list = paginator.page(page)
        
    # 1 and "" 代表降序， 2代表升序      
    if ziduan == "index":
        #降序
        if sort == "1":
            #session_list不是一个list，而是一个类的对象
            session_list = paginator.page(page)
            session_list_new = session_list
            sort = "2"
        #升序
        elif sort == "2":
            session_list = paginator.page(page)
            #经过切片之后，才是一个list，session_list.object_list也是一个list
            session_list_new = session_list[::-1]
            sort = "1"
        else:
            session_list = paginator.page(page)
            session_list_new = session_list
            sort = "2"
            
    elif ziduan == "Num":
        #降序
        if sort == "1":
            #session_list不是一个list，而是一个类的对象
            session_list = paginator.page(page)
            session_list_new = session_list
            sort = "2"
        #升序
        elif sort == "2":
            session_list = paginator.page(page)
            #经过切片之后，才是一个list，session_list.object_list也是一个list
            session_list_new = session_list[::-1]
            sort = "1"
        else:
            session_list = paginator.page(page)
            session_list_new = session_list
            sort = "2"

    else:
        session_list = paginator.page(page)
        session_list_new = session_list
        sort = "2"

    if page >= after_range_num:
        page_range = paginator.page_range[page - after_range_num : page + befor_range_num]
    else:
        page_range = paginator.page_range[0: page + befor_range_num]
    return render_to_response("test.html",locals())


