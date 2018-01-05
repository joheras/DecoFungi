# -*- coding: utf-8 -*-

#from json import JSONDecodeError

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.template import loader
import requests
import json
import os
from bs4 import  BeautifulSoup
from mvc.forms import Formulario, Formulario2, FormularioZip
import zipfile
from os import listdir
from PIL import Image


# Create your views here.
from mvc.models import ImagenyPrediccion, ObjetoFungi


def index(request):
    template = loader.get_template("Menu.html")
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
        return render(request, 'Menu.html')
    except ValueError:
        mensaje = '404 Not Found'
        return render(request, 'error.html', {'mensaje': mensaje})
    except UnboundLocalError:
        mensaje = '404 Not Found'
        return render(request, 'error.html', {'mensaje': mensaje})


def contacto(request):
    tooltiptext = "Select an image corresponding to a Petri's dish. Once that you have loaded the image, press Upload and analyse button"
    if request.method == 'POST':
        try:
            form = Formulario(request.POST, request.FILES)
            if form.is_valid():
                url = 'http://193.146.250.57:8000/fungi_classification/predictFungiClassUsingOverfeat/'
                fileName = request.FILES['image'].name
                filePath = os.path.realpath("../blog/media/"+fileName)  # CAMBIAR COMO OBTENER EL PATH
                files = {'image': open(filePath, 'rb')}
                response = requests.post(url, files=files).text
                data = json.loads(response)
                print (data)
                # Guardar en la sesión estos objetos del JSON para mostraros en la vista
                nombre = fileName.split('.')[0]
                list = [fileName, data['prediction'], nombre]
                listaPred = []
                listaPred.append(list)
                request.session['list']=listaPred
                return HttpResponseRedirect('/mvc/gracias/')
        except FileNotFoundError:
            mensaje = 'The file is not in the application directory /media/'
            form.add_error('image',mensaje)
            return render(request, 'VistaFormulario.html', {'mensaje': mensaje,
                                                            'form':form,
                                                            'pag':'Analyse one image',
                                                            'intro1':'Analyse one image: ',
                                                            'intro2':'Select one fungi image to get the prediction.',
                                                            'tooltiptext':tooltiptext})
    else:
        form = Formulario()

    return render(request, 'VistaFormulario.html', {
        'form': form,
        'pag':'Analyse one image',
        'intro1':'Analyze one image: ',
        'intro2':'Select one fungi image to get the prediction.',
        'tooltiptext': tooltiptext})



def gracias(request):
    try:
        if request.method == 'GET':
            form = Formulario(request.POST, request.FILES)
            if request.session.has_key('list'):
                list = request.session.get('list')
            return render(request, 'VistaGlobal.html', { 'list':list, 'url':'/mvc/contacto/', 'pagurl':'Analyze one image', 'con':'con1'})
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
            return HttpResponseRedirect('/mvc/')
    except UnboundLocalError:
        mensaje = '404 Not Found'
        return render(request, 'error.html', {'mensaje': mensaje})


def contacto2(request):
    tooltiptext="Select two images, one corresponds to a Petri's dish with the fungi, an the other correspond to a control image."\
                "Once that you have loaded the images, press 'Upload and analyse' button. "
    if request.method == 'POST':
        try:
            form = Formulario2(request.POST, request.FILES)
            if form.is_valid():
                url = 'http://193.146.250.57:8000/fungi_classification/predictFungiClassUsingOverfeatWithControl/'
                fileName = request.FILES['image'].name
                fileNameControl = request.FILES['control_image'].name
                filePath = os.path.realpath("../blog/media/" + fileName)
                filePathCon = os.path.realpath("../blog/media/" + fileNameControl)

                files = {'image': open(filePath, 'rb'),
                         'imageControl': open(filePathCon, 'rb')}
                response = requests.post(url, files=files).text
                data = json.loads(response)
                print(data)

                nombre = fileName.split('.')[0]
                request.session['imagenCont'] = fileNameControl
                list = [fileName, data['prediction'], nombre]
                listaPred = []
                listaPred.append(list)
                request.session['list'] = listaPred
                return HttpResponseRedirect('/mvc/gracias2/')
        except FileNotFoundError:
            mensaje = 'The file is not in the application directory /media/'
            form.add_error('image', mensaje)
            return render(request, 'VistaFormulario.html', {'mensaje': mensaje,
                                                            'form': form,
                                                            'pag': 'Analyze one image with control one',
                                                            'intro1': 'Analyze one image with control one: ',
                                                            'intro2': 'Select a fungi image and the corresponding control image asociated to get the prediction.',
                                                            'tooltiptext': tooltiptext})
    else:
        form = Formulario2()
    return render(request, 'VistaFormulario.html', {
        'form': form,
        'pag': 'Analyze one image with control one',
        'intro1': 'Analyze one image with control one: ',
        'intro2': 'Select a fungi image and the corresponding control image asociated to get the prediction.',
        'tooltiptext': tooltiptext
    })


