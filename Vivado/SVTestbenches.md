# Testbenches: An Alternative to Tcl for Simulating Digital Designs

Instead of using Tcl from the Tcl command line in Vivado, the more common way to simulate a SystemVerilog design is actually to write a testbench in SystemVerilog itself.  That testbench can be designed to drive values into your design and monitor the outputs for correctness.  This avoids the need for you to manually verify correctness by looking at a waveform display (the waveform display is most useful for _debugging_, not for _design verification_.

The rest of this document provides enough information for you to get started and write reasonable testbenches.  It is somewhat specific to the use of Vivado and its simulator.  But, the vast majority of its content applies to all tools.

## Introduction
If you know SystemVerilog you can use it to write a testbench rather than learn yet another language (Tcl).  The advantage of Tcl, however, is that it is trivial to learn to use for extremely simple testbenches (and that is why we use it in our beginning classes).  However, SystemVerilog has many advanced features which make it possible to write sophisticated testbenches that could not be reasonably coded in Tcl.

So, while it is a mixed bag for simple circuits, essentially _all_ industrial digital circuit design simulation is done using testbenches instead of Tcl.  Thus, learning how to write testbenches is a useful skill.

If you know Tcl, it is very straightforward to create an equivalent testbench.  This will be illustrated using some examples that you may choose to mimic.  Before we start here are some things to know:

1. The testbench is THE top level module in your design.  That is, it contains your design.  
1. A testbench has no input or output ports - it essentially represents the environment your design will operate inside of.
1. The main components of a testbench include:
  * Local signal declarations
  * Inserting an instance of your design and wiring the local signals up to it.
  * A clock generation block (if your design has a clock)
  * A set of statements which do the following:  a) set some of the local signal values, b) run for some time period, c) repeat.

Finally, a very big CAUTION: the SystemVerilog language features used to write testbenches _cannot_ be used in the design of circuits - the synthesis tool would not know what to do with much of it.  Rather, we use SystemVerilog in our testbenches like C or Java or python - we are using it as a sequential programming language.  This is perfectly normal and is how it is intended to be used for testbenches.  So remember - the kind of SystemVerilog you write for your digital circuits (which will be synthesized to an FPGA) is very different from the kind of SystemVerilog you write for testbenches.

## A Combinational Testbench 
Here is a simple combinational design:
```
// In file mux2.sv:
module mux2(
  input wire logic sel, 
  input wire logic a, 
  input wire logic b, 
  output wire q);

  assign q = sel?b:a;
endmodule
```  
And, here is a testbench for it:
```
// In file tb.sv:
module tb();
  
  logic sel, a, b, q;   // The local signals
  
  mux2 DUT(sel, a, b, q);  // The instantiation of the design to be tested.
                          // This is also know as the design under test (the 'DUT')
    
  // An initial block is a piece of sequential code
  // In general it cannot be synthesized and is used 
  // only for testbenches.
  initial begin   
    sel = 0;      // Set initial values
    a = 0;
    b = 0;
    #10ns;        // Simulate for 10ns
    
    sel = 0;      // Do it again
    a = 1;
    b = 0;
    #10ns;
    
    sel = 1;      // And again...
    a = 1;
    b = 0;
    #10ns;
    
    // and so on...
    
  end
endmodule
```
So, if you can write a Tcl script to exercise a combinational circuit you can certainly do one as a SystemVerilog testbench - the syntax and structure is just different.  And, to simulate, you would fire up your simulator but specify that the testbench is the top level module.  

Once the simulation starts, 
by default Vivado will initially run the simulation until one of 3 things happens:
1. Until the testbench ends (meaning all the statements in the _initial_ block have executed)
1. Until it hits a **$finish** command (see below for details)
1. Until it has simulated for 1000ns.

It will then stop, awaiting further input from you. If you would like to simulate further, you can drive it by typing commands into the Tcl console such as "run 300ns".

If you don't want Vivado to initially simulate for 1000ns in the absence of one of the other two conditions, you can change that with a command like this:
```
set_property -name {xsim.simulate.runtime} -value 100ns -objects [get_filesets sim_1]
```

Once you execute that command with a project open in the GUI, it will set the project to always use that time period.

## Testbenches for sequential circuits
The major difference here is that there is a clock:
```
//In file cnt.sv:
module cnt(input wire logic clk, clr, output logic[7:0] q);
  always_ff @(posedge clk)
    if (clr)
      q <= 0;
    else
      q <= q + 1;
endmodule
```

