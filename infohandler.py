import webapp2, jinja2, os, logging
from google.appengine.api import users
from google.appengine.ext import ndb

import classes

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
#tells which directory file is in
jinja_environment = jinja2.Environment(
  loader=jinja2.FileSystemLoader(template_dir))

class InfoHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template("info.html")
        html = template.render({})
        self.response.write(html)

        logging.info("info get")

        #getting current user key
        user = users.get_current_user().user_id()

        # user_query = CssiUser.query()
        # users = user_query.fetch().filter()
        # for user in users:
            # self.response.write("user key: %s first name: %s last name: %s <br>" %
            #                     (user.key.id(), user.first_name, user.last_name))

        contact_query = classes.Contact.query(classes.Contact.userID == user)
        contacts = contact_query.fetch()#.filter(contact_query.userid == user) #.fetch()
        for contact in contacts:
            self.response.write("<br><br>%s | %s | %s | %s <br>" %
                                (contact.contactName, contact.phoneNumber, contact.numberOfCalls, contact.dateOfLastCall))

        # template = jinja_environment.get_template("info.html")
        # html = template.render({"contactName": contactName,
        #                         "phoneNumber": phoneNumber,
        #                         "numberOfCalls": numberOfCalls,
        #                         "dateOfLastCall": dateOfLastCall})
        # self.response.write(html)