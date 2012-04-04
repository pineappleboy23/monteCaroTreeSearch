# Manages a grid of values
class Grid():
    def __init__(self, width, height, default=''):
        self.width = width
        self.data = [[default for y in range(height)] for x in range(width)]
    
    def set(self, x, y, value):
        self.data[x][y] = value
    
    def get(self, x, y):
        return self.data[x][y]

# Extension of the Grid class that can render to text
class DisplayableGrid(Grid):
    def __str__(self):
        return self.render()
    
    def render(self):
        res = []
        
        horiSplit = ' | '
        vertSplit = '\n +' + '---+' * self.width + '\n'
        
        for row in self.data:
            res.append(horiSplit + horiSplit.join(row) + horiSplit)
        
        return vertSplit + vertSplit.join(res) + vertSplit