import os
import sys
from io import open
from mimetypes import guess_type
from json import dumps, load
from uuid import uuid4
from bottle import Bottle, request, jinja2_template as render_template, redirect, static_file, TEMPLATE_PATH, response

BASEDIR = os.path.dirname(__file__)
DATADIR = os.path.join(BASEDIR, 'storage')
TEMPLATE_PATH.append(BASEDIR)

app = Bottle()

def file_expander(filename):
    stats = os.stat(os.path.join(DATADIR, filename))
    return {
        'name': filename,
        'type': guess_type(filename)[0] or 'application/octet-stream',
        'size': stats.st_size,
        'lastmod': stats.st_mtime
    }

def am_i_logged_in(req):
    with open(os.path.join(BASEDIR, 'config.json'), 'r', encoding='utf-8') as authdb:
        auth = load(authdb)
    if req.get_cookie('webdumpy') in auth['session']:
        return True
    else:
        return False

@app.route('/')
def page_index():
    if am_i_logged_in(request):
        return render_template('index', docroot=PREFIX)
    else:
        return render_template('login', docroot=PREFIX)

@app.route('/login/')
def page_login():
    return render_template('login', docroot=PREFIX)
    
@app.route('/editor')
def page_editor():
    if am_i_logged_in(request):
        filename = request.query.get('file')
        try:
            if os.path.exists(os.path.join(DATADIR, filename)):
                with open(os.path.join(DATADIR, filename), 'r', encoding='utf-8') as f:
                    data = f.read()
                return render_template('editor', filename=filename, data=data.replace('<', '&lt;').replace('>', '&gt;'), docroot=PREFIX)
            else:
                return render_template('editor', filename=filename, data='', docroot=PREFIX)
        except:            
            return render_template('5xx')
    else:
        return render_template('login', docroot=PREFIX)

@app.route('/res/<path>')
def static_route(path):
    return static_file(path, root=os.path.join(BASEDIR, 'static'))

@app.route('/do/login', method='POST')
def proc_login():
    userpass = request.forms.get('pass')
    with open(os.path.join(BASEDIR, 'config.json'), 'r') as authdb:
        auth = load(authdb)
    if userpass == auth['password']:
        token = str(uuid4())
        if 'session' in auth:
            auth['session'].append(token)
        else:
            auth['session'] = [ token ]
        with open(os.path.join(BASEDIR, 'config.json'), 'w') as authdb:
            authdb.write(dumps(auth).decode('utf-8'))
        response.set_cookie('webdumpy', token, path='/')
        redirect(PREFIX + '/')
    else:
        redirect(PREFIX + '/')

@app.route('/do/logout')
def proc_logout():
    token = request.get_cookie('webdumpy')
    with open(os.path.join(BASEDIR, 'config.json'), 'r') as authdb:
        auth = load(authdb)
    if 'session' in auth:
        auth['session'].remove(token)
    with open(os.path.join(BASEDIR, 'config.json'), 'w') as authdb:
        authdb.write(dumps(auth).decode('utf-8'))
    response.set_cookie('webdumpy', '', path='/', expires=0)
    redirect(PREFIX + '/')

@app.route('/do/upload', method='POST')
def proc_upload():
    if am_i_logged_in(request):
        uploads = request.files.getall('files')
        for f in uploads:
            f.save(os.path.join(DATADIR, f.raw_filename), overwrite=True)
        # return dumps({'code': 0, 'result': 'DONE'})
        return redirect(PREFIX + '/')
    else:
        return render_template('login', docroot=PREFIX)

@app.route('/do/listing')
def proc_listing():
    if am_i_logged_in(request):
        files = list(map(file_expander, os.listdir(DATADIR)))
        return dumps({'code': 0, 'result': files})
    else:
        return render_template('login', docroot=PREFIX)

@app.route('/do/delete', method='POST')
def proc_delete():
    if am_i_logged_in(request):
        files = request.forms.getall('file')
        for f in files:
            if os.path.exists(os.path.join(DATADIR, f)):
                os.remove(os.path.join(DATADIR, f))
        # return dumps({'code': 0, 'result': 'DONE'})
        return redirect(PREFIX + '/')
    else:
        return render_template('login', docroot=PREFIX)

@app.route('/do/rename', method='POST')
def proc_rename():
    if am_i_logged_in(request):
        source = request.forms.get('source')
        target = request.forms.get('target')
        if os.path.exists(os.path.join(DATADIR, source)) and not os.path.exists(os.path.join(DATADIR, target)):
            os.rename(os.path.join(DATADIR, source), os.path.join(DATADIR, target))
        redirect(PREFIX + '/')
    else:
        return render_template('login', docroot=PREFIX)
        
@app.route('/do/update', method='POST')
def proc_update():
    if am_i_logged_in(request):
        filename = request.forms.get('filename')
        text = request.forms.get('text')
	#try:
            # if os.path.exists(os.path.join(DATADIR, filename)):
        with open(os.path.join(DATADIR, filename), 'w', encoding='utf-8') as f:
            f.write(text.decode('utf-8'))
            f.flush()
        return redirect(PREFIX + '/editor?file=' + filename)
        #except:
        #    return str(sys.exc_info()[1])
            # return render_template('5xx', errortrace=str(sys.exc_info()[1]))
    else:
        return render_template('login', docroot=PREFIX)    

if __name__ == '__main__':
    PREFIX = ''
    app.run(port=8800, debug=True)
else:
    PREFIX = '/dashboard'
    application = app
