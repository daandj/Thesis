control = "data/".ARG1."_ucb.dat"
experiment = "data/".ARG1."_cbt.dat"
stats control using 1 name 'x' nooutput

set terminal png size 2000,1600 font ",48"
set output 'plt/'.ARG1.'.png'

set logscale x

set grid
set ytics
# set xtics 0,((x_max+1)/5)

set yrange [0:1]
set xlabel 'Number of repetitions (T)'
set ylabel 'Average gain'

set style fill transparent solid 0.7
set style fill noborder # no separate top/bottom lines

plot experiment using 1:3:4 lc "light-green" lw 1 with filledcurves notitle, \
        control using 1:3:4 lc "light-blue" lw 1 notitle with filledcurves, \
        experiment using 1:2 lc "green" lw 5 with lines title "CBT", \
        control using 1:2 lc "blue" lw 5 with lines title "UCB"
