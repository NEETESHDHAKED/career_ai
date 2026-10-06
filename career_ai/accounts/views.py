from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from resumes.models import Resume

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            return render(request, 'accounts/register.html', {'error': 'Username already exists'})
        User.objects.create_user(username=username, password=password)
        return redirect('login')
    return render(request, 'accounts/register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        return render(request, 'accounts/login.html', {'error': 'Invalid credentials'})
    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    last_resume = Resume.objects.filter(user=request.user).order_by('-id').first()
    feedback = ""
    jobs = []
    if last_resume:
        skills = (last_resume.skills or "").lower()
        score = last_resume.ats_score
        if "not a resume" in skills or "id card" in skills:
            feedback = "Ye file resume nahi hai! ID Card upload mat karo. Sahi resume PDF dalo."
            jobs = []
        elif score < 70:
            feedback = "Add more projects, numbers, and quantifiable achievements."
        elif "python" in skills and "django" in skills:
            feedback = "Great! You have Backend skills. Add AWS/Docker to get 90%+."
        else:
            feedback = f"Good score {score}%! Add 2 more skills."

        if "python" in skills:
            jobs.append(f"Python Developer - {min(95, score+5)}% Match")
        if "django" in skills or "sql" in skills:
            jobs.append(f"Backend Developer - {min(92, score+3)}% Match")
        if "react" in skills or "javascript" in skills:
            jobs.append(f"Frontend Developer - {min(90, score+2)}% Match")
        if not jobs and "not a resume" not in skills:
            jobs = [f"Software Intern - {score}% Match"]
    return render(request, 'accounts/dashboard.html', {'last_resume': last_resume, 'feedback': feedback, 'jobs': jobs})
