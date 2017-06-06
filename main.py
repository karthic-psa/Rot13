import webapp2
import jinja2
import os

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),autoescape=True)

def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

class BHandler(webapp2.RequestHandler):
    def render(self, template, **kw):
        self.response.out.write(render_str(template, **kw))

    def render_str(self, template, **params):
        return render_str(template, **params)

#    def render_str(template, **params):
#       t = jinja_env.get_template(template)
#       return t.render(params)

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

class Rot13(BHandler):
    def get(self):
        self.render('main_page.html')

    def post(self):
        rot13 = ''
        text = self.request.get('text')
        if text:
            rot13 = text.encode('rot13')

        self.render('main_page.html', text = rot13)

app = webapp2.WSGIApplication([('/rot13', Rot13)], debug=True)