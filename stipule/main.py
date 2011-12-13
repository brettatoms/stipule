import csv
import sqlalchemy as sa
import traceback

from bottle import request, route, run, template, debug, post, get, put

import model
from model import Accession, Plant

@route('/')
def index():
    """
    """
    body = ''
    return template('main', body=body)


def make_accession_link(acc_num):
    acc_link = '<a %(style)s href="/acc?acc_num=%(acc_num)s">%(acc_num)s</a>'
    style = ''
    session = model.Session()
    query = session.query(Plant).filter(Plant.acc_num == acc_num and not Plant.condition in ("D", "R", "U"))
    if query.count() == 0:
        style = 'style="color: #C00"'

    return acc_link % {'style': style, 'acc_num': acc_num}


@route('/acc')
def acc():
    """
    Return the page for a single accession.
    """
    acc_num = request.query.get('acc_num', '').strip()
    query = session.query(Accession).filter(Accession.acc_num==q)


@route('/search')
def search():
    """
    Search for accessions.
    """
    p = "<p>%s</p>"
    body = []
    q = request.query.get('q', '').strip()
    if not q:
        return template('main', body='')
    session = model.Session()
    query = session.query(Accession).\
        filter(Accession.acc_num==q or Accession.genus==q).\
        order_by(Accession.name)
    results = []
    for row in query:
        link = make_accession_link(row.acc_num)
        results.append('<div>%(link)s - %(name)s</div>' \
                           % {'link': link, 'name': row.name})
    session.close()
    body.append("\n".join(results))
    body.append("<p>%s results.</p>" % len(results))
    return template('main', body='\n'.join(body))


@get('/admin')
def admin_get():
    msg = request.forms.get('message', '')
    name = request.forms.get('name', '')
    if name == 'admin_create':
        msg = "Created database"
    return template('admin', message=msg)


def make_accession(row):
    """
    Convert a row from the BG-Base CSV dump to our model.
    """
    acc = dict()
    set_row = lambda d, s: acc.setdefault(d, row[s].decode('iso-8859-1'))
    colmap = {}
    colmap['acc_num'] = 'ACCESSIONS'
    colmap['genus'] = 'GENUS'
    colmap['name'] = 'NAME'
    colmap['common_name'] = 'COMMON_NAMES'
    colmap['range'] = 'RANGE'
    colmap['misc_notes'] = 'MISCELLANEOUS'
    colmap['recd_dt'] = 'RECEIVED_DT'
    colmap['recd_amt'] = 'NUM_RCD'
    colmap['recd_as'] = 'RECEIVED_AS'
    colmap['recd_size'] = 'RECD_SIZE'
    colmap['recd_notes'] = 'RECD_NOTES'
    colmap['psource_current'] = 'PSOURCE_CURRENT'
    colmap['psource_acc_num'] = 'PSOURCE_ACC_NUM'
    colmap['psource_acc_dt'] = 'PS_ACC_DT'
    colmap['psource_misc'] = 'PSOURCE_MISC'
    for key, value in colmap.iteritems():
        set_row(key, value)
    return acc


def make_plant(row):
    """
    Convert a row from the BG-Base CSV dump to our model.
    """
    plant = dict()
    set_row = lambda d, s: plant.setdefault(d, row[s].decode('iso-8859-1'))
    colmap = {}
    colmap['acc_num'] = 'ACCESSION_#'
    colmap['qualifier'] = 'QUAL'
    colmap['sex'] = 'S'
    colmap['loc_name'] = 'CURRENT_LOCATION'
    colmap['loc_code'] = 'CUR_LOC'
    colmap['loc_change_type'] = 'CLCT'
    colmap['loc_date'] = 'CUR_PLT_DT'
    colmap['loc_nplants'] = '#_PL'
    colmap['condition'] = 'CO'
    colmap['checked_data'] = 'CUR_CK_DT'
    colmap['checked_note'] = 'CURRENT_CHECK_NOTE'
    colmap['checked_by'] = 'CUR_CHK_BY'
    for key, value in colmap.iteritems():
        set_row(key, value)
    return plant


@post('/admin')
def admin_post():
    """
    Action to create the database tables
    """
    # TODO: option to drop existing tables first
    action = request.forms.get('action', '')
    msg = action
    if action == 'admin_create':
        msg = "Created a new database."
        try:
            model.Base.metadata.drop_all(model.engine)
            model.Base.metadata.create_all(model.engine)
        except Exception, e:
            msg = 'Error creating tables:\n' + traceback.format_exc()
    elif action == "upload_accessions":
        data = request.files.data
        if data is not None and data.file:
            # TODO: test to make sure file is readable
            rows = []
            reader = csv.DictReader(data.file, delimiter="\t")
            for row in reader:
                if not row['ACCESSIONS'].strip(): # why are them acc nums w/ ' '
                   continue
                rows.append(make_accession(row))
            insert = Accession.__table__.insert()
            conn = model.engine.connect()
            conn.execute(insert, *rows)
            conn.close()
            msg = "All accessions uploaded."
        else:
            msg = "Choose a file."
    elif action == "upload_plants":
        data = request.files.data
        if data is not None and data.file:
            # TODO: test to make sure file is readable
            rows = []
            reader = csv.DictReader(data.file, delimiter="\t")
            for row in reader:
                # why is there are plant withotu a qualifier?
                if not row['QUAL'] or not row['QUAL'].strip():
                   continue
                rows.append(make_plant(row))
            insert = Plant.__table__.insert()
            conn = model.engine.connect()
            conn.execute(insert, *rows)
            conn.close()
            msg = "All plants uploaded."
        else:
            msg = "Choose a file."
    return template('admin', message=msg)


# TODO: use ConfigParser to read host, port from config
debug(True)
run(host='localhost', port='8080', reloader=True)
