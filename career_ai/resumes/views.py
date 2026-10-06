import pymupdf
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Resume

def extract_text_from_file(file_path):
    text = ""
    try:
        doc = pymupdf.open(file_path)
        for page in doc:
            text += page.get_text()
    except:
        text = ""
    return text

def calculate_score_and_skills(text, filename=""):
    fname = filename.lower()
    if "college" in fname and "id" in fname or "id_card" in fname or "admit" in fname:
        return 15, "Not a Resume - ID Card / College Card hai"
    if not text or len(text.strip()) < 50:
        return 15, "Not a Resume - Invalid File hai"
    low = text.lower()
    if "principal" in low and "student" in low and "dob" in low:
        return 15, "Not a Resume - ID Card hai"
    if "education" not in low and "experience" not in low and "project" not in low and "skill" not in low and "email" not in low:
        return 15, "Not a Resume - ID Card hai"
    skills_list = ["python","django","java","react","sql","html","css","javascript"]
    found = [s for s in skills_list if s in low]
    if not found:
        return 40, "No tech skills found"
    score = 50 + len(found)*7
    if score > 95:
        score = 95
    return score, ", ".join(found)

@login_required
def upload_resume(request):
    if request.method == 'POST' and request.FILES.get('resume'):
        f = request.FILES['resume']
        resume = Resume.objects.create(user=request.user, file=f)
        text = extract_text_from_file(resume.file.path)
        score, skills = calculate_score_and_skills(text, f.name)
        resume.ats_score = score
        resume.skills = skills
        resume.save()
        return redirect('dashboard')
    return render(request, 'resumes/upload.html')

@login_required
def resume_history(request):
    resumes = Resume.objects.filter(user=request.user).order_by('-id')
    return render(request, 'resumes/history.html', {'resumes': resumes})
