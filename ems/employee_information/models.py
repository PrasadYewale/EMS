from datetime import datetime
from django.db import models
from django.utils import timezone

# Create your models here.


class Department(models.Model):
    name = models.TextField()
    description = models.TextField()
    status = models.IntegerField()
    date_added = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Position(models.Model):
    name = models.TextField()
    description = models.TextField()
    status = models.IntegerField()
    date_added = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Employees(models.Model):
    code = models.CharField(max_length=100, blank=True)
    firstname = models.TextField()
    middlename = models.TextField(blank=True, null=True)
    lastname = models.TextField()
    gender = models.TextField(blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    contact = models.TextField()
    address = models.TextField()
    email = models.TextField()
    department_id = models.ForeignKey(Department, on_delete=models.CASCADE)
    position_id = models.ForeignKey(Position, on_delete=models.CASCADE)
    date_hired = models.DateField()
    salary = models.FloatField(default=0)
    status = models.IntegerField()
    date_added = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.firstname + ' ' + self.middlename + ' '+self.lastname + ' '


class Activity(models.Model):
    name = models.CharField(max_length=255, db_index=True, default=0)
    description = models.CharField(max_length=255, db_index=True)
    status = models.IntegerField(default=0)
    date_added = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ActivityRule(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    activity_id = models.ForeignKey(
        Activity, default=0, on_delete=models.CASCADE)
    min_score = models.FloatField(db_index=True, default=0)
    max_score = models.FloatField(null=True, db_index=True, default=0)
    operator = models.CharField(max_length=255, db_index=True, default=0)
    status = models.IntegerField(default=0)
    points = models.FloatField(db_index=True, default=0)
    date_added = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Point(models.Model):
    points = models.FloatField(db_index=True)
    user_id = models.BigIntegerField(db_index=True)
    date_added = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user_id)


class Product(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    points = models.FloatField(db_index=True)
    quantity = models.FloatField(db_index=True)
    img = models.TextField(null=True, db_index=True)
    date_added = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Score(models.Model):
    # name = models.CharField(max_length=255, db_index=True,default=0)
    emp_id = models.ForeignKey(Employees, default=0, on_delete=models.CASCADE)
    activity_id = models.ForeignKey(
        Activity, default=0, on_delete=models.CASCADE)
    activity_rule_id = models.ForeignKey(
        ActivityRule, default=0, on_delete=models.CASCADE)
    score = models.FloatField(db_index=True, default=0)
    date_added = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    status = models.IntegerField(default=0)

    def __str__(self):
        return self.name

# ============
# Users
# ============


class EmpUsers(models.Model):
    email = models.EmailField(unique=True)
    emp_id = models.ForeignKey(Employees, on_delete=models.CASCADE)
    password = models.CharField(max_length=255)
