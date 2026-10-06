from django.db import models
from django.contrib.auth.models import User

class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    skills = models.TextField(blank=True)
    file = models.FileField(upload_to='resumes/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    extracted_text = models.TextField(blank=True)
    ats_score = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.file.name}"


    @property
    def skills_list(self):
        if self.skills:
            return [s.strip() for s in self.skills.split(',')]
            return []
