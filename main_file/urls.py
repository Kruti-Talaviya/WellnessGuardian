
from django.conf.urls.static import static
from django.conf import settings
from . import views
from django.urls import path
# from django.views import view


urlpatterns = [
#    path('',view.home, name='home')
      path('',views.index,name='index'),
      path('register',views.register,name='register'),
      path('Login',views.Login,name='Login'),
      path('logout',views.logout,name='logout'),
      path('createprofilep',views.createprofilep,name='createprofilep'),
      path('createprofileh',views.createprofileh,name='createprofileh'),
      path('welcomep',views.welcomep,name='welcomep'),
      path('welcomeh',views.welcomeh,name='welcomeh'),
      path('addrecords',views.addrecords,name='addrecords'),
      path('viewrecords',views.viewrecords,name='viewrecords'),
      path('searchpatient',views.searchpatient,name='searchpatient'),
      path('managepprofile',views.managepprofile,name='managepprofile'),
      path('managehprofile',views.managehprofile,name='managehprofile')


]+ static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
