from django.contrib.auth.models import User, Group, Permission, PermissionsMixin
from django.core.mail import  send_mail
from django.conf import settings
from rest_framework.permissions import IsAuthenticated , AllowAny
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from .serializers import UserSerializer, ImgSerializer,RolUsuariosSerializer,PasosSerializer,ProcedimientosSerializer,DocentesSerializer,User1Serializer, PermisionsMixinSerializer,  NoticiaSerializer, AspiranteSerializer, GroupSerializer, PermisionsSerializer
from rest_framework import status, viewsets, generics, mixins
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from .models import  Noticia, Aspirante,Image, Docente, Pasos ,Procedimiento, Cita, Validacion
from rest_framework.authtoken.models import Token
import json,time, random, requests, hashlib, calendar, datetime


class PermissionMixinAPICreate(mixins.CreateModelMixin, generics.ListAPIView):
    permission_classes = (AllowAny,)
    lookup_field = 'id'
    serializer_class = PermisionsMixinSerializer

    def get_queryset(self):
        return PermissionsMixin.objects.all()

    def post(self, request , *args, **kwargs):
        return self.create(request , *args, **kwargs)

@api_view(['POST','GET'])
@permission_classes((AllowAny, ))
#@authentication_classes((TokenAuthentication, ))
def asignarrol(request,id=None,id2=None):
    try:
        rol=Group.objects.get(id=id)
    except Group.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method=='POST':
        try:
            rol.user_set.add(id2)
            #rol.objects.save()
            return Response(status=status.HTTP_201_CREATED)
        except Group.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes((AllowAny, ))
#@authentication_classes((TokenAuthentication, ))
def rolusuarios(request, id=None):
    try:
        rol=Group.objects.get(id=id)
    except Group.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    try:
        rol.get_user.all()
        serializer = RolUsuariosSerializer(rol)
        return Response(serializer.data)
    except Group.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


class PermissionsAPICreate(mixins.CreateModelMixin, generics.ListAPIView):
    permission_classes = (AllowAny,)
    #authentication_classes = (TokenAuthentication,)
    #permission_classes = (IsAuthenticated,)
    lookup_field = 'id'
    serializer_class = PermisionsSerializer

    def get_queryset(self):
        return Permission.objects.all()

    def post(self, request , *args, **kwargs):
        return self.create(request , *args, **kwargs)

