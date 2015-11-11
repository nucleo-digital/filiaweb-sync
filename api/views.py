import muffin

from api import app, filiaweb

@app.register('/')
def index(request):
    """ Return JSON hello response. """
    return {'message': 'hello'}

@app.register('/process-csv', methods='POST')
def process_csv(request):
    """ Return JSON with uploaded CSV fields """
    data = yield from request.post()

    file_name = data.get('file_name')
    file_text = data.get('file_text')

    persisted_id = filiaweb.persist_csv_data(file_name, file_text)
    process_result = filiaweb.process_csv_data(persisted_id, file_text)

    return {'json': process_result}
