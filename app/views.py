from django.shortcuts import render,redirect
from django.contrib.admin.views.decorators import staff_member_required
from .models import Customers
from django.contrib.auth.models import User
from datetime import datetime
from datetime import timedelta
from django.contrib import messages
from django.http import HttpResponse
import csv
from django.core.mail import send_mass_mail
from django.core.exceptions import ObjectDoesNotExist


@staff_member_required
def Index(request):
    if request.user.is_authenticated:
        total_customers = len(Customers.objects.all())
        within_24_hours = len(Customers.objects.filter(created_on__gt=datetime.now() - timedelta(1)))
        within_past_week= len(Customers.objects.filter(created_on__gt=datetime.now() - timedelta(7)))
        total_users = len(User.objects.all())
        super_users=len(User.objects.filter(is_superuser=True))
        staff_users=len(User.objects.filter(is_staff=True))
        context = {
            "total_customers":total_customers,
            "within_24_hours":within_24_hours,
            "within_past_week":within_past_week,
            "total_users":total_users,
            "super_users":super_users,
            "staff_users":staff_users
        }
        return render(request,'app/index.html',context)

@staff_member_required
def Get_Customers(request):
    if request.user.is_authenticated:
        customers = Customers.objects.all()
        context = {
            "customers":customers
        }
        return render(request,'app/customers.html', context)

@staff_member_required
def Add_Customer(request):
    if request.user.is_authenticated:
        if request.method=="POST":
            first_name = request.POST["f_name"]
            last_name = request.POST["l_name"]
            email = request.POST["email"]

            if first_name and last_name and email:
                Customers.objects.create(first_name=first_name, last_name=last_name, email=email)
                messages.success(request,"Customer added successfully")
                return redirect('add_customer')
            else:
                messages.info(request,"All fields are required")
                return redirect('add_customer')
        return render(request,'app/addcustomer.html')

@staff_member_required
def Delete_Customer(request,id):
    if request.user.is_authenticated:
        customer = Customers.objects.get(pk=id)
        customer.delete()
        messages.success(request,"Customer removed succesffully")
        return redirect('customers_list')



@staff_member_required
def Download_Customers(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="customer-list-{}.csv"'.format(int(datetime.now().timestamp()))

    csv_writer= csv.writer(response)
    csv_writer.writerow(['First name','Last name','Email'])
    [csv_writer.writerow([c.first_name,c.last_name,c.email]) for c in Customers.objects.all()]
    return response



@staff_member_required
def Email_Customers(request):
    if request.user.is_authenticated:
        if request.method=="POST":
            try:
                customers = Customers.objects.all()
            except ObjectDoesNotExist:
                message.info(request,"An error occured somewhere please contact admin")
            subject = request.POST["subject"]
            message = request.POST["message"]
            from_email = request.user.email
            message_list =[]
            if subject and message:
                for c in customers:
                    message_list.append((subject,message,from_email,[c.email]))
                try:
                    success=send_mass_mail(
                        tuple(message_list), fail_silently=False
                    )
                    messages.success(request, f"Email sent successfully to {success} customers")
                except:
                    messages.info("Error occured somewhere")
                return redirect('send_email')
            else:
                messages.info(request,"All fields are required")
                return redirect('send_email')
        return render(request,'app/email.html')
