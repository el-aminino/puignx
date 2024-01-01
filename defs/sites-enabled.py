import os
config_path = '/etc/nginx/sites-enabled/'
listdir = os.listdir(config_path)
print(listdir)