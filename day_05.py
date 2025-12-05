def get_fresh_ingredient_ids_part1():
    fresh_ingredient_ranges = []
    ingredient_ids = []
    with open("inputs/ingredient_ids.txt") as f:
        for line in f:
            line = line.strip()
            if len(line.split("-")) == 2:
                fresh_ingredient_ranges.append(line.split("-"))
            else:
                break
            
        for line in f:
            line = line.strip()
            ingredient_ids.append(int(line))
    
    num_of_fresh_ingredients = 0
    
    for ingredient_id in ingredient_ids:
        flag = 0
        for fresh_ingredient_range in fresh_ingredient_ranges:
            if ingredient_id >= int(fresh_ingredient_range[0]) and ingredient_id <= int(fresh_ingredient_range[1]):
                flag = 1

                break
                
        if flag:
            num_of_fresh_ingredients += 1
            
    print(num_of_fresh_ingredients)
        
                
def get_fresh_ingredient_ids_part2():
    fresh_ingredient_ranges = []
    with open("inputs/ingredient_ids.txt") as f:
        for line in f:
            line = line.strip()
            if len(line.split("-")) == 2:
                a_str, b_str = line.split("-")
                fresh_ingredient_ranges.append((int(a_str), int(b_str)))
            else:
                break
            
    fresh_ingredient_ranges.sort()
        
    num_of_fresh_ingredients = 0
    
    current_start, current_end = fresh_ingredient_ranges[0]
    
    for a, b in fresh_ingredient_ranges[1:]:
        if a > current_end + 1:
            num_of_fresh_ingredients += current_end - current_start + 1
            current_start, current_end = a, b
        else:
            current_end = max(current_end, b)
            
    num_of_fresh_ingredients += current_end - current_start + 1
    
    print(num_of_fresh_ingredients)

if __name__ == "__main__":
    # get_fresh_ingredient_ids_part1()
    get_fresh_ingredient_ids_part2()
