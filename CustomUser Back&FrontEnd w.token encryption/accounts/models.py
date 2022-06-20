from django.db import models
from django.contrib.auth.models import (
	BaseUserManager, AbstractBaseUser
)
class UserManager(BaseUserManager):
	def create_user(self, email, password=None):
		"crea un utente con e-mail e password specificated"
		if not email:
			raise ValueError('user must have a email address')
		user = self.model(
			email=self.normalize_email(email),
		)
		user.set_password(password)
		user.save(self._db)
		return user
	def create_staffuser(self, email, password):
		"crea un utente con autorizzazioni staff"
		user = self.create_user(
			email=email,
			password=password
		)
		user.staff = True
		user.save(using=self._db)
		return user
	def create_superuser(self, email, password):
		"crea un amministratore con email e password"
		user = self.create_user(
			email=email,
			password=password
		)
		user.staff = True
		user.admin = True
		user.save(using=self._db)
		return user
class User(AbstractBaseUser):
	email = models.EmailField(
		verbose_name='Email address',
		max_length=255,
		unique=True
	)
	active = models.BooleanField(default=False)
	staff = models.BooleanField(default=False)  
	admin = models.BooleanField(default=False)  
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []
	def get_full_name(self):
		return str(self.email)
	def has_perm(self, perm, obj=None):
		"L'utente dispone di un'autorizzazione specifica"
		return True
	def has_module_perms(self, app_lable):
		"L'utente dispone dell'autorizzazione per visualizzare un'app specifica"
		return True
	@property
	def is_staff(self):
		"L'utente è un membro dello staff"
		return self.staff
	@property
	def is_admin(self):
		"L'utente è un membro amministratore"
		return self.admin
	@property
	def is_active(self):
		"L'utente è attivo"
		return self.active
	#collegare il gestore utenti agli oggetti
	objects = UserManager()