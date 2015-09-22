#-*- encoding:utf-8 -*-
from django.shortcuts import render_to_response

"""
    排序，点击标题可以来回倒序正序地排序
"""

"""
    该函数以id字段为例子进行举例，sort为1时，正序排；sort为2时，倒序排序
"""

def sort(request):
    ziduan = request.GET.get("ziduan","").strip()
    sort = request.GET.get("sort","").strip()
    """   一定要注意，sort获取过来的时候是字符串，比较的时候要注意数据类型    """
    if ziduan == "id":
        if sort == "1" or sort == "":
            client = Client.objects.all().order_by(ziduan)
            sort = 2
        elif sort == "2":
            client = Client.objects.all().order_by("-" + ziduan)
            sort = 1
        else:
            client = Client.objects.all()
            sort = 1
    else:
        client = Client.objects.all()
        sort = 1
        
    context = {"request":request,
               "client":client,
               "sort":sort}

    return render_to_response('client.html', context)
