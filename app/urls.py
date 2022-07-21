from . import views
from django.urls import path
from django.views.generic import RedirectView

urlpatterns = [
    path('',views.Index, name="index"),
    path('customers',views.Get_Customers, name="customers_list"),
    path('add-customer',views.Add_Customer, name="add_customer"),
    path('delete-customer/<int:id>', views.Delete_Customer, name="delete_customer"),
    path('downlod-user',views.Download_Customers, name="download_users"),
    path('send-email',views.Email_Customers, name="send_email"),
    path('logout', RedirectView.as_view(url='../../admin/logout/'), name="logout")
]
