// Auto-generated 3-level FF chain with AND gates

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


module multi_level_ff_chain (
    input clk, d0, d1, d2,
    output q0, q1, q2
);
    wire q1_0, q1_1, q1_2, q2_0, and1, q2_1, q2_2, q3_0, and2, q3_1, q3_2;
    dff_spec q1_0_inst (.clk(clk), .d(d0), .q(q1_0));
    dff_spec q1_1_inst (.clk(clk), .d(d1), .q(q1_1));
    dff_spec q1_2_inst (.clk(clk), .d(d2), .q(q1_2));
    dff_spec q2_0_inst (.clk(clk), .d(and1), .q(q2_0));
    dff_spec q2_1_inst (.clk(clk), .d(and1), .q(q2_1));
    dff_spec q2_2_inst (.clk(clk), .d(and1), .q(q2_2));
    dff_spec q3_0_inst (.clk(clk), .d(and2), .q(q3_0));
    dff_spec q3_1_inst (.clk(clk), .d(and2), .q(q3_1));
    dff_spec q3_2_inst (.clk(clk), .d(and2), .q(q3_2));
    and_gate_3 and1_inst (.a(q1_0), .b(q1_1), .c(q1_2), .y(and1));
    and_gate_3 and2_inst (.a(q2_0), .b(q2_1), .c(q2_2), .y(and2));
    assign q0 = q3_0;
    assign q1 = q3_1;
    assign q2 = q3_2;
endmodule