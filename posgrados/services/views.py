from django.contrib.auth.models import User, Group, Permission, PermissionsMixin
from rest_framework.permissions import IsAuthenticated , AllowAny
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from .serializers import UserSerializer, ImgSerializer,RolUsuariosSerializer,User1Serializer, PermisionsMixinSerializer,  NoticiaSerializer, AspiranteSerializer, GroupSerializer, PermisionsSerializer, CodigoSerializer
from rest_framework import status, viewsets, generics, mixins
from rest_framework.decorators import api_view, permission_classes, authentication_classes, action
from rest_framework.response import Response
from .models import  Noticia, Aspirante,Image, Validacion, Cita
from rest_framework.authtoken.models import Token
import json,time, random, requests, hashlib, calendar
from django.core import serializers
from datetime import datetime, date

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
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)
    lookup_field = 'id'
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.all()

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class NoticiaAPICreate(mixins.CreateModelMixin, generics.ListAPIView):
    permission_classes = (AllowAny,)
    lookup_field = 'id'
    serializer_class = NoticiaSerializer

    def get_queryset(self):
        return Noticia.objects.all()

    def post(self, request , *args, **kwargs):
        return self.create(request , *args, **kwargs)

class CodigoAPICreate(mixins.CreateModelMixin, generics.ListAPIView):
    permission_classes = (AllowAny,)
    lookup_field = 'id'
    serializer_class = CodigoSerializer

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
    apiKey = "435794978697618"
    apiSecret = "hzyKk4HoLpb_O8gTqhaYPc0FGiY"
    timestamp = calendar.timegm(time.gmtime())
    sign = "timestamp="+str(timestamp)+apiSecret
    signature = hashlib.sha1(sign.encode('utf-8')).hexdigest()
    noti= requests.post("https://api.cloudinary.com/v1_1/ddjmdjmvk/image/upload", data={'file':data["foto"], 'api_key':apiKey, 'timestamp':timestamp, 'signature':signature})
    print (noti)
    Noticia.objects.create(emcabezado=data["encabezado"],
    cuerpo=data["cuerpo"],
    fecha=data["fechas"],
    id_user_id=data["idUsuario"],
    imagenUrl=noti.json()["url"])
    content = {'guardado': True}
    return Response(content, status=status.HTTP_201_CREATED)




class AspiranteAPICreate(mixins.CreateModelMixin, generics.ListAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    permission_classes = (AllowAny,)
    lookup_field = 'id_aspirante'
    serializer_class = AspiranteSerializer

    def get_queryset(self):
        return Aspirante.objects.all()

    def post(self, request , *args, **kwargs):
        return self.create(request , *args, **kwargs)


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

@api_view(['POST'])
@permission_classes((AllowAny, ))
def agendarCita(request):
    data = json.loads(request.body)
    evento =data["evento"]
    descripcion=data["descripcion"]
    lugar=data["lugar"]
    diaCompleto=data["diaCompleto"]
    ##Fecha inicio
    fechaHoraInicio=datetime.strptime(data["FechaHoraInicio"], "%d/%m/%y %H:%M:%S")
    fechaInicio=fechaHoraInicio.strftime("%d/%m/%y")
    horaInicio=fechaHoraInicio.strftime("%H:%M:%S")
    ##Fecha fin
    fechaHoraFin=datetime.strptime(data["FechaHoraFin"], "%d/%m/%y %H:%M:%S")
    citaPara=data["citaPara"]
    citaCon=data["citaCon"]
    nombrePara=data["nombrePara"]
    nombreCon=data["nombreCon"]
            
    if (nombrePara is None and nombreCon is None and citaPara is None and citaCon is None):
        content = {'mensaje': 'No se puede agendar sin registrar los nombres de las entidades'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    else:
        if (citaPara==citaCon):
            content = {'mensaje': 'No se puede agendar citas al mismo usuario'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        if (diaCompleto==True):
            fechaHoraInicio=datetime.strptime(fechaInicio+" 00:00:00","%d/%m/%y %H:%M:%S")
            fechaHoraFin=datetime.strptime(fechaInicio+" 23:59:59","%d/%m/%y %H:%M:%S")
        
        userPara = User.objects.get(id=data["citaPara"])
        userCon = User.objects.get(id=data["citaCon"])
        
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
def obtenerCitasMes(request, mes, anio):
    an=int(anio)
    strmes=str(mes)
    diaFIn={'1':31,'2':28,'3':31,'4':30,'5':31,'6':30,'7':31,'8':31,'9':30,'10':31,'11':30,'12':31,'2b':29}
    if(an % 4 == 0 and an % 100 != 0 or an % 400 == 0):
        fin='2b'
        dFin=diaFIn[fin]
    dFin=diaFIn[strmes]
    start_date = date(int(anio), int(mes), 1)
    end_date = date(int(anio), int(mes), int(dFin))
    c=Cita.objects.values_list('id_cita','titulo','fecha_hora_inicio','fecha_hora_fin').filter(fecha_hora_inicio__range=(start_date, end_date))
    return str(c)
    #https://stackoverflow.com/questions/15874233/output-django-queryset-as-json