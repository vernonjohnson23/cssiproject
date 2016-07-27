import webapp2, jinja2, os, logging, time, datetime
from google.appengine.ext import ndb
from google.appengine.api import users

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_environment = jinja2.Environment(
  loader=jinja2.FileSystemLoader(template_dir))

class Schedule(ndb.Model):
    className = ndb.StringProperty(required=True)
    roomNumber = ndb.StringProperty(required=True)
    classTime = ndb.StringProperty(required=True)

class Contact(ndb.Model):
    contactName = ndb.StringProperty(required=True)
    phoneNumber = ndb.StringProperty(required=True)
    numberOfCalls = ndb.IntegerProperty(required=False)
    dateOfLastCall = ndb.DateProperty(required=True)
    reminder = ndb.IntegerProperty(required=True)
    dateOfReminder = ndb.DateProperty(required=True)
    userID = ndb.StringProperty(required=True)

class CssiUser(ndb.Model):
    """
    CssiUser stores information about a logged-in user.

    The AppEngine users api stores just a couple of pieces of
    info about logged-in users: a unique id and their email address.

    If you want to store more info (e.g. their real name, high score,
    preferences, etc, you need to create a Datastore model like this
    example).
    """
    first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()
