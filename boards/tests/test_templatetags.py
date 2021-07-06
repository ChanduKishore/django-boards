from django import forms
from django.test import TestCase
from boards.templatetags.form_tags import input_class, field_type

class ExampleForm(forms.Form):

	name=forms.CharField()
	password=forms.CharField(widget=forms.PasswordInput())

	class Meta:
		fields=['name','password']


class FieldTypeTest(TestCase):
	def Test_field_widget_type(self):
		form=ExampleForm()
		self.assertEquals('text',field_type(form['name']))
		self.assertEquals('password',field_type(form['password']))

class InputClassTest(TestCase):

	def test_unbound_intial_state(self):
		form=ExampleForm()

		self.assertEquals('form-control ',input_class(form['name']))

	def test_bound_valid(self):
		form=ExampleForm({'name':'ram','password':'karma'})
		self.assertEquals('form-control is-valid',input_class(form['name']))
		self.assertEquals('form-control ',input_class(form['password']))
		
	def test_bound_invalid(self):

		form=ExampleForm({'name':'','password':'karma'})
		self.assertEquals('form-control is-invalid',input_class(form['name']))
		


		
