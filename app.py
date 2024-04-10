from flask import Flask , render_template , request, session , redirect
#from flask_socketio import SocketIO , emit ,send


import defs.sitesenabled as se


app = Flask(__name__, template_folder='.')


@app.route('/listvsen')
def home_page():
    server_names = se.list_server_name("/etc/nginx/sites-available")
    return render_template("pages/dashboard/list_vs_en.html" , vss = server_names )

if __name__== '__main__':


    app.run(debug=True)