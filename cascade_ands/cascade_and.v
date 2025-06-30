module cascade_and (
    input clk,
    input d0, d1,
    output q0, q1
);
    wire q1_0, q1_1;
    wire q2_0, q2_1;
    wire and1_0, and1_1;
    dff_spec q1_0 (.clk(clk), .d(d0), .q(q1_0));
    dff_spec q1_1 (.clk(clk), .d(d1), .q(q1_1));
    dff_spec q2_0 (.clk(clk), .d(and1_0_q), .q(q2_0));
    dff_spec q2_1 (.clk(clk), .d(and1_1_q), .q(q2_1));
    and_spec #1 and1_0 (.in0(ff1_0_q), .q(and1_0_q));
    and_spec #2 and1_1 (.in0(ff1_0_q), .in1(ff1_1_q), .q(and1_1_q));
    assign q0 = q2_0;
    assign q1 = q2_1;
endmodule