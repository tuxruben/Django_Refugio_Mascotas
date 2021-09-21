from django.shortcuts import render, redirect
from django.http import HttpResponse
from apps.mascota.forms import MascotaForm
from apps.mascota.models import Mascota
from django.urls import reverse_lazy
from django.core import serializers
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator
from django.db.models import Count
from tablib import Dataset 
from apps.mascota.resources import MascotaResource
# Create your views here.
def listado(request):
    lista = serializers.serialize('json', Mascota.objects.all(), fields=['nombre', 'sexo'])
    return HttpResponse(lista, content_type= 'application/json')
def index(request):
    return render(request, "mascota/index.html")

def mascota_view(request):
    if request.method == 'POST':
        form = MascotaForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('mascota:index')

    else:
        form = MascotaForm()
    return render(request, 'mascota/mascota_form.html',{'form':form})
@permission_required('adopcion.is_empleado')
def mascota_list(request):
    queryset = request.GET.get('buscar')
    mascota = Mascota.objects.all().annotate(num_vacunas=Count('vacuna')).order_by('id')
   
    if queryset:
        mascota = Mascota.objects.filter(
              Q(nombre__icontains = queryset) |
              Q(sexo__icontains = queryset)
        ).distinct().annotate(num_vacunas=Count('vacuna')).order_by('id')
    paginator = Paginator(mascota, 2)
    page = request.GET.get('page')
    mascota = paginator.get_page(page)
    contexto = {'mascotas':mascota}

    return render(request, 'mascota/mascota_list.html', contexto)

def mascota_edit(request, id_mascota):
    mascota = Mascota.objects.get(id=id_mascota)
    if request.method == 'GET':
         form = MascotaForm(instance=mascota)
    else: 
        form = MascotaForm(request.POST, instance=mascota)
        if form.is_valid():
            form.save()
        return redirect('mascota:mascota_list')
    return render(request, 'mascota/mascota_form.html', {'form':form})
def mascota_delete(request, id_mascota):
    mascota = Mascota.objects.get(id=id_mascota)
    if request.method == 'POST':
        mascota.delete()
        return redirect('mascota:mascota_list')
    return render(request, 'mascota/mascota_delete.html', {'mascota':mascota})

class MascotaList(ListView):
    model = Mascota
    template_name = 'mascota/mascota_list.html'
    paginate_by = 2
    def get_queryset(self, **kwargs):
      queryset = self.request.GET.get('buscar')
      mascota = Mascota.objects.all().order_by('id')
    
      if queryset:
          mascota = Mascota.objects.filter(
              Q(nombre__icontains = queryset) |
              Q(sexo__icontains = queryset)
          ).distinct()
      return mascota
        
    
       
class MascotaCreate(CreateView):
    model = Mascota
    form_class = MascotaForm
    template_name = 'mascota/mascota_form.html'
    success_url = reverse_lazy('mascota:mascota_list')
class MascotaUpdate(UpdateView):
    model = Mascota
    form_class = MascotaForm
    template_name = 'mascota/mascota_form.html'
    success_url = reverse_lazy('mascota:mascota_list')

class MascotaDelete(DeleteView):
    model = Mascota
    template_name = 'mascota/mascota_delete.html'
    success_url = reverse_lazy('mascota:mascota_list')
def importar(request):  
   #template = loader.get_template('export/importar.html')  
   if request.method == 'POST':  
     mascota_resource = MascotaResource()  
     dataset = Dataset()  
     #print(dataset) 
     nuevas_mascotas = request.FILES['xlsfile'] 
     #print(nuevas_mascotas)
     imported_data = dataset.load(nuevas_mascotas.read())  
     print(imported_data['nombre'])  
     print(mascota_resource) 
     result = mascota_resource.import_data(dataset, dry_run=True) # Test the data import  
     print(result.has_errors())  
     if not result.has_errors():  
       mascota_resource.import_data(dataset, dry_run=False) # Actually import now  
   return render(request, 'export/importar.html')