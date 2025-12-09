def get_largest_rectangle_area():
    red_tiles = []
    with open("inputs/red_tile_locations.txt") as f:
        for line in f:
            red_tiles.append(list(map(int, line.strip().split(","))))
    
    largest_area = 0
    for i in range(len(red_tiles)):
        for j in range(i + 1, len(red_tiles)):
            a = abs(red_tiles[i][0] - red_tiles[j][0]) + 1
            b = abs(red_tiles[i][1] - red_tiles[j][1]) + 1
            area = a * b
            if area > largest_area:
                largest_area = a * b
                
    
    print(largest_area)
            
def get_largest_rectangle_area_using_only_red_and_green_tiles():
    red_tiles = []
    with open("inputs/red_tile_locations.txt") as f:
        for line in f:
            red_tiles.append(list(map(int, line.strip().split(","))))

    # Coordinate Compression
    # We only create grid rows/cols for the coordinates that actually exist    
    # Get all unique X and Y coordinates
    raw_xs = set(t[0] for t in red_tiles)
    raw_ys = set(t[1] for t in red_tiles)
    
    # Add border coordinates so we can fill around the shape
    min_x, max_x = min(raw_xs), max(raw_xs)
    min_y, max_y = min(raw_ys), max(raw_ys)
    raw_xs.add(min_x - 1); raw_xs.add(max_x + 1)
    raw_ys.add(min_y - 1); raw_ys.add(max_y + 1)
    
    sorted_xs = sorted(list(raw_xs))
    sorted_ys = sorted(list(raw_ys))
    
    # Calculate the width/height of each compressed column/row
    col_widths = []
    for i in range(len(sorted_xs)):
        col_widths.append(1)
        if i < len(sorted_xs) - 1:
            gap = sorted_xs[i+1] - sorted_xs[i] - 1
            if gap > 0: col_widths.append(gap)

    row_heights = []
    for i in range(len(sorted_ys)):
        row_heights.append(1)
        if i < len(sorted_ys) - 1:
            gap = sorted_ys[i+1] - sorted_ys[i] - 1
            if gap > 0: row_heights.append(gap)

    # Re-map coordinates to account for the inserted "gap" columns/rows    
    x_segments = [] # Stores width of each column
    x_to_idx = {} # Maps real X to column index
    current_idx = 0
    for i in range(len(sorted_xs)):
        x_to_idx[sorted_xs[i]] = current_idx
        x_segments.append(1)
        current_idx += 1
        if i < len(sorted_xs) - 1:
            gap = sorted_xs[i+1] - sorted_xs[i] - 1
            if gap > 0:
                x_segments.append(gap)
                current_idx += 1

    y_segments = []
    y_to_idx = {}
    current_idx = 0
    for i in range(len(sorted_ys)):
        y_to_idx[sorted_ys[i]] = current_idx
        y_segments.append(1)
        current_idx += 1
        if i < len(sorted_ys) - 1:
            gap = sorted_ys[i+1] - sorted_ys[i] - 1
            if gap > 0:
                y_segments.append(gap)
                current_idx += 1

    W = len(x_segments)
    H = len(y_segments)
    
    # Create Grid & Draw Boundary
    # 0 = Empty, 1 = Boundary
    grid = [[0] * W for _ in range(H)]

    num_tiles = len(red_tiles)
    for i in range(num_tiles):
        t1 = red_tiles[i]
        t2 = red_tiles[(i + 1) % num_tiles]
        
        c1, r1 = x_to_idx[t1[0]], y_to_idx[t1[1]]
        c2, r2 = x_to_idx[t2[0]], y_to_idx[t2[1]]
        
        if c1 == c2: # Vertical
            for r in range(min(r1, r2), max(r1, r2) + 1):
                grid[r][c1] = 1
        else: # Horizontal
            for c in range(min(c1, c2), max(c1, c2) + 1):
                grid[r1][c] = 1

    # Iterative Flood Fill
    # Mark Outside as 2 
    # Start at (0,0) which is the top-left border.
    stack = [(0, 0)]
    grid[0][0] = 2
    
    while stack:
        cx, cy = stack.pop()
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < W and 0 <= ny < H:
                if grid[ny][nx] == 0:
                    grid[ny][nx] = 2
                    stack.append((nx, ny))

    # Build Prefix Sum of Areas
    # We calculate the area of valid tiles (Inside=0 or Boundary=1)
    prefix_area = [[0] * W for _ in range(H)]
    
    for r in range(H):
        for c in range(W):
            cell_area = 0
            if grid[r][c] != 2:
                cell_area = x_segments[c] * y_segments[r]
            
            top = prefix_area[r-1][c] if r > 0 else 0
            left = prefix_area[r][c-1] if c > 0 else 0
            top_left = prefix_area[r-1][c-1] if (r > 0 and c > 0) else 0
            
            prefix_area[r][c] = cell_area + top + left - top_left

    # Check Rectangles
    largest_area = 0
    
    for i in range(len(red_tiles)):
        for j in range(i + 1, len(red_tiles)):
            t1 = red_tiles[i]
            t2 = red_tiles[j]
            
            # Calculate Geometric Area
            geo_w = abs(t1[0] - t2[0]) + 1
            geo_h = abs(t1[1] - t2[1]) + 1
            geo_area = geo_w * geo_h
            
            if geo_area <= largest_area:
                continue
            
            # Calculate Valid Area
            c1, r1 = x_to_idx[t1[0]], y_to_idx[t1[1]]
            c2, r2 = x_to_idx[t2[0]], y_to_idx[t2[1]]
            
            c_min, c_max = min(c1, c2), max(c1, c2)
            r_min, r_max = min(r1, r2), max(r1, r2)
            
            valid_area = prefix_area[r_max][c_max]
            if c_min > 0: valid_area -= prefix_area[r_max][c_min - 1]
            if r_min > 0: valid_area -= prefix_area[r_min - 1][c_max]
            if c_min > 0 and r_min > 0: valid_area += prefix_area[r_min - 1][c_min - 1]
            
            if valid_area == geo_area:
                largest_area = geo_area

    print(largest_area)

if __name__ == "__main__":
    # get_largest_rectangle_area()
    get_largest_rectangle_area_using_only_red_and_green_tiles()
