restart 
run 20 ns 
add_force clk {0} {1 5} -repeat_every 10
run 20 ns

add_force in_a 1; 
run 10 ns 

add_force in_b 1; 
run 20 ns 