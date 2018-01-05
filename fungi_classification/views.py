# -*- coding: utf-8 -*-
import time
import datetime
from django.views.decorators.csrf import csrf_exempt
from django.template import loader
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
import numpy as np
import urllib
import cv2
from overfeat.predict import categoryOfFungiImage as categoryOfFungiImageUsingOverfeat
from overfeatwithcontrol.predict import categoryOfFungiImage as categoryOfFungiImageUsingOverfeatWithControl
from googlenetwithcontrol.predict import categoryOfFungiImage as categoryOfFungiImageUsingGoogleNetWithControl
from googlenet.predict import categoryOfFungiImage as categoryOfFungiImageUsingGoogleNet
from overfeat.model.overfeat import OverfeatExtractor
from googlenet.model.googlenet import GoogleNetExtractor
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import json
import os
import zipfile
from mvc.forms import Formulario, Formulario2, FormularioZip
import requests
from mvc.models import ImagenyPrediccion, ObjetoFungi
from bs4 import  BeautifulSoup



oe = OverfeatExtractor()
#ge = GoogleNetExtractor()

def error(request):
    mensaje = '404 Not Found'
    return render(request, 'FungiClassification/error.html', {'mensaje': mensaje})

def index(request):
    template = loader.get_template("FungiClassification/index.html")
    #GESTION De lA SeSION
    try:
        if request.session.has_key('list'):
            del request.session['list']
        if request.session.has_key('imagenCont'):
            del request.session['imagenCont']
        if request.session.has_key('nombrezip'):
            del request.session['nombrezip']
        if request.session.has_key('listN'):
            del request.session['listN']
        if request.session.has_key('imagenes'):
            del request.session['imagenes']
        return render(request, 'FungiClassification/index.html')
    except ValueError:
        mensaje = '404 Not Found'
        return render(request, 'FungiClassification/error.html', {'mensaje': mensaje})
    except UnboundLocalError:
        mensaje = '404 Not Found'
        return render(request, 'FungiClassification/error.html', {'mensaje': mensaje})


def predictFungiClassUsingOverfeatViewGUI(request):
    if request.method == 'POST':
            form = Formulario(request.POST, request.FILES)
            if form.is_valid():
                data = {"success": False}
                image = _grab_image(stream=request.FILES["image"])
                # predict the class of the fungi image
                prediction = categoryOfFungiImageUsingOverfeat(image, oe)

                fileName = request.FILES['image'].name
                nombre = fileName.split('.')[0]
                myfile = request.FILES['image']
                fs = FileSystemStorage()
                extension = myfile.name[myfile.name.rfind("."):]
                ts = time.time()
                st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d-%H-%M-%S')
                fileName = fs.save("fungi-classification/" + st + extension, myfile)
                list = [fileName, prediction, nombre]
                listaPred = []
                listaPred.append(list)
                request.session['list']=listaPred
                request.session['imagenCont'] = None
                request.session['zip'] = None

                request.session['url'] = '/fungi_classification/predictFungiClass/'
                return HttpResponseRedirect('/fungi_classification/predictFungiClass/result/')
    else:
        form = Formulario()

    return render(request, 'FungiClassification/formImage.html')


def predictFungiClassUsingOverfeatViewControlGUI(request):
    if request.method == 'POST':
            form = Formulario(request.POST, request.FILES)
            if form.is_valid():
                data = {"success": False}
                image = _grab_image(stream=request.FILES["image"])
                imageControl = _grab_image(stream=request.FILES["imageControl"])
                # predict the class of the fungi image
                prediction = categoryOfFungiImageUsingOverfeatWithControl(image, imageControl, oe)

                fileName = request.FILES['image'].name
                nombre = fileName.split('.')[0]
                myfile = request.FILES['image']
                fs = FileSystemStorage()
                extension = myfile.name[myfile.name.rfind("."):]
                ts = time.time()
                st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d-%H-%M-%S')
                fileName = fs.save("fungi-classification/" + st + extension, myfile)
                list = [fileName, prediction, nombre]
                listaPred = []
                listaPred.append(list)
                request.session['list']=listaPred

                myfile = request.FILES['imageControl']
                fs = FileSystemStorage()
                extension = myfile.name[myfile.name.rfind("."):]
                ts = time.time()
                st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d-%H-%M-%S')
                fileNameControl = fs.save("fungi-classification/" + st + extension, myfile)
                request.session['imagenCont'] = fileNameControl
                request.session['zip'] = None

                request.session['url'] = '/fungi_classification/predictFungiClassControl/'
                return HttpResponseRedirect('/fungi_classification/predictFungiClass/result/')
    else:
        form = Formulario()

    return render(request, 'FungiClassification/formImageWithControl.html')

