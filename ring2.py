import os
import sys
import time

global N 
N=3

def cxt_overhead():
    pid_chk = os.getpid()
    pid = os.fork()
    pipes = []
    for i in range(4):
        pipes.append(os.pipe())
    if(pid == 0):
        # P2
        for i in range(4):
            if(i !=0):
                os.close(pipes[i][0])
            if(i !=1):
                os.close(pipes[i][1])
        pid_sum_b = os.read(pipes[0][0], 5)
        pid_sum = os.getpid() + int.from_bytes(pid_sum_b, byteorder='big')
        os.write(pipes[1][1], pid_sum.to_bytes(5, byteorder='big'))
        print("Child 1: " + str(os.getpid()))
        pid_chk += pid
    else:
        pid1 = os.fork()
        if(pid1 == 0):
            # P3
            for i in range(4):
                if(i !=1):
                    os.close(pipes[i][0])
                if(i !=2):
                    os.close(pipes[i][1])
            pid_sum_b = os.read(pipes[1][0], 5)
            pid_sum = os.getpid() + int.from_bytes(pid_sum_b, byteorder='big')
            os.write(pipes[2][1], pid_sum.to_bytes(5, byteorder='big'))
            print("Child 2: " + str(os.getpid()))
            pid_chk += pid
        else:
            pid2 = os.fork()
            if(pid2 == 0):
                # P4
                for i in range(4):
                    if(i !=2):
                        os.close(pipes[i][0])
                    if(i !=3):
                        os.close(pipes[i][1])
                pid_sum_b = os.read(pipes[2][0], 5)
                pid_sum = os.getpid() + int.from_bytes(pid_sum_b, byteorder='big')
                os.write(pipes[3][1], pid_sum.to_bytes(5, byteorder='big'))
                print("Child 3: " + str(os.getpid()))
                pid_chk += pid
            else:
                for i in range(4):
                    if(i !=3):
                        os.close(pipes[i][0])
                    if(i !=0):
                        os.close(pipes[i][1])
    
                pid_sum = os.getpid()
                os.write(pipes[0][1], pid_sum.to_bytes(5, byteorder='big'))
                print("Parent: " + str(os.getpid()))
                pid_sum = os.read(pipes[3][0], 5)
                print("PID sum = "+str(int.from_bytes(pid_sum, byteorder='big')))
                print("PID_chk = "+str(pid_chk))

                
                    






    




if __name__ == "__main__":
    cxt_overhead()
