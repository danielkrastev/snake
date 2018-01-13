import random

map_file = '/home/daniel/snake/snake/map'

def load_map(map_str):
    map = list()
    my_position = tuple()
    for i in range(20):
        row_str = map_str[i*21:(i+1)*21]
        row = list(row_str)
        if 'A' in row_str:
            my_position = (i, row.index('A'))
        map.append(row)
    return map,my_position

def map_to_string(map):
    map_str = ""
    for row in map:
        _row = "".join(row)
        map_str += _row
    return map_str
    

map_str = "....................\n\
....................\n\
....................\n\
....................\n\
....................\n\
....................\n\
....................\n\
....................\n\
....................\n\
....................\n\
....................\n\
....................\n\
....................\n\
....................\n\
....................\n\
....................\n\
....................\n\
....................\n\
....................\n\
....................\n\
"

map, p = load_map(map_str)

#Set the apples 
for i in range(25):
    x = random.randint(0,19)
    y = random.randint(0,19)
    map [x][y] = '@'
    
#Set the head of the snake somewhere
x = random.randint(0,19)
y = random.randint(0,19)
map [x][y] = 'A'


with open(map_file, 'w') as f:
    map = map_to_string(map)
    print map
    f.write(map)
    f.close()
