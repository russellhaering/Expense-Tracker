# Create your views here.
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from expenses.app.models import Expense, ExpenseType, MicroBill 
from expenses.app.forms import ExpenseForm

def expenses(request):
    expense_list = Expense.objects.all()
    return render_to_response('tracker/expenses.html', {})
 
def expense_show(request, eid):
    e = get_object_or_404(Expense, pk=eid)
    return render_to_response('tracker/show_expense.html', {'expense': e})

def expense_add(request):
    if request.method == 'POST':
        # If the form was submitted
        form = ExpenseForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('../show/' + e.id )
        else:
            return render_to_response('tracker/new_expense.html', {'form': form})
    else:
        # If this is the first display
        form = ExpenseForm()
        return render_to_response('tracker/new_expense.html', {'form': form})
