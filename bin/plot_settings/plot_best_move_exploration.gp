exp_10 = "data/best_move_parameter_10_1500.dat"
exp_50 = "data/best_move_parameter_50_1500.dat"
exp_100 = "data/best_move_parameter_100_1500.dat"
exp_150 = "data/best_move_parameter_150_1500.dat"
exp_200 = "data/best_move_parameter_200_1500.dat"
exp_250 = "data/best_move_parameter_250_1500.dat"

stats exp_10 using 1 name 'x' nooutput

set terminal pngcairo size 1000,800 font ",24"
set output 'plt/best_move_parameter_exploration.png'
set grid
set ytics

set logscale x

set key right bottom

set xlabel 'Number of repetitions'
set ylabel 'Estimated chance of picking the best move'

plot exp_10 using 1:2 with lines lc "green" lw 2 title "Exploration rate = 10", \
     exp_50 using 1:2 with lines lc "blue" lw 2 title "Exploration rate = 50", \
     exp_100 using 1:2 with lines lc "red" lw 2  title "Exploration rate = 100", \
     exp_150 using 1:2 with lines lc "pink" lw 2  title "Exploration rate = 150", \
     exp_200 using 1:2 with lines lc "magenta" lw 2  title "Exploration rate = 200", \
     exp_250 using 1:2 with lines lc "grey" lw 2  title "Exploration rate = 250"
