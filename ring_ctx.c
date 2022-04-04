#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <time.h>
#include <sched.h>
#include <sys/wait.h>
#include <signal.h>
#include <sys/resource.h>


#define N 3

static inline long long unsigned time_ns() {
  struct timespec ts;
  if (clock_gettime(CLOCK_REALTIME, &ts)) {
    exit(1);
  }
  return ((long long unsigned)ts.tv_sec) * 1000000000LLU +
         (long long unsigned)ts.tv_nsec;
}

void self_measure(){

    int p1[2];
    int p2[2];
    int c1_wr;
    int cN_rd;
    int pid_chk = getpid();
    int mesg = 1;
    // sched_getaffinity(pid_chk);
    cpu_set_t myset;
    CPU_ZERO(&myset);
    CPU_SET(2, &myset);
    sched_getaffinity(pid_chk, sizeof(myset), &myset);

    pipe(p1);
    c1_wr = dup(p1[1]);
    // printf("Parent   = %d\n", pid_chk);
    int pid_sum = getpid();
    write(c1_wr,&pid_sum, sizeof(pid_sum));
    close(c1_wr);


    for (int n=0; n<N; n++){
        pipe(p2);
        // int pid = fork();
        // if(pid == 0){
        // exit(0);
        // }
        // close(p1[1]);
        // close(p2[0]);
        fflush(stdout);
        read(p1[0], &pid_sum, sizeof(pid_sum));
        pid_sum +=getpid();
        write(p2[1], &pid_sum, sizeof(pid_sum));
        close(p1[0]);
        close(p2[1]);
        pid_chk += getpid();
        p1[0] = p2[0];
        p1[1] = p2[1];

    }
    // pipe(p2);
    //     // close(p1[1]);
    //     // close(p2[0]);
    // fflush(stdout);
    // read(p1[0], &pid_sum, sizeof(pid_sum));
    // pid_sum +=getpid();
    // write(p2[1], &pid_sum, sizeof(pid_sum));
    // close(p1[0]);
    // close(p2[1]);
    // pid_chk += getpid();
    // p1[0] = p2[0];
    // p1[1] = p2[1];

    cN_rd = p2[0];
    close(p2[1]); // *****
    read(cN_rd, &pid_sum, sizeof(pid_sum));
    close(cN_rd);
    // printf("PID sum = %d\n", pid_sum);
    // printf("PID chk = %d\n", pid_chk);
    // free memory
	// free(p1);
    // free(p2);
}

int cxt_measure()
{
    // int N = (argc > 1) ? atoi(argv[1]) : 10;
    int c1_wr;
    int cN_rd;
    int p1[2];
    int p2[2];
    int pid_chk = getpid();
    // restrict a single CPU core
    cpu_set_t myset;
    CPU_ZERO(&myset);
    CPU_SET(2, &myset);
    sched_getaffinity(pid_chk, sizeof(myset), &myset);

    // if (N <= 0 || N >= 100)
    //     N = 10;

    // Parent creates pipe for it to write to 1st child.
    pipe(p1);
    // Parent keeps open the write end of pipe to 1st child.
    // Later close(p1[0]), but c1_wr is the write end
    c1_wr = dup(p1[1]);
    // printf("%d children\n", N);
    // printf("Parent   = %d\n", pid_chk);
    
    for (int n = 0; n < N; n++)
    {
        int pid;
        // output pipe for child n. 
        pipe(p2);
        fflush(stdout);
        // child process
        pid = fork();

        if (pid == 0)
        {
            CPU_ZERO(&myset);
            CPU_SET(2, &myset);
            sched_getaffinity(pid, sizeof(myset), &myset);
            // close the write end of input pipe and and read end of output pipe
            close(p1[1]);
            close(p2[0]);
            int pid_sum;
            // read the pid sum 
            read(p1[0], &pid_sum, sizeof(pid_sum));
            pid_sum += getpid();
            write(p2[1], &pid_sum, sizeof(pid_sum));
            close(p1[0]);
            close(p2[1]);
            exit(0);
        }
        // printf("Child %2d = %d\n", n+1, pid);
        pid_chk += pid;
        // parent close both ends of input pipe to the n child and use the output pipe as the input pipe for n+1 pipe
        close(p1[0]);
        close(p1[1]);
        p1[0] = p2[0];
        p1[1] = p2[1];
    }

    // Parent keeps open the read end of the pipe from Nth child.
    cN_rd = p2[0];
    close(p2[1]);

    int pid_sum = getpid();
    write(c1_wr, &pid_sum, sizeof(pid_sum));
    close(c1_wr);
    read(cN_rd, &pid_sum, sizeof(pid_sum));
    close(cN_rd);
    // printf("PID sum = %d\n", pid_sum);
    // printf("PID chk = %d\n", pid_chk);

    return 0;
}


int main(int argc, char **argv){
    clock_t t1;
    t1 = clock();
    // const int NUM_ITERATIONS = 1000;
    // const long long unsigned t1 = time_ns();
    // for (int n=0; n<NUM_ITERATIONS; n++){
    //     self_measure();}
    self_measure();
    // cxt_measure();
    t1 = clock() - t1;
    double time_taken_t1 = ((double)t1)/CLOCKS_PER_SEC; 
    // const long long unsigned elapsed1 = time_ns() - t1;
    // printf("elapse1 time = %lld\n", elapsed1);


    clock_t t2;
    t2 = clock();
    // const long long unsigned t2 = time_ns();
    // for (int n=0; n<NUM_ITERATIONS; n++){
    //     cxt_measure();}
    cxt_measure();
    // self_measure();
    t2 = clock() - t2;
    double time_taken_t2 = ((double)t2)/CLOCKS_PER_SEC; 
    // const long long unsigned elapsed2 = time_ns() - t2;
    // printf("elapse2 time = %lld\n", elapsed2);

    // long long unsigned elapsed;
    double t3;
    t3 = (time_taken_t2 -time_taken_t1)/(N+1);
    // elapsed = (elapsed2 - elapsed1)/((N+1)*NUM_ITERATIONS);
    // printf("elapse time = %f\n", time_taken_t2);
    printf("elapse time = %f", t3);
    // printf("elapse time = %lld\n", elapsed);

}

