import cgi
import csv
import datetime
import os
import traceback

from bottle import request, route, run, template, debug, post, get, put, \
    static_file, TEMPLATE_PATH
import sqlalchemy as sa

import config
import model
from model import Accession, Plant

# look in current directory for templates
WORKING_DIR = os.path.split(__file__)[0]
TEMPLATE_PATH.append(WORKING_DIR)

# URI for form for updating plants
plant_change_form_uri = config.get('plant_change_form_uri')

# maps of plant condition codes to strings
condition_map = {'A': 'Alive',
                 'E': 'Excellent',
                 'G': 'Good',
                 'F': 'Fair',
                 'P': 'Poor',
                 'Q': 'Questionable',
                 'I': 'Indistinguishable',
                 'D': 'Dead',
                 'R': 'Deaccessioned/Removed',
                 'U': 'Unable to locate'}


@route('/')
def index():
    """
    """
    body = ''
    return template('main', body=body)


@route('/static/<filename:path>')
def static(filename):
    return static_file(filename, root='/'.join([WORKING_DIR, 'static']))


def build_accession_link(acc_num):
    acc_link = '<a %(style)s href="/acc?acc_num=%(acc_num)s">%(acc_num)s</a>'
    style = ''
    session = model.Session()
    query = session.query(Plant).\
        filter(Plant.acc_num==acc_num).\
        filter(sa.not_(Plant.condition.in_(('D','R','U'))))
    if query.count() == 0:
        style = 'style="color: #C00"'
    session.close()
    return acc_link % {'style': style, 'acc_num': acc_num}


def build_accession_table(acc):
    """
    Return an html table from the acc argument.
    """
    parts = ['<table>']
    row = '<tr><td>%s</td><td>%s</td></tr>'
        #parts.append(row % ('Name:', acc.name))
    name_href = '<a href="/search?name=%(name)s">%(name)s</a>'
    google_href = '<span style="margin-left: 40px"><a href="http://google.com/search?q=%(name)s">google</a></span>'
    name_href = name_href + google_href
    parts.append(row % ('Name:', name_href % {'name': cgi.escape(acc.name)}))
    parts.append(row % ('Acc #:', acc.acc_num))
    parts.append(row % ('Family:', acc.family.capitalize()))
    parts.append(row % ('Common name:', acc.common_name))
    parts.append(row % ('Range:', acc.range))
    parts.append(row % ("Misc. Notes:", acc.misc_notes))
    parts.append('<br />')
    parts.append(row % ("Rec'd. Date:", acc.recd_dt))
    parts.append(row % ("Rec'd. Amt:",acc.recd_amt))
    parts.append(row % ("Rec'd. Size:", acc.recd_size))
    parts.append(row % ("Rec'd. As:",
                        name_href % {'name': cgi.escape(acc.name)}))
    parts.append(row % ("Rec'd. Notes:", acc.recd_notes))

    parts.append(row % ("Source:", acc.psource_current))
    parts.append(row % ("Source Acc. #:", acc.psource_acc_num))
    parts.append(row % ("Source Acc. Date:", acc.psource_acc_dt))
    parts.append(row % ("Source Notes:", acc.psource_misc))
    parts.append('</table>')
    return ''.join(parts)


