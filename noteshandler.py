import webapp2, jinja2, os, logging
from google.appengine.ext import ndb
from google.appengine.api import users
import classes
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_environment = jinja2.Environment(
  loader=jinja2.FileSystemLoader(template_dir))

class NotesHandler(webapp2.RequestHandler):
  def readnote(self):
      current_user = users.get_current_user()
      user = users.get_current_user().user_id()
      userID = current_user.user_id()
      note_query = classes.NoteProperties.query(classes.NoteProperties.userID == user)
      return note_query.fetch()
  def writenote(self, list_of_notes):
      template = jinja_environment.get_template("noteslist.html")
      notes = ""
      for note_info in list_of_notes:
          notes += "<br>" + note_info.noteTitle +"<br>" + note_info.noteContent+ "<br>"
      html = template.render({"notes": notes})
      self.response.write(html)
  def post(self):
      noteTitle = self.request.get("noteTitle")
      noteContent= self.request.get("noteContent")
      previous_notes = self.readnote()
      current_user = users.get_current_user()
      userID=self.request.get("userID")
      user = users.get_current_user().user_id()
      note_info = classes.NoteProperties(noteTitle=noteTitle, noteContent=noteContent, userID=userID)
      # writes to data store
      note_info.put()
      logging.info(note_info.noteTitle + note_info.noteContent)
      previous_notes.append(note_info)
      logging.info(previous_notes)
      self.writenote (previous_notes)
  def get(self):
      # retrieves from the datastore
      full_notes_list = self.readnote()
      # prints inputed notes list
      self.writenote(full_notes_list)
