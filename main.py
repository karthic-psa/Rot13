  # Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import re
from string import letters

import webapp2
import jinja2

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),autoescape=True)



# def render_str(template, **params):
#         t = jinja_env.get_template(template)
#         return t.render(params)


class BHandler(webapp2.RequestHandler):
    def render(self, template, **kw):
        self.response.out.write(render_str(template, **kw))

    def render_str(template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

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

u_name = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_user(username):
    return username and u_name.match(username)

pass_w = re.compile(r"^.{3,25}$")
def valid_pass(password):
    return password and pass_w.match(password)

e_mail = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
def valid_email(email):
    return email or e_mail.match(email)

class login(BHandler):
    def get(self):
        self.render("login.html")

    def post(self):
        error_present = False
        username = self.request.get('username')
        verify = self.request.get('verify')
        email = self.request.get('email')


        params = dict(username = username,
                          email = email)


        if not valid_user(username):
            params['username_err'] = "That's not a valid username"
            error_present = True
        if not valid_pass(password):
            params['password_err'] = "That's not a valid password"
            error_present = True
        elif password!=verify:
            params['verify_err'] = "Your passwords dont match"
            error_present = True
        if not valid_email(email):
            params['email_err'] = "Your email is not valid"
            error_present = True

        if error_present:
            self.render('login.html', **params)
        else:
            self.redirect('/unit2/welcome?username=' + username)

class Welcome(BHandler):
    def get(self):
        username = self.request.get('username')
        if valid_username(username):
            self.render('welcome.html', username = username)
        else:
            self.redirect('/unit2/login')

# class MainPage(BHandler):
#     def get(self):
        #self.response.headers['Content-Type'] = 'text/plain'
        # self.response.write(form)
        # self.render("main_page.html")

# class TestHandler(webapp2.RequestHandler):
#     def post(self):
#         #q = self.request.get("q")
#         #self.response.out.write(q)
#         self.response.headers['Content-Type'] = 'text/plain'
#         self.response.out.write(self.request)

# app = webapp2.WSGIApplication([('/', Rot13)],
#     debug=True)
pp = webapp2.WSGIApplication([('/unit2/rot13', Rot13),
                               ('/unit2/login', login),
                               ('/unit2/welcome', Welcome)],
                              debug=True)