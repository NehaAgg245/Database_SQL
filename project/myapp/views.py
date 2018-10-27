from django.shortcuts import render, redirect
from django.http import HttpResponse
from dateutil.parser import parse
from django.db.models import Q
from django.db.models import Value
from django.db.models.functions import Concat
from django.contrib import messages
from .forms import *
from .models import *

i = 0
def contact(request):
	if request.method == 'POST':
		form = CForm(request.POST)
		if form.is_valid():
			fname = form.cleaned_data['fname']
			mname = form.cleaned_data['mname']
			lname = form.cleaned_data['lname']
			print(fname, mname, lname)
	form = CForm()
	return render(request, 'form.html', {'form':form})
	
def isdate(string):
	try:
		parse(string)
		return True
	except ValueError:
		return False

#This function is responsible for searching of contacts from the home page. 
# The input is checked whether it is numeric, alphanumeric, text or a string. 
# On input being a string, it is split and then iterated over each word in different categories.

def home_page(request):
	contact = Contact.objects.select_related()
	query = request.GET.get("q")
	if query:
		queryset_list = Contact.objects.select_related()
		if query.isdigit():
			phn = Contact.objects.annotate(phn = Concat('phone__area_code','phone__ph_number')).filter(phn__icontains = word).distinct().values('contact_id')
			or_lookup = (Q(phone__area_code__icontains = query) | Q(phone__ph_number__icontains = query) |
				Q(address__zip_code__icontains = query) | Q(address__address__icontains = query)| Q(contact_id__in= phn))
		elif query.isalpha() or query.isalnum():
			or_lookup = (Q(fname__icontains = query) | Q(mname__icontains = query) | Q(lname__icontains = query) |
				Q(address__address__icontains = query) | Q(address__city__icontains = query) | Q(address__state__icontains = query))
		elif isdate(query):
			dt = parse(query)
			dt = dt.strftime('%Y-%m-%d')
			or_lookup = (Q(dates__dates__icontains = dt))
		else:
			or_lookup = Q()
			for word in query.split():
				if word.isdigit():
					phn = Contact.objects.annotate(phn = Concat('phone__area_code','phone__ph_number')).filter(phn__icontains = word).distinct().values('contact_id')
					temp = (Q(phone__area_code__icontains = word) | Q(phone__ph_number__icontains = word) |
					Q(address__zip_code__icontains = word) | Q(address__address__icontains = word) | Q(contact_id__in= phn))
					or_lookup = or_lookup | temp
				elif word.isalpha()  or query.isalnum():
					temp = (Q(fname__icontains = word) | Q(mname__icontains = word) | Q(lname__icontains = word) |
					Q(address__address__icontains = word) | Q(address__city__icontains = word) | Q(address__state__icontains = word))
					or_lookup = or_lookup | temp
				elif isdate(word):
					dt = parse(word)
					dt = dt.strftime('%Y-%m-%d')
					temp = (Q(dates__dates__icontains = dt))
					or_lookup = or_lookup | temp
		queryset_list = Contact.objects.filter(or_lookup).distinct()
		if queryset_list:
			args = {'data' : queryset_list}
			return render(request, 'search.html', args)
		else:
			return render(request, 'error.html', {})
	return render(request, 'search.html', {'data': contact})

#Flag 0 = Call came from adding contact
#Flag 1 = Call came from updating contact
# This function is responsible for adding the contacts Fname, Mname and Lname. 
# It sends the contact_id to the next function address_details to maintain the foreign key relationship.
def contact_detail(request):
	if request.method == 'POST':
		form = ContactForm(request.POST)
		if form.is_valid():
			if form.has_changed():
				contact_form = form.save()
				return redirect('address_details', contact_form.contact_id, 0)
	form = ContactForm()
	return render(request,'form1.html',{'form':form})

# This function is responsible for adding the contact details of the contact. 
# It sends the contact_id to the next function phone_details to maintain the foreign key relation
def address_details(request, contact_id, flag):
	if request.method == 'POST':
		form = AddressForm(request.POST)
		if form.is_valid():
			if form.has_changed():
				address_form = form.save(False)
				address_form.contact_id = contact_id
				address_form.save()
		if 'add_another' in request.POST:
			return redirect('address_details', contact_id, flag)
		elif 'submit' in request.POST:
			if flag == 0:
				return redirect('phone_details', contact_id, flag)
			elif flag == 1:
				return redirect('update_phone', contact_id,flag)
	form = AddressForm()
	form.contact_id = contact_id
	return render(request, 'details1.html', {'form':form})

