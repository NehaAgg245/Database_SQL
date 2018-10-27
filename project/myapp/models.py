# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Address(models.Model):
    address_id = models.AutoField(db_column='Address_id', primary_key=True)  # Field name made lowercase.
    contact = models.ForeignKey('Contact', models.DO_NOTHING, db_column='Contact_id')  # Field name made lowercase.
    address_type = models.CharField(db_column='Address_type', max_length=15, blank=True, null=True)  # Field name made lowercase.
    address = models.CharField(db_column='Address', max_length=60, blank=True, null = True)  # Field name made lowercase.
    city = models.CharField(db_column='City', max_length=25, blank=True, null = True)  # Field name made lowercase.
    state = models.CharField(db_column='State', max_length=25, blank=True, null = True)  # Field name made lowercase.
    zip_code = models.CharField(db_column='Zip_code', max_length=15, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'ADDRESS'


class Contact(models.Model):
    contact_id = models.AutoField(db_column='Contact_id', primary_key=True)  # Field name made lowercase.
    fname = models.CharField(db_column='Fname', max_length=15)  # Field name made lowercase.
    mname = models.CharField(db_column='Mname', max_length=15, blank=True, null=True)  # Field name made lowercase.
    lname = models.CharField(db_column='Lname', max_length=15, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'CONTACT'


class Dates(models.Model):
    date_id = models.AutoField(db_column='Date_id', primary_key=True)  # Field name made lowercase.
    contact = models.ForeignKey(Contact, models.DO_NOTHING, db_column='Contact_id')  # Field name made lowercase.
    date_type = models.CharField(db_column='Date_type', max_length=15, blank=True, null=True)  # Field name made lowercase.
    dates = models.DateField(db_column='Dates',blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'DATES'


class Phone(models.Model):
    phone_id = models.AutoField(db_column='Phone_id', primary_key=True)  # Field name made lowercase.
    contact = models.ForeignKey(Contact, models.DO_NOTHING, db_column='Contact_id')  # Field name made lowercase.
    phone_type = models.CharField(db_column='Phone_type', max_length=15, blank=True, null=True)  # Field name made lowercase.
    area_code = models.IntegerField(db_column='Area_code',blank=True, null=True)  # Field name made lowercase.
    ph_number = models.IntegerField(db_column='Ph_number',blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'PHONE'
