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

    def __repr__(self):
        return str((self.name, self.value))

    def __unicode__(self):
        return self.value

# Widgets
class BillerWidget(forms.MultiWidget):
    def __init__(self, victims, attrs=None):
        self.victims = victims
        widgets = ((forms.TextInput()) for victim in victims)
        super(BillerWidget, self).__init__(widgets, attrs)

    def value_from_datadict(self, data, files, name):
        return [(BillValue(
            (name + '_%s' % victim.id),
            (data.get(name + '_%s' % victim.id))
        )) for victim in self.victims]

    def decompress(self, values):
        if values:
            return values
        else:
            return list((None) for widget in self.widgets)

    def render(self, name, value, attrs=None):
        # value is a list of values, each corresponding to a widget
        # in self.widgets.
        if not isinstance(value, list):
            value = self.decompress(value)
        output = []
        final_attrs = self.build_attrs(attrs)
        id_ = final_attrs.get('id', None)
        for i, widget in enumerate(self.widgets):
            try:
                widget_value = value[i].value
            except (IndexError, AttributeError):
                widget_value = None
            if id_:
                final_attrs = dict(final_attrs, id='%s_%s' % (id_, i))
            output.append(widget.render(name + "_%s" % self.victims[i].id, widget_value, final_attrs))
        return self.format_output(output)

    def format_output(self, rendered_widgets):
        output = u'\n<table>\n'
        for i, widget in enumerate(rendered_widgets):
            output = output + "<tr><th>%s</th><td>%s</td></tr>\n" % (self.victims[i], widget)
        return output + "</table>"


# Fields
class BillerField(forms.RegexField):
    currencyRe = re.compile(r'^[0-9]{1,5}(.[0-9][0-9])?$')
    def __init__(self, victims):
        self.widget = BillerWidget(victims)
        super(BillerField, self).__init__(self.currencyRe)

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
