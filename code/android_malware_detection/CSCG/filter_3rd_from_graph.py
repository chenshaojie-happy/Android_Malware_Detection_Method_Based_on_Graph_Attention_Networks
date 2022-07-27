# coding=utf-8
import json
import sys
sys.path.append('..')
from lexical_analysis.load_3rd_party import load_3rd_lib_dot
max_nodes = 1000

def filter_3rd_single(java_graph, java_graph_file_filter, _3rd_party_file, token_results, token_file_path, filter_type):
    _3rd_party = load_3rd_lib_dot(_3rd_party_file)
    # 过滤图的节点
    java_graph_filter, nodes = filter_3rd_graph(_3rd_party, java_graph, filter_type)
    print(_3rd_party_file.split('/')[-1][:-3] + ': Before filter: ' + str(len(token_results)) + ', after:' + str(len(nodes)))
    string = json.dumps(java_graph_filter)
    fo = open(java_graph_file_filter, 'w+')
    fo.write(string)
    fo.close()
    # 过滤三方库节点的token
    token_results_filter = filter_3rd_token(nodes, token_results)
    string = json.dumps(token_results_filter)
    fo = open(token_file_path, 'w+')
    fo.write(string)
    fo.close()


def filter_3rd_graph(_3rd_party, java_graph, filter_type):
    java_graph_filter = {}
    nodes = set()
    for key in java_graph:
        if in_3rd(key, _3rd_party):
            continue
        if len(nodes) >= max_nodes and key not in nodes:
            continue
        java_graph_filter[key] = []
        nodes.add(key)
        for value in java_graph[key]:
            if not in_3rd(value, _3rd_party):
                if len(nodes) >= max_nodes and value not in nodes:
                    continue
                java_graph_filter[key].append(value)
                nodes.add(value)
    # 该方法保证若筛选完三方库后节点少于100，则补充至100，总共不足100，则全部补充
    if filter_type == 'max_100':
        # 优先添加三方库中与当前已有nodes有关联的节点
        while True:
            if len(nodes) >= 100:
                break
            # n_nodes = len(nodes)
            new_nodes = set()   # 保存当前轮次新加的节点
            for key in java_graph_filter:
                # 判断已加入的node是否被其他方法调用，若是则添加关联
                for node in new_nodes:
                    if node in java_graph[key]:
                        java_graph_filter[key].append(node)
                # 从java_graph中获取未被纳入的value
                for value in java_graph[key]:
                    if value not in nodes and len(nodes) < 100:
                        nodes.add(value)
                        new_nodes.add(value)
                        java_graph_filter[key].append(value)
            if len(new_nodes) == 0:
                break
        # 仍不足100，则按顺序添加节点和变
        new_nodes = set()
        for key in java_graph:
            if len(nodes) < 100:
                if key not in java_graph_filter:
                    nodes.add(key)
                    new_nodes.add(key)
                    java_graph_filter[key] = []
            else:
                break
            # 判断已加入的node是否被其他方法调用，若是则添加关联
            for node in new_nodes:
                if node in java_graph[key]:
                    java_graph_filter[key].append(node)
            # 寻找与改节点有关联的方法，也加入列表
            for value in java_graph[key]:
                if len(nodes) < 100:
                    if value not in java_graph_filter[key]:
                        java_graph_filter[key].append(value)
                        nodes.add(value)
                        new_nodes.add(value)
                else:
                    break
    return java_graph_filter, nodes


def in_3rd(_class, _3rd_party):
    for __3rd_party in _3rd_party:
        if _class.startswith(__3rd_party):
            return True
    return False


def filter_3rd_token(nodes, token_results):
    token_results_filter = {}
    for key in token_results:
        if key in nodes:
            token_results_filter[key] = token_results[key]
    return token_results_filter

