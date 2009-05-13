from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.forms.util import ErrorList, ValidationError
import re

# Models
class ExpenseType(models.Model):
    name = models.CharField(max_length=128)
    def __unicode__(self):
        return self.name

class MicroBill(models.Model):
    applies_to = models.ForeignKey(User)
    amount = models.DecimalField(max_digits=7, decimal_places=2)

class Expense(models.Model):
    desc = models.CharField(max_length=128)
    def __unicode__(self):
        return self.desc
    type = models.ForeignKey(ExpenseType)
    issue_date = models.DateField()
    amount = models.DecimalField(max_digits=7, decimal_places=2)
    bills = models.ManyToManyField(MicroBill)
    added_by = models.ForeignKey(User)
