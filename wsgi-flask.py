from flask import Flask
from flask import Response

flask_app = Flask('flaskapp')

@flask_app.route('/brush')
def brush_cats():
    return Response(
      'Brushy brush cats in the flask\n',
      mimetype='text/plain'
    )

app = flask_app.wsgi_app
