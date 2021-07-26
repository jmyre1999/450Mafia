from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from datetime import datetime

class UserProfileManager(BaseUserManager):
	use_in_migrations = True

	def _create_user(self, email, password, **extra_fields):
		"""
		Creates and saves a User with the given email and password.
		"""
		if not email:
		    raise ValueError('The given email must be set')
		email = self.normalize_email(email)
		user = self.model(email=email, **extra_fields)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_user(self, email, password=None, **extra_fields):
		extra_fields.setdefault('is_superuser', False)
		return self._create_user(email, password, **extra_fields)

	def create_superuser(self, email, password, **extra_fields):
		extra_fields.setdefault('is_superuser', True)

		if extra_fields.get('is_superuser') is not True:
		    raise ValueError('Superuser must have is_superuser=True.')

		return self._create_user(email, password, **extra_fields)

class UserProfile(AbstractBaseUser, PermissionsMixin):
	email = models.EmailField(max_length=75, db_index=True, unique=True)
	first_name = models.CharField(max_length=25, blank=True)
	last_name = models.CharField(max_length=25, blank=True)
	nickname = models.CharField(max_length=25, blank=True)
	image = models.ImageField(upload_to='userprofile', null=True, blank=True, max_length=500)
	is_active = models.BooleanField(default=True)

	objects = UserProfileManager()

	USERNAME_FIELD =  'email'

	# When converting to string, return user's email
	def __str__(self):
		return self.nickname

	def get_full_name(self):
		return self.first_name + ' ' + self.last_name

TEAM_CHOICES = (
	('M', 'Mafia'),
	('T', 'Town'),
)

class Game(models.Model):
	timestamp = models.DateTimeField(auto_now_add=True)
	end_time = models.DateTimeField()
	winner = models.CharField(max_length=1, choices=TEAM_CHOICES)

class GameParticipation(models.Model):
	user = models.ForeignKey('UserProfile', on_delete=models.CASCADE)
	game = models.ForeignKey('Game', on_delete=models.CASCADE)
	role = models.ForeignKey('Role', on_delete=models.CASCADE)

class Role(models.Model):
	name = models.CharField(max_length=25)
	description = models.CharField(max_length=100)
	team = models.CharField(max_length=1, choices=TEAM_CHOICES)
