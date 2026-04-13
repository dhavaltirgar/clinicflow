from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Bill
from .forms import BillForm


@login_required
def bill_list(request):
    bills = Bill.objects.select_related(
        'patient', 'appointment'
    ).all().order_by('-created_at')
    return render(request, 'billing/list.html', {'bills': bills})


@login_required
def bill_add(request):
    if request.method == 'POST':
        form = BillForm(request.POST)
        try:
            if form.is_valid():
                bill = form.save()
                messages.success(
                    request,
                    f'Bill #{bill.invoice_number} created successfully!'
                )
                return redirect('bill_list')
            else:
                messages.error(request, 'Please fix the errors below.')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
    else:
        form = BillForm()

    return render(request, 'billing/form.html', {
        'form'  : form,
        'action': 'Create Bill'
    })