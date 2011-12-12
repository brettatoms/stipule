import csv
import sqlalchemy as sa
import traceback

from bottle import request, route, run, template, debug, post

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
    """
    Action to create the database tables
    """
    # TODO: option to drop existing tables first
    s = []
    try:
        model.Base.metadata.create_all(model.engine)
    except Exception, e:
        s.append('Error creating tables:')
        s.append(traceback.format_exc())
    else:
        s.append('All tables created.')
    return s


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
