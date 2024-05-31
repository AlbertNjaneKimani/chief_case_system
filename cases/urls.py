from django.urls import path
from .views import register,createprofile,createcase,dashboard,loginview, logoutview, homepage,biodatalist, appointments, cases,approvecase, rejectcase,bookappointment,editprofile,resolvecase,deletecase 

urlpatterns = [
    path('register/', register, name='register'),
    path('profile/', createprofile, name='createprofile'),
    path('case/', createcase, name='createcase'),
    path('dashboard/', dashboard, name='dashboard'),
    path('login/', loginview, name='loginview'),
    path('logout/', logoutview, name='logoutview'),
    path('', homepage, name='homepage'),
    path('/bios', biodatalist, name='biodatalist'),
    path('/cases', cases, name='cases'),
    path('/appointments', appointments, name='appointments'),
    path('approve_case/<int:case_id>/', approvecase, name='approvecase'),
    path('reject_case/<int:case_id>/', rejectcase, name='rejectcase'),
    path('resolvecase/<int:case_id>/', resolvecase, name='resolvecase'),
    path('appointment/<int:case_id>/', bookappointment, name='bookappointment'),
    path('biodata/edit/<int:user_id>/', editprofile, name='editprofile'),
     path('cases/delete/<int:case_id>/', deletecase, name='deletecase'),
    

]