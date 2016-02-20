import pysite.subhandlers # gives us BaseHandler.

import time
import cgi
from datetime import datetime, timedelta

from app import user


# python encryption examples: - useful to fix readable cookies.
# http://www.example-code.com/python/encryption.asp

def formatExpireTime(expTime):
	# Ensures the rather specific, peculiar formatting of cookie expire-time-stamps.
	sExpTime = expTime.strftime('%a, %d %b %Y %H:%M:%S GMT') # What an annoying time-format.
	return sExpTime	


def expireTime(expDeltaHours):
	# Supplies an "N hours from now" timestamp.
	later = datetime.utcnow() + timedelta(hours=expDeltaHours)
	return later


def expiresOption(deltaHours):
	t = expireTime(deltaHours)
	s = formatExpireTime(t)
	option = "Expires=" + s
	return option




def setCookieImpl(name, val, expTime, response_headers, path=''):
	sExpTime = formatExpireTime(expTime)    # expTime.strftime('%a, %d %b %Y %H:%M:%S GMT') # What an annoying time-format.
	#fixme - escape value:
	expCookie = name + '=' + val + '; Expires=' + sExpTime 

	if path:
		expCookie += '; path=' + path

	print ('full cookie string:', expCookie)

	response_headers += [
		('Set-Cookie', expCookie)
	]






def setCookie(name, val, expDeltaHours, response_headers, path=''):
	later = expireTime(expDeltaHours)   # datetime.utcnow() + timedelta(hours=expDeltaHours)
	setCookieImpl(name,val,later,response_headers,path)

def ensureCookie(name, expDeltaHours, req_data, response_headers): 
	if not req_data.get_cookie_value(name):
		val = 'rotaCookie'
		setCookie(name, str(val), expDeltaHours, response_headers)




def init ( template_info, response_headers, environ, translate, req_data ):
	print "global-init"
	return #NB -if we have a subhandler, module-init will NOT be called!
		

#def redirect ( template_info , cookies,environ ):
#	print "global-redir"
#	return # NB - will not be called, if we have a subhandler!
	


class MySubhandler(pysite.subhandlers.BaseHandler):

	# I found this in the pysite docs, but it appears to mess up the ctor:
	#def __init__( self, *args, **kw ):
	#	super(MySubhandler, self).__init__(self, *args, **kw)
		

	def init(self):
		self.redirectTo = False

		email = self.req_data.get_post_value('email')
		if email == None:
			email=''
		self.template_info['email'] =email

		pwd = self.req_data.get_post_value('password')
		if pwd == None:
			pwd=''
		self.template_info['password'] =pwd

		pwd2 = self.req_data.get_post_value('password2')
		#print('pwd2:',pwd2)
		if pwd2 == None:
			pwd2=''
		self.template_info['password2'] =pwd2

		#print ('postvalue:', email)
		if not email:
			return # just render the page then.

		if len(pwd)==0:
			self.template_info['passwordEmpty'] = True
			return

		u = user.User.dbFindByEmail(email) #Does this user account exist?
		if not u: # Unknown email: Prompt user to create this account.
			self.template_info['emailUnknown'] = True

			if not pwd2:
			  return # Unknown email: Prompt user to create this account.
			else: # we have pwd 2..
				if pwd <> pwd2:
					self.template_info['passwordsMismatch'] = True
					return
        
        # passwords match - so:					
				print('attempt account creation.')
				u = user.User(email,pwd)
				u.dbInsert()
				self.template_info['emailUnknown'] = False
				self.template_info['accountCreatedOK'] = True
				self.template_info['password'] = '' # force user to re-enter.
				return
			#
		else: #known user - so is pwd correct?
			if pwd <> u.password:
				self.template_info['passwordWrong'] = True
				return
			else: # correct login.
			  # NB - this doesn't really work, because we do a redirect - so redirect, instead, must set the cookie.
				setCookie('loginCookie', email, 1, self.response_headers) #, '/pathMain')
				self.loginCookieVal = str(email) # NB! will barf, if email contains unicode chars..
				self.redirectTo = 'afterLogin' 
				pass
		
	def redirect(self, cookies): #, template_info, environ):
		if self.redirectTo:
			print "local-redir"
			option = expiresOption(1)
			# NB! - cookie must be 'str/string', not unicode.
			cookies.append("loginCookie=" + self.loginCookieVal + "; " + option)
			return self.redirectTo

		return # end redirect.


subhandler = MySubhandler
