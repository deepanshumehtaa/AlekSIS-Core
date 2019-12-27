from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Sum
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Booking, Costcenter, Account
from .filters import BookingFilter
from .forms import BookingForm, CheckBookingForm, BookBookingForm, EditCostcenterForm, EditAccountForm


@login_required
@permission_required('fibu.request_booking')
def index(request):
    if request.method == 'POST':
        if 'booking-id' in request.POST:
            booking_id = request.POST['booking-id']
            booking = get_object_or_404(Booking, pk=booking_id)

            if 'cancel' in request.POST:
                booking.delete()
                print('Eintrag gelöscht')
                return redirect('fibu_index')

            elif 'ordered' in request.POST:
                Booking.objects.filter(id=booking_id).update(status=3)
                return redirect('fibu_index')

            elif 'submit-invoice' in request.POST:
                Booking.objects.filter(id=booking_id).update(status=4)
                return redirect('fibu_index')

            form = BookingForm(instance=booking)
        else:
            form = BookingForm(request.POST)
    else:
        form = BookingForm()

    if form.is_valid():
        description = form.cleaned_data['description']
        planned_amount = form.cleaned_data['planned_amount']
        justification = form.cleaned_data['justification']
        booking = Booking(description=description, planned_amount=planned_amount, contact=request.user,
                          justification=justification)
        booking.save()

        messages.success(request, "Der Antrag wurde erfolgreich übermittelt.")

        return redirect('fibu_index')

    bookings = Booking.objects.filter(contact=request.user).order_by('status')

    context = {'bookings': bookings, 'form': form}
    return render(request, 'fibu/index.html', context)


@login_required
@permission_required('fibu.request_booking')
def edit(request, id):
    booking = get_object_or_404(Booking, id=id)
    form = BookingForm(instance=booking)

    if request.method == 'POST':
        form = BookingForm(request.POST, instance=booking)

        if form.is_valid():
            form.save()

            messages.success(request, "Die Änderungen am Antrag wurden erfolgreich übernommen.")
            return redirect(reverse('fibu_index'))

    context = {'form': form}
    return render(request, 'fibu/booking/edit.html', context)


@login_required
@permission_required('fibu.manage_booking')
def check(request):
    if request.method == 'POST':
        if 'booking-id' in request.POST:
            booking_id = request.POST['booking-id']

            if 'allow' in request.POST:
                if "account" in request.POST:
                    account = request.POST['account']
                    print('account:', account)
                    Booking.objects.filter(id=booking_id).update(status=1, account=account)
                    messages.success(request, "Der Antrag wurde erfolgreich angenommen.")
                else:
                    messages.error(request, "Bitte wähle eine Kostenstelle aus, um den Antrag anzunehmen.")
            elif 'deny' in request.POST:
                Booking.objects.filter(id=booking_id).update(status=2)
                messages.success(request, "Der Antrag wurde erfolgreich abgelehnt.")

    booking_list = Booking.objects.filter(status=0).order_by('submission_date')
    bookings = BookingFilter(request.GET, queryset=booking_list)

    form = CheckBookingForm()
    return render(request, 'fibu/booking/check.html', {'filter': bookings, 'form': form})


@login_required
@permission_required('fibu.manage_booking')
def booking(request, is_archive=""):
    is_archive = is_archive == "archive"
    if is_archive:
        bookings = Booking.objects.filter(status=5).order_by('-status')
    else:
        bookings = Booking.objects.filter(status__lt=5).order_by('-status')
    context = {'bookings': bookings, 'is_archive': is_archive}
    return render(request, 'fibu/booking/index.html', context)


@login_required
@permission_required('fibu.manage_booking')
def book(request, id):
    booking = get_object_or_404(Booking, id=id)
    form = BookBookingForm(instance=booking)
    template = 'fibu/booking/book.html'
    if request.method == 'POST':
        form = BookBookingForm(request.POST, request.FILES, instance=booking)
        if form.is_valid():
            form.save()

            return redirect(reverse('booking'))
    context = {'form': form}
    return render(request, template, context)


@login_required
@permission_required('fibu.manage_booking')
def new_booking(request):
    form = BookBookingForm()
    template = 'fibu/booking/new.html'
    if request.method == 'POST':
        form = BookBookingForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

            return redirect(reverse('booking'))
    context = {'form': form}
    return render(request, template, context)


