import webapp2, jinja2, os, logging
from google.appengine.ext import ndb
import classschedulehandler
import classes
import sidebar
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
#tells which directory file is in
jinja_environment = jinja2.Environment(
  loader=jinja2.FileSystemLoader(template_dir))

class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template("index.html")
        html = template.render({})
        self.response.write(html)


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/classschedule', sidebar.SideBarHandler),
    ('/classlist', classschedulehandler.ClassScheduleHandler)
], debug=True)
