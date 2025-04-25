exp_10 = "data/parameter_10_1000.dat"
exp_50 = "data/parameter_50_1000.dat"
exp_100 = "data/parameter_100_1000.dat"
exp_150 = "data/parameter_150_1000.dat"
exp_200 = "data/parameter_200_1000.dat"
exp_250 = "data/parameter_250_1000.dat"

stats exp_10 using 1 name 'x' nooutput

set terminal pngcairo size 1000,800 font ",24"
set output 'plt/parameter_exploration.png'
set grid
set ytics
set xtics 0,((x_max+1)/5)

set yrange [0:1]
set xlabel 'Number of repetitions'
set ylabel 'Average gain'

plot exp_10 title "Exploration rate = 10" with lines, \
     exp_50 title "Exploration rate = 50" with lines, \
     exp_100 title "Exploration rate = 100" with lines, \
     exp_150 title "Exploration rate = 150" with lines, \
     exp_200 title "Exploration rate = 200" with lines, \
     exp_250 title "Exploration rate = 250" with lines