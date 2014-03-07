from django.shortcuts import get_object_or_404, render, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from cliente.models import Usuarios
from cliente.models import Recetas
from django.template import RequestContext, loader, Context
from django.core.context_processors import csrf
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .forms import UploadFileForm

## Show the index
def index(request):
    if not request.user.is_anonymous():
        return HttpResponseRedirect("/receta")
    context = RequestContext(request)
    if request.method == 'POST': # If the form has been submitted...
        formulario = AuthenticationForm(request.POST)
        usuario = request.POST['username']
        clave = request.POST['password']
        acceso = authenticate(username=usuario, password=clave)
        if acceso is not None:
            auth_login(request, acceso)
            return HttpResponseRedirect("/receta")
        else:
            return HttpResponse("Usuario No valido")
    else:
        formulario = AuthenticationForm()
        return render_to_response('cliente/index.html',{'formulario':formulario},context_instance=RequestContext(request))
        #template = loader.get_template('cliente/index.html')
        #return HttpResponse(template.render(context))



## Show the new user form
def newuser(request):
    if not request.user.is_anonymous():
        return HttpResponseRedirect("/receta")
    if request.method == 'POST': # If the form has been submitted...
        formulario = UserCreationForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/')
    else:
        formulario = UserCreationForm()
        return render_to_response('cliente/adduser.html',{'formulario':formulario},context_instance=RequestContext(request))

## Show the aplication
@login_required(login_url='/')
def receta(request):
    usuario = request.user
    orden = 'nombre'
    onom = '-nombre'
    oid = 'creacion'
    lista_receta = None
    if request.method == 'POST': # If the form has been submitted...
        form = UploadFileForm(request.POST, request.FILES)
        if request.POST.get('id'):
            id_mod = request.POST['id']
            r = Recetas.objects.get(id=id_mod)
            r.nombre = request.POST['nombre']
            r.texto = request.POST['texto']
            if request.FILES['file'].name:
                handle_uploaded_file(request.FILES['file'])
                r.imagen = request.FILES['file']
            r.save()
            return HttpResponseRedirect("/receta")
        handle_uploaded_file(request.FILES['file'])
        nom = request.POST['nombre']
        tex = request.POST['texto']
        ima = request.FILES['file']
        r = Recetas(nombre=nom, texto=tex, imagen=ima,creacion=timezone.now(),a=0,b=0,c=0,d=0)
        r.save();
        return HttpResponseRedirect("/receta")
    if request.method == 'GET':
        if request.GET.get('del'):
            id_del = request.GET['del']
            Recetas.objects.filter(id=id_del).delete()
            return HttpResponseRedirect("/receta")
        if request.GET.get('mod'):
            id_mod = request.GET['mod']
            r = Recetas.objects.get(id=id_mod)
            id = r.id
            nom = r.nombre
            tex = r.texto
            ima = r.imagen
            return render_to_response('cliente/modificar.html', {'usuario':usuario}, context_instance=RequestContext(request,{'nom': nom,'tex':tex,'ima':ima,'id_mod':id}))
        if request.GET.get('orden'):
            orden = request.GET['orden']
            if orden == 'nombre':
                onom = '-nombre'
            if orden == '-nombre':
                onom = 'nombre'
            if orden == 'creacion':
                oid = '-creacion'
            if orden == '-creacion':
                oid = 'creacion'
        if request.GET.get('idcal') and request.GET.get('cal'):
            idcal = request.GET['idcal']
            cal = request.GET['cal']
            r = Recetas.objects.get(id=idcal)
            a = int(r.a) + int(cal) 
            b = int(r.b) + 1
            r.a = a
            r.b = b
            r.save()
            return HttpResponseRedirect("/receta")
        if request.GET.get('buscar'):
            ## Recetas.objects.filter(nombre__startswith='').order_by( orden )[:5]
            busqueda = request.GET['buscar']
            lista_receta = Recetas.objects.filter(nombre__contains=busqueda).order_by( orden )[:5]
    if lista_receta == None:
        lista_receta = Recetas.objects.order_by( orden )[:5]
    return render_to_response('cliente/receta.html', {'usuario':usuario}, context_instance=RequestContext(request,{'lista_receta': lista_receta,'oid':oid,'onom':onom}))

## Close sesion
@login_required(login_url='/')
def cerrar(request):
    logout(request)
    return HttpResponseRedirect('/')

## Save file
def handle_uploaded_file(f):
    filename = f.name  # get the name here
    destination = open('cliente/static/imagenes/'+filename, 'wb+')
    for chunk in f.chunks(): 
        destination.write(chunk)
    destination.close()
