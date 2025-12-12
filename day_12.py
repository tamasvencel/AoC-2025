def help_elves_with_the_presents():
    shapes = {}
    regions = []
    
    current_id = None
    current_rows = []

    def finish_shape():
        if current_id is not None:
            coords = []
            for r, row in enumerate(current_rows):
                for c, char in enumerate(row):
                    if char == '#': coords.append((r, c))
            if coords:
                min_r, min_c = min(r for r,c in coords), min(c for r,c in coords)
                shapes[current_id] = [(r-min_r, c-min_c) for r,c in coords]

    try:
        with open("inputs/presents_input.txt") as f:
            for line in f:
                line = line.strip()
                if not line: continue
                if ':' in line:
                    head, rest = line.split(':', 1)
                    if 'x' in head: # Region
                        finish_shape()
                        current_id = None
                        current_rows = []
                        w, h = map(int, head.split('x'))
                        counts = list(map(int, rest.split()))
                        regions.append((w, h, counts))
                    else: # Shape
                        finish_shape()
                        current_id = int(head)
                        current_rows = []
                else:
                    current_rows.append(line)
        finish_shape()
    except FileNotFoundError:
        return

    # Precompute Variations
    variations = {}
    shape_areas = {}
    for sid, coords in shapes.items():
        shape_areas[sid] = len(coords)
        vars_set = set()
        curr = coords
        for _ in range(2): # Flip
            for _ in range(4): # Rotate
                if curr:
                    mr, mc = min(r for r,c in curr), min(c for r,c in curr)
                    vars_set.add(tuple(sorted((r-mr, c-mc) for r,c in curr)))
                curr = [(c, -r) for r,c in curr]
            curr = [(r, -c) for r,c in coords]
        variations[sid] = sorted([list(v) for v in vars_set])

    def solve_region(W, H, counts):
        total_area = sum(shape_areas[i] * c for i, c in enumerate(counts))
        initial_slack = (W * H) - total_area
        if initial_slack < 0: return False

        grid = [False] * (W * H)
        # Sort shapes largest to smallest for speed
        priority = sorted([i for i, c in enumerate(counts) if c > 0], 
                          key=lambda x: shape_areas[x], reverse=True)

        # Helper to find next empty cell
        def find_empty(start):
            for i in range(start, W * H):
                if not grid[i]: return i
            return None

        # Generator for moves at a specific index
        def get_moves(idx, current_slack):
            r, c = divmod(idx, W)
            # Try placing shapes
            for sid in priority:
                if counts[sid] > 0:
                    for var in variations[sid]:
                        indices = []
                        fits = True
                        for dr, dc in var:
                            nr, nc = r + dr, c + dc
                            nidx = nr * W + nc
                            if 0 <= nr < H and 0 <= nc < W and not grid[nidx]:
                                indices.append(nidx)
                            else:
                                fits = False; break
                        if fits:
                            yield ('place', sid, indices)
            # Try skipping (using slack)
            if current_slack > 0:
                yield ('skip', idx, [])

        start_idx = find_empty(0)
        if start_idx is None: return True

        stack = []
        stack.append([start_idx, get_moves(start_idx, initial_slack), None])
        
        current_slack = initial_slack

        while stack:
            state = stack[-1]
            idx, gen, last_move = state

            # Undo previous move if we are backtracking within this node
            if last_move:
                mtype, sid, indices = last_move
                if mtype == 'place':
                    counts[sid] += 1
                    for i in indices: grid[i] = False
                else: # skip
                    current_slack += 1
                    grid[idx] = False
                state[2] = None # Clear last move

            # Get next move
            try:
                move = next(gen)
                mtype, sid, indices = move
                
                # Apply move
                if mtype == 'place':
                    counts[sid] -= 1
                    for i in indices: grid[i] = True
                else: # skip
                    current_slack -= 1
                    grid[idx] = True
                
                state[2] = move # Record for undo

                # Prepare next level
                next_idx = find_empty(idx + 1)
                if next_idx is None:
                    return True
                
                stack.append([next_idx, get_moves(next_idx, current_slack), None])

            except StopIteration:
                stack.pop() # Backtrack

        return False

    # Main Loop
    valid_count = 0
    for W, H, counts in regions:
        if solve_region(W, H, counts):
            valid_count += 1
    print(valid_count)

if __name__ == "__main__":
    help_elves_with_the_presents()
