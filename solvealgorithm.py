from collections import deque
from time import time
from cubeclass import Cube

moves = ['F', "F'",'F2', 'L', "L'",'L2', 'B', "B'",'B2', 'R', "R'",'R2', 'D', "D'",'D2', 'U', "U'",'U2']


inverse_map = {
    "F": "F'",   "F'": "F",   "F2": "F2",
    "L": "L'",   "L'": "L",   "L2": "L2",
    "B": "B'",   "B'": "B",   "B2": "B2",
    "R": "R'",   "R'": "R",   "R2": "R2",
    "D": "D'",   "D'": "D",   "D2": "D2",
    "U": "U'",   "U'": "U",   "U2": "U2", '':''
}

def invert_permutation(move_list):
    return [inverse_map[move] for move in reversed(move_list.split(' '))]

def gen():
    checkmoves = ['']
    for i in moves:
        checkmoves.append(' '.join([i]))
    for i in moves:
        for j in moves:
            checkmoves.append(' '.join([i,j]))
    for i in moves:
        for j in moves:
            for k in moves:
                checkmoves.append(' '.join([i,j,k]))
    for i in moves:
        for j in moves:
            for k in moves:
                for l in moves:
                    checkmoves.append(' '.join([i,j,k,l]))
    for i in moves:
        for j in moves:
            for k in moves:
                for l in moves:
                    for m in moves:
                        checkmoves.append(' '.join([i,j,k,l,m]))
    for i in moves:
            for j in moves:
                for k in moves:
                    for l in moves:
                        for m in moves:
                            for n in moves:
                                checkmoves.append(' '.join([i,j,k,l,m,n]))

    cubes = []
    savemoves = []
    hashes = set()
    for i in range(len(checkmoves)):
        cube = Cube(n=2)
        cube.applymultiple(checkmoves[i])
        if cube.hash not in hashes:
            savemoves.append(' '.join(invert_permutation(checkmoves[i])))
            hashes.add(cube.hash)
            cubes.append(cube.hash)
        if i%100000 == 0:
            print(checkmoves[i])
    #print(cubes, savemoves, hashes)
    # print(len(moves))
    print(len(savemoves),len(cubes),len(hashes))
    string = '\n'.join(savemoves)
    file = open('savedsequences2x2.txt', 'w')
    file.write(string)
    file.close()

    string = '\n'.join(cubes)
    file = open('savedhashes2x2.txt', 'w')
    file.write(string)
    file.close()





savedhashes = open('savedhashes2x2.txt').read().split('\n')
savedmoves = open('savedsequences2x2.txt').read().split('\n')

posdict = {}
for i in range(len(savedhashes)):
    posdict[savedhashes[i]] = savedmoves[i]


if __name__ == '__main__':
    gen()








def simplesolve(cube):
    if cube.hash in posdict:
        return posdict[cube.hash].split(' ')
    queue = deque()
    queue.append([Cube(cube),[]])
    starttime = time()
    hashes = set()
    count = 1
    while time()-starttime < 60:
        count += 1
        pos = queue.popleft()
        
        for i in moves:
            newcube = Cube(pos[0])
            newcube.apply(i)
            if newcube.issolved():
                return pos[1]+[i]
            elif newcube.hash in posdict:
                print('Done in',time()-starttime,'seconds')
                return pos[1]+[i]+posdict[newcube.hash].split(' ')
            elif newcube.hash in hashes:
                pass
            else:
                hashes.add(newcube.hash)
                queue.append([newcube, pos[1]+[i]])
    print('Checked positions:',len(hashes), count)
    if len(queue) == 0:
        print('Impossible position reached ?')
    raise TimeoutError("Too long")


#simplesolve(three)
