from prob4 import Edge, Graph, Node
import heapq


def dijkstra(graph, tail, head):
    assert isinstance(graph, Graph)
    assert isinstance(head, Node)
    assert isinstance(tail, Node)

    seen_vertices = [tail]
    dist = {tail: 0}
    while len(seen_vertices) != len(graph) or head not in seen_vertices or head not in dist.keys():

        tmp_len = {}
        for edge in graph.edges:
            if edge.tail not in dist.keys() or edge.head in seen_vertices:
                continue

            # connected edges
            tmp_len[edge] = edge.length + dist[edge.tail]
        if tmp_len:
            min_key = None
            min_len = 1000000
            for edge, length in tmp_len.items():
                if min_len > length:
                    min_key = edge
                    min_len = length

            dist[min_key.head] = min_len
            seen_vertices.append(min_key.head)

        else:
            # nothing
            print()
            return 1000000
    return dist[head]


def main():
    with open('data/prob6_data.txt', 'r') as f:
        lines = f.readlines()

    graph = Graph(directed=True)
    for line in lines:
        tmp = line.split('\n')[0].split('\t')

        tail_id = int(tmp[0])

        for edge_str in tmp[1:]:
            head_id, length = edge_str.split(',')
            graph.add_edge(tail_id, int(head_id), edge_length=int(length))

    test_tail = 1
    test_heads = [7,37,59,82,99,115,133,165,188,197]
    ans = []
    for tail_id, head_id in zip([test_tail] * len(test_heads), test_heads):
        tail = graph.get_node(tail_id)
        head = graph.get_node(head_id)
        ans.append(dijkstra(graph, tail, head))


    print(ans)


if __name__ == '__main__':
    main()