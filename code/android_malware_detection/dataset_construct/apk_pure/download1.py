# coding=utf-8
#定义代理ip
import urllib.request
import urllib
import csv
import os
from static import root
import datetime
from multiprocessing import Pool
import shutil

# 在print内容前加上时间后打印
def time_print(string):
    print(str(datetime.datetime.now()) + ' : ' + string)


def download_apk(type, localfile):
    # if (localfile == 'I:/android_malware_detection/compare/download/APK_Downloader-master/apk/music_and_audio/Free Music player MP3 Whatlisten_v2.3.0_apkpure.com.apk'):
    #     print('I:/android_malware_detection/compare/download/APK_Downloader-master/apk/music_and_audio/Free Music player MP3 Whatlisten_v2.3.0_apkpure.com.apk')
    #     if os.path.exists(localfile):
    #         print('File Exites ' + localfile + '!')
    #         return
    if os.path.exists(localfile):
        # print('File Exites ' + localfile + '!')
        shutil.move(localfile.replace('/'+type +'/', '/bk/'), 'I:/android_malware_detection/compare/download/APK_Downloader-master/apk/bak/')
        return
    else:
        shutil.move(localfile.replace('/'+type +'/', '/bk/'), 'I:/android_malware_detection/compare/download/APK_Downloader-master/apk/'+type+'/')
        # os.system('move ' + localfile.replace('/communication/', '/bk/').replace(' ', '\ ') + ' ' + 'I:/android_malware_detection/compare/download/APK_Downloader-master/apk/communication/')
        # print('move ' + localfile.replace('/communication/', '/bk/').replace(' ', '\ ') + ' ' + 'I:/android_malware_detection/compare/download/APK_Downloader-master/apk/communication/')
        print(localfile)
        # fo = open('123456.txt', 'a+')
        # fo.write(url + '\n')
        # fo.close()
        # print(url)
        return


def parse_csv(csvfile):
    f = csv.reader(open(csvfile, 'r',encoding='utf-8'))
    count = 0
    count_50 = 0
    count_60 = 0
    count_70 = 0
    count_80 = 0
    count_null = 0
    total_size = 0.0
    for i in f:
        app_name = i[0]
        str_category = i[1]
        Latest_Version = i[2]
        Publish_Date = i[3]
        Requirements = i[4]
        app_size_ = i[5]
        apk_filepath = i[6]
        Author = i[7]
        url = i[8]

        if url == 'null' or apk_filepath.endswith('.xapk'):
            continue
        count += 1
        if app_size_.endswith(' GB'):
            app_size = float(app_size_[:-3]) * 1000
            count_50 += 1
            count_60 += 1
            count_70 += 1
            count_80 += 1
        elif app_size_.endswith(' MB'):
            app_size = float(app_size_[:-3])
            if app_size > 50:
                count_50 += 1
            if app_size > 60:
                count_60 += 1
            if app_size > 70:
                count_70 += 1
            if app_size > 80:
                count_80 += 1
        elif app_size_.endswith(' KB'):
            app_size = float(app_size_[:-3])/1000
        elif app_size_ == 'null':
            app_size = 0
            count_null += 1
        else:
            print(i, app_name, app_size_)
            continue
        if app_size <= 50:
            if not os.path.exists(root + 'compare/download/APK_Downloader-master/apk/' + str_category + '/'):
                os.mkdir(root + 'compare/download/APK_Downloader-master/apk/' + str_category + '/')
            try:
                # if (apk_filepath.strip().replace(':', '_').replace('/', '_').endswith('Football Score Schedule_v1.1_apkpure.com.apk')):
                #     print(root + 'compare/download/APK_Downloader-master/apk/' + str_category + '/' + apk_filepath.strip().replace(':', '_').replace('/', '_'))

                download_apk(str_category, root + 'compare/download/APK_Downloader-master/apk/' + str_category + '/' + apk_filepath.strip().replace(':', '_').replace('/', '_'))
            except Exception as e:
                pass
                # print(url)
            # print(url)
                # print(e)
            # print(app_size)
            total_size += app_size
    return count, count-count_null-count_50, count-count_null-count_60, count-count_null-count_70, count-count_null-count_80, count-count_null, total_size
    # print(count)

