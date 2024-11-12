import sys
from http.client import HTTPResponse
from django.core.files.storage import FileSystemStorage
from django.db.models.expressions import result
from django.http import HttpRequest
from django.shortcuts import render

def process_det_view(request: HttpRequest) -> HTTPResponse:
    a = request.GET.get("a", "")
    b = request.GET.get("b", "")
    result = a + b

    context = {
        "a": a,
        "b": b,
        "result": result,
    }
    return render(request, "requestdataapp/request-query-params.html", context=context)

def user_form(request: HttpRequest) -> HTTPResponse:
    return render(request, "requestdataapp/user-bio-form.html")

def handel_file_uploap(request: HttpRequest) -> HTTPResponse:
    if request.method == "POST" and request.FILES.get("myfile"):
        myfile = request.FILES["myfile"]
        fs = FileSystemStorage()
        print(myfile.size)
        if myfile.size > 1048576:
            print('ERROR, file size is more than 1 MB', file=sys.stderr)
            return render(request, "requestdataapp/error-message.html")
        else:
            filename = fs.save(myfile.name, myfile)
            print("saved file", filename)
    return render(request, "requestdataapp/file-upload.html")