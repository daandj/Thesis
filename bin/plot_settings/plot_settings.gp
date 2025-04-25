control = "data/".ARG1."_ucb.dat"
experiment = "data/".ARG1."_cbt.dat"
stats control using 1 name 'x' nooutput

set terminal png size 1000,800 font ",24"
set output 'plt/'.ARG1.'.png'
set grid
set ytics
set xtics 0,((x_max+1)/5)

set yrange [0:1]
set xlabel 'Number of repetitions (T)'
set ylabel 'Average gain'

plot experiment title "CBT" with lines, \
     control title "UCB" with lines