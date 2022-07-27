# -*- coding: utf-8 -*-
import os
import sys
from multiprocessing import Pool


def extractPermission(manifestDirPath, permissionExtractResDirPath):
    #提取permission列表
    permissionList = []
    permissionFile = open('Permission/permission.txt', 'r')
    lines = permissionFile.readlines()
    for line in lines:
        permissionList.append(line.strip('\n'))
    permissionFile.close()

    # p = Pool(processes=processNum)

    apkOutList = os.listdir(manifestDirPath)
    for apkOut in apkOutList:
        apkName = apkOut
        # p.apply_async(featureExtract, [permissionList, manifestDirPath + '/' + apkOut + '/AndroidManifest.xml', permissionExtractResDirPath + '/' + apkName + '.permission', ])
        featureExtract(permissionList, manifestDirPath + '/' + apkOut + '/AndroidManifest.xml',
                         permissionExtractResDirPath + '/' + apkName + '.permission')

    # p.close()
    # p.join()


def read_src_to_string(filePath):
    if not os.path.isfile(filePath):
        raise TypeError(filePath + " does not exist")

    all_the_text = open(filePath).read()
    return all_the_text


def featureExtract(permissionList, srcFilePath, resFilePath):
    features = {}
    resFile = open(resFilePath, 'w')
    try:
        source_code = str(read_src_to_string(srcFilePath))

        for permission in permissionList:
            features[permission] = source_code.count(permission)


    except Exception as e:
        print ("Error"+str(e)+" in file "+srcFilePath)

        default_val = -1
        for permission in permissionList:
            features[permission] = default_val

    for permission in permissionList:
        resFile.write(str(features[permission]) + ' ')
    resFile.close()


if __name__ == '__main__':
    # processControl(1, '/data2/android_malware_detection/apk_tool/AndroZoo/white/manifest/',
    #                   # '/audr/syc_disk/syc/AndroZoo_white/Androzoo_white_4_manifest',
    #                '/data2/android_malware_detection/features/AndroZoo/white/')
    extractPermission(1, '/home/alvin/Desktop/test1/', '/home/alvin/Desktop/')