from flask import *

from flask_sqlalchemy import *

import os

from datetime import datetime

app = Flask(__name__, static_url_path = '/static')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///trailCam.db'
db = SQLAlchemy(app)

class MotionDect(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    timeStamp = db.Column(db.DateTime, nullable = False)
    temp = db.Column(db.Float, nullable = False)
    status = db.Column(db.String(30), nullable= False)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/display')
def display():
    basepath = f"./static/images"
    #print(os.path.exists(basepath))
    dir = os.walk(basepath)
    file_list = []
    
    for path, sub, files in dir:
        for file in files:
            if file[-3:].lower()=='jpg' or file[-4:].lower() =="jpeg":
                temp = os.path.join(path, file)
                file_list.append(temp)

    return render_template('display.html', hists=file_list)


@app.route('/logs', methods = ['POST', 'GET'])
def logs():
    if(request.method == 'POST'):
        if request.form['table'] == 'Update':  
            basepath = f"./static/images"
            dir = os.walk(basepath)
            
            for path, sub, files in dir:
                if path != "./static/images\logs":
                    for file in files:
                        if file[-3:].lower()=='txt':
                            temp = os.path.join(path, file)
                            if(os.path.isfile(temp)):
                                fileOpen = open(temp, 'r')
                                newPath = path + "/logs"
                                newfile = os.path.join(newPath, "systemStatus.txt")
                                fileCopy = open(newfile, 'a');
                                for line in fileOpen.readlines():
                                    fileCopy.write(line)
                                    line = line.strip()
                                    line = line.split(',')
                                    timeStamp = datetime.strptime(line[0], '%Y-%m-%d %H:%M:%S') 
                                    log = MotionDect( timeStamp = timeStamp, temp = line[1], status = line[2])
                                    db.session.add(log)
                                    db.session.commit()
                                fileOpen.close()
                                os.remove(temp)
                                fileCopy.close()
                                
    
    logTable = MotionDect.query.all()
    return render_template('logs.html', table = logTable)

@app.route('/search', methods = ['POST', 'GET'])
def search():
    print("hello")
    
    
                    
app.app_context().push()
if __name__ == '__main__':
    app.run()