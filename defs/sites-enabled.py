import os
config_path = '/etc/nginx/sites-enabled/'
listdir = os.listdir(config_path)

for i in listdir :
    file = config_path+i
    with open(file,"r") as f :
        if "server_name" in f.readline():
            print(f.readline)




#print(listdir)