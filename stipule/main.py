from bottle import route, run, template, debug

import model

@route('/')
def index():
    """
    """
    body = ''
    return template('main', body=body)


@route('/search')
def search():
    """
    """
    body = ''
    return template('main', body=body)


@route('/admin')
def admin():
    return template('admin')

@route('/admin/create')
def admin_create():
    pass

@route('/admin/upload')
def admin_upload():
    pass

# TODO: use ConfigParser to read host, port from config
debug(True)
run(host='localhost', port='8080', reloader=True)
