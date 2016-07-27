import webapp2, jinja2, os, logging, time, datetime
from google.appengine.api import users
from google.appengine.ext import ndb

import classes

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
#tells which directory file is in
jinja_environment = jinja2.Environment(
  loader=jinja2.FileSystemLoader(template_dir))

class EditHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template("edit.html")
        html = template.render({})
        self.response.write(html)

    def post(self):
        template = jinja_environment.get_template("edit.html")
        html = template.render({})
        self.response.write(html)

        logging.info("edit post")

        contactName = self.request.get("contactName")
        phoneNumber = self.request.get("phoneNumber")
        numberOfCalls = int(self.request.get("numberOfCalls"))

        #getting date from user, splitting it into numbers
        date = str(self.request.get("dateOfLastCall"))
        dateParts = date.split('-', 2 )

        #building a date
        dateYear = int(dateParts[0])
        dateMonth = int(dateParts[1])
        dateDay = int(dateParts[2])

        dateOfLastCall = datetime.datetime(dateYear, dateMonth, dateDay)

        #number of days until next reminder
        reminder = int(self.request.get("reminder"))

        #today as a date
        today = time.time()
        newDateS = reminder * 24 * 60 * 60 + today

        #convert to sec since epoch and back into a date
        dateOfReminder = datetime.datetime.utcfromtimestamp(newDateS)

        #getting user key
        current_user = users.get_current_user()
        userID = current_user.user_id()

        #getting the relevant contact based on name,
        #editing its properties, and adding it back to the datastore
        contact = classes.Contact.query(classes.Contact.contactName == contactName).fetch()
        for contact in contact:
            contact.contactName = contactName
            contact.phoneNumber = phoneNumber
            contact.numberOfCalls = numberOfCalls
            contact.dateOfLastCall = dateOfLastCall
            contact.reminder = reminder
            contact.dateOfReminder = dateOfReminder
            contact.put()

        # template = jinja_environment.get_template("info.html")
        # html = template.render({"contact name": contactName,
        #                         "phone number": phoneNumber,
        #                         "number of calls": numberOfCalls,
        #                         "date of last call": dateOfLastCall})
        # self.response.write(html)
