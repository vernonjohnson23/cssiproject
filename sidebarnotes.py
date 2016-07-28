import webapp2
import jinja2
import os

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_environment = jinja2.Environment(
  loader=jinja2.FileSystemLoader(template_dir))

class SideBarInputNotesHandler(webapp2.RequestHandler):
        def get(self):
            template = jinja_environment.get_template("inputnotes.html")
            html = template.render({})
            self.response.write(html)
class SideBarInputNotesHandler(webapp2.RequestHandler):
        def post(self):
            template = jinja_environment.get_template("inputnotes.html")
            html = template.render({})
            self.response.write(html)