def mv_other(localfiles, filenames):
    for file_ in localfiles:
        if file_ not in filenames:
            print(file_)


if __name__ == '__main__':
    # url = 'https://download.apkpure.com/b/APK/Y29tLm1ha2l5YWoud2l0aF9sdW5hXzJfZjBmZWRmZTA?_fn=2KrYudmE2YrZhSDYp9mE2YXZg9mK2KfYrCDYqNin2YTYrti32YjYp9iqINio2K_ZiNmGINmG2KrigI5fdjcuMy4zX2Fwa3B1cmUuY29tLmFwaw&as=90aa08e5bb6cb875241306dabf95be6a5fd24d8a&ai=1024204038&at=1607617810&_sa=ai%2Cat&k=3888727441b7a094836b8cefc77b54e45fd4f012&_p=Y29tLm1ha2l5YWoud2l0aF9sdW5h&c=1%7CBEAUTY%7CZGV2PUx1bmElMjBBcHAmdD1hcGsmcz0yODUwMDkyJnZuPTcuMy4zJnZjPTI'
    # localfile = 'test1.apk'
    # download_apk(url, localfile)
    # url = 'https://download.apkpure.com/b/APK/Y29tLm1ha2l5YWoud2l0aF9sdW5hXzJfZjBmZWRmZTA?_fn=2KrYudmE2YrZhSDYp9mE2YXZg9mK2KfYrCDYqNin2YTYrti32YjYp9iqINio2K_ZiNmGINmG2KrigI5fdjcuMy4zX2Fwa3B1cmUuY29tLmFwaw&as=90aa08e5bb6cb875241306dabf95be6a5fd24d8a&ai=1024204038&at=1607617810&_sa=ai%2Cat&k=3888727441b7a094836b8cefc77b54e45fd4f012&_p=Y29tLm1ha2l5YWoud2l0aF9sdW5h&c=1%7CBEAUTY%7CZGV2PUx1bmElMjBBcHAmdD1hcGsmcz0yODUwMDkyJnZuPTcuMy4zJnZjPTI'
    # url = "https://download.apkpure.com/b/APK/Y29tLmNhbnZhLmVkaXRvcl8xMjU4NV85OWJiOTU0Ng?_fn=Q2FudmEgR3JhcGhpYyBEZXNpZ24gVmlkZW8gQ29sbGFnZSBMb2dvIE1ha2VyX3YyLjkxLjBfYXBrcHVyZS5jb20uYXBr&as=60c01c3dd655ec623bee6e574dc8a0bb5fd6eaa7&ai=1997563438&at=1607920175&_sa=ai%2Cat&k=df07cfe996221960e01486f68f4c63295fd98d2f&_p=Y29tLmNhbnZhLmVkaXRvcg&c=1%7CART_AND_DESIGN%7CZGV2PUNhbnZhJnQ9YXBrJnM9MzAzMzQ4NDMmdm49Mi45MS4wJnZjPTEyNTg1"
    # localfile = 'test2.apk'
    # download_apk(url, localfile)



    files= os.listdir(root + 'compare/download/APK_Downloader-master/pages/')
    count, count_50, count_60, count_70, count_80, count_null, total_size = 0.0,0.0,0.0,0.0,0.0,0.0,0.0
    for file in files:
        if not file.endswith('.csv'):
            continue
        # print(file)
        # if not file == 'AppMetadata_' + type+'.csv':
        #     continue
        count_, count_50_, count_60_, count_70_, count_80_, count_null_, total_size_ = parse_csv(root + 'compare/download/APK_Downloader-master/pages/' + file)
        print(file + ', ',count_, count_50_, count_60_, count_70_, count_80_, count_null_, total_size_)
        count += count_
        count_50 += count_50_
        count_60 += count_60_
        count_70 += count_70_
        count_80 += count_80_
        count_null += count_null_
        total_size += total_size_

    print(', ', count, count_50, count_60, count_70, count_80, count_null, total_size)
    # print(parse_csv(root + 'compare/download/APK_Downloader-master/pages/AppMetadata_art_and_design.csv'))