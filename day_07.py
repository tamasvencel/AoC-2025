from collections import Counter

def get_number_of_beam_splits():
    tachyon_manifold_diagram = []
    with open("inputs/tachyon_manifold_diagram.txt") as f:
        for line in f:
            line = line.rstrip("\n")
            row = list(line)
            tachyon_manifold_diagram.append(row)
                
    start_col = None
    for i in range(len(tachyon_manifold_diagram)):
        for j in range(len(tachyon_manifold_diagram[0])):
            if tachyon_manifold_diagram[i][j] == "S":
                start_row = i
                start_col = j
                break
            
        if start_col is not None:
            break
        
    active = {start_col}
    splits = 0
    
    for i in range(start_row + 1, len(tachyon_manifold_diagram)):
        next_active = set()
        for c in active:
            cell = tachyon_manifold_diagram[i][c]
            if cell == "^":
                splits += 1
                if c - 1 >= 0:
                    next_active.add(c-1)
                if c + 1 < len(tachyon_manifold_diagram[0]):
                    next_active.add(c+1)
            else:
                next_active.add(c)
        active = next_active
                
    print(splits)
            
            
        

def get_number_of_timelines_for_a_single_tachyon_particle():
    tachyon_manifold_diagram = []
    with open("inputs/tachyon_manifold_diagram.txt") as f:
        for line in f:
            line = line.rstrip("\n")
            row = list(line)
            tachyon_manifold_diagram.append(row)
                
    start_col = None
    for i in range(len(tachyon_manifold_diagram)):
        for j in range(len(tachyon_manifold_diagram[0])):
            if tachyon_manifold_diagram[i][j] == "S":
                start_row = i
                start_col = j
                break
            
        if start_col is not None:
            break
        
    active = Counter({start_col: 1})
    
    for i in range(start_row + 1, len(tachyon_manifold_diagram)):
        next_active = Counter()
        for c, ways in active.items():
            cell = tachyon_manifold_diagram[i][c]
            if cell == "^":
                if c - 1 >= 0:
                    next_active[c-1] += ways
                if c + 1 < len(tachyon_manifold_diagram[0]):
                    next_active[c+1] += ways
            else:
                next_active[c] += ways
        active = next_active
                
    print(sum(active.values()))

if __name__ == "__main__":
    # get_number_of_beam_splits()
    get_number_of_timelines_for_a_single_tachyon_particle()
