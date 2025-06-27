// Auto-generated Verilog design

module dff_spec (
    input clk,
    input d,
    output reg q
);
    always @(posedge clk)
        q <= d;

    specify
        (posedge clk => (q : d)) = (3:3:3); 
        $setup(d, posedge clk, 2);
        $hold(d, posedge clk, 1);
    endspecify
endmodule


`celldefine
module and_gate_3 (
    input in0, in1, in2,
    output y
);
    assign y = in0 & in1 & in2;

    specify
        (in0 => y) = (1:1:1);
    (in1 => y) = (1:1:1);
    (in2 => y) = (1:1:1);
    endspecify
endmodule
`endcelldefine


module multi_level_circuit (
    input clk,
    input d0,
    input d1,
    input d2,
    output q0,
    output q1,
    output q2
);
    wire q1_0, q1_1, q1_2;
    wire q2_0, q2_1, q2_2;
    wire q3_0, q3_1, q3_2;
    wire and1_out;
    wire and2_out;
    dff_spec ff1_0 (.clk(clk), .d(d0), .q(q1_0));
    dff_spec ff1_1 (.clk(clk), .d(d1), .q(q1_1));
    dff_spec ff1_2 (.clk(clk), .d(d2), .q(q1_2));
    and_gate_3 and_inst_1 (.y(and1_out), .in0(q1_0), .in1(q1_1), .in2(q1_2));
    dff_spec ff2_0 (.clk(clk), .d(and1_out), .q(q2_0));
    dff_spec ff2_1 (.clk(clk), .d(and1_out), .q(q2_1));
    dff_spec ff2_2 (.clk(clk), .d(and1_out), .q(q2_2));
    and_gate_3 and_inst_2 (.y(and2_out), .in0(q2_0), .in1(q2_1), .in2(q2_2));
    dff_spec ff3_0 (.clk(clk), .d(and2_out), .q(q3_0));
    dff_spec ff3_1 (.clk(clk), .d(and2_out), .q(q3_1));
    dff_spec ff3_2 (.clk(clk), .d(and2_out), .q(q3_2));
    assign q0 = q3_0;
    assign q1 = q3_1;
    assign q2 = q3_2;
endmodule