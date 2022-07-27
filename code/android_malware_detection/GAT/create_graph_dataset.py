# coding=utf-8
import sys
import os
import json
import xml.etree.ElementTree as etree
sys.path.append('..')
from lsi.read_data import read_filetype_old_name


def create_graph_files(filelist_file, graph_file_root, feature_file_root, output_dir, lsi_feature_file, permission_feature_path=None, type='cscg', apktool_root_path='', add_root=False):
    # Apkpure/white/5e2beee72de1af8ecf5cf22601e1b726.f375dbeedc.apk,w,0.012745213820698629 0.002463943715770459 0.053720064433362594 -0.001707193351063209 -6.103961830920841e-08 0.13562954224123752 0.0016093567340785067 0.25120926185761616 0.012069216343403731 0.13616835251437856 0.3180640909297506 -0.22413213369911372 -0.008641532507734426 -0.08803142823344158 -0.004381755768714512 -0.13613062419927655 -0.12093513341585356 -0.0903695824794753 -0.04564347198082325 0.3547261433577103 -0.14847641153295377 0.0713064106976861 -0.03240783300007409 -0.00882636771814956 -0.03389707521685319 -0.0009992846208018067 -0.022152292689704308 0.04000143130369042 0.0903469098683583 -0.029552770176404626 -0.010727752441412438 0.020352004058020876 -0.02589169682242437 -0.032357038915282486 -0.0351705066075607 -0.03266624219058941 0.04573479795574832 0.002705257600844544 -0.03988800635019643 -0.016181984706257285 -0.0017833639335224063 0.001254558848405364 -0.005858682587590381 -0.0067472128488476665 0.005440717096011697 0.013477449928392863 0.002034714641464827 -0.05321210995815617 0.0005667513438813628 0.004802209694475803 -0.005391543093898378 -0.006033495777988849 0.001278872608592974 -0.005063460001278285 -0.002210718778597749 0.0016530050108672575 -0.0187211418835286 0.006284213082936371 -0.020412500150045098 0.005029648992175583 -0.00546007162910042 0.002599335999862479 0.001916628030270298 0.0045369028615850435 -0.002180796474925652 0.0011132087258353914 -4.950147226592164e-05 -0.0006526719731261912 -0.010350116857207114 -0.001906744104338658 0.002316563792331382 0.00669446978879208 0.002998970165552093 -0.01846198473633788 0.0016558497719760948 0.020415170666915082 0.0048720313865491145 0.0035123269831606385 -0.019646028918307554 -0.00460572443888679 0.0025910697038355255 0.015564363707776589 0.006747131015533965 0.0048327652559700925 -0.015010764779891736 0.0018602832446136287 -0.005506658039792749 0.028036116275883486 0.004549346799925092 0.01721776236334142 -0.012580059488260315 -0.005261260522017831 0.0017182824416286093 0.003698934082717338 -0.011985941560040004 -0.012276903575338095 -0.005125916782988294 0.003853241135448453 0.0059677
    index = 0
    count_nodes = 0
    graph_A = []
    graph_indicator = []
    node_attributes = []
    graph_labels = []
    node_labels = []

    filelist, atype = read_filetype_old_name(filelist_file)
    out_file_prefix = filelist_file.split('/')[-1][:-7]

    if not os.path.exists(output_dir):
        os.system('mkdir -p ' + output_dir)


    # 全局的lsi特征，作为根节点
    lsi_features = load_root_feature(lsi_feature_file)

    # permission_feature_path不为空，则表示要生成graph_attributes文件
    if not permission_feature_path is None:
        permission_features = []
        print('Start transform permission features: ' + filelist_file)
        count = 0
        for filename in filelist:
            fi = open(permission_feature_path + filename + '.permission', 'r')
            permission_feature = fi.readline().strip().replace(' ', ', ')
            permission_features.append(permission_feature)
            fi.close()
            count += 1
            if count % 100 == 0:
                print('Already read permission files count: ' + str(count))
        fo = open(output_dir + out_file_prefix + '_graph_attributes.txt', 'w+')
        for permission_feature in permission_features:
            fo.write(permission_feature + '\n')
        fo.close()

    # 保存边信息A
    fo_A = open(output_dir + out_file_prefix + '_A.txt', 'w+')
    # # 保存节点归属关系indicator
    # fo_graph_indicator = open(output_dir + out_file_prefix + '_graph_indicator.txt', 'w+')
    # # 保存图的标签
    # fo_graph_labels = open(output_dir + out_file_prefix + '_graph_labels.txt', 'w+')
    # 保存节点的特征
    fo_node_attributes = open(output_dir + out_file_prefix + '_node_attributes.txt', 'w+')

    for i in range(len(filelist)):
        filename = filelist[i]
        # if filename != 'Apkpure/white/66c86d020ed958cafa8477c649267abb.466c228a5b.apk':
        #     continue
        if atype[i] == 'w':
            graph_labels.append(-1)
        else:
            graph_labels.append(1)
        # 传入时候去掉filename末尾的.apk
        lsi_feature = lsi_features[filename]
        node_count, node_names, edge_list, node_feature = load_graph_and_feature(graph_file_root, feature_file_root, filename[:-4], lsi_feature, type, add_root=add_root)
        for i in range(node_count):
            node_name = node_names[i]
            # mainDir zhongde class zhiwei 1, fouze wei 0
            mainDir = extractMainDir(apktool_root_path, filename)
            # print(node_names)
            if node_name.startswith(mainDir):
                node_labels.append(1)
            else:
                node_labels.append(0)
            graph_indicator.append(index)
            node_attribute_line = str(node_feature[node_name])[1:-1] + '\n'
            fo_node_attributes.write(node_attribute_line)
            # node_attributes.append(node_feature[node_name])
        for edge in edge_list:
            node0 = edge[0]
            node1 = edge[1]
            edge_line = str(count_nodes + node0) + ', ' + str(count_nodes + node1) + '\n'
            fo_A.write(edge_line)
            # graph_A.append((count_nodes + node0, count_nodes + node1))
        index += 1
        count_nodes += node_count

        print('read file done: ' + filename + ', graph_labels count: ' + str(len(graph_labels)) + ', total: ' + str(len(filelist)) + ', total nodes: ' + str(count_nodes) + ', total edges: ' + str(len(graph_A)))
        # raise Exception

    fo_A.close()
    fo_node_attributes.close()

    # # 保存边信息A
    # fo = open(output_dir + out_file_prefix + '_A.txt', 'w+')
    # for edge in graph_A:
    #     line = str(edge[0]) + ', ' + str(edge[1]) + '\n'
    #     fo.write(line)
    # fo.close()

    # 保存节点归属关系indicator
    fo = open(output_dir + out_file_prefix + '_graph_indicator.txt', 'w+')
    for indicator in graph_indicator:
        line = str(indicator) + '\n'
        fo.write(line)
    fo.close()

    # 保存图的标签
    fo = open(output_dir + out_file_prefix + '_graph_labels.txt', 'w+')
    for label in graph_labels:
        line = str(label) + '\n'
        fo.write(line)
    fo.close()

    # # 保存节点的特征
    # fo = open(output_dir + out_file_prefix + '_node_attributes.txt', 'w+')
    # for node_attribute in node_attributes:
    #     # 去掉转成str后的[和]
    #     line = str(node_attribute)[1:-1] + '\n'
    #     fo.write(line)
    # fo.close()

    if type == 'cscg':
        # 保存节点的biaoqian
        fo = open(output_dir + out_file_prefix + '_node_labels.txt', 'w+')
        for node_label in node_labels:
            line = str(node_label) + '\n'
            fo.write(line)
        fo.close()


