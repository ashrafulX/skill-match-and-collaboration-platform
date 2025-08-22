from django.db import models
from django.contrib.auth.models import User
from Categories.models import Categories
from multiselectfield import MultiSelectField


class JobPost(models.Model):
    JOB_TYPES = [
        ('Full Time', 'Full Time'),
        ('Part Time', 'Part Time'),
        ('Contract', 'Contract'),
        ('Internship', 'Internship'),
        ('On-Site', 'On-Site'),
        ('Remote', 'Remote'),
    ]
    STATUS_CHOICES = [
        ('Find', 'Find'),
        ('Not-Find', 'Not-Find'),
    ]

    title = models.CharField(max_length=200)
    job_type = MultiSelectField(choices=JOB_TYPES)
    
    Required_Technical_Skills = models.ManyToManyField(Categories)
    description = models.TextField() 
    posted_on = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Not-Find')

    def __str__(self):
        return f"{self.title}"

class Application(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    ]
    
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    JobPost = models.ForeignKey(JobPost, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    LinkedIn_URL = models.CharField(max_length=200)
    Additional_information = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"{self.full_name} - {self.status} for {self.JobPost.title}"

class Notification(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.recipient.username} - {'Read' if self.is_read else 'Unread'}"