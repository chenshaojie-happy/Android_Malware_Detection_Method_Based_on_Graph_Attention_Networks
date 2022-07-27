# coding=utf-8
import os
# result_file = open("/home/audr/syc_disk/syc/AndroZoo_white/Androzoo_white_4_filelist.txt",'w+')
# third_filt_result = '/home/audr/syc_disk/syc/AndroZoo_white/Androzoo_white_4_3rd/'
# apktool_result = '/home/audr/syc_disk/syc/AndroZoo_white/Androzoo_white_4_manifest/'
# java_path = '/home/audr/syc_disk/syc/AndroZoo_white/Androzoo_white_4_java/'
import zipfile
def read_old_filelist(filelist_file):
    fi = open(filelist_file, 'r')
    lines_old = []
    filelist = []
    while True:
        lines = fi.readlines(10000)
        if not lines:
            break
        for line in lines:
            lines_old.append(line.strip())
            filelist.append(line.split(' ')[0])

    fi.close()
    return lines_old, filelist

def create_filelist(filelist_file, filelist_filter, _3rd_filter_result, manifest_result, java_path):

    lines_old, filelist = read_old_filelist(filelist_file)
    # print(filelist_file, filelist_filter, _3rd_filter_result, manifest_result, java_path)
    # raise Exception
    fo = open(filelist_filter, 'w+')
    for i in range(len(filelist)):
        filename = filelist[i]
        line_old = lines_old[i]
        _3rd_file = filename[:-4] + '.3rd'
        manifest = manifest_result + filename + '/AndroidManifest.xml'
        source_zip = java_path + filename + '.zip'
        # 确保有manifest文件：
        if not os.path.exists(manifest):
            print(filename + ' not contain manifest!')
            continue
        # 确保有java源码的zip文件
        if not os.path.exists(source_zip):
            print(filename + ' not contain source.zip')
            continue
        # 确保有LiteRadar生成的3rd文件
        if not os.path.exists(source_zip):
            print(filename + ' not contain source.zip')
            continue
        # 确保zip文件里有source文件夹，证明有解析出来的java文件
        z = zipfile.ZipFile(source_zip, 'r')
        found_source = False
        for file_in_zip in z.namelist():
            # if file_in_zip.endswith('/') and file_in_zip == 'src/sources/':
            if file_in_zip.endswith('.java') and file_in_zip.startswith('src/sources/'):
                found_source = True
                break
        if not found_source:
            print(filename + ' not contain src/sources/')
            continue
        print("found file: " + filename)

        fo.write(line_old + '\n')
    fo.close()


# if __name__ == '__main__':
#     create_filelist('/data2/android_malware_detection/dataset/中心黑白/My_white_filelist.txt', \
#                     '/data2/android_malware_detection/3rd/中心黑白/white/',
#                     '/data2/android_malware_detection/apk_tool/中心黑白/white/manifest/',
#                     '/data2/android_malware_detection/java/中心黑白/white/')