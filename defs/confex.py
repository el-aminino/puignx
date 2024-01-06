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




#check configurations in Sites-enabled
def check_se(dn):
    server_in_files(se_dir)

                 

def check_sa(dn):
    print('check sa')




def check_conf(dn):
    check_se(dn)

check_conf('1')