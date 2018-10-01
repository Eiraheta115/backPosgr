from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from rest_framework import routers
from .services import views
from rest_framework.authtoken.views import ObtainAuthToken
from django.conf.urls.static import static

#router = routers.DefaultRouter()
#router.register(r'codigos', views.CodigoViewSet)


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^services/usuarios/(?P<id>(\d+))/$', views.Usuario2APICreateView.as_view(), name='usuario-create'),
    url(r'^services/asignaroless/(?P<id>(\d+))/usuario/(?P<id2>(\d+))/$', views.asignarrol, name='roles-usuarios'),
    url(r'^services/roles/$', views.GroupAPICreateView.as_view(), name='roles-create'),
    url(r'^services/permisos/$', views.PermissionsAPICreate.as_view(), name='permisos-create'),
    url(r'^services/rolpermisos/$', views.PermissionMixinAPICreate.as_view(), name='rolpermisos-create'),
    url(r'^services/noticia/$', views.NoticiaAPICreate.as_view(), name='noticia-create'),
    url(r'^services/noticia/v2/$', views.crearNoticias, name='noticias-v2'),
    url(r'^services/usuarios2/$', views.Usuario2APICreateView.as_view(), name='usuario-create'),
    url(r'^services/usuarios/$', views.Usuario2APICreateView.as_view(), name='usuario-create'),
    url(r'^services/aspirante/$', views.AspiranteAPICreate.as_view(), name='aspirante-create'),
    url(r'^services/aspirante/(?P<id_aspirante>(\d+))/$', views.AspiranteAceptado, name='aspirante-create'),
    url(r'^auth/', views.CustomObtainAuthToken.as_view()),
    url(r'^services/rol/(?P<id>(\d+))/$', views.rolusuarios, name='roles-usuarios'),
    url(r'^imagen/$', views.imageApi, name='imagen'),
    url(r'^generarCodigos/$', views.genCo, name='genCod'),
    url(r'^imprimirCodigos/$', views.impCod, name='impCod'),
    url(r'^validarCodigo/$',views.validarCodigo, name='validar-codigo'),
    url(r'^citas/crear/$',views.agendarCita, name='agendar-cita'),
    url(r'^citas/(?P<anio>(\d+))/$', views.obtenerCitasMes, name='citas-mes'),
    url(r'^citas/month/(?P<mes>(\d+))/year/(?P<anio>(\d+))/$', views.obtenerCitasMesYear, name='citas-mes'),
    url(r'^citas/(?P<anio>(\d+))/estudiantes/(?P<idEstudiante>(\d+))/$', views.obtenerCitasMesEstudiantes, name='citas-estudiantes'),
    url(r'^citas/(?P<anio>(\d+))/admin/(?P<uadmin>(\d+))/$', views.obtenerCitasMesAdmin, name='citas-admin'),
    url(r'^citas/detalle/(?P<idCita>(\d+))/$', views.detalleCita, name='detalle-cita'),
    url(r'^citas/cancelar/(?P<idCita>(\d+))/$', views.cancelarCita, name='cancelar-cita'),
    url(r'^citas/detalle/editar/(?P<idCita>(\d+))/$', views.editarCita, name='editar-cita'),
    url(r'^citas/notificaciones/$',views.notificacionesManana, name='notificaciones-cita'),
    url(r'^citas/citasProximas/$',views.citasProximas, name='cita-proximas'),
    url(r'^citas/entidades/(?P<idCargo>(\d+))/$', views.entidades, name='entidades-cita'),
    url(r'^services/docentes/$',views.DocenteViewSet.as_view(), name='docentes-create'),
    url(r'^services/docentes/(?P<id_docente>(\d+))/$',views.DocenteViewSetRetrive.as_view(), name='docentes-create'),
    url(r'^services/pasos/(?P<id_paso>(\d+))/$',views.PasosApiCreateRetrive.as_view(), name='pasos-create'),
    url(r'^services/pasos/$',views.Pasosnuevos, name='pasos-create'),
    url(r'^services/procedimiento/(?P<id_procedimiento>(\d+))/$',views.ProcedimientoApiCreateRetrive.as_view(), name='procedimiento-create'),
    url(r'^services/procedimiento/$',views.ProcedimientoApiCreate.as_view(), name='procedimiento-create'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
