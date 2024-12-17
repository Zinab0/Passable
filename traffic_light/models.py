from django.db import models

class Incident(models.Model):
    # IncidentID = models.AutoField(primary_key=True)
    IntersectionID = models.IntegerField(default=2)
   # Image = models.TextField(max_length=1000, null=True, blank=True)
    Date = models.DateField()  
    Time = models.TimeField()  
    IsAccident = models.BooleanField(null=True)
    IsCongestion = models.BooleanField(null=True)
    class Meta:
        managed = False  # Tell Django not to manage this model's table
        db_table = 'Incident'
        

class UploadImg(models.Model):
    OPTION_ONE = 'Accident'
    OPTION_TWO = 'Congestion'
    CHOICES = [
        (OPTION_ONE, 'Accident'),
        (OPTION_TWO, 'Congestion'),
    ]
    # Example field with choices
    choice_field = models.CharField(max_length=20, choices=CHOICES, default=OPTION_ONE)
    image = models.ImageField(blank=False, null=False, upload_to='images/')
    date = models.DateTimeField(auto_now_add=True)
    time = models.DateTimeField(auto_now=True)


class tst(models.Model):
    img = models.ImageField()