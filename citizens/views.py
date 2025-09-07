from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .forms import CitizenRegistrationForm, IssueReportForm
from issues.models import Issue, UserProfile, Category

def register(request):
    if request.method == 'POST':
        form = CitizenRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('citizen_dashboard')
    else:
        form = CitizenRegistrationForm()
    return render(request, 'citizens/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.userprofile.role == 'Citizen':
                login(request, user)
                return redirect('citizen_dashboard')
            else:
                messages.error(request, 'Invalid credentials for Citizen login.')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'citizens/login.html')

@login_required
def citizen_dashboard(request):
    if request.user.userprofile.role != 'Citizen':
        return redirect('staff_dashboard')
    issues = Issue.objects.filter(reported_by=request.user)
    return render(request, 'citizens/dashboard.html', {'issues': issues})

@login_required
def report_issue(request):
    if request.user.userprofile.role != 'Citizen':
        return redirect('staff_dashboard')
    if request.method == 'POST':
        form = IssueReportForm(request.POST, request.FILES)
        if form.is_valid():
            issue = form.save(commit=False)
            issue.reported_by = request.user

            # Handle GPS location
            use_current_location = form.cleaned_data.get('use_current_location')
            manual_address = form.cleaned_data.get('manual_address')

            if use_current_location:
                # Get coordinates from POST data (will be set by JavaScript)
                latitude = request.POST.get('latitude')
                longitude = request.POST.get('longitude')
                if latitude and longitude:
                    issue.latitude = latitude
                    issue.longitude = longitude
                    issue.location = f"GPS: {latitude}, {longitude}"
                else:
                    # Fallback to manual address if GPS fails
                    issue.location = manual_address or "Location not provided"
            else:
                issue.location = manual_address

            # AI categorization
            description = issue.description.lower()
            if 'gutter' in description or 'drain' in description:
                issue.ai_category = 'Gutter'
            elif 'garbage' in description or 'waste' in description:
                issue.ai_category = 'Garbage'
            elif 'streetlight' in description or 'light' in description:
                issue.ai_category = 'Streetlight'
            elif 'water' in description:
                issue.ai_category = 'Water'
            else:
                issue.ai_category = 'Other'

            # Simple prediction based on priority
            priority_days = {
                'Low': 14,
                'Medium': 7,
                'High': 3,
                'Critical': 1
            }
            days = priority_days.get(issue.priority, 7)
            issue.predicted_resolution_time = timezone.now() + timezone.timedelta(days=days)

            issue.save()
            messages.success(request, f'Issue reported successfully! Priority: {issue.priority}')
            return redirect('citizen_dashboard')
    else:
        form = IssueReportForm()
    categories = Category.objects.all()
    return render(request, 'citizens/report_issue.html', {'form': form, 'categories': categories})
