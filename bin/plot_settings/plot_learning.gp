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
set xtics 0,((x_max+1)/5)

set yrange [0:1]
set xlabel 'Number of repetitions'
set ylabel 'Average gain'

plot learning_0 title "Learning rate = 0" with lines, \
     learning_500 title "Learning rate = 500" with lines, \
     learning_1000 title "Learning rate = 1000" with lines, \
     learning_1500 title "Learning rate = 1500" with lines, \
     learning_2000 title "Learning rate = 2000" with lines, \
     learning_2500 title "Learning rate = 2500" with lines