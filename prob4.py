from random import sample


class Edge:
    def __init__(self, head, tail, length=1, directed=False):
        self.head = head
        self.tail = tail
        self.length = length
        self.directed = directed

    def __add__(self, other):
        assert other.tail == self.head
        self.length += other.length
        self.head = other.head

    def __hash__(self):
        return hash(f'{self.head.ids}_{self.tail.ids}_{self.length}')

    def __eq__(self, other):
        return self.head == other.head and \
               self.tail == other.tail and \
               self.length == other.length and \
               self.directed == other.directed

    def __str__(self):
        return f'Edge {self.tail.ids} -> {self.head.ids}'

    def __le__(self, other):
        return self.length <= other.length

    def __ge__(self, other):
        return self.length >= other.length

    def __lt__(self, other):
        return self.length < other.length

    def __gt__(self, other):
        return self.length > other.length

    def __ne__(self, other):
        return self.length != other.length


class Node:
    def __init__(self, ids):
        self.ids = ids
        self.explored = False
        self.leader = None

    def set_leader(self, obj):
        self.leader = obj

    def __hash__(self):
        return hash(self.ids)

    def __eq__(self, other):
        return self.ids == other.ids

    def __str__(self):
        return f'ID: {self.ids}'

    def __le__(self, other):
        return self.ids <= other.ids

    def __ge__(self, other):
        return self.ids >= other.ids

    def __lt__(self, other):
        return self.ids < other.ids

    def __gt__(self, other):
        return self.ids > other.ids

    def __ne__(self, other):
        return self.ids != other.ids


class Graph:
    def __init__(self, directed=False):
        self._nodes = {}
        self._edges = []
        self._directed = directed

    def add_node(self, node):
        assert isinstance(node, Node)
        self._nodes[node.ids] = node

    def remove_node(self, node):
        assert isinstance(node, Node)
        assert node in self._nodes.values()
        self._nodes.pop(node.ids)

    def node_in_graph(self, node_id):
        return node_id in self._nodes.keys()

    def add_edge(self, node1_id, node2_id, edge_num=1, edge_length=1):
        assert isinstance(node1_id, int)
        assert isinstance(node2_id, int)
        if not self.node_in_graph(node1_id):
            self.add_node(Node(node1_id))
        if not self.node_in_graph(node2_id):
            self.add_node(Node(node2_id))

        node1 = self.get_node(node1_id)
        node2 = self.get_node(node2_id)
        self._edges.extend([Edge(node1, node2, length=edge_length, directed=self._directed)] * edge_num)

    def remove_edge(self, node1, node2, edge_num=1, length=1):
        assert isinstance(node1, int)
        assert isinstance(node2, int)

        node1 = self.get_node(node1)
        node2 = self.get_node(node2)
        if node1 is None or node2 is None:
            return

        for edge in self._edges:
            assert isinstance(edge, Edge)
            if edge.tail == node1 and edge.head == node2 and edge.length == length:
                self._edges.remove(edge)
                edge_num -= 1
            if edge_num == 0:
                break

    @ property
    def node_list(self):
        return list(self._nodes.values())

    def get_node(self, node_id):
        return self._nodes[node_id] if node_id in self._nodes.keys() else None

    @property
    def edges(self):
        return self._edges

    def __str__(self):
        print_str = [str(node) for node in self._nodes]
        return str(print_str)

    def __iter__(self):
        for n in self._nodes.values():
            yield n

    def reverse(self):
        assert self._directed, 'Graph must be directed graph'
        _edges = []
        for i, edge in enumerate(self._edges):
            edge.head, edge.tail = edge.tail, edge.head
            self._edges[i] = edge

        self._edges = _edges

    def __len__(self):
        return len(self._nodes)


def min_cut(graph: Graph) -> int:

    while len(graph) > 2:
        edge = sample(graph.edges, k=1)[0]
        node1, node2 = edge
        if node1.is_linked(node2):
            graph.merge_link(node1.ids, node2.ids)

    return list(graph.node_list[0].link_nodes.values())[0]


def main():
    with open('data/prob4_data.txt', 'r') as f:
        s = f.readlines()

    iter_times = 200
    history = {}
    for _ in range(iter_times):

        graph = Graph()
        for _s in s:
            _s = _s[:-1].split('\t')
            adj_list = [int(__s) for __s in _s]
            if graph.get_node(adj_list[0]) is None:
                tail_node = Node(adj_list[0])
                graph.add_node(tail_node)

            end_node = graph.get_node(adj_list[0])

            for node_id in adj_list[1:]:
                node = graph.get_node(node_id)
                if node is None:
                    graph.add_edge(end_node.ids, node_id)
                else:
                    if not end_node.is_linked(node):
                        graph.add_edge(end_node.ids, node.ids)
        min_cuts = min_cut(graph)
        history[min_cuts] = graph

    min_hist = min(history.keys())
    print(min_hist)
    print(history[min_hist])


if __name__ == '__main__':
    main()