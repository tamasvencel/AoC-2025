def crack_north_pole_base_secret_entrance_lock():
    rotations = []
    with open("inputs/rotations.txt", "r") as file:
        for line in file:
            rotations.append(line.strip().upper())
    
    dial = 50
    password = 0
    
    for rotation in rotations:
        if rotation[0] == "L":
            if dial == 0:
                password += int(rotation[1:]) // 100
            elif ((dial - int(rotation[1:])) <= 0):
                password += (int(rotation[1:]) - dial + 100)//100
        
            dial = (dial - int(rotation[1:])) % 100
        elif rotation[0] == "R":
            if ((dial + int(rotation[1:])) > 99):
                password += ((dial + int(rotation[1:]))//100)
                
            dial = (dial + int(rotation[1:])) % 100
            
    print(password)


if __name__ == "__main__":
    crack_north_pole_base_secret_entrance_lock()