@login_required
@permission_required('fibu.manage_costcenter')
def costcenter(request):
    if request.method == 'POST':
        if 'costcenter-id' in request.POST:
            costcenter_id = request.POST['costcenter-id']
            costcenter = Costcenter.objects.get(id=costcenter_id)
            if 'cancel' in request.POST:
                costcenter.delete()

                print('Eintrag gelöscht')
                return redirect('costcenter')
            print('Edit-Form erstellt ############# form.is_valid:', form.is_valid())
            form = EditCostcenterForm(instance=costcenter)
        else:
            form = EditCostcenterForm(request.POST or None)
    else:
        form = EditCostcenterForm()
    if form.is_valid():
        name = form.cleaned_data['name']
        year = form.cleaned_data['year']
        costcenter = Costcenter(name=name, year=year)
        costcenter.save()

        return redirect('costcenter')
    costcenterlist = Costcenter.objects.filter()
    context = {'costcenterlist': costcenterlist, 'form': form}
    return render(request, 'fibu/costcenter/index.html', context)


@login_required
@permission_required('fibu.manage_costcenter')
def costcenter_edit(request, id):
    costcenter = get_object_or_404(Costcenter, id=id)
    form = EditCostcenterForm(instance=costcenter)
    template = 'fibu/costcenter/edit.html'
    if request.method == 'POST':
        form = EditCostcenterForm(request.POST, instance=costcenter)
        print('\n\n\nBLUBB', form)
        if form.is_valid():
            form.save()

            return redirect(reverse('costcenter'))
    context = {'form': form}
    return render(request, template, context)


@login_required
@permission_required('fibu.manage_account')
def account(request):
    if request.method == 'POST':
        if 'account-id' in request.POST:
            account_id = request.POST['account-id']
            account = Account.objects.get(id=account_id)
            if 'cancel' in request.POST:
                account.delete()

                print('Eintrag gelöscht')
                return redirect('account')
            print('Edit-Form erstellt ############# form.is_valid:', form.is_valid())
            form = EditAccountForm(instance=account)
        else:
            form = EditAccountForm(request.POST or None)
    else:
        form = EditAccountForm()
    if form.is_valid():
        name = form.cleaned_data['name']
        costcenter = form.cleaned_data['costcenter']
        income = form.cleaned_data['income']
        budget = form.cleaned_data['budget']
        account = Account(name=name, costcenter=costcenter, income=income, budget=budget)
        account.save()

        return redirect('account')
    accounts = Account.objects.filter()
    context = {'accounts': accounts, 'form': form}
    return render(request, 'fibu/account/index.html', context)


@login_required
@permission_required('fibu.manage_account')
def account_edit(request, id):
    account = get_object_or_404(Account, id=id)
    form = EditAccountForm(instance=account)
    template = 'fibu/account/edit.html'
    if request.method == 'POST':
        form = EditAccountForm(request.POST, instance=account)
        print('\n\n\nBLUBB', form)
        if form.is_valid():
            form.save()

            return redirect(reverse('account'))
    context = {'form': form}
    return render(request, template, context)


@login_required
@permission_required('fibu.manage_booking')
def reports(request):
    return render(request, 'fibu/reports/index.html')


@login_required
@permission_required('fibu.manage_booking')
def expenses(request):
    costcenterlist = Costcenter.objects.filter()
    costcenter_accounts = {}
    account_rests = {}
    for costcenter in costcenterlist:
        accounts = Account.objects.filter(costcenter=costcenter)
        # update saldo
        for account in accounts:
            saldo = Booking.objects.filter(account=account).aggregate(Sum('amount'))
            saldo = saldo['amount__sum']
            try:
                rest = account.budget - saldo
            except:
                rest = 0
            try:
                Account.objects.filter(id=account.id).update(saldo=saldo, rest=rest)
            except:
                Account.objects.filter(id=account.id).update(saldo=0, rest=0)

        costcenter_accounts[costcenter.name] = list(Account.objects.filter(costcenter=costcenter).order_by('-income'))
    context = {'costcenter_accounts': costcenter_accounts, 'account_rests': account_rests}
    return render(request, 'fibu/reports/expenses.html', context)
