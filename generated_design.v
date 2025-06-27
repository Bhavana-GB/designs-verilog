// Code generated using Python

module dff_spec (
    input clk,
    input d,
    output reg q
);
    always @(posedge clk)
        q <= d;

    specify
        (posedge clk => (q : d)) = (1:2:3); 
        $setup(d, posedge clk, 2);
        $hold(d, posedge clk, 1);
    endspecify
endmodule


module multi_level_circuit (
    input clk,
    input [2:0] in,
    output [2:0] out
);
    wire q1_0;
    wire q1_1;
    wire q1_2;
    dff_spec ff1_0 (.clk(clk), .d(in[0]), .q(q1_0));
    dff_spec ff1_1 (.clk(clk), .d(in[1]), .q(q1_1));
    dff_spec ff1_2 (.clk(clk), .d(in[2]), .q(q1_2));
    wire and1_out = q1_0 & q1_1 & q1_2;
    wire q2_0;
    wire q2_1;
    wire q2_2;
    dff_spec ff2_0 (.clk(clk), .d(and1_out), .q(q2_0));
    dff_spec ff2_1 (.clk(clk), .d(and1_out), .q(q2_1));
    dff_spec ff2_2 (.clk(clk), .d(and1_out), .q(q2_2));
    assign out = { q2_2, q2_1, q2_0 };
endmodule