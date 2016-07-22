import webapp2, jinja2, os, logging
from google.appengine.ext import ndb

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
#tells which directory file is in
jinja_environment = jinja2.Environment(
  loader=jinja2.FileSystemLoader(template_dir))

class BlogPost(ndb.Model):
  title = ndb.StringProperty(required=True)
  post = ndb.StringProperty(required=True)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template("index.html")
        html = template.render({})
        self.response.write(html)

class SiteHandler(webapp2.RequestHandler):
    def post(self):
        title = self.request.get("title")
        post = self.request.get("post")

        blog_post = BlogPost(title=title, post=post)
        blog_post.put()
        logging.info(blog_post.title + blog_post.post)
        template = jinja_environment.get_template("inputpage.html")
        html = template.render({})
        self.response.write(template.render({"title": title, "post": post}))

class BlogPostHandler(webapp2.RequestHandler):
    def get(self):
        logging.info("get function")
        self.response.write('Blog Posts <br>')
        blog_post_query = BlogPost.query()
        blog_posts = blog_post_query.fetch()
        for blog_post in blog_posts:
            self.response.write("by " + blog_post.title + "<br>" +blog_post.text_of_post + "<br>")

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/input', SiteHandler),
    ('/info', BlogPostHandler)
], debug=True)
