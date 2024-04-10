#import libraries
import os
config_path = '/etc/nginx/sites-available/'


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



def list_server_name(config_path):
    server_names = {}

    available = list_server_available("/etc/nginx/sites-enabled")

    #check existance of nginx directory
    if not os.path.exists(config_path) :
        print(f"Directory does not exist")
        return server_name
    
    
    #save file list in var
    config_files = os.listdir(config_path)
    index = 1 
    for file_name in config_files:
        file_path = os.path.join(config_path,file_name)

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
                                print(type(port_temp))
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


if __name__ == '__main__':
    print(list_server_name(config_path))