# This function is responsible for adding the phone details.
# It sends the contact_id to the next function date_details to maintain the foreign key relation.
def phone_details(request, contact_id, flag):
	if request.method == 'POST':
		form = PhoneForm(request.POST)
		if form.is_valid():
			if form.has_changed():
				phone_form = form.save(False)
				phone_form.contact_id = contact_id
				phone_form.save()
		if 'add_another' in request.POST:
			return redirect('phone_details', contact_id, flag)
		elif 'submit' in request.POST:
			if flag == 0:
				return redirect('date_details', contact_id, flag)
			elif flag == 1:
				return redirect('update_date', contact_id, flag)
	form = PhoneForm()
	form.contact_id = contact_id
	return render(request, 'details1.html', {'form':form})

# This function is responsible for date details. 
# It renders to an acknowledgement page on successful submission.
def date_details(request, contact_id,flag):
	if request.method == 'POST':
		form = DateForm(request.POST)
		if form.is_valid():
			if form.has_changed():
				date_form = form.save(False)
				date_form.contact_id = contact_id
				date_form.save()
		if 'add_another' in request.POST:
			return redirect('date_details', contact_id, flag)
		elif 'submit' in request.POST:
			return render(request, 'done.html', {})
	form = DateForm()
	form.contact_id = contact_id
	return render(request, 'details1.html', {'form':form})

# Responsible for updating the name of the contact. 
# Sends the contact_id to the next function update_address so that addresses for that contact_id can be retrived and then updated.
def update_contact(request,contact_id):
	contact = Contact.objects.filter(contact_id = contact_id)
	if request.method == 'POST':
		form = ContactForm(request.POST)
		if form.is_valid():
			contact.update(fname = form.cleaned_data['fname'], mname = form.cleaned_data['mname'], lname = form.cleaned_data['lname'])
			return redirect('update_address', contact_id, 1)
	form = ContactForm({'fname':contact[0].fname, 'mname' : contact[0].mname, 'lname' : contact[0].lname})
	return render(request,'form1.html',{'form':form})

# Responsible for updating the address of the contact.
# Sends the contact_id to the next function update_phone so that phones for that contact_id can be retrived and then updated.
def update_address(request,contact_id,flag):
	address = Address.objects.filter(contact_id = contact_id)
	global i
	if request.method == 'POST':
		form = AddressForm(request.POST)
		if form.is_valid():
			address_id = address[i].address_id
			if 'submit' in request.POST:
				address.filter(address_id = address_id).update(address_type = form.cleaned_data['address_type'], address = form.cleaned_data['address'], city = form.cleaned_data['city'], state = form.cleaned_data['state'],  zip_code = form.cleaned_data['zip_code'])
				i = i+1
				if i == len(address)-1:
					form = AddressForm({'address_type':address[i].address_type, 'address':address[i].address, 'city' : address[i].city, 'state': address[i].state, 'zip_code':address[i].zip_code})
					return render(request, 'details.html', {'form' : form})
				elif i < len(address)-1:
					form = AddressForm({'address_type':address[i].address_type, 'address':address[i].address, 'city' : address[i].city, 'state': address[i].state, 'zip_code':address[i].zip_code})
					return render(request, 'form.html', {'form' : form})
				elif i >= len(address):
					i = 0
					return redirect('update_phone', contact_id, flag)
			elif 'add_another' in request.POST:
				address.filter(address_id = address_id).update(address_type = form.cleaned_data['address_type'], address = form.cleaned_data['address'], city = form.cleaned_data['city'], state = form.cleaned_data['state'],  zip_code = form.cleaned_data['zip_code'])
				return redirect('address_details', contact_id, flag)
			elif 'delete' in request.POST:
				address.filter(address_id=address_id).delete()
				i = i+1
				if i == len(address)-1 or i >= len(address):
					return redirect('address_details', contact_id, flag)
				elif i < len(address)-1:
					form = AddressForm({'address_type':address[i].address_type, 'address':address[i].address, 'city' : address[i].city, 'state': address[i].state, 'zip_code':address[i].zip_code})
					return render(request, 'details.html', {'form' : form})
	if not address:
		return redirect('address_details', contact_id, flag)
	elif i+1 == len(address):			
		form = AddressForm({'address_type': address[0].address_type, 
			'address':address[0].address, 
			'city' : address[0].city, 
			'state': address[0].state, 
			'zip_code':address[0].zip_code})
		template = 'details.html'
	else:
		form = AddressForm({'address_type': address[0].address_type, 
			'address':address[0].address, 
			'city' : address[0].city, 
			'state': address[0].state, 
			'zip_code':address[0].zip_code})
		template = 'form.html'
	return render(request, template, {'form' : form})

