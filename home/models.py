from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Base_model(models.Model):
    created_At = models.DateTimeField(auto_now_add=True)
    updated_At = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Main_Model(Base_model):
    user = models.ForeignKey(User , on_delete=models.CASCADE )
    link = models.URLField(default=None)
    query = models.TextField(max_length=300)
    response = models.TextField(max_length=1000 , null=True , blank=True)

    def __str__(self) -> str:
        return f"{self.user.username}-{self.query}"
