from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import User
class RegisterForm(forms.ModelForm):
	password = forms.CharField(label='Password', widget=forms.PasswordInput)
	password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)
	class Meta:
		model = User
		fields = ('email',)
	def clean_email(self):
		"controlla se l'email esiste già"
		email = self.cleaned_data.get('email')
		qs = User.objects.filter(email=email)
		if qs.exists():
			raise forms.ValidationError('email already exists')
		return email
	def clean_password2(self):
		"controlla se le due password corrispondono"
		password1 = self.cleaned_data.get('password')
		password2 = self.cleaned_data.get('password2')
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError('passwords don\'t match')
		return password2
class AdminUserCreationForm(forms.ModelForm):
	"modulo per la creazione di nuovi utenti amministratori con tutti i campi e il campo password ripetuta"
	password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
	password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)
	class Meta:
		model = User
		fields = ('email',)
	def clean_email(self):
		"controlla se l'email esiste già"
		email = self.cleaned_data.get('email')
		qs = User.objects.filter(email=email)
		if qs.exists():
			raise forms.ValidationError('email already exists')
		return email
	def clean_password2(self):
		"controlla se le due password corrispondono"
		password1 = self.cleaned_data.get('password')
		password2 = self.cleaned_data.get('password2')
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError('passwords don\'t match')
		return password2
	def save(self, commit=False):
		"salva la password in formato hash"
		user = super().save(commit=False)
		user.set_password(self.cleaned_data['password1'])
		if commit:
			user.save()
		return user
class UserAdminChangeForm(forms.ModelForm):
	"un modulo per l'aggiornamento degli utenti che include tutti i campi tranne il campo della password con hash"
	password = ReadOnlyPasswordHashField()
	class Meta:
		model = User
		fields = ('email', 'password', 'active', 'admin')
	def clean_password(self):
		return self.initial["password"]