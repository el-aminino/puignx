import os
import re
se_dir = "/etc/nginx/sites-enabled"
sa_dir = "/etc/nginx/sites-available"

def server_in_files(dir): 
    lines_dict=dict({})
    lines_list=list([])
    #list directory
    for i in os.listdir(dir) :
        #open conf file
        with open((dir+'/'+i)) as f :
            lines_list=[]
            #check this line belongs to wich file
            for (j,line) in enumerate(f , 1) :
                if 'server {' in line : 
                    if line[0] == '#' :
                        continue
                    else :
                        lines_list.append(j)
        lines_dict[i]=lines_list
    return lines_dict

def find_srv_name(dir) :
    list_dict = server_in_files(dir)
    key_list = list(list_dict.keys())
    
    for i in key_list :
        val_list=[]
        print(val_list)
        with open (dir+'/'+i) as f :
            val_list = list_dict[i]
            for j in val_list:            
                    print(f.readlines(j) , j)
                    
            
            





#check configurations in Sites-enabled
def check_se(dn):
    find_srv_name(se_dir)

                 

def check_sa(dn):
    print('check sa')




def check_conf(dn):
    check_se(dn)

check_conf('1')