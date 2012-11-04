#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from http.server import BaseHTTPRequestHandler
import os
import json
from config import events
import urllib
import cgi
import time

class HTTPAdminHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		if self.path[0:7] == "/admin/":
			data = ""
			self.send_response(200)
			self.send_header("Content-Type", "text/json; charset=UTF-8")
			self.end_headers();
			self.wfile.write(json.dumps(data).encode("utf-8"));
			pass
		else:
			path = os.curdir + os.sep + "admin" + os.sep + self.path
			if os.path.isdir(path):
				path = path + os.sep + "index.html"
			if not os.path.exists(path):
				self.send_error(404)
			else:
				f = open(path)
				self.send_response(200)
				self.end_headers()
				self.wfile.write(f.read().encode("utf-8"))
				f.close()

	def do_POST(self):
		ctype, params = cgi.parse_header(self.headers['Content-Type'])
		clen = int(self.headers['Content-Length']);
		data = {}
		if ctype == "multipart/form-data":
			data = cgi.FieldStorage(fp = self.rfile, headers = self.headers, environ={'REQUEST_METHOD':'POST'})
		else:
			body = self.rfile.read(clen).decode("utf-8")
			data = urllib.parse.parse_qs(body)

		if self.path[0:12] == "/admin/event":
			if len(events) > 0:
				data['eventid'] = events[-1]['eventid'] + 1;
			else:
				data['eventid'] = 1;
			data['timestamp'] = time.time();
			events.append(data)
		if self.path[0:11] == "/admin/init":
			event = {}
			if len(events) > 0:
				event['eventid'] = events[-1]['eventid'] + 1;
			else:
				event['eventid'] = 1;
			event['type'] = 'init';
			event['timestamp'] = time.time();
			event['data'] = json.loads(data['questions'].file.read().decode("utf-8"))
			events.append(event)
		self.send_response(301);
		self.send_header("Location", "/admin.html")
		self.end_headers()
		self.wfile.write("...".encode("utf-8"))
