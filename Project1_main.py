# 201433264 Park Seong Won #
# Selfi-Rone Project # 

from Project1_utils import *
import time

if __name__ == "__main__":
    myDrone = intializeTello()
    while True:
        instruction = input('Input the instruction : ')
        if ((instruction == 's') or (instruction == 'h') or (instruction == 'f')) :
            myDrone.takeoff()
            if (instruction == 's') :
                selfiMode(myDrone)
                myDrone.land()  
                
            elif (instruction == 'h') :
                halfMode(myDrone)
                myDrone.land()
                
            else :
                fullMode(myDrone)
                myDrone.land()
                
        elif (instruction == 'q') :
            print('Terminate the Selfi-Rone')
            myDrone.land()
            break
        else : 
            print('Wrong Instruction!')