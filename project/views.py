from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm, AddCustomerForm
from django.contrib.auth import login,logout, authenticate
from .models import Record, Customer
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_users
from django.contrib.auth.models import Group, User
from django.db import IntegrityError
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm 
from django.conf import settings
import uuid

def login_user(request):
     if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # Authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have been Logged in!")

            if user.groups.filter(name='admin').exists():
                return redirect('admin_dashboard')  
            elif user.groups.filter(name='finance').exists():
                return redirect('finance_dashboard') 
            elif user.groups.filter(name='technician').exists():
                return redirect('technician_dashboard') 
            else:
                return redirect('default_dashboard') 
           
        else:
            messages.error(request, "There was an Error logging in Please try again...")
            return redirect('login')
     else:
        return render(request, 'login.html', )
     
def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # Authenticte and login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user )
            messages.success(request, "You have succesfully registered Welcome")
            return redirect('login')
    else: 
            form = SignUpForm()
            return render(request, 'register.html', {'form':form})
    
    return render(request, 'register.html', {'form':form})
        

def logout_user(request):
    logout(request)
    messages.success(request, "You have been Logged out...")
    return redirect('login')   

def default_dashboard(request):
    return render(request, 'default_dashboard.html')

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin',])
def admin_dashboard(request):
    records = Record.objects.all()

    return render(request, 'admin/admin_dashboard.html', {'records':records})

@login_required(login_url='login')
@allowed_users(allowed_roles=['finance',])
def finance_dashboard(request):
    return render(request, 'finance/finance_dashboard.html')

@login_required(login_url='login')
@allowed_users(allowed_roles=['technician',])
def tech_dashboard(request):
    return render(request, 'technician/technician_dashboard.html')

@login_required(login_url='login')
def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                try:
                    add_record = form.save()   
                    messages.success(request, "Record Added..")
                    return redirect('records')
                except IntegrityError:
                    form.add_error('Id_no', 'A customer with this ID already exists.')
        return render(request, 'add_record.html', {'form':form})
    else:
        messages.success(request, "You must be logged in..")   
        return redirect('login')
    
@login_required(login_url='login')
def booking_record(request, pk):
   

    if request.user.is_authenticated:
        # look up for records
        booking_record = Record.objects.get(id=pk)
        return render(request, 'booking_record.html', {'booking_record':booking_record,})
    else:
        messages.success(request, "You must be logged in to view that page..")
        return redirect('login')
    
def test(request):
     paypal_dict = {
        "business": "larkbusiness@gmail.com",
        "amount": "10.00",
        "item_name": "booking",
        "invoice": "unique-invoice-id",
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        "return": request.build_absolute_uri(reverse('payment_success')),
        "cancel_return": request.build_absolute_uri(reverse('payment_failed')),
        "custom": "premium_plan",  # Custom command to correlate to some function later (optional)
    }

    # Create the instance.
     form = PayPalPaymentsForm(initial=paypal_dict)
     context = {"form": form}
     return render(request, "test.html", context)   
    
@login_required(login_url='login')   
def record(request):
    records = Record.objects.all()
    paginator = Paginator(records, 10)  # Show 10 records per page

    page_number = request.GET.get('page')  # Get the page number from the URL
    records = paginator.get_page(page_number)
    return render(request, 'records.html', {'records':records}) 


@login_required(login_url='login')
def delete_record(request, pk):
    if request.user.is_authenticated:
        delete_it = Record.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, "Record deleted successfully..")
        return redirect('records')
    else:
        messages.success(request, "You must be logged in to do that..")
        return redirect('login')   

@login_required(login_url='login')
def update_record(request, pk):
    if request.user.is_authenticated:
        current_record = Record.objects.get(id=pk)
        form =  AddRecordForm(request.POST or None, instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request, "Record has been updated..")
            return redirect('records')
        return render(request, 'update_record.html', {'form':form})
    else:
         messages.success(request, "You must be logged in..")   
         return redirect('login')    
    
def status(request):
    return render(request, 'admin/status.html')    

def products(request):
    return render(request, 'admin/products.html')  

def customer(request):
    customers = Customer.objects.all()
    paginator = Paginator(customers, 10)  # Show 10 customers per page

    page_number = request.GET.get('page')  # Get the page number from the URL
    customers = paginator.get_page(page_number)
    return render(request, 'admin/customer.html', {'customers':customers})  

@login_required(login_url='login')
def add_customer(request):
    form = AddCustomerForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                try:
                    add_customer = form.save()   
                    messages.success(request, "Record Added..")
                    return redirect('customer')
                except IntegrityError:
                    form.add_error('Id_no', 'A customer with this ID already exists.')
        return render(request, 'admin/add_customer.html', {'form':form})
    else:
        messages.success(request, "You must be logged in..")   
        return redirect('login')
    

@login_required(login_url='login')
def customer_record(request, pk):
    if request.user.is_authenticated:
        # look up for records
        customer_record = Customer.objects.get(id=pk)
        return render(request, 'admin/customer_record.html', {'customer_record':customer_record})
    else:
        messages.success(request, "You must be logged in to view that page..")
        return redirect('login')  

@login_required(login_url='login')
def delete_customer(request, pk):
    if request.user.is_authenticated:
        delete_it = Customer.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, "Record deleted successfully..")
        return redirect('customer')
    else:
        messages.success(request, "You must be logged in to do that..")
        return redirect('login')   

@login_required(login_url='login')
def update_customer(request, pk):
    if request.user.is_authenticated:
        current_customer = Customer.objects.get(id=pk)
        form =  AddCustomerForm(request.POST or None, instance=current_customer)
        if form.is_valid():
            form.save()
            messages.success(request, "Record has been updated..")
            return redirect('customer')
        return render(request, 'admin/update_customer.html', {'form':form})
    else:
         messages.success(request, "You must be logged in..")   
         return redirect('login')
    
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin',])
def manage_users(request):
    users = User.objects.all()
    groups = Group.objects.all()
    paginator = Paginator(users, 10)  # Show 10 users per page

    page_number = request.GET.get('page')  # Get the current page number from the URL
    users = paginator.get_page(page_number)
    return render(request, 'admin/users.html', {'users': users, 'groups': groups})    
@login_required
@allowed_users(allowed_roles=['admin'])
def add_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        group_id = request.POST.get('group')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Check if password and confirm_password match
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('add_user')  # Redirect to the same page to display the error
        
        # Create the user
        try:
            user = User.objects.create_user(username=username, password=password, email=email,
                                             first_name=first_name, last_name=last_name)
            group = Group.objects.get(id=group_id)
            user.groups.add(group)
            messages.success(request, "User added successfully.")
            return redirect('manage_users')  # Redirect to manage users after successful creation
        except Exception as e:
            messages.error(request, f"Error adding user: {e}")
            return redirect('add_user')  # Redirect to the same page to display the error

    return render(request, 'admin/add_user.html', {'groups': Group.objects.all()})

@login_required
@allowed_users(allowed_roles=['admin'])
def user_detail(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return render(request, 'admin/user_detail.html', {'user': user})

@login_required
@allowed_users(allowed_roles=['admin'])
def user_update(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.save()
        messages.success(request, 'User updated successfully!')
        return redirect('user_detail', user_id=user.id)
    return render(request, 'admin/user_update.html', {'user': user})

@login_required
@allowed_users(allowed_roles=['admin'])
def user_delete(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    messages.success(request, 'User deleted successfully!')
    return redirect('manage_users')    
           

def payment_success(request):
    return render(request, "payment/payment_success.html")

def payment_failed(request):
    return render(request, "payment/payment_failed.html")