from drawcube import draw

#    XXX      X..     ...     ..X
#0-  ...   1- X..  2- ...  3- ..X 
#    ...      X..     XXX     ..X
# face: (face, row that turns), in order of cubie-giving on clockwise
turnmaps = {0:[(5,2),(3,1),(4,0),(1,3)],
            1:[(5,1),(0,1),(4,1),(2,1)],
            2:[(5,0),(1,1),(4,2),(3,3)],
            3:[(5,3),(2,3),(4,3),(0,3)],
            4:[(0,2),(3,2),(2,0),(1,2)],
            5:[(0,0),(1,0),(2,2),(3,0)]}

numtoface = {0:'F',
             1:'L',
             2:'B',
             3:'R',
             4:'D',
             5:'U'}

facetonum = {'F': 0,
             'L': 1,
             'B': 2,
             'R': 3,
             'D': 4,
             'U': 5}


class Cube:
    def __init__(self, faces=None, n = 3):
        self.n = n
        if isinstance(faces,Cube):
            self.n = faces.n
            faces = faces.faces
        if isinstance(faces, str):
            assert len(faces) == 6*self.n**2
            self.faces = []
            for i in range(6):
                self.faces.append([])
                for j in range(n):
                    self.faces[i].append([])
                    for k in range(n):
                        self.faces[i][j].append(faces[n**2*i+n*j+k])
        elif faces:
            # Expecting a 6-element list of 3x3 lists
            self.faces = [ [row[:] for row in face] for face in faces ]
        else:
            # Default to solved cube
            
            self.faces =  [[list(color * n) for _ in range(n)] for color in ['W', 'O', 'Y', 'R', 'G', 'B']]
            
        self.hash = self.gethash()



    def issolved(self):
        for face in self.faces:
            string = ''.join([''.join(i) for i in face])
            if string.count(string[0]) != self.n**2:
                return False
        return True

    def rotateface(self,face, clockwise):
        new = [['']*self.n for i in range(self.n)]
        if clockwise:
            newplaces = [[(0,self.n-1),(1,2),(self.n-1,self.n-1)],
                        [(0,1),(1,1),(2,1)],
                        [(0,0),(1,0),(self.n-1,0)]]
        else:
            newplaces = [[(self.n-1,0),(1,0),(0,0)],
                        [(2,1),(1,1),(0,1)],
                        [(self.n-1,self.n-1),(1,2),(0,self.n-1)]]
        for i in range(self.n):
            for j in range(self.n):
                if self.n == 3:
                    new[newplaces[i][j][0]][newplaces[i][j][1]] = face[i][j]
                elif self.n ==2:
                    new[newplaces[2*i][2*j][0]][newplaces[2*i][2*j][1]] = face[i][j]
                else:
                    raise NotImplemented()
        return new
        
    def getcubies(self,face, row):
        if row == 0:
            return face[0].copy()[::-1]
        if row == 2:
            return face[self.n-1].copy()
        if row == 1:
            return [face[i][0] for i in range(self.n)]
        if row == 3:
            return [face[i][self.n-1] for i in range(self.n)][::-1]

    def setcubies(self,cubies, face, row):
        if row == 0:
            face[0] = cubies[::-1]
        if row == 2:
            face[self.n-1] = cubies
        if row == 1:
            for i in range(self.n):
                face[i][0] = cubies[i]
        if row == 3:
            for i in range(self.n):
                face[self.n-1-i][self.n-1] = cubies[i]

    def gethash(self):
        total = ''
        for i in self.faces:
            for j in i:
                for k in j:
                    total += k
        return total

    def rotate(self, face,clockwise):
        self.faces[face] = self.rotateface(self.faces[face], clockwise)

        turnmap = turnmaps[face]
        if not clockwise:
            turnmap = turnmap[::-1]
        cubies = []
        for i in turnmap:
            cubies.append(self.getcubies(self.faces[i[0]], i[1]))
        for i in range(4):
            self.setcubies(cubies[i], self.faces[turnmap[(i+1)%4][0]], turnmap[(i+1)%4][1])
        self.hash = self.gethash()

    def apply(self, symbol):
        if not symbol:
            return
        self.rotate(facetonum[symbol[0].upper()] ,'\'' in symbol)
        if '2' in symbol:
            self.rotate(facetonum[symbol[0].upper()] ,'\'' in symbol)

    def applymultiple(self, symbols):
        try:
            for i in symbols.split(' '):
                self.apply(i)
        except AttributeError:
            for i in symbols:
                self.apply(i)

        

    def draw(self):
        draw(self.faces)

    def __lt__(self, other):
        return self.hash < other.hash
    
    def __eq__(self, other):
        return self.hash == other.hash

    def __repr__(self):
        return self.hash
    


