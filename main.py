import webapp2, jinja2, os, logging
from google.appengine.ext import ndb

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
#tells which directory file is in
jinja_environment = jinja2.Environment(
  loader=jinja2.FileSystemLoader(template_dir))

class Contact(ndb.Model):
    contactName = ndb.StringProperty(required=True)
    phoneNumber = ndb.StringProperty(required=True)
    numberOfCalls = ndb.StringProperty(required=True)


class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template("index.html")
        html = template.render({})
        self.response.write(html)

class InputHandler(webapp2.RequestHandler):
    def post(self):
        contactName = self.request.get("contactName")
        phoneNumber = self.request.get("phoneNumber")
        numberOfCalls = self.request.get("numberOfCalls")

        contact = Contact(contactName=contactName, phoneNumber=phoneNumber, numberOfCalls=numberOfCalls)
        contact.put()
        logging.info(contact.contactName + contact.phoneNumber + contact.numberOfCalls)

        template = jinja_environment.get_template("inputpage.html")
        html = template.render({"contactName": contactName, "phoneNumber": phoneNumber, "numberOfCalls": numberOfCalls})
        self.response.write(html)

class InfoHandler(webapp2.RequestHandler):
    def get(self):
        logging.info("get function")
        self.response.write('Contacts <br>')
        contact_query = Contact.query()
        contacts = contact_query.fetch()
        for contact in contacts:
            logging.info(contact.contactName + contact.phoneNumber + contact.numberOfCalls)
            self.response.write(contact.contactName + " | " + contact.phoneNumber + " | " + contact.numberOfCalls + "<br>")

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/input', InputHandler),
    ('/info', InfoHandler)
], debug=True)
