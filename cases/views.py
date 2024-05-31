from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Case, User, Appointment,UserProfile
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .forms import UserRegisterForm, UserProfileForm, CaseForm, UserLoginForm, AppointmentForm
from datetime import datetime
from django.core.mail import send_mail
def register(request):
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            login(request, user)
            messages.success(request, 'User Account created successfully.')
            return redirect('loginview')
    else:
        user_form = UserRegisterForm()
    return render(request, 'register.html', {'user_form': user_form})

@login_required
def createprofile(request):
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST)
        if profile_form.is_valid():
            profile = profile_form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, 'Bio data added successfully.')
            return redirect('biodatalist') 
    else:
        profile_form = UserProfileForm()
    return render(request, 'profile.html', {'biodata_form': profile_form})

@login_required
def createcase(request):
    if request.method == 'POST':
        form = CaseForm(request.POST)
        if form.is_valid():
            case = form.save(commit=False)
            case.complainant = request.user
            case.save()
            messages.success(request, 'Case created successfully.')
            return redirect('dashboard')
    else:
        form = CaseForm()
    return render(request, 'case.html', {'form': form})

@login_required
def biodatalist(request):
    bio_data = UserProfile.objects.all()
    return render(request, 'bios.html', {'bio_data': bio_data})



from datetime import datetime

@login_required
def cases(request):
    search_name = request.GET.get('search_name')
    search_category = request.GET.get('search_category')
    search_owner = request.GET.get('search_owner')
    search_status = request.GET.get('search_status')
    search_date = request.GET.get('search_date')
    
    cases = Case.objects.all()
    if search_name:
        cases = cases.filter(title__icontains=search_name)
    if search_category:
        cases = cases.filter(casecategory__icontains=search_category)
    if search_owner:
        cases = cases.filter(complainant__first_name__icontains=search_owner) | \
                cases.filter(complainant__last_name__icontains=search_owner)
    if search_status:
        cases = cases.filter(status=search_status)
    if search_date:
        search_date = datetime.strptime(search_date, '%Y-%m-%d').date()
        cases = cases.filter(date_created__date=search_date)

    for case in cases:
        if case.complainant:
            complainant_user = case.complainant
            case.complainant_name = f"{complainant_user.first_name} {complainant_user.last_name}"
        else:
            case.complainant_name = None

    return render(request, 'cases.html', {'cases': cases})



@login_required
def appointments(request):
    appointments = Appointment.objects.all()
    return render(request, 'appointments.html', {'appointments': appointments})



def loginview(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                error_message = "Invalid username or password."
                messages.error(request, error_message)
                return render(request, 'login.html', {'form': form})
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})
def logoutview(request):
    logout(request)
    return redirect('loginview')

def homepage(request):
    return render(request, 'index.html')    

@login_required
def approvecase(request, case_id):
    case = get_object_or_404(Case, id=case_id)
    if request.user.is_staff: 
        case.status = 'approved'
        case.save()
        messages.success(request, 'Case approved successfully.')
    else:
        messages.error(request, 'You do not have permission to approve cases.')
    return redirect('cases')

@login_required
def rejectcase(request, case_id):
    case = get_object_or_404(Case, id=case_id)
    if request.user.is_staff: 
        case.status = 'rejected'
        case.save()
        messages.success(request, 'Case rejected successfully.')
    else:
        messages.error(request, 'You do not have permission to reject cases.')
    return redirect('cases')    

@login_required
def resolvecase(request, case_id):
    case = get_object_or_404(Case, id=case_id)
    if request.user.is_staff: 
        case.status = 'solved'
        case.save()
        messages.success(request, 'Case resolved successfully.')
    else:
        messages.error(request, 'You do not have permission to resolve cases.')
    return redirect('cases')

@login_required
def completeappointment(request, case_id):
    appointment = get_object_or_404(Appointment, id=case_id)
    if request.user.is_staff: 
        appointment.appointment_status = 'completed'
        appointment.save()
        messages.success(request, 'appointment completed Successfully.')
    else:
        messages.error(request, 'You do not have permission to complete appointment.')
    return redirect('appointments')    

@login_required
def bookappointment(request, case_id):
    
    case = get_object_or_404(Case, pk=case_id)
    
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.case = case  
            appointment.chief = request.user  
            appointment.complainant = request.user  
            appointment.appointment_status = 'active' 
            appointment.save()
            
            send_appointment_email(appointment)
            
            messages.success(request, 'Invitation created successfully.')
            return redirect(reverse('bookappointment', args=[case_id]))
    else:
        form = AppointmentForm()
    return render(request, 'book_appointment.html', {'form': form})

def send_appointment_email(appointment):
    
    complainant_email = appointment.case.complainant.email
    complainant_name = appointment.case.complainant.get_full_name()
    
    subject = 'Invitation To Chiefs Office'
    message = (
        f"Dear {complainant_name},\n\n"
        "You have Been Invited to chiefs office concerning the case that you submitted. "
        "See the invitation details below:\n\n"
        f"Case Number: {appointment.case.id}\n"
        f"Case Name: {appointment.case.title}\n"
        f"Appointment Date: {appointment.date}\n"
        f"Appointment Time: {appointment.time}\n"
        f"Venue: {appointment.location}\n\n"
        "Best Regards,\n\n"
        "Area Chief."
    )
    
    # Send the email
    send_mail(subject, message, 'your_email@example.com', [complainant_email], fail_silently=False)

@login_required
def editprofile(request, user_id):
    profile = get_object_or_404(UserProfile, user_id=user_id)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Biodata updated successfully.')
            return redirect('biodatalist')
    else:
        form = UserProfileForm(instance=profile)
    
    return render(request, 'edit_profile.html', {'form': form, 'profile': profile})
@login_required   
def casedetails(request, case_id):
    case = get_object_or_404(Case, pk=case_id)
    return render(request, 'case_detail.html', {'case': case})

@login_required
def deletecase(request, case_id):
    case = get_object_or_404(Case, id=case_id)
    case.delete()
    messages.success(request, "Case deleted successfully")
    return redirect('dashboard')

@login_required
def dashboard(request):
    # Fetch data for metrics
    total_cases = Case.objects.count()
    total_complainants = User.objects.filter(role='complainant').count()
    total_pending_cases = Case.objects.filter(status='pending').count()
    total_solved_cases = Case.objects.filter(status='solved').count()
    total_rejected_cases = Case.objects.filter(status='rejected').count()
    total_active_appointments = Appointment.objects.filter(appointment_status='active').count()
    
    # Fetch top 10 cases (assuming we want to show the latest or most relevant cases)
    top_cases = Case.objects.all().order_by('-date_created')[:10]

    return render(request, 'dashboard.html', {
        'total_cases': total_cases,
        'total_complainants': total_complainants,
        'total_pending_cases': total_pending_cases,
        'total_solved_cases': total_solved_cases,
        'total_rejected_cases': total_rejected_cases,
        'total_active_appointments': total_active_appointments,
        'top_cases': top_cases
    })
