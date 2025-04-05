control = "data/".ARG1."_ucb.dat"
experiment = "data/".ARG1."_cbt.dat"

set terminal png
set output 'plt/'.ARG1.'.png'
set grid
plot experiment title "CBT" with lines, \
     control title "UCB" with lines