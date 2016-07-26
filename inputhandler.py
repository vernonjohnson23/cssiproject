import webapp2, jinja2, os, logging
from google.appengine.api import users
from google.appengine.ext import ndb

import classes

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
#tells which directory file is in
jinja_environment = jinja2.Environment(
  loader=jinja2.FileSystemLoader(template_dir))

class InputHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template("inputpage.html")
        html = template.render({})
        self.response.write(html)

    def post(self):
        template = jinja_environment.get_template("inputpage.html")
        html = template.render({})
        self.response.write(html)

        logging.info("input post")

        contactName = self.request.get("contactName")
        phoneNumber = self.request.get("phoneNumber")
        numberOfCalls = int(self.request.get("numberOfCalls"))
        dateOfLastCall = self.request.get("dateOfLastCall")

        #getting user key
        current_user = users.get_current_user()
        userID = current_user.user_id()

        contact = classes.Contact(
            contactName=contactName,
            phoneNumber=phoneNumber,
            numberOfCalls=numberOfCalls,
            dateOfLastCall=dateOfLastCall,
            userID=userID,
            )
        contact.put()

        template = jinja_environment.get_template("inputpage.html")
        html = template.render({"contact name": contactName,
                                "phone number": phoneNumber,
                                "number of calls": numberOfCalls,
                                "date of last call": dateOfLastCall})
