def connect_closest_junction_boxes():
    boxes = []
    with open("inputs/junction_box_positions.txt") as f:
        for line in f:
            boxes.append(list(map(int, line.strip().split(","))))
            
    n = len(boxes)
    
    # Calculate distances between all pairs
    edges = []
    for i in range(n):
        for j in range(i+1, n):
            dist_sq = sum((boxes[i][k] - boxes[j][k])**2 for k in range(3))
            edges.append((dist_sq, i, j))
            
    # Sort by distance and keep only the top 1000 connections
    edges.sort()
    top_edges = edges[:1000]
    
    # Build the graph (adjacency list)
    adj = {i: [] for i in range(n)}
    for _, u, v in top_edges:
        adj[u].append(v)
        adj[v].append(u)
        
    # Find sizes of all circuits (connected components)
    visited = set()
    sizes = []
    
    for i in range(n):
        if i not in visited:
            # Start a search (DFS) for this new circuit
            stack = [i]
            visited.add(i)
            count = 0
            while stack:
                node = stack.pop()
                count += 1
                for neighbor in adj[node]:
                    if neighbor not in visited:
                        visited.add(neighbor)
                        stack.append(neighbor)
            sizes.append(count)
            
    # Multiply the 3 largest sizes
    sizes.sort(reverse=True)
    print(sizes[0] * sizes[1] * sizes[2])
    
def multiply_together_the_x_coordinates_of_the_last_two_connected_junction_boxes():
    boxes = []
    with open("inputs/junction_box_positions.txt") as f:
        for line in f:
            boxes.append(list(map(int, line.strip().split(","))))
            
    n = len(boxes)
    
    # Calculate distances between all pairs
    edges = []
    for i in range(n):
        for j in range(i+1, n):
            dist_sq = sum((boxes[i][k] - boxes[j][k])**2 for k in range(3))
            edges.append((dist_sq, i, j))
            
    # Sort by distance
    edges.sort()
    
    # Track which group each box belongs to
    # Initially, every box is in its own unique group
    groups = list(range(n))
    num_groups = n
    
    for _, u, v in edges:
        group_v = groups[v]
        group_u = groups[u]
        
        # If they are in different groups, connect them
        if group_u != group_v:
            # Merge the two groups: update all boxes in group_u to be in group_v
            for k in range(n):
                if groups[k] == group_u:
                    groups[k] = group_v

            num_groups -= 1
            
            # If only 1 group remains, all of them are connected
            if num_groups == 1:
                print(boxes[u][0] * boxes[v][0])
                return

if __name__ == "__main__":
    # connect_closest_junction_boxes()
    multiply_together_the_x_coordinates_of_the_last_two_connected_junction_boxes()
