import re
from itertools import combinations
from functools import reduce
from operator import xor
from fractions import Fraction
import itertools
import math


def get_button_presses_part1():
    machines = []
    
    with open("inputs/machines.txt") as f:
        for line in f:
            line = line.strip()

            # Parse target diagram [] to a bitmask integer
            diag_str = line.split("]")[0].strip("[")
            target = sum(1 << i for i, char in enumerate(diag_str) if char == '#')

            # Parse buttons () to a list of bitmask integers
            buttons = []
            for parts in re.findall(r'\(([\d,]+)\)', line):
                btn_mask = sum(1 << int(x) for x in parts.split(','))
                buttons.append(btn_mask)
            
            machines.append((target, buttons))

    # Solve for minimum presses
    total_presses = 0
    
    for target, buttons in machines:
        found = False
        # Try combinations of length 0, then 1, then 2, etc.
        for r in range(len(buttons) + 1):
            for combo in combinations(buttons, r):
                # Check if XORing all buttons in this combination equals the target
                if reduce(xor, combo, 0) == target:
                    total_presses += r
                    found = True
                    break
            if found: break

    print(total_presses)

def get_button_presses_part2():
    total_presses = 0
    
    with open("inputs/machines.txt") as f:
        content = f.read().strip()
        
    for line in content.split('\n'):
        line = line.strip()
        if not line: continue
        
        # Parse targets {}
        m_t = re.search(r'\{([\d,]+)\}', line)
        if not m_t: continue
        targets = list(map(int, m_t.group(1).split(',')))
        
        # Parse buttons ()
        buttons = []
        for grp in re.findall(r'\(([\d,]+)\)', line):
            buttons.append(list(map(int, grp.split(','))))
            
        num_vars = len(buttons)
        num_eqs = len(targets)
        
        # Build Matrix A and Vector b for Ax = b
        # A is num_eqs x num_vars
        A = [[Fraction(0) for _ in range(num_vars)] for _ in range(num_eqs)]
        b = [Fraction(t) for t in targets]
        
        for j, affected_rows in enumerate(buttons):
            for r in affected_rows:
                if r < num_eqs:
                    A[r][j] = Fraction(1)
                    
        # Gaussian Elimination to Row Reduced Echelon Form (RREF)
        pivot_row = 0
        pivots = {}
        
        for col in range(num_vars):
            if pivot_row >= num_eqs: break
            
            # Find a row with a non-zero value in this column
            sel = -1
            for r in range(pivot_row, num_eqs):
                if A[r][col] != 0:
                    sel = r
                    break
            
            if sel == -1: continue
                
            # Swap rows to bring pivot to top
            A[pivot_row], A[sel] = A[sel], A[pivot_row]
            b[pivot_row], b[sel] = b[sel], b[pivot_row]
            
            # Normalize the pivot row so the pivot is 1
            coeff = A[pivot_row][col]
            for j in range(col, num_vars):
                A[pivot_row][j] /= coeff
            b[pivot_row] /= coeff
            
            # Eliminate this column from all other rows
            for r in range(num_eqs):
                if r != pivot_row and A[r][col] != 0:
                    factor = A[r][col]
                    for j in range(col, num_vars):
                        A[r][j] -= factor * A[pivot_row][j]
                    b[r] -= factor * b[pivot_row]
            
            pivots[pivot_row] = col
            pivot_row += 1
            
        # Check for inconsistency
        possible = True
        for r in range(pivot_row, num_eqs):
            if b[r] != 0:
                possible = False
                break
        if not possible: continue
            
        # Identify Free Variables
        pivot_col_indices = set(pivots.values())
        free_vars = [j for j in range(num_vars) if j not in pivot_col_indices]
        
        # Determine bounds for free variables to limit search
        # A button press cannot exceed the smallest target it contributes to.
        bounds = []
        for fv in free_vars:
            relevant_targets = [targets[r] for r in buttons[fv]]
            if relevant_targets:
                bounds.append(min(relevant_targets))
            else:
                bounds.append(0)
        
        # Iterate over free variables to find minimum integer solution
        min_presses = math.inf
        
        # Create ranges for each free variable (0 to bound)
        ranges = [range(limit + 1) for limit in bounds]
        
        for free_vals in itertools.product(*ranges):
            current_presses = sum(free_vals)
            if current_presses >= min_presses: continue 
            
            # Map free variable index to its current test value
            fv_map = dict(zip(free_vars, free_vals))
            
            valid_solution = True
            
            # Calculate implied values for pivot variables
            for r, p_col in pivots.items():
                val = b[r]
                for fv in free_vars:
                    if A[r][fv] != 0:
                        val -= A[r][fv] * fv_map[fv]
                
                # Check if result is a non-negative integer
                if val.denominator != 1 or val < 0:
                    valid_solution = False
                    break
                
                current_presses += int(val)
            
            if valid_solution:
                if current_presses < min_presses:
                    min_presses = current_presses
                    
        if min_presses != math.inf:
            total_presses += min_presses
            
    print(total_presses)
    
if __name__ == "__main__":
    # get_button_presses_part1()
    get_button_presses_part2()
