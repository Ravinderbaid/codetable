from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Files_saveds(models.Model):
	title = models.CharField(max_length = 100)
	author = models.ForeignKey(User, verbose_name="by")
	created_date = models.DateTimeField(auto_now_add=True, editable=False)
	modified_date = models.DateTimeField(auto_now_add=True)   