from django.db import models

# Create your models here.
from django.db.models import CASCADE


class ClientRegister_Model(models.Model):
    username = models.CharField(max_length=30)
    email = models.EmailField(max_length=30)
    password = models.CharField(max_length=10)
    phoneno = models.CharField(max_length=10)
    country = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    address = models.CharField(max_length=300)
    gender = models.CharField(max_length=30)


class predict_stress_detection(models.Model):

    FID= models.CharField(max_length=300)
    MEAN_RR= models.CharField(max_length=300)
    MEDIAN_RR= models.CharField(max_length=300)
    SDRR= models.CharField(max_length=300)
    RMSSD= models.CharField(max_length=300)
    SDSD= models.CharField(max_length=300)
    SDRR_RMSSD= models.CharField(max_length=300)
    HR= models.CharField(max_length=300)
    VLF= models.CharField(max_length=300)
    VLF_PCT= models.CharField(max_length=300)
    LF= models.CharField(max_length=300)
    LF_PCT= models.CharField(max_length=300)
    LF_NU= models.CharField(max_length=300)
    HF= models.CharField(max_length=300)
    HF_PCT= models.CharField(max_length=300)
    HF_NU= models.CharField(max_length=300)
    TP= models.CharField(max_length=300)
    LF_HF= models.CharField(max_length=300)
    HF_LF= models.CharField(max_length=300)
    sampen= models.CharField(max_length=300)
    higuci= models.CharField(max_length=300)
    Prediction= models.CharField(max_length=300)

class detection_accuracy(models.Model):

    names = models.CharField(max_length=300)
    ratio = models.CharField(max_length=300)

class detection_ratio(models.Model):

    names = models.CharField(max_length=300)
    ratio = models.CharField(max_length=300)



