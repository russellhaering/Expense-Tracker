from django import forms
from django.forms.util import ErrorList, ValidationError
import re
from expenses.app.models import ExpenseType
from django.contrib.auth.models import User

# Random Utilities
class BillValue(object):
    def __init__(self, name, value):
        self.value = value
        self.name = name

    def __unicode__(self):
        return self.value

# Widgets
class BillerWidget(forms.MultiWidget):
    def __init__(self, victims, attrs=None):
        self.victims = victims
        widgets = ((forms.TextInput()) for victim in victims)
        super(BillerWidget, self).__init__(widgets, attrs)

    def value_from_datadict(self, data, files, name):
        return [BillValue(name + '_%s' % i, widget.value_from_datadict(data, files, name + '_%s' % i)) for i, widget in enumerate(self.widgets)]

    def decompress(self, values):
        if values:
            return values
        else:
            return list((None) for widget in self.widgets)

    def format_output(self, rendered_widgets):
        output = u'\n<table>\n'
        for i, widget in enumerate(rendered_widgets):
            output = output + "<tr><th>%s</th><td>%s</td></tr>\n" % (self.victims[i], widget)
        return output + "</table>"


# Fields
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
        value.value = float(super(BillerField, self).clean(value.value))
        return value

    def clean(self, values):
        errors = ErrorList()
        cleaned_values = []
        for value in values:
            try:
                cleaned_values.append(self._clean_value(value))
            except ValidationError:
                raise ValidationError(u'Every field must contain a valid US Dollar amount')
        return cleaned_values

# Forms
class ExpenseForm(forms.Form):
    type = forms.ModelChoiceField(queryset=ExpenseType.objects.all())
    desc = forms.CharField(max_length=128)
    amount = forms.FloatField()
    issue_date = forms.DateField()
    bills = BillerField(User.objects.all())

    def clean(self):
        print self.cleaned_data
        return self.cleaned_data
