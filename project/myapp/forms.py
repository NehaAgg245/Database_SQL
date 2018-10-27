from django import forms
from .models import Contact, Dates, Address, Phone 

class CForm(forms.Form):
	fname = forms.CharField()
	mname = forms.CharField(required = False)
	lname = forms.CharField()

class ContactForm(forms.ModelForm):

	class Meta:
		model = Contact
		labels = {"fname" : "First Name", "mname" :"Middle Name", "lname" : "Last Name"}
		fields = ('fname', 'mname', 'lname')

class DateForm(forms.ModelForm):

	class Meta:
		model = Dates
		label = {"date_type" : "Date Type", "dates" : "Date"}
		fields = ('date_type', 'dates')
		# widgets = {'contact' : forms.HiddenInput()}

class PhoneForm(forms.ModelForm):

	class Meta:
		model = Phone
		label = {"phone_type": "Phone Type", "area_code" :"Area Code" , "ph_number" : "Number"}
		fields = ('phone_type','area_code','ph_number')

class AddressForm(forms.ModelForm):

	class Meta:
		model = Address
		label = {"address_type" :"Address Type", "zip_code" : "Zip Code"}
		fields = ('address_type','address','city','state','zip_code')