and here is the testbench:
```  
// In file tb.sv
module tb();
  
  logic clk, clr;
  logic[7:0] q;

  cnt DUT(clk, clr, q);  // Instantiate the design under test (DUT)

  // Here is how we make a clock generator with a 10ns period:
  initial begin
    clk = 0;
    forever clk = #5ns ~clk;
  end

  // Here is how we assert signals. 
  // Note, rather than worry about ns, 
  // we just wait for negative edges of the clock
  // to change our input signals.  This 
  // ensures they don't change right at the 
  // clock rising edge (which, if they did,
  // would cause a "race" and make you pull your hair out
  // trying to debug it).
  initial begin
    clr = 0;
    @(negedge clk);  // Wait until the next falling edge of the clock

    clr = 1;
    @(negedge clk);
 
    clr = 0;
    repeat(13) @(negedge clk);   // Wait for 13 clock cycles

    clr = 1;
    repeat(2) @(negedge clk);
    
    // and so on...
    

  end
endmodule
```

### Multiple Initial Blocks in a Testbench
So, what happens when you have two _initial_ blocks in a testbench?  It turns out that the simulator will simulate them as if they executed in parallel.  That is, they are both are running all the time (or so the simulator makes it seem).  Thus, the clock generator block can run independently of the actual main block that exercises the circuit.  In reality, the simulator is a sequential program and so it is designed to give the illusion that the _initial_ blocks are running in parallel.  

## Writing a Self-Checking Testbench
A testbench can have the ability to check to see if your design outputs correct answers.  Here it is for the MUX testbench above:
```
// In file tb.sv:
module tb();

  logic sel, a, b, q;   // The local signals
  int error_count = 0;  // Define an error count variable and set it to 0
  
  mux2 M0(sel, a, b, q);  // The instantiation
  
  // A function definition to help us check correctness
  function void checkData(logic expected);
    if (expected != q) begin
      $display("ERROR at time %t: got a %d but expected a %d", $time, q, expected);
      error_count += 1;
    end
  endfunction
  
  initial begin   
    sel = 0;      // Set initial values
    a = 0;
    b = 0;
    #10ns;        // Run for 10ns
    checkData(0);
    
    sel = 0;      // Do it again
    a = 1;
    b = 0;
    #10ns;
    checkData(1);
    
    sel = 1;      // And again...
    a = 1;
    b = 0;
    #10ns;
    checkData(0);
    
    // and so on...
    
  end
endmodule
```

This testbench uses a function to check correctness and has a _$display()_ function to print messages to the console.  

SystemVerilog supports not only functions, but also _tasks_.  A task is like a function except a) it **cannot** return a value and b) it **can** advance simulation time.  Using a task, the above testbench could be rewritten like this:
```
module tb();

  logic sel, a, b, q;   // The local signals
  int error_count = 0;  // Define an error count variable and set it to 0

  mux2 M0(sel, a, b, q);  // The instantiation

  // A function definition to help us check correctness
  function void checkData(logic expected);
    if (expected != q) begin
      $display("ERROR at time %t: got a %d but expected a %d", $time, q, expected);
      error_count += 1;
    end
  endfunction

  task applyValuesAndCheck(logic sin, ain, bin, expected);
    sel = sin;
    a = ain;
    b = bin;
    #10ns;
    checkData(expected);
  endtask

  initial begin   
    applyValuesAndCheck(0, 0, 0, 0);
    applyValuesAndCheck(0, 1, 0, 1);
    applyValuesAndCheck(1, 1, 0, 0);

    // and so on...
    
  end
endmodule
```

The testbench just got much, much shorter (and simpler). Importantly, the actual interesting stuff (the values to apply and the expected answers) are concentrated in just a few lines of code, making it (a) easy to understand and (b) easy to add new input combinations without much typing.

Also, since SystemVerilog _is_ a full-featured programming language it has features so that the list of inputs and expected values could be stored in an array, read from a file, etc. 

A similar structure could be applied to the construction of a testbench for a sequential circuit.  

## Using $finish
By default, when you start a simulation in Vivado it will run for a set amount of time (1000ns) and then stop, awaiting further input from you.

If you want your simulation to quit before that, you can stop it early by putting a **$finish** call into your testbench like this:
```
    ...

    clr = 0;
    #100ns;
      
    $finish;
  end
endmodule
```

The simulation will stop and return control to the GUI.  At this point, if you want you can continue simulating using the Tcl console or the buttons at the top of the simulation window.

