from django.db import models

# Create your models here.
class fileDetails(models.Model):
    csv_file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)