from collections import deque


def topo_sort(graph):
    in_degree = {node: 0 for node in graph}
    for node in graph:
        for neighbour in graph[node]:
            in_degree[neighbour] += 1

    queue = deque([node for node in in_degree if in_degree[node] == 0])

    result = []
    while queue:
        node = queue.popleft()
        result.append(node)
        for neighbour in graph[node]:
            in_degree[neighbour] -= 1
            if in_degree[neighbour] == 0:
                queue.append(neighbour)

    if len(result) != len(graph):
        raise Exception("Graph contains a cycle.")
    return result

