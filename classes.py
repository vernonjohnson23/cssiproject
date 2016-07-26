import webapp2, jinja2, os, logging
from google.appengine.ext import ndb

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_environment = jinja2.Environment(
  loader=jinja2.FileSystemLoader(template_dir))

class Schedule(ndb.Model):
    className = ndb.StringProperty(required=True)
    roomNumber = ndb.StringProperty(required=True)
    classTime = ndb.StringProperty(required=True)
