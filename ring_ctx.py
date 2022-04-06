import os
import sys
import time
import gc
import csv

# num of children
global N
N = 2

def self_overhead():
    pid_chk = os.getpid()
    affinity = os.sched_getaffinity(pid_chk)
    p1 = os.pipe()
    c1_wr = os.dup(p1[1])
    # print("Parent = " +str(pid_chk))
    pid_sum = os.getpid()
    os.write(c1_wr, pid_sum.to_bytes(5, byteorder='big'))
    os.close(c1_wr)

    for n in range(N):
        pid = os.fork()
        if(pid==0):
            os._exit(os.EX_OK)

    for n in range(N):
        # pipes.append(os.pipe)
        p2 = os.pipe()
        sys.stdout.flush()
        pid_sum_b = os.read(p1[0], 5)
        pid_sum = os.getpid() + int.from_bytes(pid_sum_b, byteorder='big')
        os.write(p2[1], pid_sum.to_bytes(5, byteorder='big'))
        os.close(p1[0])
        os.close(p2[1])
        pid_chk += os.getpid()
        p1 = (p2[0], p2[1])
    cN_rd = p2[0]
    pid_sum = os.read(cN_rd, 5)
    os.close(cN_rd)
    # print("PID sum = "+str(int.from_bytes(pid_sum, byteorder='big')))
    # print("PID_chk = "+str(pid_chk))
    # free memory
    # del p1
    # del p2
    # gc.collect()


def cxt_overhead():

    pid_chk = os.getpid()
    affinity = os.sched_getaffinity(pid_chk)
    # Parent creates pipe for it to write to 1st child.
    p1 = os.pipe()
    # Parent keeps open the write end of pipe to 1st child.
    # Later close(p1[0]), but c1_wr is the write end
    c1_wr = os.dup(p1[1])
    # print("Parent = " +str(pid_chk))

    for n in range(N):
        p2 = os.pipe()
        sys.stdout.flush()
        
        pid = os.fork()
        affinity = os.sched_getaffinity(pid)
        # child process
        if(pid == 0):
            # close the write end of input pipe and and read end of output pipe
            affinity = os.sched_getaffinity(pid)
            os.close(p1[1])
            os.close(p2[0])
            pid_sum_b = os.read(p1[0], 5)
            pid_sum = os.getpid() + int.from_bytes(pid_sum_b, byteorder='big')
            os.write(p2[1], pid_sum.to_bytes(5, byteorder='big'))
            os.close(p1[0])
            os.close(p2[1])
            os._exit(os.EX_OK)
        # print("Child "+str(n+1) +" = "+str(pid))
        pid_chk += pid
        # parent close both ends of input pipe to the n child and use the output pipe as the input pipe for n+1 pipe
        os.close(p1[0])
        os.close(p1[1])
        p1 = (p2[0], p2[1])

    # Parent keeps open the read end of the pipe from Nth child.
    cN_rd = p2[0]
    os.close(p2[1])
    pid_sum = os.getpid()
    os.write(c1_wr, pid_sum.to_bytes(5, byteorder='big'))
    os.close(c1_wr)
    pid_sum = os.read(cN_rd, 5)
    os.close(cN_rd)
    # print("PID sum = "+str(int.from_bytes(pid_sum, byteorder='big')))
    # print("PID_chk = "+str(pid_chk))

def main():
    # self measurement
    p1_start = time.time()
    # for i in range(1000):
    #     self_overhead()
    self_overhead()
    p1_end = time.time()
    self_time = p1_end - p1_start
    # cxt measurement
    p2_start = time.time()
    # for j in range(1000):
    #     cxt_overhead()
    cxt_overhead()
    p2_end = time.time()
    cxt_time = (p2_end-p2_start-self_time)/((N+1))
    cst_time_us = "{:.3f}".format(cxt_time*1e6)
    print("Context switch time is: "+str(cxt_time))
    with open('./pidsum.csv','a', newline='') as csvfile:
            csvWriter = csv.writer(csvfile)
            csvWriter.writerow([cst_time_us])


if __name__ == "__main__":
    main()
    # self_overhead()