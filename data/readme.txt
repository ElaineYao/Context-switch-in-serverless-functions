
For lmbench.csv
Context switching - times in microseconds - smaller is better
-------------------------------------------------------------------------
Host                 OS  2p/0K 2p/16K 2p/64K 8p/16K 8p/64K 16p/16K 16p/64K
                         ctxsw  ctxsw  ctxsw ctxsw  ctxsw   ctxsw   ctxsw
--------- ------------- ------ ------ ------ ------ ------ ------- -------
elaine    Linux 5.13.0- 1.2400 1.5300 1.7800 2.2900 2.5000 2.36000 2.81000
elaine    Linux 5.13.0- 1.4700 1.5700 1.6300 2.0700 6.7200 2.29000 2.69000
elaine    Linux 5.13.0- 1.5000 1.4700 1.5800 2.1500 2.2400 2.35000 2.65000
elaine    Linux 5.13.0- 1.5700 1.6000 1.6400 2.1000 1.8900 2.38000 2.42000
elaine    Linux 5.13.0- 1.6200 1.5400 1.5700 2.0900 2.1300 2.32000 2.55000
elaine    Linux 5.13.0- 1.3900 1.5200 1.6900 2.1200 2.3100 2.41000 2.51000
elaine    Linux 5.13.0- 1.2100 1.5100 1.7000 2.0500 2.1600 2.56000 2.54000
elaine    Linux 5.13.0- 1.6900 1.5500 1.6900 2.0700 2.1600 2.93000 3.12000
elaine    Linux 5.13.0- 1.4900 1.5200 1.6300 2.2900 2.0300 5.79000 4.53000
elaine    Linux 5.13.0- 1.4400 1.4300 1.9800 3.1000 2.3200 3.49000 2.53000

for local.csv
pingpong, condvar, thread_pipe, lmbench, proc_ring