# 读取每个graph根节点的特征值，即apk文件整体的lsi特征，存在model/lsi/<dataset>/lsi_result(_test).txt里
def load_root_feature(feature_file):
    feature = {}
    fi = open(feature_file)
    while True:
        lines = fi.readlines(10000)
        if not lines:
            break
        for line in lines:
            parts = line.strip().split(',')
            feature[parts[0]] = [float(tk) for tk in parts[2].split(' ')]
    return feature

def load_graph_and_feature(graph_file_root, feature_file_root, filename, lsi_feature, type='cscg', add_root=False):
    # print(lsi_feature)
    # print(feature_file_root)
    index = 0
    node_list = []
    edge_list = []
    node_feature = {}

    _filename = filename.split('/')[-1]
    if type == 'cscg':
        graph_file = graph_file_root + filename.replace(_filename, 'filter-cscg-' + _filename)
        # print(filename, graph_file)
        # raise Exception
    else:
        print('Only support cscg, not include ' + type + '!')
    feature_file = feature_file_root + _filename + feature_type(type)
    # print(feature_file)
    # raise Exception

    # 没有graph文件，则返回单节点
    if not os.path.exists(graph_file) or not os.path.exists(feature_file):
        dimension = get_feature_dimension(feature_file_root, type)
        print(feature_file)
        print('Feature dimension: ' + str(dimension))
        node_list.append('0')
        node_feature[0] = [0.0 for i in range(dimension)]
        index += 1
    else:
        print(graph_file)
        texts = load_graph(graph_file)
        node_feature = load_feature(feature_file)
        root_key = '!!!root'
        if add_root:
            node_feature[root_key] = lsi_feature
            node_list, index, status = append_node_list(node_list, index, root_key)
            # TODO
            root_values = set()
            for key in node_feature:
                root_values.add(key)
            root_values.remove(root_key)

        for key in texts:
            if key not in node_list:
                node_list, index, status = append_node_list(node_list, index, key)
                if status == False:
                    continue
                # if key in root_values:
                #     root_values.remove(key)
                # print(texts[key])
            for node in texts[key]:
                if add_root:
                    if node in root_values:
                        root_values.remove(node)
                if node not in node_list:
                    node_list, index, status = append_node_list(node_list, index, node)
                else:
                    status = True
                if key != node and status == True:
                    edge_list.append((node_list.index(key), node_list.index(node)))
        for key in node_feature:
            if key not in node_list:
                # print(key)
                node_list, index, status = append_node_list(node_list, index, key)
                if status == False:
                    continue
        if add_root:
            for value in root_values:
                edge_list.append((node_list.index(root_key), node_list.index(value)))
            print('no father node: ', len(root_values))
    return index, node_list, edge_list, node_feature


