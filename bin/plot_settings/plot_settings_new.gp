control = "data/".ARG1."_ucb.dat"
experiment = "data/".ARG1."_cbt.dat"
stats control using 1 name 'x' nooutput

set terminal png size 1000,800 font ",24"
set output 'plt/'.ARG1.'.png'

set logscale x

set grid ytics
set ytics
set xtics scale 0
set xtics ("T=10" 10, "T=100" 100, "T=1000" 1000, "T=10000" 10000, "T=100000" 100000)

set autoscale noextend
set offsets graph 0.06, graph 0.06, 0.001, 0.001

set xlabel 'Number of repetitions'
set ylabel "Difference of average\n outcome and minimax value"

set errorbars 4

plot experiment using ($1*0.85):2:3:4 with yerrorbars title "CBT" lc "red" lw 2 pt 2 ps 3, \
     control using ($1*1.15):2:3:4 with yerrorbars title "UCB" lc "blue" lw 2 pt 2 ps 3
