
from imaplib import _Authenticator
from django.shortcuts import render
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import auth
from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import datetime, timezone
from .models import Custom_User, MediRecord, hospitalInfo, patientInfo,login
from django.core.mail import send_mail


def index(request):
   return render(request,'Home.html')

def welcomep(request):
   request.session['Login_id']=request.session['Login_id']
   return render(request,'welcome.html')

def welcomeh(request):
   request.session['Login_id']=request.session['Login_id']
   return render(request,'welcomeh.html')

def managepprofile(request):
   if 'Login_id' not in request.session:
        return redirect('Login')
   else:
        request.session['Login_id']=request.session['Login_id']
   user_id=request.session['Login_id']

   profile = patientInfo.objects.get(user_id=user_id)

   if request.method == 'POST':
        fullname = request.POST.get('fullname')
        age = request.POST.get('age')
        dob = request.POST.get('dob')
        contact_no = request.POST.get('contact_no')
        address = request.POST.get('address')
        profile_photo = request.FILES.get('profile_pht')
 
        formatted_dob = datetime.strptime(dob,'%B %d, %Y').strftime('%Y-%m-%d')
        
        profile.fullname = fullname
        profile.age = age
        profile.dob =  formatted_dob
        profile.contact_number= contact_no
        profile.address = address
        profile.profile_photo = profile_photo
        profile.save()

        return redirect(welcomep)
   else:
       return render(request,'manage_profile_p.html',{'profile' : profile })

def managehprofile(request):
   if 'Login_id' not in request.session:
        return redirect('Login')
   else:
        request.session['Login_id']=request.session['Login_id']
   user_id=request.session['Login_id']

   profile = hospitalInfo.objects.get(user_id=user_id)

   if request.method == 'POST':
        fullname = request.POST.get('fullname')
        address = request.POST.get('address')
        speciality = request.POST.get('speciality')
        # hospital_photo = request.FILES.get('hospital_photo')
        certificates = request.FILES.get('certificates')
        contact_number = request.POST.get('contact_number')
        
        profile.hospital_name = fullname
        profile.speciality = speciality
        profile.certificates =  certificates
        profile.contact_number= contact_number
        profile.address = address
        # profile.hospital_photo = hospital_photo
        profile.save()

        return redirect(welcomeh)
   else:
       return render(request,'manage_profile_h.html',{'profile' : profile })


def createprofilep(request):
   if 'Login_id' not in request.session:
        return redirect('Login')
   else:
        request.session['Login_id']=request.session['Login_id']

   user_id=request.session['Login_id']
   if request.method == 'POST':
       fullname = request.POST.get('fullname')
       age = request.POST.get('age')
       gender = request.POST.get('gender')
       dob = request.POST.get('dob')
       address = request.POST.get('address')
       profile_photo = request.FILES.get('profile_photo')
       contact_number = request.POST.get('contact_number')
    #    if dob:
       dob_obj = datetime.strptime(dob, "%m/%d/%Y")
       formatted_dob = dob_obj.strftime("%Y-%m-%d")
    #    else:
    #     formatted_dob = None
       profile = patientInfo.objects.create(
            user_id=user_id,
            fullname=fullname,
            age=age,
            gender=gender,
            dob=formatted_dob,
            address=address,
            profile_photo=profile_photo,
            contact_number=contact_number
        )
       profile.save()
       return redirect('welcomep')
   else:
       return render(request, 'Create_Profile_p.html')

def createprofileh(request):
   if 'Login_id' not in request.session:
        return redirect('Login')
   else:
        request.session['Login_id']=request.session['Login_id']

   user_id=request.session['Login_id']
   if request.method == 'POST':
       fullname = request.POST.get('fullname')
       address = request.POST.get('address')
       speciality = request.POST.get('speciality')
    #    hospital_photo = request.FILES.get('hospital_photo')
       certificates = request.FILES.get('certificates')
       contact_number = request.POST.get('contact_number')
       
       profileh = hospitalInfo.objects.create(
            user_id=user_id,
            hospital_name=fullname,
            address=address,
            certificates=certificates,
            speciality=speciality,
            # hospital_photo=hospital_photo,
            contact_number=contact_number
        )
       profileh.save()
       return redirect('welcomeh')
   else:
       return render(request, 'create_profile_h.html')