# 将key添加到node_list中，返回添加后的node_list, index，以及状态为True；
# 限制node_list的上限为max，index超过max则不添加，并返回状态为False
def append_node_list(node_list, index, key, max=2001):
    if index < max:
        node_list.append(key)
        index += 1
        return node_list, index, True
    else:
        # raise Exception
        return node_list, index, False




def get_feature_dimension(feature_file_root, type):
    files = os.listdir(feature_file_root)
    for _file in files:
        if _file.endswith(feature_type(type)):
            feature_dict = load_feature(feature_file_root + _file)
            if not feature_dict == {}:
                key = list(feature_dict.keys())[0]
                return len(feature_dict[key])


def feature_type(type):
    if type == 'cscg':
        feature_file = '.lsiClassSet'
    else:
        feature_file = '.lsiJava'
    return feature_file


def load_graph(graph_file):
    fi = open(graph_file, 'r')
    line = fi.readline().strip()
    fi.close()
    texts = json.loads(line)
    return texts


def load_feature(feature_file):
    fi = open(feature_file, 'r')
    feature_dict = {}
    for line in fi.readlines():
        _line = line.strip()
        feature_string = _line.split(',')[-1]
        features = feature_string.split(' ')
        key = _line[:-(len(feature_string) + 1)]
        feature_dict[key] = [float(i) for i in features]
    return feature_dict


def extractMainDir(apktool_root_path, filename):
    manifest_file = apktool_root_path + 'manifest/' + filename + '/AndroidManifest.xml'
    package = ''
    if os.path.exists(manifest_file):
        try:
            tree = etree.ElementTree(file=manifest_file)
            root = tree.getroot()
            package = root.attrib['package']
        except Exception as e:
            print("Error occurred: " + manifest_file + '\t' + e)
    else:
        print('No such file: ' + manifest_file)
    mainDir = package
    return mainDir
