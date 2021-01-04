from django.db import models

class h1b_1(models.Model):
    appl_no = models.IntegerField
    ben_name = models.CharField(max_length=30)
    ben_dob = models.CharField(max_length=30)
    ben_gender = models.CharField(max_length=6)
    ben_addr = models.CharField(max_length=50)
    nationality = models.CharField(max_length=20)
    job_title = models.CharField(max_length=20)
    hours_per_week = models.CharField(max_length=5)
    salary = models.CharField(max_length=5)
    employer_name = models.CharField(max_length=30)
    occupation = models.CharField(max_length=20)
    full_time_position = models.CharField(max_length=3)
    location = models.CharField(max_length=20)
    status = models.CharField(max_length=15)
    is_uni = models.CharField(max_length=3)
    def __str__(self):
        return self.ben_name
