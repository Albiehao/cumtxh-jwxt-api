from http.server import SimpleHTTPRequestHandler, HTTPServer
import os
import threading
from datetime import datetime
from icalendar import Calendar

class CalendarHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, ics_path=None, **kwargs):
        self.ics_path = ics_path
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        if self.path == '/schedule.ics':
            self.send_response(200)
            self.send_header('Content-type', 'text/calendar')
            self.end_headers()
            with open(self.ics_path, 'rb') as f:
                self.wfile.write(f.read())
        else:
            self.send_response(404)
            self.end_headers()

def run_server(ics_path, port=8000):
    handler = lambda *args: CalendarHandler(*args, ics_path=ics_path)
    server = HTTPServer(('', port), handler)
    print(f"日历服务已启动: http://139.224.41.131:{port}/schedule.ics")
    server.serve_forever()

def start_calendar_service(ics_path, port=8000):
    """启动日历服务"""
    thread = threading.Thread(target=run_server, args=(ics_path, port))
    thread.daemon = True
    thread.start()
    return thread