# Responsible for updating the phone of the contact.
# Sends the contact_id to the next function update_dates so that dates for that contact_id can be retrived and then updated.
def update_phone(request,contact_id,flag):
	global i
	phone = Phone.objects.filter(contact_id = contact_id)
	if request.method == 'POST':
		form = PhoneForm(request.POST)
		if form.is_valid():
			phone_id = phone[i].phone_id
			if 'submit' in request.POST:
				phone.filter(phone_id = phone_id).update(phone_type = form.cleaned_data["phone_type"], area_code = form.cleaned_data["area_code"], ph_number = form.cleaned_data["ph_number"])
				i = i+1
				if i == len(phone)-1:
					form = PhoneForm({'phone_type':phone[i].phone_type,
					'area_code':phone[i].area_code,
					'ph_number':phone[i].ph_number})
					return render(request, 'details.html', {'form' : form})
				elif i <len(phone)-1:
					form = PhoneForm({'phone_type':phone[i].phone_type,
					'area_code':phone[i].area_code,
					'ph_number':phone[i].ph_number})
					return render(request, 'form.html', {'form' : form})
				elif i >= len(phone):
					i = 0
					return redirect('update_date', contact_id, flag)
			elif 'add_another' in request.POST:
				phone.filter(phone_id = phone_id).update(phone_type = form.cleaned_data["phone_type"], area_code = form.cleaned_data["area_code"], ph_number = form.cleaned_data["ph_number"])
				return redirect('phone_details',contact_id,flag)
			elif 'delete' in request.POST:
				phone.filter(phone_id=phone_id).delete()
				i = i+1
				if i == len(phone)-1 or i >= len(phone):
					return redirect('phone_details', contact_id, flag)
				elif i < len(phone)-1:
					form = PhoneForm({'phone_type':phone[i].phone_type,
					'area_code':phone[i].area_code,
					'ph_number':phone[i].ph_number})
					return render(request, 'form.html', {'form' : form})
	if not phone:
		return redirect('phone_details',contact_id,flag)
	elif i+1 == len(phone):
		form = PhoneForm({'phone_type':phone[0].phone_type,
			'area_code':phone[0].area_code,
			'ph_number':phone[0].ph_number})
		template = 'details.html'
	else:
		form = PhoneForm({'phone_type':phone[0].phone_type,
			'area_code':phone[0].area_code,
			'ph_number':phone[0].ph_number})
		template = 'form.html'
	return render(request,template, {'form' : form})

# Responsible for updating the dates of a contact. 
# It renders to an acknowledgement page on successful submission.
def update_date(request,contact_id,flag):
	global i 
	dates = Dates.objects.filter(contact_id = contact_id)
	if request.method == 'POST':
		form = DateForm(request.POST)
		if form.is_valid():
			date_id = dates[i].date_id
			if 'submit' in request.POST:
				dates.filter(date_id = date_id).update(date_type = form.cleaned_data["date_type"], dates = form.cleaned_data["dates"])
				i = i+1
				if i == len(dates)-1:
					form = DateForm({'date_type': dates[i].date_type, 'dates' : dates[i].dates})
					return render(request, 'details.html', {'form' : form})
				elif i < len(dates)-1:
					form = DateForm({'date_type': dates[i].date_type, 'dates' : dates[i].dates})
					return render(request, 'form.html', {'form' : form})
				elif i >= len(dates):
					i = 0
					return render(request, 'done.html')
			elif 'add_another' in request.POST:
				dates.filter(date_id = date_id).update(date_type = form.cleaned_data["date_type"], dates = form.cleaned_data["dates"])
				return redirect('date_details', contact_id, flag)
			elif 'delete' in request.POST:
				dates.filter(date_id=date_id).delete()
				i = i+1
				if i == len(dates)-1 or i >= len(dates):
					return redirect('date_details', contact_id, flag)
				elif i < len(dates)-1:
					form = DateForm({'date_type': dates[i].date_type, 'dates' : dates[i].dates})
					return render(request, 'form.html', {'form' : form})
	if not dates:
		return redirect('date_details', contact_id, flag)
	elif i+1 == len(dates):
		form = DateForm({'date_type': dates[0].date_type, 'dates' : dates[0].dates})
		template = 'details.html'
	else:
		form = DateForm({'date_type': dates[0].date_type, 'dates' : dates[0].dates})
		template = 'form.html'
	return render(request,template, {'form' : form})
#This function is responsible for the deletion of complete contact.
def delete_contact(request,contact_id):
	contact = Contact.objects.filter(contact_id = contact_id).select_related()
	contact.delete()
	return render(request, 'done.html')