def gracias2(request):
    try:
        if request.method == 'GET':
            if request.session.has_key('list'):
                list = request.session.get('list')
            if request.session.has_key('imagenCont'):
                imagenCont = request.session.get('imagenCont')
            control='control'
            return render(request, 'VistaGlobal.html', {'list':list, 'control':control, 'imagenCont':imagenCont, 'url':'/mvc/contacto2/', 'pagurl':'Analyze one image with control one: ', 'con':'con2'})
        if request.method == 'POST':
            if request.session.has_key('list'):
                list = request.session.get('list')
            prediccion = request.POST.get('resultado')
            nombre = request.POST.get('nombre')
            tinte = request.POST.get('tinte')
            notas = request.POST.get('notas')

            #Capa de persistencia
            ip=ObjetoFungi(name=nombre, dye=tinte, image=('/mvc/media/')+list.__getitem__(0)[0], prediction=prediccion, description=notas)
            ip.save()
            return HttpResponseRedirect('/mvc/')
    except UnboundLocalError:
            mensaje = '404 Not Found'
            return render(request, 'error.html', {'mensaje': mensaje})

def contacto3(request):
    tooltiptext="Take care, the file must have zip extension and the zip file should only contain the images to analyse. Once that you have loaded the zip file, press Upload and analyse' button."\
                "The processing of the images might take some time depending on the number of images. "
    if request.method == 'POST':
        try:
            form = FormularioZip(request.POST, request.FILES)
            if form.is_valid():
                url = 'http://193.146.250.57:8000/fungi_classification/predictFungiClass/zip/'
                fileName = request.FILES['zip_file'].name
                if(fileName.endswith('.zip')==False):
                    mensaje = 'The file is not a zip file'
                    form.add_error('zip_file',mensaje)
                    return render(request, 'VistaFormulario.html', {
                        'form': form,
                        'pag': 'Analyze a zip',
                        'intro1': 'Analyze a zip: ',
                        'intro2': 'Select a zip file to get the prediction of several images. ',
                        'tooltiptext': tooltiptext
                    })

                filePath = os.path.realpath("../blog/media/" + fileName)

                files = {'zip': open(filePath, 'rb')}
                response = requests.post(url, files=files).text

                #PARSEO HTML
                soup = BeautifulSoup(response, "html.parser")
                img=soup.find_all("img")#Lista de imagenes
                listaimg=[]
                listanombr=[]
                for i in img:
                    repElemImg=i.get('src')
                    list=repElemImg.split('/')
                    a=list[len(list)-1].split('.')[0]
                    listanombr.append(a)
                    listaimg.append(list[len(list)-1])

                pred=soup.find_all("p")#Lista de predicciones
                listapred=[]
                for p in pred:
                    if "Prediction:" in p.text:
                        pr=p.text.split(" ")
                        listapred.append(pr[1].rstrip())

                #listObj=[]
                        #for n,l,m in zip(listaimg, listapred, listanombr): #Como van a tener la misma longitud  las dos listas creo una lista de objetos
                        #ip=ImagenyPrediccion(nombreImagen=n,prediccion=l, nombre=m)
                        #listObj.append(ip)

                        # diccionario=dict([ (p.nombreImagen,{ p.prediccion: p.nombre}) for p in listObj ])#IMPORTANTE:Creo un diccionario de pares Imagen, Prediccion
                        #print(diccionario)
                        #request.session['diccionario'] = diccionario

                listFinal=[]
                for n, l, m in zip(listaimg, listapred, listanombr):
                    list=[n,l,m]
                    listFinal.append(list)

                request.session['list']=listFinal
                request.session["imagenes"] = listaimg

                return HttpResponseRedirect('/mvc/gracias3/')
        except FileNotFoundError:
            mensaje = 'The file is not in the application directory /media/'
            form.add_error('zip_file', mensaje)
            return render(request, 'VistaFormulario.html', {
                'form': form,
                'pag': 'Analyze a zip',
                'intro1': 'Analyze a zip: ',
                'intro2': 'Select a zip file to get the prediction of several images. ',
                'tooltiptext': tooltiptext
            })
    else:
        form = FormularioZip()

    return render(request, 'VistaFormulario.html', {
        'form': form,
        'pag': 'Analyze a zip',
        'intro1': 'Analyze a zip: ',
        'intro2': 'Select a zip file to get the prediction of several images. ',
        'tooltiptext': tooltiptext
    })


