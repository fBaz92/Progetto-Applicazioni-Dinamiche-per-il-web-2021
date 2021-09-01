from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse 
import json
import urllib.request
from portale.models import Notice, Lesson, OfficeHour, Student
import datetime
from datetime import date
from django.middleware.csrf import get_token
# Create your views here.

def GetUpdates (request):
    date = json.loads(request.body)['day']
    if len(date) == 0:
        date = datetime.date.today().strftime("%Y-%m-%d")
    res = urllib.request.urlopen('https://www.di.univr.it/?ent=evento&idDip=30&' + 'a=' + date[0:4] + '&g=' + date[8:] + 
    '&m=' + date[5:7] + '&out=json').read()
    res = res.decode("utf-8")
    res = str(res).replace('"note": new Element(\'span\').set(\'html\', ','"note": ')
    res = str(res).replace(').get(\'text\'), "intervallo":', ', "intervallo":')
    res = res.replace('	', ' ')
    data = json.loads(res)
    Notices = []
    Lessons = []
    Officehours = []
    date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
    for notice in data['notices']:
       if not Notice.objects.filter(data_notice= date, data_pubblicazione = datetime.datetime.strptime(
       str(notice['dataPubblicazione']), '%b %d, %Y %H:%M:%S'), titolo = str(notice['titolo'])).exists():
         new_notice = Notice.objects.create(data_notice= date, data_pubblicazione = datetime.datetime.strptime(
         str(notice['dataPubblicazione']), '%b %d, %Y %H:%M:%S'), 
         titolo = str(notice['titolo']), testo = str(notice['testo']), mittenti = str(notice['mittenti']))
         new_notice.save() 
       n = [str(notice['titolo']), str(notice['testo']), str(notice['mittenti']) ]
       Notices.append(n)

    for lesson in data['lessons']['value']:
       if not Lesson.objects.filter(data_lesson= date, nome = str(lesson['nome']), 
       ora_inizio = datetime.datetime.strptime(str(lesson['intervallo'][0]['oraInizio']), '%b %d, %Y %H:%M:%S')).exists(): 
         new_lesson = Lesson.objects.create(data_lesson= date, nome = str(lesson['nome']), 
         ora_inizio = datetime.datetime.strptime(str(lesson['intervallo'][0]['oraInizio']), '%b %d, %Y %H:%M:%S'), 
         ora_fine = datetime.datetime.strptime(str(lesson['intervallo'][0]['oraFine']), '%b %d, %Y %H:%M:%S'), 
         id_edificio = str(lesson['intervallo'][0]['luogo'][0]['idEdificio']), 
         tipo_luogo = str(lesson['intervallo'][0]['luogo'][0]['tipo']), 
         nome_luogo = str(lesson['intervallo'][0]['luogo'][0]['nome']), )
         new_lesson.save() 
       l = [str(lesson['nome']), str(lesson['intervallo'][0]['oraInizio' ]), str(lesson['intervallo'][0]['oraFine']), 
       str(lesson['intervallo'][0]['luogo'][0]['tipo']), str(lesson['intervallo'][0]['luogo'][0]['nome'])  ] 
       Lessons.append(l)

    for office_hour in data['officehours']['value']:
       new_id_edificio = ''
       new_tipo_luogo = ''
       new_nome_luogo = '' 
       if not OfficeHour.objects.filter(data_officehour= date, nome = str(office_hour['nome']), 
       ora_inizio = datetime.datetime.strptime(str(office_hour['intervallo'][0]['oraInizio']), '%b %d, %Y %H:%M:%S'),
       ora_fine = datetime.datetime.strptime(str(office_hour['intervallo'][0]['oraFine']), '%b %d, %Y %H:%M:%S')).exists(): 
         if "note" in office_hour:
             new_note = str(office_hour['note'])
         else:
              new_note = ''

         if len(office_hour['intervallo'][0]['luogo']) != 0:
             new_id_edificio = str(office_hour['intervallo'][0]['luogo'][0]['idEdificio'])
             new_tipo_luogo = str(office_hour['intervallo'][0]['luogo'][0]['tipo'])
             new_nome_luogo = str(office_hour['intervallo'][0]['luogo'][0]['nome'])
         else:
             new_id_edificio = ''
             new_tipo_luogo = ''
             new_nome_luogo = ''
         new_office_hour = OfficeHour.objects.create(data_officehour = date, nome = str(office_hour['nome']), note = new_note, 
         ora_inizio = datetime.datetime.strptime(str(office_hour['intervallo'][0]['oraInizio']), '%b %d, %Y %H:%M:%S'), 
         ora_fine = datetime.datetime.strptime(str(office_hour['intervallo'][0]['oraFine']), '%b %d, %Y %H:%M:%S'), 
         id_edificio = new_id_edificio, 
         tipo_luogo = new_tipo_luogo, 
         nome_luogo = new_nome_luogo)
         new_office_hour.save() 

       o = [str(office_hour['nome']), str(office_hour['intervallo'][0]['oraInizio' ]), str(office_hour['intervallo'][0]['oraFine']), 
       new_tipo_luogo, new_nome_luogo ] 
       Officehours.append(o)
    return JsonResponse({'result': 'ok'})  

