from . import views
from django.urls import path

urlpatterns = [
	path('', views.contact),
	path('home', views.home_page, name = "home"),
	path('contact', views.contact_detail, name = "contact"),
	path('contact/<int:contact_id>/<int:flag>/date_details', views.date_details, name = "date_details"),
	path('contact/<int:contact_id>/<int:flag>/address_details', views.address_details, name = "address_details"),
	path('contact/<int:contact_id>/<int:flag>/phone_details', views.phone_details, name = "phone_details"),
	path('delete_contact/<int:contact_id>', views.delete_contact, name = "delete_contact"),
	path('update_contact/<int:contact_id>', views.update_contact, name = "update_contact"),
	path('update_contact/<int:contact_id>/<int:flag>/update_address', views.update_address, name = "update_address"),
	path('update_contact/<int:contact_id>/<int:flag>/update_phone', views.update_phone, name = "update_phone"),
	path('update_contact/<int:contact_id>/<int:flag>/update_date', views.update_date, name = "update_date"),
]
 