def find_all_different_paths_part1():
    with open("inputs/devices_and_outputs.txt") as f:
        data = f.read().strip()
        
    graph = {}
    for line in data.splitlines():
        parts = line.replace(":", "").split()
        graph[parts[0]] = parts[1:]
        
    count = 0
    stack = ["you"]
    
    while stack:
        node = stack.pop()
        
        if node == "out":
            count += 1
        else:
            stack.extend(graph.get(node, []))
            
    print(count)
        

def find_all_different_paths_part2():
    with open("inputs/devices_and_outputs.txt") as f:
        data = f.read().strip()

    graph = {}
    for line in data.splitlines():
        parts = line.replace(":", "").split()
        graph[parts[0]] = parts[1:]

    # Calculate "In-Degree" (number of incoming cables for each device)
    in_degree = {node: 0 for node in graph}
    # Ensure 'out' and 'svr' are in the dictionary even if they have no connections
    in_degree['out'] = 0 
    in_degree['svr'] = 0
    
    for u in graph:
        for v in graph[u]:
            in_degree[v] = in_degree.get(v, 0) + 1

    # Initialize DP State
    dp = {node: {} for node in in_degree}
    
    dp['svr'][(False, False)] = 1

    # Process nodes (Topological Sort / Kahn's Algorithm)
    queue = [node for node in in_degree if in_degree[node] == 0]

    while queue:
        node = queue.pop(0)
        
        # If this node is unreachable from svr, skip it
        if not dp[node]:
            for neighbor in graph.get(node, []):
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
            continue

        # Push our current path counts to all neighbors
        for neighbor in graph.get(node, []):
            
            # Check if the neighbor is one of the special devices
            is_dac = (neighbor == 'dac')
            is_fft = (neighbor == 'fft')

            for (seen_dac, seen_fft), count in dp[node].items():
                # Update the flags for the neighbor
                new_state = (seen_dac or is_dac, seen_fft or is_fft)
                
                # Add the count to the neighbor's total for that specific state
                dp[neighbor][new_state] = dp[neighbor].get(new_state, 0) + count

            # Decrement neighbor's dependency count
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    result = dp['out'].get((True, True), 0)
    
    print(result)

if __name__ == "__main__":
    # find_all_different_paths_part1()
    find_all_different_paths_part2()
