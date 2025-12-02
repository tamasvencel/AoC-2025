from collections import Counter

def is_invalid(num: int) -> bool:
    s = str(num)
    return s in (s + s)[1:-1]

def get_invalid_ids():
    with open("inputs/id_ranges.txt") as f:
        id_ranges = f.read().split(",")
        
    invalid_ids_sum = 0
    
    for id_range in id_ranges:
        start, end = id_range.split("-")
        
        # part 1
        # for num in range(int(start), int(end)+1):
        #     if str(num)[:len(str(num))//2] == str(num)[len(str(num))//2:]:
        #         invalid_ids_sum += num
        
        for num in range(int(start), int(end)+1):
            if is_invalid(num):
                invalid_ids_sum += num
                
    print(invalid_ids_sum)

if __name__ == "__main__":
    get_invalid_ids()
