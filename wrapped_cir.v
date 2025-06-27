// Auto-generated circular AND + FF graph circuit

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
module and_gate_2 (
    input a, b,
    output y
);
    assign y = a & b;
    specify
        (a => y) = (1:1:1);
        (b => y) = (1:1:1);
    endspecify
endmodule
`endcelldefine


module circular_and_circuit (
    input clk, d0, d1, d2,
    output q0, q1, q2
);
    wire q1_0, q1_1, q1_2, q2_0, q2_1, q2_2, q3_0, q3_1, q3_2, and1_0, and1_1, and1_2, and2_0, and2_1, and2_2;
    dff_spec q1_0_inst (.clk(clk), .d(d0), .q(q1_0));
    dff_spec q1_1_inst (.clk(clk), .d(d1), .q(q1_1));
    dff_spec q1_2_inst (.clk(clk), .d(d2), .q(q1_2));
    dff_spec q2_0_inst (.clk(clk), .d(and1_0), .q(q2_0));
    dff_spec q2_1_inst (.clk(clk), .d(and1_1), .q(q2_1));
    dff_spec q2_2_inst (.clk(clk), .d(and1_2), .q(q2_2));
    dff_spec q3_0_inst (.clk(clk), .d(and2_0), .q(q3_0));
    dff_spec q3_1_inst (.clk(clk), .d(and2_1), .q(q3_1));
    dff_spec q3_2_inst (.clk(clk), .d(and2_2), .q(q3_2));
    and_gate_2 and1_0_inst (.a(q1_0), .b(q1_1), .y(and1_0));
    and_gate_2 and1_1_inst (.a(q1_1), .b(q1_2), .y(and1_1));
    and_gate_2 and1_2_inst (.a(q1_2), .b(q1_0), .y(and1_2));
    and_gate_2 and2_0_inst (.a(q2_0), .b(q2_1), .y(and2_0));
    and_gate_2 and2_1_inst (.a(q2_1), .b(q2_2), .y(and2_1));
    and_gate_2 and2_2_inst (.a(q2_2), .b(q2_0), .y(and2_2));
    assign q0 = q3_0;
    assign q1 = q3_1;
    assign q2 = q3_2;
endmodule