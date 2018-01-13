import time
import sys

class Queue:
    def __init__(self):
        self.queue = list()

    def add(self, elem):
        self.queue.append(elem)
        
    def pop(self):
        first = self.queue[0]
        self.queue = self.queue[1:]
        return first
    
    def is_empty(self):
        return len(self.queue) == 0
    
    def print_me(self):
        print self.queue
    
    def contains(self, elem):
        return elem in self.queue
    
    def __str__(self):
        return self.queue
    
def load_map_string(map_file):
    map_str = None
    with open(map_file) as f:
        map_str = f.read()
    return map_str.replace("\n","")

def load_map(map_str):
    map = list()
    my_position = tuple()
    for i in range(20):
        row_str = map_str[i*20:(i+1)*20]
        row = list(row_str)
        if 'A' in row_str:
            my_position = (i, row.index('A'))
        map.append(row)
    return map,my_position

class SnakeGame:
    def __init__(self, map_str):
        map,head = load_map(map_str)
        self.map = map
        self.head = head
        self.snake = [head]
        self.charlist = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ-'
        self.dir = "up"
        self.alive = True
        self.last_move = None
        self.moves = 0
        
    def print_map(self):
        for row in self.map:
            print row
        print
    
    def print_visited(self, visited):
        for v in visited:
            self.map[v[0]][v[1]] = '+'
        self.print_map()
        
    def check_crash(self):
        if self.head[0] < 0 or self.head[0] > 19 or \
            self.head[1] < 0 or self.head[1] > 19 or \
            self.map[self.head[0]][self.head[1]] not in ['.','@']:
            print "CRASH!!!"
            self.alive = False
            sys.exit(1)
        
    def left(self, position):
        if position[1] > 0:
            return self.map[position[0]][position[1]-1]
        else:
            return '-'
        
    def right(self, position):
        if position[1] < 19:
            return self.map[position[0]][position[1]+1]
        else:
            return '-'
        
    def up(self, position):
        if position[0] > 0: 
            return self.map[position[0]-1][position[1]]
        else:
            return '-'
        
    def down(self, position):
        if position[0] < 19:
            return self.map[position[0]+1][position[1]]
        else:
            return '-'
    
    def _map(self, position):
        return self.map[position[0]][position[1]]
    
    def is_wall(self, position):
        if position[0] < 0 or position[0] > 19:
            return True
        if  position[1] < 0 or position[1] > 19:
            return True
        return self._map(position) in self.charlist
        
    def make_move(self, direction):
        map = self.map
        snake = self.snake
        
        if direction == "left":
            self.head = (self.head[0],self.head[1]-1)
        elif direction == "right":
            self.head = (self.head[0],self.head[1]+1)
        elif direction == "up":
            self.head = (self.head[0]-1, self.head[1])
        elif direction == "down":
            self.head = (self.head[0]+1, self.head[1])

        self.check_crash()

        got_apple = False
        if map[self.head[0]][self.head[1]] == '@':
            got_apple = True

        snake.insert(0, self.head)
        last = snake[-1]
        if not got_apple:
            self.snake = snake[:-1]
        
        for i in range(len(self.snake)):
            map[snake[i][0]][snake[i][1]] = self.charlist[i]
        if not got_apple:
            map[last[0]][last[1]] = '.'
        
        self.last_move = direction
        self.moves += 1
        self.print_map()
        time.sleep(.2)
        
    def go_right(self):
        self.make_move("right")
    
    def go_left(self):
        self.make_move("left")
        
    def go_up(self):
        self.make_move("up")
        
    def go_down(self):
        self.make_move("down")
        
    def set_direction(self, dir):
        def is_opposite_direction():
            if dir == "w":
                return self.dir == "down"
            if dir == "s":
                return self.dir == "up"
            if dir == "a":
                return self.dir == "right"
            if dir == "d":
                return self.dir == "left"
            else:
                return True
            
        if dir not in ['a', 's', 'd', 'w', 'left', 'right', 'up', 'down']:
            return
        if is_opposite_direction():
            return

        if dir == "w":
            self.dir = "up"
        if dir == "s":
            self.dir = "down"
        if dir == "a":
            self.dir = "left"
        if dir == "d":
            self.dir = "right"  

    def get_direcion(self):
        return self.dir    

    def is_alive(self):
        return self.alive
    
    def go_to(self, target):
        #horizontal_moves = abs(self.head[0] - target[0])
        #if self.head[0] > target[0]:
        if self.head == target:
            return
        neighbours = self.get_neighbours(self.head)
        possible = list()
        for n in  neighbours:
            if not self.is_wall(n):
                possible.append(n)
        if len(possible) == 1:
            new_target = possible[0]
            if self.head[0] + 1 == new_target[0]: 
                self.go_down() 
            elif self.head[0] - 1 == new_target[0]:
                self.go_up()
            elif self.head[1] + 1 == new_target[1]:
                self.go_right()
            else:
                self.go_left()
            
        else:
            if self.head[0]  > target[0]:
                if self.up(self.head) not in self.charlist and self.last_move != "down":
                    self.go_up()
                elif self.left(self.head) not in self.charlist:
                    self.go_left()
                else:
                    self.go_right()
                    
            elif self.head[0] < target[0]:
                if self.down(self.head) not in self.charlist and self.last_move != "up":    
                    self.go_down()
                elif self.left(self.head) not in self.charlist:
                    self.go_left()
                else:
                    self.go_right()
                    
            elif self.head[1] > target[1]:
                if self.left(self.head) not in self.charlist and self.last_move != "right":
                    self.go_left()
                elif self.down(self.head) not in self.charlist:
                    self.go_down()
                else:
                    self.go_up()
                    
            elif self.head[1] < target[1]: 
                if self.right(self.head) not in self.charlist and self.last_move != "left":    
                    self.go_right()
                elif self.down(self.head) not in self.charlist:
                    self.go_down()
                else:
                    self.go_up()

            return self.go_to(target)
    
    def get_neighbours(self, position):
        neighbours = list()
        if position[0] - 1 >= 0:
            neighbours.append((position[0] - 1, position[1]))
        if position[0] + 1 < 20:
            neighbours.append((position[0] + 1, position[1]))
        if position[1] - 1 >= 0:
            neighbours.append((position[0], position[1]-1))
        if position[1] + 1 < 20:
            neighbours.append((position[0], position[1]+1))
        return neighbours
        
    def find_nearest(self):
        position = self.head
        path = list()
        bfs_queue = Queue()
        visited = list()
        
        bfs_queue.add(position)
        
        while not bfs_queue.is_empty() :
            #self.print_visited(visited)
            #time.sleep(.06)
            current = bfs_queue.pop()
            if self.map[current[0]][current[1]] == '@':
                print current
                return current
            else:
                if current not in visited:
                    visited.append(current)
                for n in self.get_neighbours(current):
                    if n not in visited and not bfs_queue.contains(n):
                        bfs_queue.add(n)
                
           
def get_user_input(snake):
    while snake.is_alive():
        inp = raw_input()
        snake.set_direction(inp)
    
map_file = '/home/daniel/snake/snake/map'
map_str = load_map_string(map_file)
map, my_position = load_map(map_str)

snake = SnakeGame(map_str)
snake.print_map()
while True:
    target = snake.find_nearest()
    if target:
        snake.go_to(target)
    else:
        break
print (snake.moves)
#inp = threading.Thread(target=get_user_input, args=[snake])
#inp.start()

#while True:
#    snake.print_map()
#    time.sleep(0.5)
    #print ("direction is %s" % snake.dir)
#    snake.gogo()
    #snake.make_move(snake.dir)

