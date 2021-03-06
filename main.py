import webapp2
import cgi
import jinja2
import os
from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.write(*a, **kw)
        
    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)
        
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))        

class Post(db.Model):
    title = db.StringProperty(required = True)
    post = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
        
# class MainHandler(Handler):
    # def render_front(self, title="", post="", error=""):
        # posts = db.GqlQuery("SELECT * FROM Post ORDER BY created DESC")
        # self.render("blog.html", title=title, post=post, error=error, posts=posts)
        
    # def get(self):
        # self.render_front()
        
class BlogMain(Handler):
    def get_blog(self, title="", post="", error=""):
        posts = db.GqlQuery("SELECT * FROM Post ORDER BY created DESC")
        self.render("blog.html", title=title, post=post, error=error, posts=posts)
        
    def get(self):
        self.get_blog()
        
class NewPost(Handler):
    def new_post(self, title="", post="", error=""):
        self.render("newpost.html", title=title, post=post, error=error)
        
    def get(self):
        self.new_post()
    
    def post(self):
        title = self.request.get("title")
        post = self.request.get("post")
        
        if title and post:
            p = Post(title = title, post = post)
            key = p.put()
            self.redirect("/blog/%d" % key.id())
            
        else:
            error = "We need both a title and a post."
            self.new_post(title, post, error)      

class BlogPage(Handler):
    def get(self, id):
        s = Post.get_by_id(int(id))
        self.render("blogpage.html", posts = [s])

app = webapp2.WSGIApplication([
    # ('/', MainHandler),
    ('/blog', BlogMain),
    ('/blog/newpost', NewPost),
    webapp2.Route('/blog/<id:\d+>', BlogPage)
], debug=True)
