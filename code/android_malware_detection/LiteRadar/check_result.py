import json
import os
log_path = 'E:\\graduate_design\\3rd_party_filter\\log\\'
result_path = 'E:\\graduate_design\\LiteRadar\\samples_result\\'
library_count = {}
for file in os.listdir(result_path):
    filename = log_path+file.split('.')[0]+'.'+file.split('.')[1]+'.log'
    if(os._exists(filename)):
        continue
    result_file = open(result_path+file)
    result = json.load(result_file)
    for item in result:
        library_name = item['Library']
        if library_name in library_count:
            library_count[library_name]+=1
        else:
            library_count[library_name]=1

check_result=open('check_result_new.txt','w+')
for key in library_count:
    check_result.write(str(key)+' '+str(library_count[key])+'\n')