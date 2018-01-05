from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from statisticalComparison import statisticalComparison
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        report = statisticalComparison.statisticalComparison(BASE_DIR+uploaded_file_url)
        fs.delete(filename)
        return render(request, 'statisticalAnalysis/simple_upload.html', {
            'uploaded_file_url': uploaded_file_url, 'report' : report
        })
    return render(request, 'statisticalAnalysis/simple_upload.html')