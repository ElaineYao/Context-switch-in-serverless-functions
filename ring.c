#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main(int argc, char **argv)
{
    int N = (argc > 1) ? atoi(argv[1]) : 10;
    int c1_wr;
    int cN_rd;
    int p1[2];
    int p2[2];
    int pid_chk = getpid();

    if (N <= 0 || N >= 100)
        N = 10;

    // Parent creates pipe for it to write to 1st child.
    pipe(p1);
    // Parent keeps open the write end of pipe to 1st child.
    // Later close(p1[0]), but c1_wr is the write end
    c1_wr = dup(p1[1]);
    printf("%d children\n", N);
    printf("Parent   = %d\n", pid_chk);

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
        printf("Child %2d = %d\n", n+1, pid);
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
    printf("PID sum = %d\n", pid_sum);
    printf("PID chk = %d\n", pid_chk);

    return 0;
}
