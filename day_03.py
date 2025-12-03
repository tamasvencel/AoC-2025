def find_total_joltage_part1():
    joltage_ratings = []
    with open("inputs/joltage_ratings.txt") as f:
        for line in f:
            joltage_ratings.append(line.strip())
    
    sum_of_max_joltages = 0
    for joltage_rating in joltage_ratings:
        max_num = 0
        for i in range(len(str(joltage_rating))):
            for j in range(i+1, len(str(joltage_rating))):
                
                if i != j:
                    current_joltage_rating = ""
                    current_joltage_rating += str(joltage_rating[i])
                    current_joltage_rating += str(joltage_rating[j])
                    
                    if int(current_joltage_rating) > max_num:
                        max_num = int(current_joltage_rating)
        
        print(max_num)
        sum_of_max_joltages += max_num
        
    print(sum_of_max_joltages)
    
    
def find_total_joltage_part2():
    joltage_ratings = []
    with open("inputs/joltage_ratings.txt") as f:
        for line in f:
            joltage_ratings.append(line.strip())
                
    sum_of_max_joltages = 0

    for joltage_rating in joltage_ratings:
        joltage_ratings_stack = []
        allowed_num_of_digit_deletions = len(joltage_rating) - 12
        current_num_of_digit_deletions = 0

        joltage_ratings_stack.append(joltage_rating[0])
        for j in range(1, len(str(joltage_rating))):
                while bool(joltage_ratings_stack) and joltage_ratings_stack[-1] < joltage_rating[j]:
                    if current_num_of_digit_deletions < allowed_num_of_digit_deletions:
                        joltage_ratings_stack.pop()
                        current_num_of_digit_deletions += 1
                    else:
                        break
                joltage_ratings_stack.append(joltage_rating[j]) 
                        
        result = joltage_ratings_stack[:12]
        sum_of_max_joltages += int("".join(result))
        
    print(sum_of_max_joltages)
            

if __name__ == "__main__":
    # find_total_joltage_part1()
    find_total_joltage_part2()
