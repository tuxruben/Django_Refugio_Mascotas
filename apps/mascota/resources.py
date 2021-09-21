from import_export import  resources 

from apps.mascota.models import Mascota



class MascotaResource(resources.ModelResource):  

    class Meta:
        model = Mascota
        import_id_fields= ['nombre']

      
  