class CustomObtainAuthToken(ObtainAuthToken):
    def post(self,request,*args, **kwargs):
        response = super(CustomObtainAuthToken, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        user = User.objects.get(id=token.user_id)
        serializer = User1Serializer(user, many=False)
        return Response({'token': token.key, 'user': serializer.data})


class GroupAPICreateView(mixins.CreateModelMixin,generics.ListAPIView):
    permission_classes = (AllowAny,)
    #authentication_classes = (TokenAuthentication,)
    #permission_classes = (IsAuthenticated,)
    lookup_field = 'id'
    serializer_class = GroupSerializer

    def get_queryset(self):
        return Group.objects.all()

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class Usuario2APICreateView(mixins.CreateModelMixin,generics.ListAPIView):
    #authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)

    #permission_classes = (IsAuthenticated,)
    lookup_field = 'id'
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.all()

    def post(self, request,id=None, *args, **kwargs):

        return self.create(request, *args, **kwargs)


class NoticiaAPICreate(mixins.CreateModelMixin, generics.ListAPIView):
    permission_classes = (AllowAny,)
    lookup_field = 'id'
    serializer_class = NoticiaSerializer

    def get_queryset(self):
        return Noticia.objects.all().order_by('-fecha')

    def post(self, request , *args, **kwargs):
        return self.create(request , *args, **kwargs)


class AspiranteAPICreate(mixins.CreateModelMixin, generics.ListAPIView):
    permission_classes = (AllowAny,)
    lookup_field = 'id_aspirante'
    serializer_class = AspiranteSerializer

    def get_queryset(self):
        return Aspirante.objects.all()


    def post(self, request , *args, **kwargs):
        json_data=json.loads(request.body)
        nombre=json_data["nombre_aspirante"]
        user=User.objects.create()
        user.first_name=nombre
        user.objects.save()
        self.apirante.id_user=user.id

        return self.create(request , id=user.id, *args, **kwargs)

@api_view(['GET'])
@permission_classes((AllowAny, ))
def AspiranteAceptado(request, id_aspirante=None):
    try:
        aspirante= Aspirante.objects.get(id_aspirante=id_aspirante)
    except Aspirante.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        aspirante.aceptado=True
        serializer=AspiranteSerializer(aspirante)
        aspirante.save()
        asunto='Aspirante aceptado '
        mensaje_email='usted a sido aceptado para formar parte de la escuela de posgrados, favor de pasar a recoger su carte de aceptacion a la escuela'
        email_from=settings.EMAIL_HOST_USER
        email_to=[aspirante.email,'maud3ca@hotmail.es']
        send_mail(asunto,
                  mensaje_email,
                  email_from,
                  email_to,
                  fail_silently=False
                  )
        return Response(serializer.data)



@api_view(['GET','POST'])
@permission_classes((AllowAny, ))
def imageApi(request):
    if request.method=='GET':
        imagenes=Image.objects.all()
        serializer=ImgSerializer(imagenes, many=True)
        return Response(serializer.data)
    elif request.method=='POST':
        serializer =ImgSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            ruta=str(Image.objects.latest('img'))
            print(ruta)

            return Response(ruta, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DocenteViewSet(generics.ListCreateAPIView):
    permission_classes=(AllowAny,)
    lookup_field = 'id_docente'
    serializer_class = DocentesSerializer

    def get_queryset(self):
        return Docente.objects.all()






class DocenteViewSetRetrive(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=(AllowAny, )
    lookup_field = 'id_docente'
    serializer_class = DocentesSerializer

    def get_queryset(self):
        return Docente.objects.all()


class PasosApiCreate(generics.ListCreateAPIView):
    permission_classes=(AllowAny, )
    lookup_field = 'id_paso'
    serializer_class = PasosSerializer

    def get_queryset(self):


        return Pasos.objects.all()

    def perform_create(self, serializer_class):
        pasos=Pasos.objects.all(filter(id_procedimiento=self.request.data.id_proceimiento))
        ordennuevo=pasos.count()+1
        self.request.orden=ordennuevo
        serializer_class.save(self.request)
        return ordennuevo


@api_view(['GET','POST'])
@permission_classes((AllowAny, ))
def Pasosnuevos(request):
    if request.method=='POST':
        json_data= json.loads(request.body)
        pasos=Pasos.objects.filter(id_proceimiento=json_data["id_proceimiento"])
        serializer=PasosSerializer(json_data)

        if(pasos.count()==0):
            orden=1
        else:
            orden=pasos.count()+1
        json_data["orden"]=orden
        try:
            serializer = PasosSerializer(data=json_data)
            if serializer.is_valid():
                serializer.save()

        except:
            fail={'fail':True}
            return Response(fail)

        return Response (status=status.HTTP_201_CREATED)
    if request.method=='GET':
        pasos=Pasos.objects.all()
        serializer=PasosSerializer(pasos, many=True)
        return Response( serializer.data)





class PasosApiCreateRetrive(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=(AllowAny, )
    lookup_field = 'id_paso'
    serializer_class = PasosSerializer

    def get_queryset(self):
        return Pasos.objects.all()


class ProcedimientoApiCreate( generics.ListCreateAPIView):
    permission_classes=(AllowAny, )
    lookup_field = 'id_procedimiento'
    serializer_class = ProcedimientosSerializer

    def get_queryset(self):
        return Procedimiento.objects.all()

class ProcedimientoApiCreateRetrive( generics.RetrieveUpdateDestroyAPIView):
    permission_classes=(AllowAny, )
    lookup_field = 'id_procedimiento'
    serializer_class = ProcedimientosSerializer

    def get_queryset(self):
        return Procedimiento.objects.all()

@api_view(['POST'])
@permission_classes((AllowAny, ))
def genCo(request):
    data = json.loads(request.body)
    cantidad = data["cantidad"]
    fecha = data["vigencia"]
    anio = datetime.date.today().year
    dia = datetime.date.today().day
    mes = datetime.date.today().month
    lista=[]
    for i in range(0,cantidad):
        hora = datetime.datetime.now().hour
        minuto = datetime.datetime.now().minute
        segundo = datetime.datetime.now().second
        randomNumber=random.randint(1,99999)
        cod = str(anio)+"p0sgr4"+str(dia)+str(i)+str(mes)+"UES"+str(randomNumber)
        while (Validacion.objects.filter(codigo=cod).exists()):
            print("exception")
            randomNumber=random.randint(1,999999)
        c= Validacion.objects.create(codigo=cod, vigencia=fecha, activo=True, impreso=False)
        jsonCode ={
            'id':c.id_codigo,
            'codigo':c.codigo,
            'vigencia':c.vigencia
        }
        lista.append(jsonCode)
    content = {'Guardado': True, "codigos": lista}
    return Response(content, status=status.HTTP_201_CREATED)

@api_view(['PUT'])
@permission_classes((AllowAny, ))
def impCod(request):
    data = json.loads(request.body)
    ids = data["ids"]
    for id in ids:
        Validacion.objects.filter(id_codigo=id).update(impreso=True)
    content = {'Actualizado': True}
    return Response(content, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes((AllowAny, ))
def validarCodigo(request):
    data = json.loads(request.body)
    codigo = data["codigo"]
    if (Validacion.objects.filter(codigo=codigo).exists()):
        v=Validacion.objects.get(codigo=codigo)
        content = {'existe': True, 'id':v.id_codigo}
        estado = status.HTTP_200_OK
    else:
        content = {'existe': False}
        estado = status.HTTP_404_NOT_FOUND
    return Response(content, status=estado)

@api_view(['POST'])
@permission_classes((AllowAny, ))
def crearNoticias(request):
    data = json.loads(request.body)
    apiKey = "217796461126348"
    apiSecret = "INJTRbK_mh3rfqIXblwJd8tz5LQ"
    timestamp = calendar.timegm(time.gmtime())
    sign = "timestamp="+str(timestamp)+apiSecret
    signature = hashlib.sha1(sign.encode('utf-8')).hexdigest()
    noti= requests.post("https://api.cloudinary.com/v1_1/dhbegt4ry/image/upload", data={'file':data["foto"], 'api_key':apiKey, 'timestamp':timestamp, 'signature':signature})
    print (noti)
    Noticia.objects.create(emcabezado=data["encabezado"],
    cuerpo=data["cuerpo"],
    fecha=data["fechas"],
    id_user_id=data["idUsuario"],
    imagenUrl=noti.json()["url"])
    content = {'guardado': True}
    return Response(content, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes((AllowAny, ))
def agendarCita(request):
    data = json.loads(request.body)
    evento =data["evento"]
    descripcion=data["descripcion"]
    lugar=data["lugar"]
    diaCompleto=data["diaCompleto"]
    ##Fecha inicio
    fechaHoraInicio=datetime.datetime.strptime(data["FechaHoraInicio"], "%Y-%m-%d %H:%M:%S")
    fechaInicio=fechaHoraInicio.strftime("%Y-%m-%d")
    
    citaPara=data["citaPara"]
    citaCon=data["citaCon"]
 
    if (citaPara is None and citaCon is None):
        content = {'mensaje': 'No se puede agendar sin registrar los nombres de las entidades'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    else:
        if (citaPara==citaCon):
            content = {'mensaje': 'No se puede agendar citas al mismo usuario'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        if (diaCompleto==True):
            fechaHoraInicio=datetime.datetime.strptime(fechaInicio+" 00:00:00","%Y-%m-%d %H:%M:%S")
            fechaHoraFin=datetime.datetime.strptime(fechaInicio+" 23:59:59","%Y-%m-%d %H:%M:%S")
        else:
            fechaHoraFin=datetime.datetime.strptime(data["FechaHoraFin"], "%Y-%m-%d %H:%M:%S")
        
        try:
            userPara = User.objects.get(id=data["citaPara"])
            nombrePara=userPara.username
        except User.DoesNotExist:
            content = {'mensaje': 'UsuarioPara no existe'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        try:
            userCon = User.objects.get(id=data["citaCon"])
            nombreCon = userCon.username
        except User.DoesNotExist:
            content = {'mensaje': 'UsuarioCon no existe'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        
        c=Cita.objects.get_or_create(titulo=evento,
        descripcion=descripcion,
        fecha_hora_inicio=fechaHoraInicio,
        fecha_hora_fin=fechaHoraFin,
        lugar=lugar,
        nombre_para=nombrePara,
        nombre_con=nombreCon,
        cancelado=False,
        dia_completo=diaCompleto,
        id_user_para=userPara,
        id_user_con=userCon)
        
        if (c[1]==False):
            content = {'mensaje':'Cita previamente guardada'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        else:
            content = {'guardado':True}
            return Response(content, status=status.HTTP_201_CREATED)
        

@api_view(['GET'])
@permission_classes((AllowAny, ))
def obtenerCitasMes(request, anio):
    data=[]
    start_date = datetime.date(int(anio), 1, 1)
    end_date = datetime.date(int(anio), 12, 31)
    citas=Cita.objects.filter(fecha_hora_inicio__range=(start_date, end_date),cancelado=False)
    for cita in citas:
        cit ={
            'id':cita.id_cita,
            'title':cita.titulo,
            'start':cita.fecha_hora_inicio,
            'end':cita.fecha_hora_fin
        }
        data.append(cit)
    
    content = {"citas": data}
    return Response(content, status=status.HTTP_200_OK)
    #https://stackoverflow.com/questions/15874233/output-django-queryset-as-json

@api_view(['GET'])
@permission_classes((AllowAny, ))
def detalleCita(request, idCita):
    try:
        cita = Cita.objects.get(id_cita=idCita)
        cita ={
            'evento':cita.titulo,
            'descripcion':cita.descripcion,
            'fechaHorainicio':cita.fecha_hora_inicio,
            'fechaHorafin':cita.fecha_hora_fin,
            'lugar':cita.lugar,
            'citaPara':cita.id_user_para.username,
            'citaCon':cita.id_user_con.username,
            'cancelado':cita.cancelado
        }
        content = {"detalle": cita}
        return Response(content, status=status.HTTP_200_OK)
    except Cita.DoesNotExist:
        content = {"mensaje": "La cita no existe"}
        return Response(content, status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
@permission_classes((AllowAny, ))
def cancelarCita(request, idCita):
    try:
        c=Cita.objects.get(id_cita=idCita)
        c.cancelado=True
        c.save()
        content = {"actualizado": True}
        return Response(content, status=status.HTTP_200_OK)
    except Cita.DoesNotExist:
        content = {"mensaje": "La cita no existe"}
        return Response(content, status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
@permission_classes((AllowAny, ))
def editarCita(request, idCita):
    data = json.loads(request.body)
    try:
        c=Cita.objects.get(id_cita=idCita)

        if (data["evento"] is None):
            data["evento"]=c.titulo
        if (data["descripcion"] is None):
            data["descripcion"]=c.descripcion
        if (data["lugar"] is None):
            data["lugar"]=c.lugar
        if (data["diaCompleto"] is None):
            data["diaCOmpleto"]=c.diaCompleto
        if (data["FechaHoraInicio"] is None):
            data["FechaHoraInicio"]=c.fecha_hora_inicio
        if (data["FechaHoraFin"] is None):
            data["FechaHoraFin"]=c.fecha_hora_fin
        if (data["citaPara"] is None):
            data["citaPara"]=c.fecha_hora_fin
        if (data["citaCon"] is None):
            data["citaCon"]=c.fecha_hora_fin

        evento =data["evento"]
        descripcion=data["descripcion"]
        lugar=data["lugar"]
        diaCompleto=data["diaCompleto"]
        ##Fecha inicio
        fechaHoraInicio=datetime.datetime.strptime(data["FechaHoraInicio"], "%Y-%m-%d %H:%M:%S")
        fechaInicio=fechaHoraInicio.strftime("%Y-%m-%d")
        
        citaPara=data["citaPara"]
        citaCon=data["citaCon"]
    
        if (citaPara is None and citaCon is None):
            content = {'mensaje': 'No se puede agendar sin registrar los nombres de las entidades'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        else:
            if (citaPara==citaCon):
                content = {'mensaje': 'No se puede agendar citas al mismo usuario'}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
            if (diaCompleto==True):
                fechaHoraInicio=datetime.datetime.strptime(fechaInicio+" 00:00:00","%Y-%m-%d %H:%M:%S")
                fechaHoraFin=datetime.datetime.strptime(fechaInicio+" 23:59:59","%Y-%m-%d %H:%M:%S")
            else:
                fechaHoraFin=datetime.datetime.strptime(data["FechaHoraFin"], "%Y-%m-%d %H:%M:%S")
            
            try:
                userPara = User.objects.get(id=data["citaPara"])
                nombrePara=userPara.username
            except User.DoesNotExist:
                content = {'mensaje': 'UsuarioPara no existe'}
                return Response(content, status=status.HTTP_404_NOT_FOUND)
            try:
                userCon = User.objects.get(id=data["citaCon"])
                nombreCon = userCon.username
            except User.DoesNotExist:
                content = {'mensaje': 'UsuarioCon no existe'}
                return Response(content, status=status.HTTP_404_NOT_FOUND)
            
            c.titulo=evento
            c.descripcion=descripcion
            c.fecha_hora_inicio=fechaHoraInicio
            c.fecha_hora_fin=fechaHoraFin
            c.lugar=lugar
            c.nombre_para=nombrePara
            c.nombre_con=nombreCon
            c.dia_completo=diaCompleto
            c.id_user_para=userPara
            c.id_user_con=userCon
            c.save()
            content = {'editado':True}
            return Response(content, status=status.HTTP_200_OK)
    except Cita.DoesNotExist:
        content = {"mensaje": "La cita no existe"}
        return Response(content, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes((AllowAny, ))
def notificacionesManana(request):
    anio = (datetime.date.today() + datetime.timedelta(days=1)).year
    dia = (datetime.date.today() + datetime.timedelta(days=1)).day
    mes = (datetime.date.today() + datetime.timedelta(days=1)).month
    citas=Cita.objects.filter(fecha_hora_inicio=datetime.date(anio,mes,dia),id_user_para=1).count()
    content = {'cantida':citas}
    return Response(content, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes((AllowAny, ))
def citasProximas(request):
    data=[]
    anio = (datetime.date.today() + datetime.timedelta(days=1)).year
    dia = (datetime.date.today() + datetime.timedelta(days=1)).day
    mes = (datetime.date.today() + datetime.timedelta(days=1)).month
    citas=Cita.objects.filter(fecha_hora_inicio=datetime.date(anio,mes,dia),id_user_para=1)
    for cita in citas:
        c ={
            'id':cita.id_cita,
            'evento':cita.titulo,
            'descripcion':cita.descripcion,
            'FechaHoraInicio':cita.fecha_hora_inicio.strftime("%Y-%m-%d %H:%M"),
            'FechaHoraFin':cita.fecha_hora_fin.strftime("%Y-%m-%d %H:%M"),
            'lugar':cita.lugar
        }
        data.append(c)
    content = {'citas':data}
    return Response(content, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes((AllowAny, ))
def entidades(request, idCargo):
    usuarios=[]
    grupos = {'1':'comunicaciones','2':'secretaria'}
    g=grupos[str(idCargo)]
    if (g=="comunicaciones"):
        users=User.objects.exclude(id=1)
    else:
        users=User.objects.all()
    for u in users:
        user={
            'id':u.id,
            'nombreUsuario':u.username,
            'nombre':u.first_name,
            'apellido':u.last_name
        }
        usuarios.append(user)
    content = {'usuarios':usuarios}
    return Response(content, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes((AllowAny, ))
def obtenerCitasMesEstudiantes(request, anio, idEstudiante):
    try:
        u=User.objects.get(id=idEstudiante)
        data=[]
        
        start_date = datetime.date(int(anio), 1, 1)
        end_date = datetime.date(int(anio), 12, 31)
        citas=Cita.objects.filter(fecha_hora_inicio__range=(start_date, end_date),cancelado=False, id_user_para=u)
        for cita in citas:
            cit ={
                'id':cita.id_cita,
                'title':cita.titulo,
                'start':cita.fecha_hora_inicio,
                'end':cita.fecha_hora_fin
            }
            data.append(cit)
        content = {"citas": data}
        return Response(content, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        content = {"mensaje": 'usuario no existe'}
        return Response(content, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes((AllowAny, ))
def obtenerCitasMesAdmin(request, anio, uadmin):
    data=[]
    an=int(anio)
    
    start_date = datetime.date(int(anio), 1, 1)
    end_date = datetime.date(int(anio), 12, 31)
    
    try:
        u=User.objects.get(id=uadmin)

        grupos = {'1':'comunicaciones','2':'secretaria'}
        g=grupos[str(uadmin)]

        if (g=="comunicaciones"):
            citas=Cita.objects.filter(fecha_hora_inicio__range=(start_date, end_date),cancelado=False).exclude(id_user_para=1)
            for cita in citas:
                cit ={
                    'id':cita.id_cita,
                    'title':cita.titulo,
                    'start':cita.fecha_hora_inicio,
                    'end':cita.fecha_hora_fin
                }
                data.append(cit)
            
            content = {"citas": data}
            return Response(content, status=status.HTTP_200_OK)
        else:
            citas=Cita.objects.filter(fecha_hora_inicio__range=(start_date, end_date),cancelado=False, id_user_para=1)
            for cita in citas:
                cit ={
                    'id':cita.id_cita,
                    'title':cita.titulo,
                    'start':cita.fecha_hora_inicio,
                    'end':cita.fecha_hora_fin
                }
                data.append(cit)
            
            content = {"citas": data}
            return Response(content, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        content = {"mensaje": 'usuario no existe'}
        return Response(content, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes((AllowAny, ))
def obtenerCitasMesYear(request, mes, anio):
    data=[]
    an=int(anio)
    strmes=str(mes)
    diaFIn={'1':31,'2':28,'3':31,'4':30,'5':31,'6':30,'7':31,'8':31,'9':30,'10':31,'11':30,'12':31,'2b':29}
    if(an % 4 == 0 and an % 100 != 0 or an % 400 == 0):
        fin='2b'
        dFin=diaFIn[fin]
    dFin=diaFIn[strmes]
    start_date = datetime.date(int(anio), int(mes), 1)
    end_date = datetime.date(int(anio), int(mes), int(dFin))
    citas=Cita.objects.filter(fecha_hora_inicio__range=(start_date, end_date),cancelado=False)
    for cita in citas:
        cit ={
            'id':cita.id_cita,
            'title':cita.titulo,
            'start':cita.fecha_hora_inicio,
            'end':cita.fecha_hora_fin
        }
        data.append(cit)
    
    content = {"citas": data}
    return Response(content, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes((AllowAny, ))
def regApirante(request):
    data = json.loads(request.body)
    u, userAsp = User.objects.get_or_create(username=data["nombreuser_aspirante"], email=data["email"])
    if userAsp:
        u.set_password(data["password"])
        u.save()
        try:
            v = Validacion.objects.get(id_codigo=data["idVal"])
        except Validacion.DoesNotExist:
            content = {"msj": "codigo no existe"}
            return Response(content, status=status.HTTP_404_NOT_FOUND)

        Aspirante.objects.create(
            nombre_aspirante=data["nombreAsp"],
            apellido_aspirante=data["apellidoAsp"],
            contrasena_aspirante=hashlib.md5(data["password"].encode('utf-8')),
            dui=data["dui"],
            genero=data["genero"],
            fechas_nac=data["fechas_nac"],
            t_fijo=data["t_fijo"],
            t_movil=data["t_movil"],
            email=data["email"],
            titulo_pre=data["titulo_pre"],
            institucion=data["institucion"],
            f_expedicion=data["f_expedicion"],
            municipio=data["municipio"], 
            lugar_trab=data["lugar_trab"],  
            programa=data["programa"],
            aceptado=False,
            nombreuser_aspirante=data["nombreuser_aspirante"],
            id_user=u,
            id_val=v
            )
        content = {"guardado": True}
        return Response(content, status=status.HTTP_201_CREATED)
    else:
        content = {"msj": "usuario ya existe"}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)

