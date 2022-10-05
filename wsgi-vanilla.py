def app(env, start_response):
  status = '200 MAYBE'
  response_headers = [('Content-Type', 'text/plain')]
  start_response(status, response_headers)

  return [b'Brush my hairy cats because they fell on some sticky vanilla\n']
