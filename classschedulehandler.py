import webapp2, jinja2, os, logging
from google.appengine.ext import ndb
import classes
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_environment = jinja2.Environment(
  loader=jinja2.FileSystemLoader(template_dir))


class ClassScheduleHandler(webapp2.RequestHandler):
  def readschedule(self):
      class_info_query = classes.Schedule.query()
      return class_info_query.fetch()
  def writeschedule(self, list_of_schedules):
      template = jinja_environment.get_template("classlist.html")
      classes = ""
      for class_info in list_of_schedules:
          classes += "<br>" + str(class_info.className) +"<br>" +str(class_info.roomNumber) +"<br>" +str(class_info.classTime)+"<br>"
      html = template.render({"classes": classes})
      self.response.write(html)
  def post(self):
      className = self.request.get("className")
      roomNumber = self.request.get("roomNumber")
      classTime = self.request.get('classTime')
      old_classes = self.readschedule()

      class_info = classes.Schedule(className=className, roomNumber=roomNumber, classTime=classTime)
      # writes to data store
      class_info.put()
      logging.info(class_info.className + class_info.roomNumber + class_info.classTime)
      old_classes.append(class_info)

      self.writeschedule (old_classes)
  def get(self):
      # retrieves from the datastore
      full_schedule = self.readschedule()
      # prints inputed class schedules
      self.writeschedule(full_schedule)
