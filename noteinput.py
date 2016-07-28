import webapp2, jinja2, os, logging, time, datetime
from google.appengine.ext import ndb
from google.appengine.api import users

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_environment = jinja2.Environment(
  loader=jinja2.FileSystemLoader(template_dir))

class NoteProperties(ndb.Model):
    noteTitle = ndb.StringProperty(required=True)
    noteContent = ndb.StringProperty(required=True)