def build_plants_table(accession):
    """
    Return an html table with the plants of acc_num.
    """
    parts = ['<div>']
    parts.append('Plants:')
    parts.append('<table>')
    map_uri = config.get('map_uri')
    map_href = '<a href="%s">map</a>' % map_uri
    plants_href = '<a href="%(form)s&entry_0=%(name)s&entry_1=%(date)s&entry_2=%(acc_num)s&entry_3=%(qualifier)s&entry_5=%(location)s">%(plant)s</a>'
    for plant in accession.plants:
        parts.append('<tr>')
        href = plants_href % \
            {'form': plant_change_form_uri, 'name': accession.name,
             'acc_num': accession.acc_num, 'qualifier': plant.qualifier,
             'date': datetime.date.today(), 'location': plant.loc_code,
             'plant': '%s*%s' % (accession.acc_num, plant.qualifier)}
        map_span = '<span style="margin-left: 40px">%s</span>' % map_href
        parts.append('<td>%s:</td><td>%s (%s) %s</td>' \
                         % (href, plant.loc_name, plant.loc_code, map_span))
        parts.append('</tr><tr>')
        nplants = plant.loc_nplants
        if nplants in (None, ''):
            nplants = '??'
        loc_date = plant.loc_date
        if not loc_date in (None, ''):
            loc_date = '??'

        parts.append('<td>&nbsp;</td><td>%s plants on %s</td>' \
                         % (nplants, plant.loc_date))
        parts.append('</tr><tr>')
        checked_date = plant.checked_date
        if not checked_date:
            checked_date = '??'
        condition = condition_map.get(plant.condition, plant.condition)
        if plant.condition in ('DRU'):
            condition = '<span style="color:red">%s</span>' % condition
        parts.append('<td>&nbsp;</td><td>Condition: %s on %s</td>' \
                         % (condition, checked_date))
        parts.append('</tr><tr>')
        parts.append('<td>&nbsp;</td><td>Checked by %s: %s</td>' \
                         % (plant.checked_by, plant.checked_note))
        parts.append('</tr>')
    parts.append('</table>')
    parts.append('</div>')
    return ''.join(parts)



@route('/acc')
def acc():
    """
    Return the page for a single accession.
    """
    acc_num = request.query.get('acc_num', '').strip()
    session = model.Session()
    query = session.query(Accession).filter(Accession.acc_num==acc_num)
    acc = query.first()
    body = []
    body.append(build_accession_table(acc))
    body.append('<br />')
    body.append(build_plants_table(acc))
    body.append('<br />')
    # append "Add a plant..." for adding more plants
    add_form_href = '<p><a href="%(form)s&entry_0=%(name)s&entry_1=%(date)s&entry_2=%(acc_num)s">Add a plant...</a></p>' % \
        {'form': plant_change_form_uri, 'name':acc.name,
         'date': datetime.date.today(), 'acc_num': acc.acc_num}
    body.append(add_form_href)
    session.close()
    return template('main', body='\n'.join(body))


@route('/search')
def search():
    """
    Search for accessions.
    """
    p = "<p>%s</p>"
    body = []
    q = request.query.get('q', '').strip()
    name = request.query.get('name', '').strip()
    session = model.Session()
    query = session.query(Accession)
    lower = lambda c: sa.func.lower(c)
    if q:
        if len(q) < 3:
            return template('main', body='<p>Search string too short.<p>')
        query = query.\
            filter(sa.or_(Accession.acc_num==q,
                          Accession.acc_num.like('%%%s' % q.lower()),
                          lower(Accession.genus)==q.lower(),
                          lower(Accession.name).like('%%%s%%' % q.lower()),
                          lower(Accession.common_name).like('%%%s%%'%q.lower()),
                          lower(Accession.family)==q.lower()
                          )).order_by(Accession.name)
    elif name:
        query = query.filter(Accession.name==name).order_by(Accession.name)
    else:
        return template('main', body='')

    results = []
    for row in query:
        link = build_accession_link(row.acc_num)
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


def make_accession_row(row):
    """
    Convert a row from the BG-Base CSV dump to our model.
    """
    acc = dict()
    set_row = lambda d, s: acc.setdefault(d, row[s].decode('iso-8859-1'))
    colmap = {}
    colmap['acc_num'] = 'ACCESSIONS'
    colmap['genus'] = 'GENUS'
    colmap['family'] = 'FAM'
    colmap['name'] = 'NAME'
    colmap['common_name'] = 'COMMON_NAME(S)'
    colmap['range'] = 'RANGE'
    colmap['misc_notes'] = 'MISCELLANEOUS'
    colmap['recd_dt'] = 'RECEIVED_DT'
    colmap['recd_amt'] = '#RCD'
    colmap['recd_as'] = 'RECEIVED AS'
    colmap['recd_size'] = 'RECD_SIZE'
    colmap['recd_notes'] = 'RECD_NOTES'
    colmap['psource_current'] = 'PSOURCE_CURRENT'
    colmap['psource_acc_num'] = 'PSOURCE_ACC_#'
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
    colmap['checked_date'] = 'CUR_CK_DT'
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
                rows.append(make_accession_row(row))
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


if config.get('debug').lower() == 'true':
    debug(True)

# run the app
host = config.get('host')
port = config.get('port')
run(host=host, port=port, reloader=True)

