import jinja2
import subprocess
import os
import shutil
import re

#This is a Nginx config sample 
nginx_template = """
server {
    listen {{ port }};
    server_name {{ server_name }};
    root {{ document_root }};
    index index.html;

    location / {
        try_files $uri $uri/ =404;
    }

    access_log /var/log/nginx/{{ server_name }}.access.log;
    error_log /var/log/nginx/{{ server_name }}.error.log;
}
"""

domain_regex = r'(([\da-zA-Z])([_\w-]{,62})\.){,127}(([\da-zA-Z])[_\w-]{,61})?([\da-zA-Z]\.((xn\-\-[a-zA-Z\d]+)|([a-zA-Z\d]{2,})))'
domain_regex = '{0}$'.format(domain_regex)

#This configurations will be applied
config_data = {
    'port': 80,
    'server_name': 'example.com',
    'document_root': '/var/www/html',  
}

#take values from user for configurations
port = input("Please Enter Listen port (Default: 80): ")


#Validate Listen port
try:
    port=int(port)
except (ValueError , TypeError) :
   print("Invalid port Number")
   port = 80
   print("default Port implemented")
   
#Take Hostname
srv_name = input("Please Enter Server Name (default: Example.com): ")
#Validate Hostname
srv_name_check = re.match(domain_regex,srv_name)

if srv_name_check :
    pass
else :
    print("invalid Hostname")
    srv_name = "example.com"
    print("default hostname implemented")
#take document root
doc_root = input("Please Enter Root Directory for virtual server (Default: /var/www/html ) : ")
if doc_root[0] != '/' :
    print("invalid document root")
    doc_root = ' /var/www/html'
    print("default hostname implemented")



#check the values existance
if port :
    config_data['port'] = port

if srv_name :
    config_data['server_name'] = srv_name
else :
    config_data['server_name'] = "_"

if doc_root :
    config_data['document_root'] = doc_root

template = jinja2.Template(nginx_template)
nginx_config = template.render(config_data)

config_templ = '/etc/nginx/sites-available/{{ server_name }}'
config_temp = jinja2.Template(config_templ)
if config_data['server_name'] == '_':
    tem_srv_name = 'default'
    config_path = config_temp.render(server_name=tem_srv_name)
else :
    config_path = config_temp.render(server_name=config_data['server_name'])



#write Nginx configurations into sites-available
with open(config_path, 'w') as f:
    f.write(nginx_config)
#create a soft link for site-available into sites-enabled
subprocess.run(['ln', '-s', config_path, '/etc/nginx/sites-enabled/'])
#restart Nginx service
subprocess.run(['systemctl', 'reload', 'nginx'])

#Checking Document Root existance 
root_doc = config_data['document_root']
if os.path.exists(root_doc) == False :
    print("document root is unavailable ! it may not exist.")
    print("Creating Directory")
    try :
        os.mkdir(root_doc)
        shutil.chown(group='www-data',path=root_doc)
    except FileNotFoundError :
        tstr = '/'
        root_ex = root_doc.split('/')
        root_ex.pop(0)
        for i in root_ex :
            tstr = tstr+i+'/'
            if os.path.exists(tstr) :
                print(tstr)
            else:
                os.mkdir(tstr)
        shutil.chown(group='www-data',path=root_doc)
    
    if os.path.exists(root_doc) == True :
        print("Directory created !")
else :
    shutil.chown(group='www-data',path=root_doc)

#Check index existance
print("Checking Index existance")
index_file = root_doc+'/'+"index.html"
if os.path.exists(index_file) == True :
    print("index exist!")
else :
    print("index not exist \n Creating Index file")
    shutil.copy(src="../pages/default_index.html", dst=index_file)
    