A good use for this is to always put a **$finish** in your testbench where you know it finishes its testing (which may be 100000's of ns into the simulation.  Then, once the simulation runs the first 1000ns, you can type:
```
  run -all
```
in the console window which instructs the simulator to run until it hits a **$finish** command.  This way you don't have to know precisely at what time your simulation will end.  

If you do this, the simulator will print a message to the Tcl console when it finishes, telling you when it ended and why:
```
  $finish called at time : 2640 ns : File "/home/nelson/cnt/cnt.srcs/sources_1/new/tb.sv" Line 61
```

## Printing a Simulation Summary
You will notice in the testbenches above an error count signal was incremented every time an error occurs.  It makes sense to print a summary statement of the number of errors that occurred before the $finish statement is executed.

In fact, you might save all kinds of simulation statistics in your testbench (numbers of tests conducted, what input combinations were covered, ...).  You could then define a function to call before calling **$finish** which prints out a detailed simulation report.  **CAUTION:** recent versions of Vivado have a bug (not yet fixed) where you cannot call **$finish** from inside a function.  So, put your **$finish** statement in the _initial_ block and not inside a function which gets called from the _initial_ block.

## Debugging in Simulation 
The Vivado simulator has debug capabilities similar to what you find in programming language tools (like gdb for example).  Once you are in simulation mode you can open up your testbench and set breakpoints at various lines.  The simulation will stop when it gets to those lines.  

How do you set a breakpoint?  It is pretty simple - the large circles next to each executable line of testbench code are the breakpoint markers.  Click one, it becomes solid colored, and you have now set a breakpoint at that line.  Click it again, it becomes open, and you have unset the breakpoint.

Experiment with the features of the simulator to learn what else it has to offer.

## Moving On
If you have read this far, you are definitely interested in learning to simulate more effectively using testbenches. 

Where to go to next? A web search for "verilog testbench" or "systemverilog testbench" will turn up many, many tutorials on the subject.  But, some words of CAUTION are in order:  
  * There is, frankly, a lot of junk out there on the web regarding testbench design so be careful.  For example, some will advocate changing the inputs at the rising of the clock (bad idea - that will create a race).  
  * Many will attempt to fix the above bad practice using **#0** delays (don't even ask what these are for --- they are a kludgy patch on an already bad design practice).  Instead it is easiest to stick with what was shown above --- changing inputs on the falling edge of the clock is a commonly accepted practice that avoids a number of race problems.  Later, you will learn that SystemVerilog has automated features to give you even better control on when to apply inputs and when to sample outputs.
  * A final challenge you will have is that if you search for "systemverilog testbench" you will likely find some advanced materials on using the object oriented SystemVerilog features to create very sophisticated testbenches. While this is good, learning this is significant undertaking (we teach an entire class on it) and it might be beyond what you are looking for at this point in time.

So, what to do to learn more?  The basic structure above is very good for typical testbenches.  
* Through the use of functions and tasks you can organize and make your testbenches even more efficient.  They can start to look and feel like regular programming code as long as you remember that there is a clock, simulation time is passing, and you are driving values into a circuit model.
* Learn about SystemVerilog's other control structures: loops, file creation/reading/writing, and the like.
* Learn about SystemVerilog's data structures.  It has arrays, queues, structs, objects, etc.
* Learn how to create randomized inputs (SystemVerilog has functions to generate random values) to drive into your design.  If you do this, however, your self-checking testbench will need a new twist - it will need a Golden Model to check whether the circuit did the right thing.  That is, after you drive a random input into your DUT, you then call a function you have written which computes what the DUT should have done.  Then, once you get the DUT's output back you can call a function to see if it did the same thing that the Golden Model did.  If they don't match you have found a design error in your DUT.  

### Randomized Input Testing and Golden Testbenches
But, you say, the last point above about randomized inputs requires you to write a Golden Model which has the same functionality as the DUT.  Doesn't that mean you have do a whole 2nd design to write the Golden Model?

NO!  Your DUT is likely a complex sequential circuit which takes multiple clock cycles to compute a result.  It has to interact with memory controllers and I/O subsystems to do its work.  It is likely controlled by a complex finite state machine.  And, it has to contain only synthesizable SystemVerilog code using just the data types that the synthesizer understands (signals containing one or more bits). 

In contrast, your Golden Model can be essentially a high level program written in SystemVerilog (it does not get synthesized - it exists only for simulation).  It need not model the cycle by cycle behavior of the DUT - it just needs to compute the same result for comparison purposes.  It can use any data type and data structure supported by SystemVerilog such as integers, arrays, fifos, and even objects.  

A classical example would be for a simple microprocessor design.  The DUT may take 3-10 cycles to execute each instruction and have to interact with a memory controller and a buss and ...  The Golden Model can just be a function which contains a big CASE statement to compute what the new register values, flags, and memory contents should be given the current design state and a new instruction.  It stores those register values, flag, and memory contents in arrays of values.  

It has no timing, it knows nothing about clock cycles.  In short, it is a fairly trivial model to write.  Then, during simulation, every time your testbench knows an instruction has completed it can compare the Golden Model's state representation with that in the DUT to see if the DUT has executed correctly.

## Other Resources To Learn More
If you would like to learn more, here are some ideas:

1. Read through the testbenches used in your digital design class labs.  Many are written in basic Verilog but some are SystemVerilog.  You can learn from all of them but focus on the SystemVerilog one(s).  They were written later and follow the concepts described in this document.
1. In the past we have taught SystemVerilog-based testing as a grad course in the department.  Talk to the CpE faculty to learn more.
1. The best book I know of on the subject is: "SYSTEMVERILOG FOR VERIFICATION - A Guide to Learning the Testbench Language Features", Third Edition by Spear and Tumbush, 2011.  It is what we use in our class here at BYU.

---------------------------------------
Created by Brent Nelson, March 2020.