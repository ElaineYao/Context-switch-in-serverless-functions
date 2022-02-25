# Learn from geeksforgeeks
import os
import time

def ping_pong():
  # Create a pipe
  r, w = os.pipe()
  # Create a child process
  pid = os.fork()

  # parent process
  if pid>0:
    # close reading end of the pipe
    os.close(r)
    print("Parent process is writing")
    text = b"Hello child process"
    os.write(w, text)
    print("Written text:", text.decode())
  
  # child process
  else:
    # close writing end of the pipe
    os.close(w)
    print("\nChild process is reading")
    r = os.fdopen(r)
    print("Read text:", r.read())

def measure_self():
  # Create a pipe
  r, w = os.pipe()
  # Write to myself
  print("Parent process is writing")
  text = b"Hello child process"
  os.write(w, text)
  print("Written text:", text.decode())
  # Read from myself
  print("\nChild process is reading")
  str1 = os.fdopen(r)
  print("Read text:", str1.read(19))

def main():
  p1_start = time.time()
  print("###p1_start###: "+ str(p1_start))
  measure_self()
  p1_end = time.time()
  print("###p1_end###: "+ str(p1_end))
  self_time = p1_end-p1_start
  print("self time: "+ str(self_time))

  p2_start = time.time()
  print("###p2_start###: "+ str(p2_start))
  ping_pong()
  p2_end = time.time()
  print("###p2_end###: "+ str(p2_end))
  two_process_time = p2_end-p2_start
  print("two process time: "+ str(two_process_time))

  print("Context switch time: "+ str((two_process_time-self_time)/2))

if __name__ == "__main__":
    main()


    
    