def predictFungiClassUsingOverfeatViewZIPControlGUI(request):
    if request.method == 'POST':
        zip_file = request.FILES['zip']
        if (zip_file is None):
            error = 'Select a zip file'
            return render(request, 'FungiClassification/formZip.html', {'error': error})
        fileName = zip_file.name
        if (fileName.endswith('.zip') == False):
            error = 'The file is not a zip file'
            return render(request, 'FungiClassification/formZipControl.html',{'error':error})



        fs = FileSystemStorage()
        extension = zip_file.name[zip_file.name.rfind("."):]
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d-%H-%M-%S')
        fs.save("zip-files/" + st + extension, zip_file)
        zip_ref = zipfile.ZipFile(MEDIA_URL + "/zip-files/" + st + extension, 'r')
        zip_ref.extractall("media/zip-files/" + st)
        zip_ref.close()
        fs.delete("zip-files/" + st + extension)
        (_, files) = fs.listdir("zip-files/" + st)
        if (not(files.__contains__('control.jpg'))):
            error = 'The zip file should contain a file called control.jpg'
            return render(request, 'FungiClassification/formZipControl.html', {'error': error})


        predictions = [(file,
                        categoryOfFungiImageUsingOverfeatWithControl(_grab_image(path="media/zip-files/" + st + "/" + file),
                                                                     _grab_image("media/zip-files/" + st + "/control.jpg"),oe)) for file in files
                                                                     if file != "control.jpg"]

        request.session['list'] = [["../../../media/zip-files/" + st + "/"+img, pred, img[img.rfind('/')+1:]] for (img, pred) in predictions]
        request.session["imagenes"] = ["../../../media/zip-files/" + st + "/"+img for (img, _) in predictions]
        request.session['imagenCont'] = "../../../media/zip-files/" + st + "/control.jpg"
        request.session['zip'] = True
        request.session['url'] = '/fungi_classification/predictFungiClassControl/zip/'
        return HttpResponseRedirect('/fungi_classification/predictFungiClass/result/')
    else:
        return render(request, 'FungiClassification/formZipControl.html')

def about(request):
    return render(request,'FungiClassification/about.html')

def tutorial(request):
    return render(request,'FungiClassification/tutorial.html')

def predictFungiClassUsingOverfeatViewZIPGUI(request):
    if request.method == 'POST':
        zip_file = request.FILES['zip']
        fileName = zip_file.name
        if (zip_file is None):
            error = 'Select a zip file'
            return render(request, 'FungiClassification/formZip.html', {'error': error})

        if (fileName.endswith('.zip') == False):
            error = 'The file is not a zip file'
            return render(request, 'FungiClassification/formZip.html',{'error':error})

        fs = FileSystemStorage()
        extension = zip_file.name[zip_file.name.rfind("."):]
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d-%H-%M-%S')
        fs.save("zip-files/" + st + extension, zip_file)
        zip_ref = zipfile.ZipFile("media/zip-files/" + st + extension, 'r')
        zip_ref.extractall("media/zip-files/" + st)
        zip_ref.close()
        fs.delete("zip-files/" + st + extension)
        (_, files) = fs.listdir("zip-files/" + st)
        print(files)
        predictions = [("../../../media/zip-files/" + st + "/" + file,
                        categoryOfFungiImageUsingOverfeat(_grab_image(path="media/zip-files/" + st + "/" + file),
                                                          oe)) for file in files]

        request.session['list'] = [[img, pred, img[img.rfind('/')+1:]] for (img, pred) in predictions]
        request.session["imagenes"] = [img for (img, _) in predictions]
        request.session['imagenCont'] = None
        request.session['zip'] = True
        request.session['url'] = '/fungi_classification/predictFungiClass/zip/'
        return HttpResponseRedirect('/fungi_classification/predictFungiClass/result/')
    else:
        return render(request, 'FungiClassification/formZip.html')










def predictFungiClassUsingOverfeatViewGUIResult(request):
    try:
        if request.method == 'GET':
            form = Formulario(request.POST, request.FILES)
            if request.session.has_key('list'):
                list = request.session.get('list')
            return render(request, 'FungiClassification/results.html', { 'list':list, 'url':'/fungi_classification/predictFungiClass/', 'pagurl':'Analyse one image', 'con':'con1'})
        if request.method == 'POST':
            if request.session.has_key('list'):
                list = request.session.get('list')
            prediccion = request.POST.get('resultado')
            nombre=request.POST.get('nombre')
            tinte=request.POST.get('tinte')
            notas=request.POST.get('notas')

            # ALMACENAR EN BASE DE DATOS
            p = ObjetoFungi(name=nombre, dye=tinte, image=list.__getitem__(0)[0], prediction=prediccion, description=notas)
            p.save()
            return HttpResponseRedirect('/fungi_classification/predictFungiClass/')
    except UnboundLocalError:
        mensaje = '404 Not Found'
        return render(request, 'FungiClassification/error.html', {'mensaje': mensaje})



