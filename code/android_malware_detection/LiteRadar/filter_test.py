import os
import subprocess
apks_path = 'D:\\apk_samples\\white\\'
result_path = 'D:\\apk_samples\\white_3rd_result\\'
i=0
for file in os.listdir(apks_path):
    print(file)
    print(i)
    i+=1
    filename = file.split('.')[0]

    if os.path.exists(result_path + filename + '.result'):
        print('already')
        continue

    apk_file = apks_path+file

    '''
    if 'apk' not in file:
        os.rename(apk_file,apk_file+'.apk')
        apk_file=apk_file+'.apk'
        print 'rename'
        print apk_file
    '''

    jar_command = 'py -2 literadar.py '+apk_file+' > '+result_path+filename+'.result'

    child = subprocess.Popen(jar_command,shell=True)
    child.wait()