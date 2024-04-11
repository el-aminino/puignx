#import libraries
import os
import jinja2
import subprocess
import shutil
config_path = '/etc/nginx/sites-available/'


#Check write rights for file
def file_is_writable(config_path):



    #check existance of nginx directory
    if not os.path.exists(config_path) :
        print(f"Directory does not exist")

    
    #save file list in var
    config_files = os.listdir(config_path)
    
    for file_name in config_files:
        file_path = os.path.join(config_path,file_name)

        if os.path.isfile(file_path) and os.access(file_path, os.W_OK):
            return True
        else :
            return False




#check server-name directive in any file 
def list_server_available(config_path):
    server_names = []


    #check existance of nginx directory
    if not os.path.exists(config_path) :
        print(f"Directory does not exist")
        return server_name
    
    
    #save file list in var
    config_files = os.listdir(config_path)
    
    for file_name in config_files:
        file_path = os.path.join(config_path,file_name)

        if os.path.isfile(file_path) and os.access(file_path, os.R_OK):
            with open(file_path, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    line = line.strip()
                    if line.startswith('server_name'):
                        server_name= line.split()[1].split(';')[0]
                        server_names.append(server_name)
    
    return server_names


#export server_name and other directives in specified file(like Port, IP, roor directory)
def list_server_name(config_path):
    #this dicitionary will be filled
    server_names = {}
    available = list_server_available("/etc/nginx/sites-enabled")

    #check existance of nginx directory
    if not os.path.exists(config_path) :
        print(f"Directory does not exist")
        return server_name
    
    
    #List all files in directory
    config_files = os.listdir(config_path)
    

    #Itterate over each config file
    index = 1 
    for file_name in config_files:
        file_path = os.path.join(config_path,file_name)

        #check if it's file and readable 
        if os.path.isfile(file_path) and os.access(file_path, os.R_OK):
            with open(file_path, 'r') as f:
                lines = f.readlines()
                server_name = None
                port = None
                root = None
                port_list = None
                enabled  = False

                for line in lines:
                    line = line.strip()

                    if line.startswith('server_name'):
                        server_name = line.split()[1].split(';')[0]


                    if line.startswith('listen'):
                        port = line.split()[1].split(';')[0]
                        port_list = port.split(':')
                        
                        if ':' in port:
                            if "[" in port and "]" in port:
                                port_temp= port_list[len(port_list)-1]
                                port_list = []
                                port_list.append(port.replace(port_temp,""))
                                port_list.append(port_temp)
                                port_temp = port_list[0]
                                port_temp = port_temp[:-1]
                                port_list[0] = port_temp
                            port = port_list
                        else :         
                            port_list[0] = "0.0.0.0"
                            port_list.append(port)
                            port = port_list


                    if line.startswith('root'):
                        root = line.split()[1].split(';')[0]
                        
                    for i in available :
                        if i == server_name:
                            enabled = True
                            break

                    if server_name and port and root:
                        server_names[index] = {'file_name':file_name ,'server_name': server_name , 'port' : port , 'root' : root , 'enabled' : enabled}
                        index = index +1
                        server_name = None
                        port = None
                        root = None
                        enabled = False
    
    return server_names

def create_virtual_server(srv_name,port,doc_root):
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
   
    #This configurations will be applied
    config_data = {
        'port': 80,
        'server_name': 'example.com',
        'document_root': '/var/www/html',  
    }

    config_data['server_name'] = srv_name
    config_data['port']= port
    config_data['document_root']= doc_root

    template = jinja2.Template(nginx_template)
    nginx_config = template.render(config_data)

    config_file_template = '/etc/nginx/sites-available/{{ server_name }}'
    config_file_templ = jinja2.Template(config_file_template)

    config_path = config_file_templ.render(server_name = srv_name)

    with open(config_path, 'w') as f:
        f.write(nginx_config)
    
    subprocess.run(['ln', '-s', config_path, '/etc/nginx/sites-enabled/'])


    
    if os.path.exists(doc_root) == False :
        print("document root is unavailable ! it may not exist.")
        print("Creating Directory")
        try :
            os.mkdir(doc_root)
            shutil.chown(group='www-data',path=doc_root)
        except FileNotFoundError :
            tstr = '/'
            root_ex = doc_root.split('/')
            root_ex.pop(0)
            for i in root_ex :
                tstr = tstr+i+'/'
                if os.path.exists(tstr) :
                    print(tstr)
                else:
                    os.mkdir(tstr)
            shutil.chown(group='www-data',path=doc_root)
        
        if os.path.exists(doc_root) == True :
            print("Directory created !")
    else :
        shutil.chown(group='www-data',path=doc_root)



    subprocess.run(['systemctl', 'reload', 'nginx'])

