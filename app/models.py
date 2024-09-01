from django.db import models

class Resume(models.Model):
    name = models.CharField(max_length=255)
    gdrive_link = models.URLField(max_length=1024)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
