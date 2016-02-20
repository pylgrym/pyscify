# -*- coding: utf-8 -*-
from pysite.conf import PySiteConfiguration
from pysite.compat import PORTABLE_STRING

class HelloworldConf(PySiteConfiguration):
	sitename = 'helloworld'
	translations = ['en']
	sitetitle = PORTABLE_STRING('yes')
	
	def __init__(self,basedir):
		super(HelloworldConf, self).__init__(basedir)

siteconf = HelloworldConf
