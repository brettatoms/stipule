import csv
import sqlalchemy as sa
import traceback

from bottle import request, route, run, template, debug, post, get

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


@get('/admin')
def admin_get():
    msg = request.forms.get('message', '')
    name = request.forms.get('name', '')
    if name == 'admin_create':
        msg = "Created database"
    return template('admin', message=msg)


@post('/admin')
def admin_post():
    """
    Action to create the database tables
    """
    # TODO: option to drop existing tables first
    action = request.forms.get('action', '')
    msg = action
    if action == 'admin_create':
        msg = "Created databased"
        try:
            model.Base.metadata.create_all(model.engine)
        except Exception, e:
            msg = 'Error creating tables:\n' + traceback.format_exc()
    return template('admin', message=msg)




@post('/admin/upload')
def admin_upload():
    cls = request.query.get('class', '').lower()
    data = request.files.file
    if cls == 'plant':
        cls = model.Plant
        return 'imported Plants'

    elif cls == 'accession':
        cls = model.Accession
        return 'imported Accessions'
    else:
        return ['unknown class: %s' % cls]

    # rows = []
    # for row in data:
    #     rows.append(row)
    # return rows




# TODO: use ConfigParser to read host, port from config
debug(True)
run(host='localhost', port='8080', reloader=True)
