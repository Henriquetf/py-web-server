from pyramid.config import Configurator
from pyramid.response import Response

def brush_cats(request):
  return Response(
    'Brushy brush cats in the Egyptian pyramids\n',
    content_type='text/plain'
  )

config = Configurator()
config.add_route('brush', '/brush')
config.add_view(brush_cats, route_name='brush')
app = config.make_wsgi_app()
