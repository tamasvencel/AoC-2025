def get_num_of_accessible_rolls_of_paper():
    matrix = []    
    with open("inputs/paper_roll_locations_diagram.txt") as f:
        for line in f:
            line = line.strip()
            row = []
            row.append(".")

            for i in range(len(line)):
                row.append(line[i])
                
            row.append(".")
            matrix.append(row)
                
    matrix_row_count = len(matrix)
    matrix_col_count = len(matrix[0])
    
    padding_row = ["."] * matrix_col_count
    
    matrix.insert(0, padding_row)
    matrix.append(padding_row)
        
    matrix_row_count = len(matrix)
    matrix_col_count = len(matrix[0])
    
    accessable_paper_rolls = 0
        
    dirs = [
    (-1, -1), (-1, 0), (-1, 1),
    ( 0, -1),          ( 0, 1),
    ( 1, -1), ( 1, 0), ( 1, 1),
    ]
    
    for i in range(1, matrix_row_count-1):
        for j in range(1, matrix_col_count-1):
            adjacent_rolls_count = 0
            
            if matrix[i][j] == "@":
                for di, dj in dirs:
                    if matrix[i + di][j + dj] == "@":
                        adjacent_rolls_count += 1
                        
                if adjacent_rolls_count < 4:
                    accessable_paper_rolls += 1
    
    print(accessable_paper_rolls)
    
def get_num_of_removable_rolls_of_papers():
    matrix = []    
    with open("inputs/paper_roll_locations_diagram.txt") as f:
        for line in f:
            line = line.strip()
            row = []
            row.append(".")

            for i in range(len(line)):
                row.append(line[i])
                
            row.append(".")
            matrix.append(row)
                
    matrix_row_count = len(matrix)
    matrix_col_count = len(matrix[0])
    
    padding_row = ["."] * matrix_col_count
    
    matrix.insert(0, padding_row)
    matrix.append(padding_row)
        
    matrix_row_count = len(matrix)
    matrix_col_count = len(matrix[0])
            
    dirs = [
    (-1, -1), (-1, 0), (-1, 1),
    ( 0, -1),          ( 0, 1),
    ( 1, -1), ( 1, 0), ( 1, 1),
    ]
    
    number_of_removable_rolls_of_paper = 0
    
    while True:
        accessable_paper_rolls = 0
        for i in range(1, matrix_row_count-1):
            for j in range(1, matrix_col_count-1):
                adjacent_rolls_count = 0
                
                if matrix[i][j] == "@":
                    for di, dj in dirs:
                        if matrix[i + di][j + dj] == "@":
                            adjacent_rolls_count += 1
                            
                    if adjacent_rolls_count < 4:
                        accessable_paper_rolls += 1
                        matrix[i][j] = "x"
                        number_of_removable_rolls_of_paper += 1
                        
        if accessable_paper_rolls == 0:
            break
    
    print(number_of_removable_rolls_of_paper)

if __name__ == "__main__":
    # get_num_of_accessible_rolls_of_paper()
    get_num_of_removable_rolls_of_papers()