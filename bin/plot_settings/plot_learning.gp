learning_0 = "data/parameter_10_0.dat"
learning_500 = "data/parameter_10_500.dat"
learning_1000 = "data/parameter_10_1000.dat"
learning_1500 = "data/parameter_10_1500.dat"
learning_2000 = "data/parameter_10_2000.dat"
learning_2500 = "data/parameter_10_2500.dat"

stats learning_0 using 1 name 'x' nooutput

set terminal pngcairo size 1000,800 font ",24"
set output 'plt/parameter_learning.png'
set grid
set ytics

set key left bottom

set logscale x

# set yrange [0:1]
set xlabel 'Number of repetitions'
set ylabel "Difference of average\n outcome and minimax value"

plot learning_0 using 1:2 lc "green" lw 3 with lines title "Learning rate = 0", \
     learning_500 using 1:2 lc "blue" lw 3 with lines title "Learning rate = 500", \
     learning_1000 using 1:2 lc "red" lw 3 with lines title "Learning rate = 1000", \
     learning_1500 using 1:2 lc "pink" lw 3 with lines title "Learning rate = 1500", \
     learning_2000 using 1:2 lc "magenta" lw 3 with lines title "Learning rate = 2000", \
     learning_2500 using 1:2 lc "grey" lw 3 with lines title "Learning rate = 2500"