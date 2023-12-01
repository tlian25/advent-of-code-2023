# Utility for reading inputs quickly

def read_input_file(day:int) -> list:
    filename = f'../inputs/day{str(day).zfill(2)}_input.txt'
    print("Input file: ", filename)
    with open(filename) as f:
        lines = f.readlines()
        
    # Remove new line char
    return [l.replace('\n', '') for l in lines]