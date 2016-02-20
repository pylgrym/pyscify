import pysite.subhandlers # gives us BaseHandler.


class MySubhandler(pysite.subhandlers.BaseHandler):
  def init(self):
    val = self.req_data.get_cookie_value('loginCookie')
    print ('gotten cookie:', val)
    self.template_info['signedInUser'] =  val

subhandler = MySubhandler
