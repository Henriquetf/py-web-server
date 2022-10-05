import socket
import io
import sys
import datetime

class WSGIServer:

    address_family = socket.AF_INET
    socket_type = socket.SOCK_STREAM
    request_queue_size = 1

    def __init__(self, server_address):
      listen_socket = socket.socket(self.address_family, self.socket_type)
      listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
      listen_socket.bind(server_address)
      listen_socket.listen(self.request_queue_size)

      host, port = listen_socket.getsockname()[:2]

      self.listen_socket = listen_socket
      self.server_name = socket.getfqdn(host)
      self.server_port = port
      self.headers_set = []

    def set_app(self, application):
      self.application = application

    def serve_forever(self):
      while True:
        self.client_connection, client_address = self.listen_socket.accept()
        self.handle_one_request()

    def handle_one_request(self):
      request_data = self.client_connection.recv(1024)
      request_data = request_data.decode('utf-8')

      print(''.join(
        f'< {line}\n' for line in request_data.splitlines()
      ))

      self.request_data = request_data
      self.parse_request(request_data)

      env = self.get_environment()

      result = self.application(env, self.start_response)

      self.finish_response(result)

    def parse_request(self, text):
      request_first_line = text.splitlines()[0]
      request_first_line = request_first_line.rstrip('\r\n')

      (
        self.request_method,
        self.path,
        self.request_version
      ) = request_first_line.split()

    def get_environment(self):
      env = {}

      env['wsgi.version'] = (1, 0)
      env['wsgi.url_scheme'] = 'http'
      env['wsgi.input'] = io.StringIO(self.request_data)
      env['wsgi.errors'] = sys.stderr
      env['wsgi.multithread'] = False
      env['wsgi.multiprocess'] = False
      env['wsgi.run_once'] = False

      env['REQUEST_METHOD'] = self.request_method
      env['PATH_INFO'] = self.path
      env['SERVER_NAME'] = self.server_name
      env['SERVER_PORT'] = str(self.server_port)

      return env

    def start_response(self, status, response_headers, exc_info=None):
      now = datetime.datetime.now()
      now_formatted = now.strftime('%a, %d %b %Y %H:%M:%S %Z')

      server_headers = [
        ('Date', now_formatted)
      ]
      self.headers_set = [status, response_headers + server_headers]

    def finish_response(self, result: list[bytes]):
      try:
        status, response_headers = self.headers_set
        response = f'HTTP/1.1 {status}\r\n'

        for header in response_headers:
          response += '{0}: {1}\r\n'.format(*header)

        response += '\r\n'

        for data in result:
          response += data.decode('utf-8')

        print(''.join(
          f'> {line}\n' for line in response.splitlines()
        ))

        response_bytes = response.encode()
        self.client_connection.sendall(response_bytes)
      finally:
        self.client_connection.close()

SERVER_ADDRESS = (HOST, PORT) = '', 8080

def make_server(server_address, application):
  server = WSGIServer(server_address)
  server.set_app(application)

  return server

if __name__ == '__main__':
  if len(sys.argv) < 2:
    sys.exit('Provide a WSGI application object as module:callable')

  app_path = sys.argv[1]
  module, application = app_path.split(':')
  module = __import__(module)
  application = getattr(module, application)
  httpd = make_server(SERVER_ADDRESS, application)
  print(f'WSGIServer: Serving HTTP on port {PORT} ...\n')
  httpd.serve_forever()
