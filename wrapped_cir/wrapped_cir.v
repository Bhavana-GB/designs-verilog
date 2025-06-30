//Python Generated
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
        (a => y) = 1;
        (b => y) = 1;
    endspecify
endmodule
`endcelldefine

module circular_and_circuit (
    input clk, d0, d1,
    output q0, q1
);
    wire q1_0, q1_1, q2_0, q2_1, and1_0, and1_1;
    dff_spec q1_0_inst (.clk(clk), .d(d0), .q(q1_0));
    dff_spec q1_1_inst (.clk(clk), .d(d1), .q(q1_1));
    dff_spec q2_0_inst (.clk(clk), .d(and1_0), .q(q2_0));
    dff_spec q2_1_inst (.clk(clk), .d(and1_1), .q(q2_1));
    and_gate_2 and1_0_inst (.a(q1_0), .b(q1_1), .y(and1_0));
    and_gate_2 and1_1_inst (.a(q1_1), .b(q1_0), .y(and1_1));
    assign q0 = q2_0;
    assign q1 = q2_1;
endmodule