@csrf_exempt
def predictFungiClassUsingOverfeat(request):
    """CURL example: curl -X POST -F image=@ad71aem_control.jpg 'http://localhost:8000/fungi_classification/predictFungiClassUsingOverfeat/'; echo "" """

    # initialize the data dictionary to be returned by the request
    data = {"success": False}

    # check to see if this is a post request
    if request.method == "POST":
        # check to see if an image was uploaded
        if request.FILES.get("image", None) is not None:
            # grab the uploaded image
            image = _grab_image(stream=request.FILES["image"])

        # otherwise, assume that a URL was passed in
        else:
            # grab the URL from the request
            url = request.POST.get("url", None)

            # if the URL is None, then return an error
            if url is None:
                data["error"] = "No URL provided."
                return JsonResponse(data)

            # load the image and convert
            image = _grab_image(url=url)

        # predict the class of the fungi image
        prediction = categoryOfFungiImageUsingOverfeat(image,oe)

        # Saving the file for further usage
        myfile = request.FILES['image']
        fs = FileSystemStorage()
        extension = myfile.name[myfile.name.rfind("."):]
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d-%H-%M-%S')
        filename = fs.save("fungi-classification/"+st + extension, myfile)
        uploaded_file_url = fs.url(filename)

        # update the data dictionary with the categories
        data.update({"prediction": prediction})
        data.update({"success": True})
        data.update({"uploaded_file_url":uploaded_file_url})

    # return a JSON response
    return JsonResponse(data)

@csrf_exempt
def predictFungiClassUsingOverfeatView(request):
    if request.method == 'POST':
        """and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        report = statisticalComparison.statisticalComparison(BASE_DIR+uploaded_file_url)
        fs.delete(filename)"""
        print(request.POST)
        predictionJSON = predictFungiClassUsingOverfeat(request)

        return render(request, 'FungiClassification/simple_upload.html', json.loads(predictionJSON.content))
    return render(request, 'FungiClassification/simple_upload.html')



@csrf_exempt
def predictFungiClassUsingOverfeatViewZIP(request):
    """CURL example: curl -X POST -F zip=@images.zip 'http://193.146.250.57:8000/fungi_classification/predictFungiClass/zip/'; echo "" """
    if request.method == 'POST':
        zip_file = request.FILES['zip']
        fs = FileSystemStorage()
        extension = zip_file.name[zip_file.name.rfind("."):]
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d-%H-%M-%S')
        fs.save("zip-files/" + st + extension, zip_file)
        zip_ref = zipfile.ZipFile("media/zip-files/"+ st + extension, 'r')
        zip_ref.extractall("media/zip-files/"+ st)
        zip_ref.close()
        fs.delete("zip-files/" + st + extension)
        (_,files)=fs.listdir("zip-files/"+ st)
        print(files)
        predictions = [("../../../media/zip-files/"+st+"/"+file,categoryOfFungiImageUsingOverfeat(_grab_image(path="media/zip-files/"+ st+"/"+file), oe)) for file in files]
        data = {"success": True}
        data.update({"predictions": predictions})
        predictionJSON = JsonResponse(data)

        return render(request, 'FungiClassification/zip_upload.html', json.loads(predictionJSON.content))
    return render(request, 'FungiClassification/zip_upload.html')


@csrf_exempt
def predictFungiClassUsingOverfeatViewExamples(request,num=1):
    image = _grab_image(path="media/fungi-classification/" + num + ".jpg")
    # predict the class of the fungi image
    prediction = categoryOfFungiImageUsingOverfeat(image, oe)

    nombre = num + ".jpg"
    fileName = "../../../media/fungi-classification/" + num + ".jpg"
    list = [fileName, prediction, nombre]
    listaPred = []
    listaPred.append(list)
    request.session['list'] = listaPred
    request.session['imagenCont'] = None
    request.session['zip'] = None

    request.session['url'] = '/fungi_classification/predictFungiClass/'
    return HttpResponseRedirect('/fungi_classification/predictFungiClass/result/')

