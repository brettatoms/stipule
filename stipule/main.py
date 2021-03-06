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

@route('/favicon.ico')
def favicon():
    return static_file('favicon.ico', root='/'.join([WORKING_DIR, 'static']))

@route('/admin.js')
def adminjs():
    return static_file('admin.js', root=WORKING_DIR)

@route('/main.js')
def mainjs():
    return static_file('main.js', root=WORKING_DIR)


@route('/')
def index():
    """
    """
    body = ''
    return template('main', body=body)


@route('/static/<filename:path>')
def static(filename):
    return static_file(filename, root='/'.join([WORKING_DIR, 'static']))


def build_accession_div(accession):
    """
    """
    div = '<div %(class)s><a %(class)s href="/acc?acc_num=%(acc_num)s">%(acc_num)s</a> - %(name)s</div>'
    cls = ''
    session = model.Session()
    query = session.query(Plant).\
        filter(Plant.acc_num==accession.acc_num).\
        filter(sa.not_(Plant.condition.in_(('D','R','U'))))
    if query.count() == 0:
        cls = 'class="dead"'
    session.close()
    return div % {'class': cls, 'acc_num': accession.acc_num,
                  'name': accession.name}


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
    # remove the qualifier if it has one
    num = acc_num.split('*')[0]
    if num is not None:
        acc_num = num
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
    min_length = 3
    if q:
        if len(q) < min_length:
            return template('main', body='<p>Search string needs to be at least %s characters long.<p>' % min_length)
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
        div = build_accession_div(row)
        results.append(div)
    session.close()
    body.append("\n".join(results))
    body.append('<br /><div onclick="show_dead()" id="show-dead" style="cursor: pointer">Show dead...</div>')
    body.append("<p>%s results.</p>" % len(results))
    return template('main', body='\n'.join(body))


@get('/admin')
def admin_get():
    msg = request.forms.get('message', '')
    name = request.forms.get('name', '')
    if name == 'admin_create':
        msg = "Created database"
    return template('admin', message=msg)


acc_colmap = {}
acc_colmap['acc_num'] = 'ACCESSIONS'
acc_colmap['genus'] = 'GENUS'
acc_colmap['family'] = 'FAM'
acc_colmap['name'] = 'NAME'
acc_colmap['common_name'] = 'COMMON_NAME(S)'
acc_colmap['range'] = 'RANGE'
acc_colmap['misc_notes'] = 'MISCELLANEOUS'
acc_colmap['recd_dt'] = 'RECEIVED_DT'
acc_colmap['recd_amt'] = '#RCD'
acc_colmap['recd_as'] = 'RECEIVED AS'
acc_colmap['recd_size'] = 'RECD_SIZE'
acc_colmap['recd_notes'] = 'RECD_NOTES'
acc_colmap['psource_current'] = 'PSOURCE_CURRENT'
acc_colmap['psource_acc_num'] = 'PSOURCE_ACC_#'
acc_colmap['psource_acc_dt'] = 'PS_ACC_DT'
acc_colmap['psource_misc'] = 'PSOURCE_MISC'

def make_accession_row(row):
    """
    Convert a row from the BG-Base CSV dump to our model.
    """
    acc = dict()
    for key, value in acc_colmap.iteritems():
        if row[value] is None:
            acc[key] = None
        else:
            acc.setdefault(key, row[value].decode('iso-8859-1'))
    return acc

plant_colmap = {}
plant_colmap['acc_num'] = 'ACCESSION_#'
plant_colmap['qualifier'] = 'QUAL'
plant_colmap['sex'] = 'S'
plant_colmap['loc_name'] = 'CURRENT_LOCATION'
plant_colmap['loc_code'] = 'CUR_LOC'
plant_colmap['loc_change_type'] = 'CLCT'
plant_colmap['loc_date'] = 'CUR_PLT_DT'
plant_colmap['loc_nplants'] = '#_PL'
plant_colmap['condition'] = 'CO'
plant_colmap['checked_date'] = 'CUR_CK_DT'
plant_colmap['checked_note'] = 'CURRENT_CHECK_NOTE'
plant_colmap['checked_by'] = 'CUR_CHK_BY'

def make_plant(row):
    """
    Convert a row from the BG-Base CSV dump to our model.
    """
    plant = dict()
    for key, value in plant_colmap.iteritems():
        if row[value] is None:
            plant[key] = None
        else:
            plant.setdefault(key, row[value].decode('iso-8859-1'))
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

    # return message to be used added to top of admin page
    return msg


if config.get('debug').lower() == 'true':
    debug(True)

# run the app
host = config.get('host')
port = config.get('port')
run(host=host, port=port, reloader=True)