def gracias3(request):
    try:
        if request.method == 'GET':
            if request.session.has_key('list'):
                list = request.session.get('list')
                zipM = 'zip'
            return render(request, 'VistaGlobal.html',
                          {'list': list, 'zip': zipM, 'url': '/mvc/contacto3/', 'pagurl': 'Analyze a zip',
                           'con': 'con3'})
        if request.method == 'POST':
            if request.session.has_key('imagenes'):
                imagenes = request.session.get('imagenes')
                del request.session['imagenes']
            predicciones = request.POST.getlist("resultado")
            nombre = request.POST.getlist('nombre')
            tinte = request.POST.getlist('tinte')
            notas = request.POST.getlist('notas')
            for n, l, m, o, p in zip(nombre, tinte, imagenes, predicciones, notas):
                ip = ObjetoFungi(name=n, dye=l, image=m, prediction=o, description=p)
                ip.save()
            return HttpResponseRedirect('/mvc/')
    except UnboundLocalError:
        mensaje = '404 Not Found'
        return render(request, 'error.html', {'mensaje': mensaje})

##MEJORAS MODELO METODO 4

def contacto4(request):
    tooltiptext="Take care, the file must have zip extension and the zip file should only contain the images with the same" \
                " dye to analyse. Also the zip folder must contain one control.jpg image corresponds to the control image."\
                "Once that you have loaded the zip file, press 'Upload and analyse' button. The processing of the images might "\
                "take some time depending on the number of images. "
    if request.method == 'POST':
        try:
            form = FormularioZip(request.POST, request.FILES)
            if form.is_valid():
                url = 'http://193.146.250.57:8000/fungi_classification/predictFungiClassUsingOverfeatWithControl/'
                fileName = request.FILES['zip_file'].name
                if (fileName.endswith('.zip') == False):
                    mensaje = 'The file is not a zip file'
                    form.add_error('zip_file', mensaje)
                    return render(request, 'VistaFormulario.html', {
                        'form': form,
                        'pag': 'Analyze zip control',
                        'intro1': 'Analyze a zip with control: ',
                        'intro2': 'Select a zip file images with the same dye and their correspondent control image named control.jpg to get the prediction. ',
                        'tooltiptext': tooltiptext
                    })

                filePath = os.path.realpath("../blog/media/" + fileName)
                nombreZip=fileName.split('.')

                #Una vez que obtenemos el zip hay que descomprimirlo
                zf = zipfile.ZipFile(filePath, "r")
                dirname ="../blog/media/"+nombreZip[0]+'/'
                for name in zf.namelist():
                    if not os.path.exists(dirname):
                        os.makedirs(dirname)
                    zf.extract(name, dirname)

                listPred=[]
                listNombr=[]
                if listdir(dirname).__contains__('control.jpg')==False:
                    mensaje='The zip folder does not contains control.jpg named image.'
                    if os.path.exists(dirname):
                        for root, dirs, files in os.walk(dirname, topdown=False):
                            # borramos los archivos
                            for name in files:
                                os.remove(os.path.join(root, name))
                            # borramos los subdirectorios
                            for name in dirs:
                                os.rmdir(os.path.join(root, name))
                                # ahora podemos borrar el directorio
                        os.rmdir(dirname)
                    request.GET.__setattr__('mensaje',mensaje)
                    form.add_error('zip_file', mensaje)
                    return render(request, 'VistaFormulario.html', {
                        'form': form,
                        'pag': 'Analyze zip control',
                        'intro1': 'Analyze a zip with control: ',
                        'intro2': 'Select a zip file images with the same dye and their correspondent control image named control.jpg to get the prediction. ',
                        'tooltiptext': tooltiptext
                    })
                for file in listdir(dirname):
                    if (file.__contains__('control')==False):
                        listNombr.append(file)
                        files = {'image': open(dirname+'control.jpg', 'rb'),
                                 'imageControl': open(dirname+file, 'rb')}
                        response = requests.post(url, files=files).text
                        data=json.loads(response)
                        list=[file,data['prediction'],file.split('.')[0]]
                        listPred.append(list)
                request.session['list'] = listPred
                request.session['listN'] = listNombr#No se usa en la vista solo apra guardar en la bd
                request.session['nombrezip']=nombreZip[0]
                return HttpResponseRedirect('/mvc/gracias4/')
        except FileNotFoundError:
            mensaje = 'The file is not in the application directory /media/'
            form.adderror('zip_file', mensaje)
            return render(request, 'VistaFormulario.html', {
                'form': form,
                'pag': 'Analyze zip control',
                'intro1': 'Analyze a zip with control: ',
                'intro2': 'Select a zip file images with the same dye and their correspondent control image named control.jpg to get the prediction. ',
                'tooltiptext': tooltiptext
            })
    else:
        try:
            form = FormularioZip()
            if request.session.has_key('nombrezip'):
                nombrezip = request.session.get('nombrezip')
                #del request.session['nombrezip']
            refer = request.META.get('HTTP_REFERER')
            if (refer=='http://127.0.0.1:8000/mvc/gracias4/'):
                dirname = '../blog/media/'+nombrezip+'/'
                if os.path.exists(dirname):
                    for root, dirs, files in os.walk(dirname, topdown=False):
                        # borramos los archivos
                        for name in files:
                            os.remove(os.path.join(root, name))
                        # borramos los subdirectorios
                        for name in dirs:
                            os.rmdir(os.path.join(root, name))
                            # ahora podemos borrar el directorio
                    os.rmdir(dirname)
        except UnboundLocalError:
            mensaje = '404 Not Found'
            return render(request, 'error.html', {'mensaje': mensaje})
    return render(request, 'VistaFormulario.html', {
        'form': form,
        'pag': 'Analyze zip control',
        'intro1': 'Analyze a zip with control: ',
        'intro2': 'Select a zip file images with the same dye and their correspondent control image named control.jpg to get the prediction. ',
        'tooltiptext': tooltiptext
    })


