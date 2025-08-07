from cubeclass import Cube
from solvealgorithm import simplesolve
from time import sleep

while True:
    print("Enter moves below:")
    cubee = Cube(n=2)
    cubee.draw()
    #User-input scramble (to be replaced)
    for i in range(100):
        try:
            inp = input()
            if inp == '':
                raise Exception()
            cubee.applymultiple(inp)
            cubee.draw()

        except:
            break

    print("Solving...")
    print("Position hash-",cubee.hash)
    result = simplesolve(cubee)

    print('Solved in',len(result),'moves:', ' '.join(result))

    input("Enter to apply")
    demo = Cube(cubee)           
    for i in result:
        sleep(2/(len(result)+1))
        demo.apply(i)
        demo.draw()
    assert demo.issolved()




