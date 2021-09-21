
from django.urls import path
from apps.adopcion.views import solicitud_list, index_adopcion, SolicitudList, SolicitudCreate, SolicitudUpdate, SolicitudDelete
urlpatterns = [
    path('index', index_adopcion),
    path('solicitud/listar', solicitud_list, name='solicitud_listar'),
    path('solicitud/nueva', SolicitudCreate.as_view(), name='solicitud_crear'),
    path('solicitud/editar/<pk>', SolicitudUpdate.as_view(), name='solicitud_editar'),
    path('solicitud/eliminar/<pk>', SolicitudDelete.as_view(), name='solicitud_eliminar'),

]