#-*- encoding:utf-8 -*-
from django.http import HttpResponse

f1 = "/tmp/1.txt"
f2 = "/tmp/2.txt"
f3 = "/tmp/3.txt"
f4 = "/tmp/4.txt"

def write_file(filename, c):
    with open(filename, "w") as f:
        f.write(c)

def increase_file(filename, c):
    with open(filename, "a") as f:
        f.write(c)

class DefendAttackMiddleWare(object):
    def process_request(self, request):
        #count = request.session.get("avisit", 1)
        count = request.session["avisit"] if request.session.has_key("avisit") else 1
        write_file(f1, str(count))
        if int(count) > 100000:
            return HttpResponse("Forbiddeniiiii  %s" % count, status = 403)
        #request.session["avisit"] = request.session.get("avisit", 1) + 1
        request.session["avisit"] = count + 1
        write_file(f2, str(request.session["avisit"]))
        request.session.set_expiry(0)
        write_file(f3, str(request.session["avisit"]))
        #increase_file(f4, "\nprocess request\n")
        #return HttpResponse("bbbb" + str(request.session["avisit"]))


    def process_view(self, request, view_name, *args, **kwargs):
        return 
        #return HttpResponse("bbbb" + str(request.session["avisit"]))
        #increase_file(f4, "process view\n")
        #increase_file(f4, view_name.func_name)
        

    #def process_response(self, request, response):
        #return HttpResponse("这是中间件 process_response 方法返回的结果")
        #return HttpResponse("aaaaa" + str(request.session["avisit"]))
    
    
    def process_exception(self, request, exception):
        increase_file(f4, "cuole")
        increase_file(f4, str(exception))
        return HttpResponse(exception)
