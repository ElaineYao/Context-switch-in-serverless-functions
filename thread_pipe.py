import  os
import threading
import time
import csv

NUM_ITERATATION = 1000

def measure_self(n):
    global p1_start, p1_end, self_time, p2_start, p2_end
    # Create a pipe
    # r, w = os.pipe()
    p1_start = time.time()
    print("###p1_start###: "+ str(p1_start))
    
    for i in range(n):
        r, w = os.pipe()
        # Write to myself
        # print("Parent process is writing")
        text = b"Hello"
        os.write(w, text)
        # print("Written text:", text.decode())
        # Read from myself
        # print("\nChild process is reading")
        str1 = os.fdopen(r)
        # print("Read text:", str1.read(5))
        os.close(w)

    p1_end = time.time()
    print("###p1_end###: "+ str(p1_end))

def pingpong_parent(r, w):
    global p1_start, p1_end, self_time, p2_start, p2_end

    # print("Current thread: " + str(threading.get_ident()))
    # print(r, w)
    # print("Parent process is writing")
    text = b"Hello"
    os.write(w, text)
    # print("Written text:", text.decode(),'\n')

def pingpong_child(r, w):
    global p1_start, p1_end, self_time, p2_start, p2_end
    # print("Current thread: " + str(threading.get_ident()))
    # close writing end of the pipe
    os.close(w)
    # print("Child process is reading")
    r = os.fdopen(r)
    # print("Read text:", r.read())

def main():
    global p1_start, p1_end, self_time, p2_start, p2_end

    measure_self(NUM_ITERATATION)
    self_time = p1_end-p1_start
    print("self time: "+ str(self_time))
    p2_start = time.time()
    # print("###p2_start###: "+ str(p2_start))
    for i in range(NUM_ITERATATION):
        r, w = os.pipe()
        pingpong_parent(r, w)
        child = threading.Thread(target=pingpong_child, args=(r, w))
        child.start()
        child.join()
    p2_end = time.time()
    # print("###p2_end###: "+ str(p2_end))

    two_process_time = p2_end-p2_start
    print("two process time: "+ str(two_process_time))

    print("Context switch time: "+ str((two_process_time-self_time)/(2*NUM_ITERATATION)))
    cxt_time =(two_process_time-self_time)*1e6/(2*NUM_ITERATATION)
    with open('./thread_pipe.csv','a', newline='') as csvfile:
            csvWriter = csv.writer(csvfile)
            csvWriter.writerow([cxt_time])

if __name__ == "__main__":
    main()