import queue

def remove_unneeded_edges(graph):
    visited = set()
    removable_edges = []
    visited_edges = set()

    queue_nodes = queue.Queue(len(graph))
    queue_nodes.put(next(iter(graph)))
    visited.add(next(iter(graph)))

    while not queue_nodes.empty():
        node = queue_nodes.get()
        for neighbor in graph[node]:
            edge = tuple(sorted((node, neighbor)))
            if neighbor not in visited:
                visited.add(neighbor)
                queue_nodes.put(neighbor)
                visited_edges.add(edge)
            elif edge not in visited_edges:
                removable_edges.append(edge)
                visited_edges.add(edge)
    return removable_edges

if __name__ == '__main__':

    graph = {
        'A': ['B', 'C'],
        'B': ['A', 'D', 'E'],
        'C': ['A', 'F', 'G'],
        'D': ['B', 'H'],
        'E': ['B', 'G', 'I'],
        'F': ['C', 'J'],
        'G': ['E', 'C', 'J'],
        'H': ['D'],
        'I': ['E', 'J'],
        'J': ['I', 'G', 'F']
    }

    unneeded_edges = remove_unneeded_edges(graph)
    print("Edges that can be removed:", unneeded_edges)