def gracias4(request):
    try:
        if request.method == 'GET':
            if request.session.has_key('list'):
                list = request.session.get('list')
            if request.session.has_key('nombrezip'):
                nombrezip = request.session.get('nombrezip')
            zipM='zip'
            control='control'
            imagenContr='control.jpg'
            return render(request, 'VistaGlobal.html', {'list':list, 'nombrezip':nombrezip, 'zip':zipM, 'control':control, 'imagenCont':imagenContr,
                                                        'url':'/mvc/contacto4/', 'pagurl':'Analyze a zip control','con':'con4'})
        if request.method== 'POST':
            if request.session.has_key('listN'):
                listimagenes = request.session.get('listN')
                del request.session['listN']
            if request.session.has_key('nombrezip'):
                nombrezip = request.session.get('nombrezip')
                del request.session['nombrezip']
            predicciones = request.POST.getlist("resultado")
            nombre = request.POST.getlist('nombre')
            tinte = request.POST.get('tinte')
            notas = request.POST.getlist('notas')
            for n, m, o, p in zip(nombre, listimagenes,predicciones, notas):
                ip = ObjetoFungi(name=n, dye=tinte, image='/mvc/media/'+nombrezip+'/'+m, prediction=o, description=p)
                ip.save()
            return HttpResponseRedirect('/mvc/')
    except UnboundLocalError:
            mensaje = '404 Not Found'
            return render(request, 'error.html', {'mensaje': mensaje})

