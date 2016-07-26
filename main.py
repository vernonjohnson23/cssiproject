import webapp2, jinja2, os, logging
from google.appengine.api import users
from google.appengine.ext import ndb

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
#tells which directory file is in
jinja_environment = jinja2.Environment(
  loader=jinja2.FileSystemLoader(template_dir))

class Contact(ndb.Model):
    contactName = ndb.StringProperty(required=True)
    phoneNumber = ndb.StringProperty(required=True)
    numberOfCalls = ndb.StringProperty(required=True)
    dateOfLastCall = ndb.StringProperty(required=True)
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

class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template("index.html")
        html = template.render({})
        self.response.write(html)

        user = users.get_current_user()
        # If the user is logged in...
        if user:
            email_address = user.nickname()
            cssi_user = CssiUser.get_by_id(user.user_id())

            template = jinja_environment.get_template("welcome.html")
            html = template.render({})
            self.response.write(html)

            signout_link_html = '<a href="%s">Sign Out</a>' % (
                  users.create_logout_url('/'))
          # If the user has previously been to our site, we greet them!
            if cssi_user:
                self.response.write('''
                    Welcome %s %s (%s)! <br> %s <br>''' % (
                    cssi_user.first_name,
                    cssi_user.last_name,
                    email_address,
                    signout_link_html))
            # If the user hasn't been to our site, we ask them to sign up
            else:
                self.response.write('''
                    Welcome to our site, %s!  Please sign up! <br>
                    <form method="post" action="/">
                    <input type="text" name="first_name">
                    <input type="text" name="last_name">
                    <input type="submit">
                    </form><br> %s <br>
                    ''' % (email_address, signout_link_html))
                    # Otherwise, the user isn't logged in!

        else:
            self.response.write('''
                Please log in to use our site! <br>
                <a href="%s">Sign in</a>''' % (
                users.create_login_url('/')))

    def post(self):
        logging.info("main post")

        template = jinja_environment.get_template("welcome.html")
        html = template.render({})
        self.response.write(html)

        user = users.get_current_user()
        if not user:
          # You shouldn't be able to get here without being logged in
          self.error(500)
          return
        cssi_user = CssiUser(
            first_name=self.request.get('first_name'),
            last_name=self.request.get('last_name'),
            id=user.user_id(),
            )

        cssi_user.put()

class InputHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template("inputpage.html")
        html = template.render({})
        self.response.write(html)

    def post(self):
        logging.info("input post")

        contactName = self.request.get("contactName")
        phoneNumber = self.request.get("phoneNumber")
        numberOfCalls = self.request.get("numberOfCalls")
        dateOfLastCall = self.request.get("dateOfLastCall")

        #getting user key
        current_user = users.get_current_user()
        userID = current_user.user_id()

        contact = Contact(
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
        contact = Contact(contactName=contactName, phoneNumber=phoneNumber, numberOfCalls=numberOfCalls, dateOfLastCall=dateOfLastCall)
        contact.put()
        logging.info(contact.contactName + contact.phoneNumber + contact.numberOfCalls + contact.dateOfLastCall)

        template = jinja_environment.get_template("inputpage.html")
        html = template.render({"contactName": contactName, "phoneNumber": phoneNumber, "numberOfCalls": numberOfCalls, "dateOfLastCall": dateOfLastCall})
        self.response.write(html)

class InfoHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template("info.html")
        html = template.render({})
        self.response.write(html)

        logging.info("info get")
        self.response.write('Contacts <br>')

        #getting current user key
        user = users.get_current_user().user_id()

        # user_query = CssiUser.query()
        # users = user_query.fetch().filter()
        # for user in users:
            # self.response.write("user key: %s first name: %s last name: %s <br>" %
            #                     (user.key.id(), user.first_name, user.last_name))

        contact_query = Contact.query(Contact.userID == user)
        contacts = contact_query.fetch()#.filter(contact_query.userid == user) #.fetch()
        for contact in contacts:
            self.response.write("%s | %s | %s | %s <br>" %
                                (contact.contactName, contact.phoneNumber, contact.numberOfCalls, contact.dateOfLastCall))
        logging.info("get function")
        self.response.write('Contacts <br>')
        contact_query = Contact.query()
        contacts = contact_query.fetch()
        for contact in contacts:
            self.response.write(contact.contactName + " | " + contact.phoneNumber + " | " + contact.numberOfCalls + " | " + contact.dateOfLastCall + "<br>")

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/input', InputHandler),
    ('/info', InfoHandler)
], debug=True)
