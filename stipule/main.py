import csv
import sqlalchemy as sa
import traceback

from bottle import request, route, run, template, debug, post, get, put

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


#ACCESSIONS   GENUS	NAME	SPECIES	SPECIES_2	CULTIVAR	CULTIVAR_2	FAM	COMMON_NAMES	RANGE	MISCELLANEOUS	RECEIVED_DT	NUM_RCD	RECEIVED_AS	RECD_SIZE	RECD_NOTES	PSOURCE_CURRENT	PSOURCE_ACC_NUM	PS_ACC_DT	PSOURCE_MISC
def make_accession(row):
    acc = dict()
    acc['acc_num'] = row['ACCESSIONS']
    return acc


# ACC_NUM*QUAL	ACCESSION_#	QUAL	S	CURRENT_LOCATION	CUR_LOC	CLCT	CUR_PLT_DT	#_PL	CO	CUR_CK_DT	CURRENT_CHECK_NOTE	CUR_CHK_BY
def make_plant(row):
    plant = dict()
    plant['acc_num'] = row['ACCESSION_#']
    plant['qualifier'] = row['QUAL']
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
            insert = model.Accession.__table__.insert()
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
            insert = model.Plant.__table__.insert()
            conn = model.engine.connect()
            conn.execute(insert, *rows)
            conn.close()
            msg = "All plants uploaded."
        else:
            msg = "Choose a file."
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
