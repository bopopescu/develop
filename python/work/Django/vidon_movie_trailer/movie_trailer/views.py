#-*- encoding:utf-8 -*-

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger

from models import Movie_Name, Movie_Info, Movie_Name_ZH, Movie_Info_ZH
import os
import logging

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

MOVIE_PATH = r"/mnt/nas/other/download_movie"
LOG_FILENAME = r"/home/goland/movie_trailer.log"
SPECIAL_CHARS_LIST = ['\\', '/', ':', '*', '?', '"','<', '>', '|', '+', ',', '.', ' ']

def log(info):
    logging.basicConfig(filename = LOG_FILENAME, level = logging.NOTSET, filemode = "a", format = "%(asctime)s : %(message)s")
    logging.info(info)


def paging(records, page):
    #使用分页类显示分页
    after_range_num, befor_range_num = 5, 4
    count = 20
    paginator = Paginator(records, count)
    #跳转至请求页面，如果该页面不存在或者超过则跳转至尾页
    try:
        records = paginator.page(page)
    except (EmptyPage, InvalidPage, PageNotAnInteger):
        page = paginator.num_pages
        records = paginator.page(page)
    if page >= after_range_num:
        page_range = paginator.page_range[page - after_range_num: page + befor_range_num]
    else:
        page_range = paginator.page_range[0: page + befor_range_num]
    return paginator, page_range, records


def search_result(movie_names, moviename):
    if moviename:
        movie_names = movie_names.extra(where = ["name like'%%" + moviename + "%%'"])
    return movie_names

def index_old(request):
    #below is session test
    #if "c" in request.session:
    #    request.session["c"] += 1
    #else:
    #    request.session["c"] = 1
    #return HttpResponse(request.session["c"])
    context = {}
    language = request.GET.get("language", "").strip()
    try:
        page = int(request.GET.get("page", "1").strip())
    except ValueError:
        page = 1
    movie_names = Movie_Name.objects.all()
    if language:
        movie_names = movie_names.filter(language=language)
    moviename = request.GET.get("moviename", "").strip()
    movie_names = search_result(movie_names, moviename)
    paginator, page_range, movie_names = paging(movie_names, page)
    context["page"] = page
    context["paginator"] = paginator
    context["page_range"] = page_range
    context["language"] = language
    context["moviename"] = moviename
    context["movie_names"] = movie_names
    return render_to_response("index.html", context)


def index(request):
    context = {}
    language = request.GET.get("language", "").strip()
    try:
        page = int(request.GET.get("page", "1").strip())
    except ValueError:
        page = 1
    movie_names = Movie_Name.objects.all()
    if language.lower() == "english":
        movie_names = Movie_Name.objects.all()
    elif language.lower() == "chinese":
        movie_names = Movie_Name_ZH.objects.all()
    #else:
    #    return HttpResponse("1111111111111111")
    moviename = request.GET.get("moviename", "").strip()
    movie_names = search_result(movie_names, moviename)
    paginator, page_range, movie_names = paging(movie_names, page)
    context["page"] = page
    context["paginator"] = paginator
    context["page_range"] = page_range
    context["language"] = language
    context["moviename"] = moviename
    context["movie_names"] = movie_names
    return render_to_response("index.html", context)


def display_movie_info_old(request, params):
    context = {}
    movie_name = Movie_Name.objects.get(id=params)
    movie_infos = movie_name.movie_name_set.all()
    context["movie_name"] = movie_name.name
    context["language"] = movie_name.language
    context["movie_infos"] = movie_infos
    #return HttpResponse(context["language"])
    return render_to_response("display_movie_info.html", context)


def display_movie_info(request, params):
    context = {}
    language = request.GET.get("language", "").strip()
    if language.lower() == "english":
        movie_name = Movie_Name.objects.get(id=params)
    elif language.lower() == "chinese":
        movie_name = Movie_Name_ZH.objects.get(id=params)
    
    movie_infos = movie_name.movie_name_set.all()
    context["movie_name"] = movie_name.name
    context["language"] = movie_name.language
    context["movie_infos"] = movie_infos
    #return HttpResponse(context["language"])
    return render_to_response("display_movie_info.html", context)

