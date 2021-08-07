from django.db import models
import datetime

# Create your models here.

class users(models.Model):

    id = models.AutoField(primary_key=True)
    fname = models.CharField(max_length=255, default=None)
    lname = models.CharField(max_length=255, default=None)
    email = models.CharField(max_length=255, default=None, unique= True)
    password = models.CharField(max_length=255, default=None)
    position_id = models.IntegerField(default=0)
    status = models.IntegerField(default=0)
    role = models.CharField(max_length=255, default='VOTER')
    msisdn = models.CharField(max_length=255, default=None)
    device_uid = models.CharField(max_length=255, default='JESUS')
    created_at = models.DateTimeField(default=None)
    updated_at = models.DateTimeField(default=None)


class election(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, default=None)
    description = models.CharField(max_length=500, default=None)
    status = models.IntegerField(default=0)
    startdate = models.DateTimeField(default=None)
    tokentime = models.IntegerField(default=0)
    enddate = models.DateTimeField(default=None)
    created_at = models.DateTimeField(default=None)
    updated_at = models.DateTimeField(default=None)

class position(models.Model):
    
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, default=None)
    description = models.CharField(max_length=500, default=None)
    election_id = models.IntegerField(default=0)
    status = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=None)
    updated_at = models.DateTimeField(default=None)

class vote_token(models.Model):
    
    id = models.AutoField(primary_key=True)
    token = models.CharField(max_length=1000, default=None)
    user_id = models.IntegerField(default=None)
    election_id = models.IntegerField(default=0)
    status = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=None)
    updated_at = models.DateTimeField(default=None)

class votes(models.Model):
    
    id = models.AutoField(primary_key=True)
    voter_id = models.IntegerField(default=None)
    position_id = models.IntegerField(default=None)
    candidate_id = models.IntegerField(default=None)
    status = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=None)
    updated_at = models.DateTimeField(default=None)

class winner(models.Model):
    id = models.AutoField(primary_key=True)
    position_id=models.IntegerField(default=None)
    candidate_id = models.IntegerField(default=None)
    candidate_fname = models.CharField(max_length=255, default=None)
    candidate_lname = models.CharField(max_length=255, default=None)
    total = models.IntegerField(default=None)
    created_at = models.DateTimeField(default=None)
    updated_at = models.DateTimeField(default=None)