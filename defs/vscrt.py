import jinja2
import subprocess

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

config_data = {
    'port': 80,
    'server_name': 'example.com',
    'document_root': '/var/www/html',  
}

port = input("Please Enter Listen port: ")
srv_name = input("Please Enter Server Name: ")
doc_root = input("Please Enter Root Directory for virtual server : ")

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




with open(config_path, 'w') as f:
    f.write(nginx_config)

subprocess.run(['ln', '-s', config_path, '/etc/nginx/sites-enabled/'])

subprocess.run(['systemctl', 'reload', 'nginx'])