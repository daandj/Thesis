set terminal png
set output 'plt/minimal.png'
set grid
plot "data/minimal_cbt.dat" title "CBT" with lines, \
     "data/minimal_ucb.dat" title "UCB" with lines