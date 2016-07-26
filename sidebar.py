import webapp2, jinja2, os, logging
from google.appengine.ext import ndb
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
#tells which directory file is in
jinja_environment = jinja2.Environment(
  loader=jinja2.FileSystemLoader(template_dir))

class SideBarHandler(webapp2.RequestHandler):
        def get(self):
            template = jinja_environment.get_template("classschedule.html")
            html = template.render({})
            self.response.write(html)
