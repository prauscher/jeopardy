#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import json
from http.server import SimpleHTTPRequestHandler
from config import events
import urllib

class HTTPFrontendHandler(SimpleHTTPRequestHandler):
	def do_POST(self):
		body = self.rfile.read(int(self.headers['Content-Length'])).decode("utf-8")
		indata = urllib.parse.parse_qs(body)
		if 'stateid' in indata:
			stateid = int(indata['stateid'][0])
		else:
			stateid = 0
		
		data = {'events': []}
		data['events'] = events[stateid:]
		
		data_json = json.dumps(data)
		self.send_response(200)
		self.send_header("Content-Type", "text/json; charset=UTF-8" )
		self.send_header("Content-Length", len(data_json.encode("UTF-8")))
		self.end_headers()
		self.wfile.write(data_json.encode("UTF-8"))

