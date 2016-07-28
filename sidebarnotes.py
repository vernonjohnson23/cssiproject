import webapp2
import jinja2
import os
from google.appengine.api import users
import classes
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_environment = jinja2.Environment(
  loader=jinja2.FileSystemLoader(template_dir))

class ListNotesHandler(webapp2.RequestHandler):
        def readnote(self):
            current_user = users.get_current_user()
            user = users.get_current_user().user_id()
            userID = current_user.user_id()
            note_query = classes.NoteProperties.query()
            return note_query.fetch()
        def writenote(self, list_of_notes):
            template = jinja_environment.get_template("noteslist.html")
            notes = ""
            for note_info in list_of_notes:
                notes += "<br>" + note_info.noteTitle +"<br>" + note_info.noteContent+ "<br>"
            html = template.render({"notes": notes})
            self.response.write(html)
        def get(self):
             # retrieves from the datastore
             full_notes_list = self.readnote()
             # prints inputed notes list
             self.writenote(full_notes_list)
        # def post(self):
        #     template = jinja_environment.get_template("noteslist.html")
        #     html = template.render({})
        #     self.response.write(html)
