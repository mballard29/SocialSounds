from django.core import signing
from django.core.validators import validate_email
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User, Group
from django.conf import settings as django_settings
from django.shortcuts import render, redirect, reverse

from rest_framework.authtoken.models import Token
from api.models import Profile
from api.models import Player 

from . import settings as auth_settings
import re
# CREDIT: Most of this file is based very closely off of the tutorial from Education Ecosystem on YouTube (cited in README).

# AuthTools class contains only static methods
class AuthTools:

	password_salt = auth_settings.AUTH_PASSWORD_SALT
	token_age = auth_settings.AUTH_TOKEN_AGE

    # creates/issues the token for a user
	@staticmethod
	def issue_user_token(user, salt):

		if user is not None:
			if (salt == 'login'):
				token, _ = Token.objects.get_or_create(user=user)
			else:
				token = signing.dumps({'pk': user.pk}, salt=salt)

			return token

		return None

    # verifies the token for a user
	@staticmethod
	def get_user_from_token(token, salt):

		try:
			value = signing.loads(token, salt=AuthTools.password_salt, max_age=900)
		except signing.SignatureExpired:
			return None
		except signing.BadSignature:
			return None

		user = User.objects.get(pk=value['pk'])

		if user is not None:
			return user

		return None

    # basically wraps Django authenticate method (by username)
	@staticmethod
	def authenticate(username, password):

		try:
            # below is built-in Django authenticate function
			user = authenticate(username=username, password=password)
			if user is not None:
				return user
		except:
			pass

		return None

    # same as authenticate basically but for email
	@staticmethod
	def authenticate_email(email, password):

		# use regex pattern match to see if email is valid
		if re.match(r'[^@]+@[^@]+\.[^@]+', email):
			user = AuthTools.get_user_by_email(email)
			if user is not None:
				return AuthTools.authenticate(user.username, password)
		else:
			# option to log in with username
			return AuthTools.authenticate(email, password)

		return None

    # helper to return whole user by email
	@staticmethod
	def get_user_by_email(email):
	
		if email:
			try:
				user = User.objects.filter(email=email, is_active=True)[0]
				return user
			except:
				pass

		return None

    # helper to return whole user by username
	@staticmethod
	def get_user_by_username(username):

		try:
			user = User.objects.filter(username=username, is_active=True)[0]
			return user
		except:
			pass

		return None

    # log in a user
	@staticmethod
	def login(request, user):

		if user is not None:
			try:
				login(request, user)
				return True
			except Exception as e:
				template = "An exception of type {0} occured. Arguments:\n{1!r}"
				message = template.format(type(e).__name__, e.args)

		return False

    # logs out a user
	@staticmethod
	def logout(request):

		if request:
			try:
				Token.objects.filter(user=request.user).delete()
				logout(request)
				return True
			except Exception as e:
				print(e)
				pass

		return False

	@staticmethod
	def createPlayer(user_data):
		album_id = user_data['album_id']

		try:
			# player = Player.create_player(album_id)
			player_data = {
				'album_id': album_id
			}
			player = Player(album_id)
			# player = Player.create_player(album_id=album_id)

			player.save()
			return {
				'created': True
			}

		except Exception as e:
			print(str(e))
			raise Exception(e)

		return None

    # registers a user
	@staticmethod
	def register(user_data, profile_data, group):
		# user_data = {'username', 'email', 'password'}
		# profile_data = {'role', 'position'}
		first_name = user_data['first_name']
		last_name = user_data['last_name']
		username = user_data['username']
		email = user_data['email']
		password = user_data['password']
		profile_data = {}

		try:
			# check if email already exists
			email_exists = User.objects.filter(email=user_data['email'])
			if email_exists:
				return {
					'email': email_exists[0],
					'is_new': False
				}

			# check if username already exists
			username_exists = User.objects.filter(username=user_data['username'])
			if username_exists:
				return {
					'user': username_exists[0],
					'is_new': False
				}

			user = User.objects.create_user(username, email, password,
				first_name=first_name, last_name=last_name)

			profile_data['owner'] = user
			profile = Profile(**profile_data)
			profile.save()

            # group is for different user levels (admin or non-admin)
			group = Group.objects.get(name=group)
			group.user_set.add(user)

            # return a dict
			return {
				'user': user,
				'is_new': True
			}

		except Exception as e:
			print(str(e))
			raise Exception(e)

		return None


	@staticmethod
	def profile_register(user, profile_data):
	
		# profile_data = {'role', 'position'}

		try:
			return Profile.objects.get(pk=user.id)

		except ObjectDoesNotExist:
			try:
				profile_data['user'] = user
				profile = Profile(**profile_data)
				profile.save()

				group = Group.objects.get(name=profile_data['role'] + '_basic')
				group.user_set.add(user)

				return profile
			except:
				pass

		return None

    # helper function to set a user password
	@staticmethod
	def set_password(user, password, new_password):

		if user.has_usable_password():
			if user.check_password(password) and password != new_password:
				user.set_password(new_password)
				user.save()
				return True
		elif new_password:
			user.set_password(new_password)
			user.save()
			return True

		return False

    # helper function to reset a user password if necessary
	@staticmethod
	def reset_password(token, new_password):

		user = AuthTools.get_user_from_token(token, AuthTools.password_salt)

		if user is not None:
			user.set_password(new_password)
			user.save()
			return user

		return None

    # helper function to check that a username is in correct format and not taken by another user
	@staticmethod
	def validate_username(username):

		min_username_length = 3
		stats = 'valid'

		if len(username) < min_username_length:
			stats = 'invalid'
		elif re.match("^[a-zA-Z0-9_-]+$", username) is None:
			stats = 'invalid'
		else:
			user = AuthTools.get_user_by_username(username)

			if user is not None:
				stats = 'taken'

		return stats

    # helper function to check that an email is in correct format and not taken by another user
	@staticmethod
	def validate_email(email):

		status = 'valid'

		try:
			validate_email(email)
			user = AuthTools.get_user_by_email(email)

			if user is not None:
				status = 'taken'

		except:
			status = 'invalid'

		return status

    # helper to make sure password is valid and of correct length
	@staticmethod
	def validate_password(password):

		min_password_length = 7
		is_valid = True

		if len(password) < min_password_length:
			is_valid = False

		return is_valid