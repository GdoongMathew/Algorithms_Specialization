from urllib.request import urlopen
from prob4 import Node, Graph
import sys, threading
sys.setrecursionlimit(1000000)
threading.stack_size(67108864)


def download_scc():
    url = 'https://raw.githubusercontent.com/ppizarro/coursera-stanford-algorithms1/master/programming4/SCC.txt'
    scc = urlopen(url).read()
    print('Start writing to file.')
    with open('data/prob5_data.txt', 'w') as f:
        f.write(bytes.decode(scc, 'utf-8'))


tmp_t = 0
s = None


def get_scc(graph):
    global s
    assert isinstance(graph, Graph)

    f_t = {}

    def dfs(_graph, _node, leader):
        global tmp_t, s
        _node.explored = True
        _node.set_leader(leader)
        for _h_node in _node.links:

            # _node is tail node and head node not yet explored
            if not _h_node.explored:
                dfs(_graph, _h_node, leader)

        tmp_t += 1
        f_t[tmp_t] = _node

    def dfs_loop(_graph, node_labels):
        assert isinstance(_graph, Graph)
        assert isinstance(node_labels, dict)
        global s

        node_labels_ids = sorted(node_labels, reverse=True)

        for iter_ids in node_labels_ids:
            _node = node_labels[iter_ids]
            if not _node.explored:
                dfs(_graph, _node, _node)

    tmp_labels = {_node.ids: _node for _node in graph.node_list}
    graph.reverse()
    dfs_loop(graph, tmp_labels)

    graph.reverse()

    # reset
    for node in graph:
        node.explored = False

    dfs_loop(graph, f_t)

    ans = {}
    for node in graph:
        if node.leader.ids not in ans:
            ans[node.leader.ids] = 0
        ans[node.leader.ids] += 1

    scc_num = sorted(ans.values(), reverse=True)
    i = 0
    for num in scc_num:
        if i < 6:
            for _id, _num in ans.items():
                if _num == num:
                    print(num)
            i += 1
        else:
            break


def main():
    with open('data/prob5_data.txt', 'r') as f:
        data = f.readlines()

    x = Graph(directed=True)

    for line in data:
        if '\n' in line:
            tail_node, head_node = line.split(' \n')[0].split(' ')
        else:
            tail_node, head_node = line.split(' ')[:2]
        x.add_edge(int(tail_node), int(head_node))
    scc = get_scc(x)

    print(scc)


if __name__ == '__main__':

    thread = threading.Thread(target=main)
    thread.start()
    # main()


