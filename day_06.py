from math import prod

def solve_cephalopod_math_problem_part1():
    problems = []
    with open("inputs/math_worksheet.txt") as f:
        for line in f:
            line = line.strip()
            problems.append(line.split(" "))
            
    problems = [[x for x in row if x != ''] for row in problems]
    
    grand_total = 0
    
    for i in range(len(problems[0])):
        solution = 1
        operator = problems[-1][i]
        for problem in problems[:-1]:
            if operator == "*":
                solution *= int(problem[i])
            if operator == "+":
                solution += int(problem[i])
                
        if operator == "+":
            solution -= 1
            
        grand_total += solution
        
    print(grand_total)
        
def solve_cephalopod_math_problem_part2():
    problems = []
    new_problems = []
    with open("inputs/math_worksheet.txt") as f:
        for line in f:
            line = line.rstrip("\n")
            problems.append(line)
    
    width = max(len(line) for line in problems)
    problems = [line.ljust(width) for line in problems]
    
    grand_total = 0
    
    new_problems = []
    i = 0
    while i < width:
        while i < width and all(row[i] == " " for row in problems):
            i += 1
        if i >= width:
            break
        
        start = i
        while i < width and not all(row[i] == " " for row in problems):
            i += 1
        end = i

        new_problem = []
        for row in problems:
            new_problem.append(row[start:end])
        new_problems.append(new_problem)
    
    for problem in new_problems:
        operator = None
        for ch in problem[-1]:
            if ch in "+*":
                operator = ch
                break
        
        num_digits_of_largest_num = len(problem[0])
        padded_problem = [s.ljust(num_digits_of_largest_num) for s in problem[:-1]]
           
        final_problem = []
        for col in reversed(list(zip(*padded_problem))):
            new_number = ""
            for ch in col:
                if ch.isdigit():
                    new_number += ch
            
            if new_number:
                final_problem.append(int(new_number))
                
        if operator == "*":
            grand_total += prod(final_problem)
        if operator == "+":
            grand_total += sum(final_problem)
            
    print(grand_total)
    

if __name__ == "__main__":
    # solve_cephalopod_math_problem_part1()
    solve_cephalopod_math_problem_part2()
