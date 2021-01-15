# Social Sounds

## Team Members: 
- Mason Ballard
- Melissa Ma
- Chad McGuire
- Homer McMillan

## Description:
Instagram is great, but it has its limits. It's great for sharing photos and videos, but what about music? Meet SocialSounds.<br/><br/>
SocialSounds is a social media web app made for sharing your favorite music from Spotify. Spotify has a limited set of features for sharing music with your friends (called "Friend Activity"), but SocialSounds isolates and builds on these features. Users can post their favorite music from Spotify and listen in-app with our embedded Spotify players. Create a profile. Like and comment on your friends posts. And listen away!

## Instructions for User Interface:
<img src="http://g.recordit.co/jEfh9WPud3.gif">

## Python Libraries:
- Django
- Django Rest Framework
- Spotipy
<br/><br/>(Please see the `requirements.txt` document for all packages and versions installed for development)

## Resources:
The following tutorials were helpful in setting up and designing the structure of a Django-based social media web app:<br/>
- How To Create Instagram Like App in Python Django Tutorial (https://www.youtube.com/watch?v=oXrc6tNCFI4) - This tutorial was the most helpful for learning how to set up the strcure of a Django web app. This tutorial helped us to model the paradigm of using models, views, and serializers. This tutorial also guided us in user authentication (including the AuthTools wrapper class to modify built-in Django authentication methods and serilaizers and posts for authentication functionality).
- Workflow: Python and Virtualenv (https://www.youtube.com/watch?v=nnhjvHYRsmM) - This tutorial helped us in setting up virtualenv for our Django development.
- How to Reset Migrations (https://simpleisbetterthancomplex.com/tutorial/2016/07/26/how-to-reset-migrations.html) - This tutorial helped us in resetting the Django migrations in the case of major updates to the database models.

## Separation of Work:
- Mason Ballard - I worked primarily on set up and backend, setting up the database and schema in models.py, and the 'api' django app, and registering each model on the admin page
- Melissa Ma _ I worked primarily on the front-end templates as well as integration with the backend. I designed the website pages in HTML with the Bulma CSS framework, and rendered the website pages correctly and aesthetically to reflect the data in our databases by connecting it to the API endpoints. I created forms to take in user input such as the login, register, and create post pages to create new objects using Django Rest Framework to add to the database. 
- Chad McGuire - I worked primarily on the backend of the application, wrote the views and serializers for the backend social media API, worked on building/modifying many of the database models, and developed user authentication functionality (including all views, serializers, urls, and other utilities needed).
- Homer McMillan
<br/>
(Please see the git log for more detailed contributions)

## How to Deploy: 

1. Create venv with `python3 -m venv [name of env]`
2. Activate virtual environment: `source [name of env]/bin/activate`
3. Navigate to the directory that contains the file `manage.py`
4. Install packages in requirements.txt in venv/virtualenv: `pip3 install -r requirements.txt `
5. Make migrations: `python3 manage.py makemigrations api`
6. Migrate: `python3 manage.py migrate`
7. Initialize an admin account (follow the prompts on the screen to complete): `python3 manage.py createsuperuser`
8. Deploy and run with: `python3 manage.py runserver`
9. Upon the creation of the database and admin account, go to `[localhost_base_url]/admin` in your browser after running the server and add `consumer_basic` and `staff_basic` to the Groups model (required for permissions)
10. Have fun sharing!

## Changes from Proposal:

In most facets, we stayed true to our proposal, but there are some changes that we made. Primarily due to time constraints, we decided it was best to host/deploy our web app locally and focus on other features as opposed to deploying to a service such as AWS or Azure. We also decided to go with only public profiles (once logged in, each user can see the posts/profiles of all other users). Additionally, we went with Django's built-in user authentication protocols rather than using a 3rd-party service such as Firebase. Finally, we did not include User's comments and likes for the front-end except to implement a caption, due to a focus on displaying the feed of shared posts more than on the social aspect of following, unfollowing, finding friends, and liking and commenting. However, we have the serializers set up in the back-end to create and track the count of Like and Comment objects. 