def index (request): 
    return render(request,'index.html')


def Login (request):
  if request.method == 'POST':
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username = username, password = password)
    if user is not None:
      login(request, user)
      return redirect ('user/' + username)
    else:
      messages.info(request,'username or password not valid')
      return redirect ('login')       
  else:
    return render(request,'login.html')

def Logout(request):
    logout(request)
    return redirect('login')
        
    

def register(request):
     if request.method == 'POST':
         username = request.POST['username']
         email = request.POST['email']
         password = request.POST['password']
         password2 = request.POST['password2']
         if password != password2:
             messages.info(request,'password does not match')
             return redirect ('register')
         elif Student.objects.filter(email = email).exists():
             messages.info(request,'email already used')
             return redirect ('register')
         elif Student.objects.filter(username = username).exists():
             messages.info(request,'username already used')
             return redirect ('register')
         else:
             Student.objects.create_user(username = username, email = email, password = password)
             return redirect('Login')
     else:
         return render(request,'register.html')

def user(request, username):
    return render(request, 'user.html', {'username': username})

def LoadUpdates(request):
    username = None
    if request.user.is_authenticated:
        username = request.user.username
    student = Student.objects.get(username = username)
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
      today = date.today()
      date_request = json.loads(request.body)['day']
      if len(date_request) > 0:
        today = datetime.datetime.strptime(date_request, '%Y-%m-%d').date()
      else:
        date_request = today.strftime("%Y-%m-%d")
      
      notice_on = list(Notice.objects.filter(data_notice = today ).exclude(student__id = student.id).values())
      notice_off = list(Notice.objects.filter(student__id = student.id, data_notice = today ).values())

      
      lesson_on = list(Lesson.objects.filter(data_lesson = today).exclude(student__id = student.id).values()) 
      lesson_off = list(Lesson.objects.filter(student__id = student.id, data_lesson = today).values()) 

     
      office_hour_on = list(OfficeHour.objects.filter(data_officehour = today).exclude(student__id = student.id).values())
      office_hour_off = list(OfficeHour.objects.filter(student__id = student.id, data_officehour = today).values())  

      return JsonResponse([notice_on, notice_off, lesson_on, lesson_off, office_hour_on, office_hour_off], safe=False, status = 200)
       
    

def getuser(request):
    username = None
    if request.user.is_authenticated:
        username = request.user.username
    return JsonResponse({"username": username}, safe=False, status = 200)

def generate_csrf(request):
    return JsonResponse({'csrf_token': get_token(request)}, status=200)

def hide(request):
  username = None
  if request.user.is_authenticated:
      username = request.user.username
  element = json.loads(request.body)
  if 'titolo' in element.keys():
    Student.objects.get(username = username).notice.add(Notice.objects.get(data_notice = element['data_notice'], titolo = element['titolo']))
  elif 'note' in element.keys():
    Student.objects.get(username = username).office_hour.add(OfficeHour.objects.get(data_officehour = element['data_officehour'], nome = element['nome'], ora_inizio = element['ora_inizio'])) 
  elif 'nome' in element.keys():
    Student.objects.get(username = username).lesson.add(Lesson.objects.get(data_lesson = element['data_lesson'], nome = element['nome'], ora_inizio = element['ora_inizio'])) 
  
  return JsonResponse({'result': 'ok'})

def retrive(request):
  username = None
  if request.user.is_authenticated:
      username = request.user.username
  element = json.loads(request.body)
  if 'titolo' in element.keys():
    Student.objects.get(username = username).notice.remove(Notice.objects.get(data_notice = element['data_notice'], titolo = element['titolo']))
  elif 'note' in element.keys():
    Student.objects.get(username = username).office_hour.remove(OfficeHour.objects.get(data_officehour = element['data_officehour'], nome = element['nome'], ora_inizio = element['ora_inizio'])) 
  elif 'nome' in element.keys():
    Student.objects.get(username = username).lesson.remove(Lesson.objects.get(data_lesson = element['data_lesson'], nome = element['nome'], ora_inizio = element['ora_inizio'])) 
  return JsonResponse({'result': 'ok'})

  
    