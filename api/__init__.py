import muffin

app = application = muffin.Application(
    'api', CONFIG='api.config.debug')

muffin.import_submodules(__name__)