def addrecords(request):
    if 'Login_id' not in request.session:
        return redirect('Login')
    else:
        request.session['Login_id']=request.session['Login_id']
    user_id=request.session['Login_id']
    if request.method == 'POST':
        hospital_name = request.POST.get('hospital_name')
        diseases = request.POST.get('diseases')
        medi_document = request.FILES.get('medi_document')
        note = request.POST.get('note')

        record = MediRecord.objects.create(
            user_id=user_id,
            hospital_name=hospital_name,
            diseases=diseases,
            medi_document=medi_document,
            note=note
        )
        record.save()
        return redirect('welcomep') 
    else:
      return render(request, 'add_history.html')

def viewrecords(request):
   if 'Login_id' not in request.session:
        return redirect('Login')
   else:
        request.session['Login_id']=request.session['Login_id']
   user_id=request.session['Login_id']

   record = MediRecord.objects.filter(user_id=user_id)
   return render(request,'viewrecord.html',{'record' : record })

# def searchhospital(request):
#    if 'Login_id' not in request.session:
#         return redirect('Login')
#    else:
#         request.session['Login_id']=request.session['Login_id']
#    user_id=request.session['Login_id']

#    record = MediRecord.objects.filter(user_id=user_id)
# #    return render(request,'viewrecord.html',{'record' : record })
#    return render(request, 'search_hospital.html')


def searchpatient(request):
   if 'Login_id' not in request.session:
        return redirect('Login')
   else:
        request.session['Login_id']=request.session['Login_id']
   
   if request.method == 'POST':
        patient_id = request.POST['patient_id'] 
        record = MediRecord.objects.filter(user_id=patient_id)
        pinfo = patientInfo.objects.get(user_id=patient_id)
        return render(request,'s_patient_data.html',{'record': record, 'pinfo': pinfo})
   
   else: 
    return render(request, 'search_patient.html')

def Login(request):
    if request.method == 'POST':
        user_id = request.POST['userid'] 
        username = request.POST['username']
        password = request.POST['password']
      
        user = authenticate(request, username=user_id, password=password) 
        if user is not None:
         
             auth_login(request, user)
             new_login = login.objects.create(user_id=user_id)
             new_login.save()
             request.session['Login_id'] = user_id
              
             if user.user_type == 'Patient':
                  if patientInfo.objects.filter(user_id=user.user_id).exists():  
                    return redirect('welcomep') 
                  else:
                    return redirect('createprofilep')
             else:
                  if hospitalInfo.objects.filter(user_id=user.user_id).exists():
                     return redirect('welcomeh')
                  else:
                    return redirect('createprofileh')  
        else:
            return redirect('Login') 
    else:
        return render(request, 'log_in.html')

    
def register(request):
    if request.method == 'POST':
        user_type = request.POST['user_type']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password1']
        password2 = request.POST['password2']
    
        if password == password2:
            if Custom_User.objects.filter(username=username).exists():
                messages.info(request, 'Username taken')
                return redirect('register')
            # elif Custom_User.objects.filter(email=email).exists():
            #     messages.info(request, 'Email taken')
            #     return redirect('register')
            else:
                user = Custom_User.objects.create_user(user_type=user_type, username=username, email=email, password=password)
                user.save()
                messages.success(request, 'User created successfully')
                user_id= user.user_id
                send_mail('Your WellnessGuardian User id', 
                          f'Thank you so much for sign up in our website, this is you user id {user_id} for using our site ', 
                          'talaviyakruti@gmail.com',
                           [user.email])
                return redirect('Login')
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('register')
    else:
        return render(request, 'sign_in.html')


def logout(request):
    auth.logout(request)
    request.session.flush()
    return redirect('/')
    