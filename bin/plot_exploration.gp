exp_10 = "data/parameter_10_1000.dat"
exp_50 = "data/parameter_50_1000.dat"
exp_100 = "data/parameter_100_1000.dat"
exp_150 = "data/parameter_150_1000.dat"
exp_200 = "data/parameter_200_1000.dat"
exp_250 = "data/parameter_250_1000.dat"

stats exp_10 using 1 name 'x' nooutput

set terminal pngcairo size 2000,1600 font ",48"
set output 'plt/parameter_exploration.png'
set grid
set ytics
# set xtics 0,((x_max+1)/5)

set logscale x

set yrange [0:1]
set xlabel 'Number of repetitions'
set ylabel 'Average gain'

set style fill transparent solid 0.7
set style fill noborder # no separate top/bottom lines

plot exp_10 using 1:3:4 lc "light-green" lw 1 with filledcurves notitle, \
     exp_50 using 1:3:4 lc "light-blue" lw 1 notitle with filledcurves, \
     exp_100 using 1:3:4 lc "light-red" lw 1 notitle with filledcurves, \
     exp_150 using 1:3:4 lc "light-pink" lw 1 notitle with filledcurves, \
     exp_200 using 1:3:4 lc "light-magenta" lw 1 notitle with filledcurves, \
     exp_250 using 1:3:4 lc "light-grey" lw 1 notitle with filledcurves, \
     exp_10 using 1:2 lc "green" lw 5 with lines title "Exploration rate = 10", \
     exp_50 using 1:2 lc "blue" lw 5 with lines title "Exploration rate = 50", \
     exp_100 using 1:2 lc "red" lw 5 with lines title "Exploration rate = 100", \
     exp_150 using 1:2 lc "pink" lw 5 with lines title "Exploration rate = 150", \
     exp_200 using 1:2 lc "magenta" lw 5 with lines title "Exploration rate = 200", \
     exp_250 using 1:2 lc "grey" lw 5 with lines title "Exploration rate = 250"
