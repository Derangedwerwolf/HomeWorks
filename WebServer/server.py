from http.server import BaseHTTPRequestHandler
import mimetypes
from pathlib import Path
import socket
import urllib.parse
from routes.main import routes


class Server(BaseHTTPRequestHandler):
    def do_HEAD(self):
        return
    
    
    def do_POST(self):
        data = self.rfile.read(int(self.headers['Content-Length']))
        data_parse = urllib.parse.unquote_plus(data.decode())
        print(data_parse)
        
        data_dict = {key: value for key, value in [
            el.split('=') for el in data_parse.split('&')
            ]}
        print(data_dict)
        
        self.send_response(302)
        self.send_header('Location', '/')
        self.end_headers()
        #return
    
    
    def do_GET(self):
        self.respond()
        
    
    def handle_http(self):
        status = 200
        content_type = "text/plain"
        response_content = ""
        pr_url = urllib.parse.urlparse(self.path)

        if pr_url.path in routes:
            print(routes[pr_url.path])
            
            route_content = routes[pr_url.path]['template']
            #filepath = Path("templates/{}".format(route_content))
            
            filepath = Path().resolve().joinpath("templates", route_content)
            print(filepath, pr_url.path)
            
            if filepath.is_file():
                content_type = "text/html"
                with open(filepath, 'rb') as rc:
                    response_content = rc.read()
                # response_content = open(Path().resolve().joinpath("templates", route_content))
                # response_content = response_content.read()
            else:
                status = 404
                content_type = "text/html"
                with open(filepath, 'rb') as rc:
                    response_content = rc.read()
        else:
            if Path().joinpath(pr_url.path[1:]).exists():
                print(Path().joinpath(pr_url.path[1:]))
                return self.send_static(pr_url.path)
                #response_content = self.send_static(pr_url.path)
                #print(response_content)
                #return response_content
            # content_type = "text/plain"
            # response_content = b"404 Not Found"
            else:
                status = 404
                content_type = "text/html"
                with open(Path().resolve().joinpath("templates", "error.html"), 'rb') as rc:
                    response_content = rc.read()
                #response_content = bytes(Path().resolve().joinpath("templates", "error.html"))
            
        self.send_response(status)
        self.send_header('Content-type', content_type)
        self.end_headers()
        #route_content = routes.get(self.path)
        
        #return bytes("Hello, World!", "UTF-8")
        #return bytes("<h2><center>Hello, World!</center></h2>", "UTF-8")
        #return bytes(route_content, "UTF-8")
        return response_content
    
    
    def send_static(self, path):
        self.send_response(200)
        mt = mimetypes.guess_type(path)
        print(f'{mt[0]=}')
        
        if mt:
            self.send_header("Content-type", mt[0])
        else:
            self.send_header("Content-type", 'text/plain')
        
        self.end_headers()
        with open(f'.{path}', 'rb') as file:
            #self.wfile.write(file.read())
            return file.read()
            
    def echo_server(host, port):
        with socket.socket() as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((host, port))
            s.listen(1)
            
            conn, addr = s.accept()
            print(f"Connected by {addr}")
            
            with conn:
                while True:
                    data = conn.recv(1024)
                    print(f'From client: {data}')
                    if not data:
                        break
                    conn.send(data.upper())


    def respond(self):
        content = self.handle_http()
        self.wfile.write(content)