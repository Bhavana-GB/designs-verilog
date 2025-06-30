`timescale 1ns / 1ps

module tb_cascading_and;

    // Inputs
    reg clk;
    reg d0, d1;

    // Outputs
    wire q0, q1;

    // Instantiate DUT
    cascading_and uut (
        .clk(clk),
        .d0(d0),
        .d1(d1),
        .q0(q0),
        .q1(q1)
    );

    // Clock gen
    initial begin
        clk = 0;
        forever #5 clk = ~clk;
    end

    // Stimulus
    initial begin
        $display("Time\tclk\td0 d1\tq0 q1");
        $monitor("%0t	%b	  %b  %b	  %b  %b", $time, clk, d0, d1, q0, q1);

        d0 = 0;
        d1 = 0;
        #20;

        d0 = 1;
        d1 = 0;
        #20;

        d0 = 1;
        d1 = 0;
        #20;

        d0 = 1;
        d1 = 1;
        #20;

        d0 = 1;
        d1 = 0;
        #20;

        d0 = 0;
        d1 = 1;
        #20;

        $finish;
    end
endmodule