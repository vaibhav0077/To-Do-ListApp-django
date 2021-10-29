from django.db import models
from django.db.models import fields
from django.db.models.enums import Choices
from django.contrib.auth.models import User
from django.forms.widgets import NumberInput
from django.contrib.admin.widgets import AdminDateWidget




class TODO(models.Model):
    status_choice = [
        ('C', 'COMPLETE'),
        ('P', 'PENDING')
    ]
    priority_choices = [
        ('1', '1️⃣'),
        ('2', '2️⃣'),
        ('3', '3️⃣'),
        ('4', '4️⃣'),
        ('5', '5️⃣'),
        ('6', '6️⃣'),
        ('7', '7️⃣'),
        ('8', '8️⃣'),
        ('9', '9️⃣'),



    ]

    
    title = models.CharField(max_length=50, verbose_name="Title")
    status = models.CharField(max_length=10, choices=status_choice , default="P")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(verbose_name="Start Date", auto_now_add=True,  null=True )
    priority = models.CharField(max_length=2, choices=priority_choices)
    end_date = models.DateField(verbose_name="End Date", null=True)

    


 