import curses

class Map():
    def __init__(self, filename, start_position):
        #load the map to be rendered
        self.map = []
        f = open(filename, 'r')
        lines = f.readlines()
        for line in lines:
            self.map.append(line.rstrip('\n'))

        #initialize player position (row, column)
        #coordinates start at 0,0 in top right corner
        self.player_pos = start_position

    def get_size(self):
        return len(self.map), len(self.map[0])
        
    #prints the map
    def render(self, screen):
        for i in range(len(self.map)):
            screen.addstr(i,0, self.map[i])
        screen.addch(self.player_pos[0], self.player_pos[1], 'x')

    #moves the character
    #handles collision issues
    def move_player(self, direction):
        obstacles = ['#', '+', '=', ":", "^", '"', '~']
        if direction == 'w' and self.player_pos[0] > 0:
            if self.map[self.player_pos[0]-1][self.player_pos[1]] not in obstacles:
                self.player_pos[0] -= 1
        elif direction == 'd' and self.player_pos[1] < len(self.map[0])-1:
            if self.map[self.player_pos[0]][self.player_pos[1]+1] not in obstacles:
                self.player_pos[1] += 1
        elif direction == 's' and self.player_pos[0] < len(self.map)-1:
            if self.map[self.player_pos[0]+1][self.player_pos[1]] not in obstacles:
                self.player_pos[0] += 1
        elif direction == 'a' and self.player_pos[1] > 0:
            if self.map[self.player_pos[0]][self.player_pos[1]-1] not in obstacles:
                self.player_pos[1] -= 1

    def flip_doors(self):
        for shifts in [[0, 1], [0, -1], [1, 0], [-1, 0]]:
            flipped = False
            try:
                if self.map[self.player_pos[0]+shifts[0]][self.player_pos[1]+shifts[1]] == '+':
                    self.map[self.player_pos[0]+shifts[0]] = self.map[self.player_pos[0]+shifts[0]][0:self.player_pos[1]+shifts[1]] + '/' + self.map[self.player_pos[0]+shifts[0]][self.player_pos[1]+shifts[1]+1:]
                    flipped = True
            except:
                print("Error 1")
                pass
            try:
                if not flipped and self.map[self.player_pos[0]+shifts[0]][self.player_pos[1]+shifts[1]] == '/':
                    self.map[self.player_pos[0]+shifts[0]] = self.map[self.player_pos[0]+shifts[0]][0:self.player_pos[1]+shifts[1]] + '+' + self.map[self.player_pos[0]+shifts[0]][self.player_pos[1]+shifts[1]+1:]
            except:
                print("Error 2")
                pass
            
        
    def interact(self):
        self.flip_doors()