#download small file
def download_movie_small_file(request):
    movie_name = request.GET.get("movie_name", "").strip()
    language = request.GET.get("language", "").strip()
    if language.lower() == "chinese":
        parent_folder = "yugaopian"
    else:
        parent_folder = "movie_trailers"
    movie_name = dealwith_moviename(movie_name)
    movie_filename = request.GET.get("movie_filename", "")
    movie_file = os.path.join(os.path.join(os.path.join(MOVIE_PATH, parent_folder), movie_name), os.path.basename(movie_filename))
    #movie_file = movie_file.replace("Z:/other", "/mnt/nas/other")
    try:
        f = open(movie_file)
        data = f.read()
        f.close()
        response = HttpResponse(data, mimetype='application/octet-stream')
        response["Content-Length"] = os.path.getsize(movie_file)
        response["Content-Disposition"] = "attachment; filename=%s" % movie_file
        return response
    except Exception, e:
        failed_result = "Sorry, because of some reasons, download movie failed!"
        return HttpResponse(failed_result) 
        

#download big file
def read_big_file(filename, buf_size = 8192):
    with open(filename, "rb") as f:
        while 1:
            content = f.read(buf_size)
            if content:
                yield content
            else:
                break


def dealwith_moviename(movie_name):
    for each_char in SPECIAL_CHARS_LIST:
        if each_char in movie_name:
            movie_name = movie_name.replace(each_char, "_")
    return movie_name


def download_movie(request):
    movie_name = request.GET.get("movie_name", "").strip()
    language = request.GET.get("language", "").strip()
    if language.lower() == "chinese":
        parent_folder = "yugaopian"
    else:
        parent_folder = "movie_trailers"
    movie_name = dealwith_moviename(movie_name)
    movie_filename = request.GET.get("movie_filename", "").strip()
    try:
        movie_file = os.path.join(os.path.join(os.path.join(MOVIE_PATH, parent_folder), movie_name), os.path.basename(movie_filename))
        response = HttpResponse(read_big_file(movie_file), mimetype='application/octet-stream')
        response["Content-Length"] = os.path.getsize(movie_file)
        response["Content-Disposition"] = "attachment; filename=%s" % movie_file.encode("utf-8")
        return response
    except Exception, e:
        failed_result = "Sorry, because of some reasons, download movie failed!"
        return HttpResponse(failed_result) 


def download_movie1(request):
    from django.core.servers.basehttp import FileWrapper
    movie_name = request.GET.get("movie_name", "").strip()
    movie_name = dealwith_moviename(movie_name)
    language = request.GET.get("language", "").strip()
    if language.lower() == "chinese":
        parent_folder = "yugaopian"
    else:
        parent_folder = "movie_trailers"
    movie_filename = request.GET.get("movie_file", "")
    #movie_file = movie_file.replace("Z:/other", "/mnt/nas/other")
    movie_file = os.path.join(os.path.join(os.path.join(MOVIE_PATH, parent_folder), movie_name), os.path.basename(movie_filename))
    wrapper = FileWrapper(file(movie_file))
    response = HttpResponse(wrapper, content_type = "application/octet-stream") 
    response["Content-Length"] = os.path.getsize(movie_file)
    response["Content-Disposition"] = "attachment; filename=%s" % movie_file
    return response


"""
this method requires Django version 1.5 or above!!!

#use csv to downlaod big file
#import csv
#from django.utils.six.moves import range
#from django.http import StreamingHttpResponse

class Echo(object):
    # An object that implements just the write method of the file-like interface
    def write(self, value):
        #Write the value by returning it, instead of storing in a buffer
        return value

def download_movie(request):
    #A view that streams a large CSV file 
    #Generate a sequence of rows. The range is based on the maximum number of rows that can be handled by a single sheet in most spreadsheet applications
    rows = (["Row {0}".format(idx), str(idx)] for idx in range(65536))
    pseudo_buffer = Echo()
    writer = csv.writer(pseudo_buffer)
    response = StreamingHttpResponse((writer.writerow(row) for row in rows), content_type="text/csv")
    response["Content-Disposition"] = "attachment; filename='somefilename.csv'"
    return httpresponse

"""
