# Manages a grid of values
class Grid():
    def __init__(self, width, height, default=''):
        self.width = width
        self.height = height
        self.data = [[default for y in range(height)] for x in range(width)]
    
    def set(self, x, y, value):
        self.data[y][x] = value
    
    def get(self, x, y):
        return self.data[y][x]

# Extension of the Grid class that can be rotated
class RotatableGrid(Grid):
    def rotateCoords(self, x, y, rotation=0):
        # Get rotation
        r = rotation % 4
        
        # Get the offset values
        w = self.width // 2
        h = self.height // 2
        ox = x - w
        oy = y - h
        
        # Set up the default response
        res = {
            'x': x,
            'y': y,
        }
        
        # Create the new x and y depending on the rotation
        if r == 1:
            res = {
                'x': -oy,
                'y': ox,
            }
        elif r == 2:
            res = {
                'x': -ox,
                'y': -oy,
            }
        elif r == 3:
            res = {
                'x': oy,
                'y': -ox,
            }
        
        # Correct the offset if not different
        if res['x'] != x and res['y'] != y:
            res['x'] += w
            res['y'] += h
        
        # Return the rotated coordinates
        return res
    
    def set(self, x, y, value, rotation=0):
        coords = self.rotateCoords(x, y, rotation)
        Grid.set(self, coords['x'], coords['y'], value)
    
    def get(self, x, y, rotation=0):
        coords = self.rotateCoords(x, y, rotation)
        return Grid.get(self, coords['x'], coords['y'])

# Extension of the RotatableGrid class that can render to text and rotate
class DisplayableGrid(RotatableGrid):
    def __str__(self):
        return self.render()
    
    def render(self):
        res = []
        
        horiSplit = ' | '
        vertSplit = '\n +' + '---+' * self.width + '\n'
        
        for row in self.data:
            res.append(horiSplit + horiSplit.join(row) + horiSplit)
        
        return vertSplit + vertSplit.join(res) + vertSplit