@csrf_exempt
def predictFungiClassUsingOverfeatViewControlExamples(request,num=1):
    image = _grab_image(path="media/fungi-classification/" + num + ".jpg")
    control_image = _grab_image(path="media/fungi-classification/control-" + num + ".jpg")
    # predict the class of the fungi image
    prediction = categoryOfFungiImageUsingOverfeatWithControl(image,control_image, oe)

    nombre = num + ".jpg"
    fileName = "../../../media/fungi-classification/" + num + ".jpg"
    list = [fileName, prediction, nombre]
    listaPred = []
    listaPred.append(list)
    request.session['list'] = listaPred
    request.session['imagenCont'] = "../../../media/fungi-classification/control-" + num + ".jpg"
    request.session['zip'] = None


    request.session['url'] = '/fungi_classification/predictFungiClassControl/'
    return HttpResponseRedirect('/fungi_classification/predictFungiClass/result/')


@csrf_exempt
def predictFungiClassUsingOverfeatWithControl(request):
    """CURL example: curl -X POST -F image=@ad71aem_control.jpg -F imageControl=@ad71aem_control.jpg 'http://localhost:8000/fungi_classification/predictFungiClassUsingOverfeatWithControl/'; echo "" """

    # initialize the data dictionary to be returned by the request
    data = {"success": False}

    # check to see if this is a post request
    if request.method == "POST":
        # check to see if an image was uploaded
        if request.FILES.get("image", None) is not None and request.FILES.get("imageControl", None) is not None:
            # grab the uploaded image
            image = _grab_image(stream=request.FILES["image"])
            imageControl = _grab_image(stream=request.FILES["imageControl"])
        else:
            data.update({"Error": "You must upload two images"})
            return JsonResponse(data)

        # predict the class of the fungi image
        prediction = categoryOfFungiImageUsingOverfeatWithControl(image,imageControl,oe)

        # update the data dictionary with the faces detected
        data.update({"prediction": prediction})
        data.update({"success": True})

    # return a JSON response
    return JsonResponse(data)



@csrf_exempt
def predictFungiClassUsingGoogleNet(request):
    """CURL example: curl -X POST -F image=@ad71aem_control.jpg 'http://localhost:8000/fungi_classification/predictFungiClassUsingGoogleNet/'; echo "" """
    # initialize the data dictionary to be returned by the request
    data = {"success": False}

    # check to see if this is a post request
    if request.method == "POST":
        # check to see if an image was uploaded
        if request.FILES.get("image", None) is not None:
            # grab the uploaded image
            image = _grab_image(stream=request.FILES["image"])

        # otherwise, assume that a URL was passed in
        else:
            # grab the URL from the request
            url = request.POST.get("url", None)

            # if the URL is None, then return an error
            if url is None:
                data["error"] = "No URL provided."
                return JsonResponse(data)

            # load the image and convert
            image = _grab_image(url=url)

        # predict the class of the fungi image
        prediction = categoryOfFungiImageUsingGoogleNet(image,ge)

        # update the data dictionary with the faces detected
        data.update({"prediction": prediction})
        data.update({"success": True})

    # return a JSON response
    return JsonResponse(data)


@csrf_exempt
def predictFungiClassUsingGoogleNetWithControl(request):
    """CURL example: curl -X POST -F image=@ad71aem_control.jpg -F imageControl=@ad71aem_control.jpg 'http://localhost:8000/fungi_classification/predictFungiClassUsingGoogleNetWithControl/'; echo "" """

    # initialize the data dictionary to be returned by the request
    data = {"success": False}

    # check to see if this is a post request
    if request.method == "POST":
        # check to see if an image was uploaded
        if request.FILES.get("image", None) is not None and request.FILES.get("imageControl", None) is not None:
            # grab the uploaded image
            image = _grab_image(stream=request.FILES["image"])
            imageControl = _grab_image(stream=request.FILES["imageControl"])
        else:
            data.update({"Error": "You must upload two images"})
            return JsonResponse(data)

        # predict the class of the fungi image
        prediction = categoryOfFungiImageUsingGoogleNetWithControl(image,imageControl,ge)

        # update the data dictionary with the faces detected
        data.update({"prediction": prediction})
        data.update({"success": True})

    # return a JSON response
    return JsonResponse(data)


def _grab_image(path=None, stream=None, url=None):
    # if the path is not None, then load the image from disk
    print path
    if path is not None:
        image = cv2.imread(path)

    # otherwise, the image does not reside on disk
    else:
        # if the URL is not None, then download the image
        if url is not None:
            resp = urllib.urlopen(url)
            data = resp.read()

        # if the stream is not None, then the image has been uploaded
        elif stream is not None:
            data = stream.read()

        # convert the image to a NumPy array and then read it into
        # OpenCV format
        image = np.asarray(bytearray(data), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)

    # return the image
    return image



import random
randomnums = []
@csrf_exempt
def randomGenerator(request,num=1):
    randomnums.append(random.randint(1, int(num)))
    response = HttpResponse('\n'.join([str(n) for n in randomnums]))
    return response
