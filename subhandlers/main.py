import pysite.subhandlers # gives us BaseHandler.

import time
import cgi
from datetime import datetime, timedelta

from app import user


# python encryption examples: - useful to fix readable cookies.
# http://www.example-code.com/python/encryption.asp

def setCookieImpl(name, val, expTime, response_headers, path=''):
	sExpTime = expTime.strftime('%a, %d %b %Y %H:%M:%S GMT') # What an annoying time-format.
	#fixme - escape value:
	expCookie = name + '=' + val + '; Expires=' + sExpTime 

	if path:
		expCookie += '; path=' + path

	print ('cook:', expCookie)

	response_headers += [
		('Set-Cookie', expCookie)
	]



def setCookie(name, val, expDeltaHours, response_headers, path=''):
	later = datetime.utcnow() + timedelta(hours=expDeltaHours)
	setCookieImpl(name,val,later,response_headers,path)

def ensureCookie(name, expDeltaHours, req_data, response_headers): 
	if not req_data.get_cookie_value(name):
		val = 'rotaCookie'
		setCookie(name, str(val), expDeltaHours, response_headers)




def init ( template_info , response_headers , environ,translate , req_data ):
	return #NB -if we have a subhandler, module-init will NOT be called!
		

def redirect ( template_info , cookies,environ ):
	return # NB - will not be called, if we have a subhandler!
	


class MySubhandler(pysite.subhandlers.BaseHandler):

  # I found this in the pysite docs, but it appears to mess up the ctor:
	#def __init__( self, *args, **kw ):
	#	super(MySubhandler, self).__init__(self, *args, **kw)
		
	def redirect (template_info, cookies, environ):
		return

	def init(self):
		#self.template_info['remote_addr'] = self.environ.get('REMOTE_ADDR')
		#self.template_info['some_environ'] = self.environ[0] #.get('REMOTE_ADDR')

		a = str (self.req_data.query_string) #.get('REMOTE_ADDR')
		self.template_info['some_environ'] = a
		self.template_info['say_hello'] = self.translate('Hello')

		ensureCookie('myCook', 1, self.req_data, self.response_headers)
		setCookie('myCook', 'maincook', 1, self.response_headers, '/pathMain')

		#MyDB.ensureDB()
		user.testUser()
		


subhandler = MySubhandler





#    if not req_data.get_cookie_value('bar'):
#    inOneHour = datetime.utcnow() + timedelta(hours=1)
#    expTime = inOneHour.strftime('%a, %d %b %Y %H:%M:%S GMT') # What an annoying time-format.
#    expCookie = 'bar=20; Expires='+expTime #cgi.escape('bar=20; Expires='+expTime )
#    template_info['expCookie'] = expCookie #cgi.escape('bar=20; Expires='+expTime )
#    template_info['utc'] = cgi.escape( expTime )
#    response_headers += [ ('Set-Cookie', expCookie) ]


