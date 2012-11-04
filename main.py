#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from http.server import HTTPServer
from threading import Thread

from admin import HTTPAdminHandler
from frontend import HTTPFrontendHandler

class FrontendServerHandler(Thread):
	def run(self):
		httpd_frontend = HTTPServer(('127.0.0.1', 1337), HTTPFrontendHandler)
		httpd_frontend.serve_forever()

class AdminServerHandler(Thread):
	def run(self):
		httpd_admin = HTTPServer(('127.0.0.1', 1338), HTTPAdminHandler)
		httpd_admin.serve_forever()

def run():
	FrontendServerHandler().start()
	AdminServerHandler().start()

if __name__ == '__main__':
	run()
