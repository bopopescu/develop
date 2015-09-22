#-*- encoding:utf-8 -*-
from django.shortcuts import render_to_response

"""
    排序，点击标题可以来回倒序正序地排序
"""

"""
    该函数只是以id字段为例子进行举例，desc为1时，正序排；desc为2时，倒序排
"""

def sort(request):
    ziduan = request.GET.get("ziduan","").strip()
    desc = request.GET.get("desc","").strip()
    """   一定要注意，desc获取过来的时候是字符串，比较的时候要注意数据类型    """
    if ziduan == "id":
        if desc == "1" or desc == "":
            client = Client.objects.all().order_by(ziduan)
            desc = 2
        elif desc == "2":
            client = Client.objects.all().order_by("-" + ziduan)
            desc = 1
        else:
            client = Client.objects.all()
            desc = 1
    else:
        client = Client.objects.all()

    return render_to_response('client.html', locals())
