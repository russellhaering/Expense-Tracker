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
    amount = models.IntegerField()

class Expense(models.Model):
    desc = models.CharField(max_length=128)
    def __unicode__(self):
        return self.desc
    type = models.ForeignKey(ExpenseType)
    issue_date = models.DateField()
    amount = models.IntegerField()
    bills = models.ManyToManyField(MicroBill)
    added_by = models.ForeignKey(User)

# Forms
class BillerWidget(forms.MultiWidget):
    def __init__(self, victims):
        self.victims = victims
        widgets = ((forms.TextInput()) for victim in victims)
        super(BillerWidget, self).__init__(widgets)

    def decompress(self, values):
        if values:
            return values
        else:
            return list((None) for widget in self.widgets)

    def format_output(self, rendered_widgets):
        output = u'<table>'
        for i, widget in enumerate(rendered_widgets):
            output = output + "<tr><th>%s</th><td>%s</td></tr>\n" % (self.victims[i], widget)
        return output + "</table>" 

class BillerField(forms.RegexField):
    currencyRe = re.compile(r'^[0-9]{1,5}(.[0-9][0-9])?$')
    error_messages = {
        'invalid': u'Enter a valid USD amount',
    }
    def __init__(self, victims):
        self.victims = victims
        self.widget = BillerWidget(victims)
        super(BillerField, self).__init__(self.currencyRe, error_messages=self.error_messages)

    def _clean_value(self, value):
        value = super(BillerField, self).clean(value)
        return float(value)

    def clean(self, values):
        errors = ErrorList()
        cleaned_values = []
        for value in values:
            try:
                cleaned_values.append(self._clean_value(value))
            except ValidationError, e:
                errors.extend(e.messages) 
        if errors:
            raise ValidationError(errors)
        return cleaned_values

class ExpenseForm(forms.Form):
    type = forms.ModelChoiceField(queryset=ExpenseType.objects.all())
    desc = forms.CharField(max_length=128)
    amount = forms.FloatField()
    issue_date = forms.DateField()
    bills = BillerField(User.objects.all())
