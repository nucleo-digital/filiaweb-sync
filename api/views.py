import muffin

from api import app

@app.register('/')
def index(request):
    """ Return JSON hello response. """
    return {'message': 'hello'}
