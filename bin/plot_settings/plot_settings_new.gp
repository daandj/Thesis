control = "data/".ARG1."_ucb.dat"
experiment = "data/".ARG1."_cbt.dat"
stats control using 1 name 'x' nooutput

set terminal png size 1000,800 font ",24"
set output 'plt/'.ARG1.'.png'

set logscale x

set grid
set ytics
# set xtics 0,((x_max+1)/5)

set xrange [1:*]
# set yrange [0:1]
set xlabel 'Number of repetitions (T)'
set ylabel 'Average gain'

set errorbars 8

plot experiment using 1:2:3:4 with yerrorbars title "CBT" lc "green" lw 2 pt 1 ps 5, \
     control using 1:2:3:4 with yerrorbars title "UCB" lc "blue" lw 2 pt 2 ps 5
