from flask import Flask , render_template , request, session , redirect
import os
import subprocess
#from flask_socketio import SocketIO , emit ,send


import defs.defs as defs

app = Flask(__name__, template_folder='.')

sites_enabled = "/etc/nginx/sites-enabled"
sites_available = "/etc/nginx/sites-available"

writable = defs.file_is_writable(sites_available)

@app.route('/listvsen')
def home_page():
    server_names = defs.list_server_name(sites_available)
    return render_template("pages/dashboard/list_vs_en.html" , vss = server_names , writable = writable )




@app.route('/action_enable', methods=['GET','POST'])
def action_enable():
    index = None
    enabled = None
    path = None
    file_name = None
    if request.method == 'POST':
        clicked = request.form.get('hidin')

    server_names = defs.list_server_name(sites_available)
    
    for i in server_names:
        if server_names[i]['server_name'] == clicked:
            index = i
            enabled = server_names[i]['enabled']
            file_name = server_names[i]['file_name']
            path=sites_available+"/"+file_name
            dest = sites_enabled+'/'+file_name
            if enabled == False:
                 os.symlink(path,dest)
            if enabled == True:
                os.remove(dest)
            subprocess.run(['systemctl', 'reload', 'nginx'])
 
    #server_name = server_names[clicked][server_name]
    #enabled = server_names[clicked][enabled]
    #if request.method == 'POST' :
    return redirect('/listvsen')






if __name__== '__main__':


    app.run(debug=True)