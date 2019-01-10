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
    url(r'^services/$', views.greetings, name='greetings'),
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
    url(r'^services/aspirante/v2/$',views.regApirante, name='reg-aspv2'),
    url(r'^services/pregunta/$',views.PreguntaApiCreate.as_view(), name='pregunta-create'),
    url(r'^services/pregunta/(?P<id_pregunta>(\d+))/$',views.PreguntaApiCreateRetrive.as_view(), name='pregunta-retrive'),
    url(r'^services/encuestas/$',views.EncuestanApiCreate.as_view(), name='encuesta-create'),
    url(r'^services/encuestas/(?P<id_encuensta>(\d+))/$',views.EncuestaApiCreateRetrive.as_view(), name='encuesta-retrive'),
    ## Documentos
    url(r'^services/documentos/$',views.regDocumento, name='documentos-create'),
    url(r'^services/documentos/all/$',views.getDocumento, name='documentos-all'),
    url(r'^services/documentos/(?P<id_documento>(\d+))/$',views.detDocumento, name='documento-update'),
    ##Clasificacion
    url(r'^services/clasificaciones/$',views.regClasificacion, name='clasificaciones-create'),
    url(r'^services/clasificaciones/all/$',views.getClasificacion, name='clasificaciones-all'),
    url(r'^services/clasificaciones/(?P<id_clasificacion>(\d+))/$',views.detClasificacion, name='clasificaciones-update'),
    ##categorias
    url(r'^services/categorias/$',views.regCategoria, name='categorias-create'),
    url(r'^services/categorias/all/$',views.getCategoria, name='categorias-all'),
    url(r'^services/categorias/(?P<id_categoria>(\d+))/$',views.detCategoria, name='categorias-update'),
    ##Encuestas
    url(r'^services/encuestas/$',views.regEncuesta, name='encuestas-create'),
    url(r'^services/encuestas/all/$',views.getCategoria, name='encuestas-all'),
    url(r'^services/encuestas/(?P<id_categoria>(\d+))/$',views.detCategoria, name='encuestas-update'),
    ##Respuestas
    url(r'^services/respuestas/$',views.RespuestaApiCreate.as_view(), name='respuestas-create'),
    url(r'^services/respuestas/(?P<id_respuesta>(\d+))/$',views.RespuestaApiCreateRetrive.as_view(), name='respuestas-retrive'),
    url(r'^services/clasificacion/$',views.ClasificacionApiCreate.as_view(), name='clasificacion-create'),
    url(r'^services/clasificacion/(?P<id_clasificacion>(\d+))/$',views.ClasificacionApiCreateRetrive.as_view(), name='clasificacion-retrive'),
    ##horario
    url(r'^services/horarios/$',views.regHorario, name='horario-create'),
    url(r'^services/horarios/all/$',views.getHorario, name='horario-all'),
    url(r'^services/horarios/unable/(?P<id_horario>(\d+))/$',views.unableHorario, name='horario-create'),
    ##aula
    url(r'^services/aulas/$',views.regAula, name='aula-create'),
    url(r'^services/aulas/all/$',views.getAula, name='aula-all'),
    url(r'^services/aulas/(?P<id_aula>(\d+))/$',views.detAula, name='aula-det'),
    url(r'^services/aulas/unable/(?P<id_aula>(\d+))/$',views.unableAula, name='aula-unable'),
    ##ciclo
    url(r'^services/ciclos/$',views.regCiclo, name='ciclo-create'),
    url(r'^services/ciclos/all/$',views.getCiclo, name='ciclo-all'),
    url(r'^services/ciclos/(?P<id_ciclo>(\d+))/$',views.detCiclo, name='ciclo-det'),
    url(r'^services/ciclos/unable/(?P<id_ciclo>(\d+))/$',views.unableCiclo, name='ciclo-unable'),
    ##programa
    url(r'^services/programas/$',views.regPrograma, name='programa-create'),
    url(r'^services/programas/all/$',views.getPrograma, name='programa-all'),
    url(r'^services/programas/(?P<id_programa>(\d+))/$',views.detPrograma, name='programa-det'),
    url(r'^services/programas/unable/(?P<id_programa>(\d+))/$',views.unablePrograma, name='programa-unable'),
    ##materia
    url(r'^services/materias/$',views.regMateria, name='materia-create'),
    url(r'^services/materias/all/$',views.getMateria, name='materia-all'),
    url(r'^services/materias/(?P<id_materia>(\d+))/$',views.detMateria, name='materia-det'),
    url(r'^services/materias/unable/(?P<id_materia>(\d+))/$',views.unableMateria, name='materia-unable'),
    ##grupoTeorico
    url(r'^services/gruposT/$',views.regGrupoT, name='grupoT-create'),
    ##Inscripcion
    url(r'^services/inscripciones/$',views.regInscripcion, name='ins-create'),
    url(r'^services/inscripciones/all/$',views.getInscripcion, name='ins-all'),
    url(r'^services/inscripciones/unable/(?P<id_inscripcion>(\d+))/$',views.unableInscripcion, name='ins-unable'),
    #url(r'^services/solventes/estudiantes/inscripcion/(?P<id_estudiante>(\d+))/inscripcion/(?P<id_inscripcion>(\d+))/$',views.insEstudiante, name='ins-estudiante'),
    ##Solventes
    url(r'^services/solventes/inscripcion/(?P<id_inscripcion>(\d+))/$',views.genSolventes, name='gen-solventes'),
    url(r'^services/solventes/estudiantes/unable/(?P<id_estudiante>(\d+))/inscripcion/(?P<id_inscripcion>(\d+))/$',views.unablePermisoEst, name='perm-unable'),
    ##Estudiantes
    url(r'^services/estudiantes/(?P<id_estudiante>(\d+))/$',views.detEstudiante, name='estudiante-det'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
