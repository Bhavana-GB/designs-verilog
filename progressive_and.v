module prog_add_and (
  input clk,
  input [2:0] in,
  output [2:0] out
);

  // Level 1 Flip-Flops
  wire q1_0, q1_1, q1_2;
  dff_spec ff1_0 (.clk(clk), .d(in[0]), .q(q1_0));
  dff_spec ff1_1 (.clk(clk), .d(in[1]), .q(q1_1));
  dff_spec ff1_2 (.clk(clk), .d(in[2]), .q(q1_2));

  //  AND Gates Between L1 → L2
  wire and1_0 = q1_0;
  wire and1_1 = q1_0 & q1_1;
  wire and1_2 = q1_0 & q1_1 & q1_2;

  // Level 2 Flip-Flops
  wire q2_0, q2_1, q2_2;
  dff_spec ff2_0 (.clk(clk), .d(and1_0), .q(q2_0));
  dff_spec ff2_1 (.clk(clk), .d(and1_1), .q(q2_1));
  dff_spec ff2_2 (.clk(clk), .d(and1_2), .q(q2_2));

  // AND Gates Between L2 → L3 
  wire and2_0 = q2_0;
  wire and2_1 = q2_0 & q2_1;
  wire and2_2 = q2_0 & q2_1 & q2_2;

  // Level 3 Flip-Flops 
  wire q3_0, q3_1, q3_2;
  dff_spec ff3_0 (.clk(clk), .d(and2_0), .q(q3_0));
  dff_spec ff3_1 (.clk(clk), .d(and2_1), .q(q3_1));
  dff_spec ff3_2 (.clk(clk), .d(and2_2), .q(q3_2));

  // Output from Level 3
  assign out = {q3_2, q3_1, q3_0};

endmodule


module dff_spec (
  input clk,
  input d,
  output reg q
);
  always @(posedge clk)
    q <= d;

  specify
    (posedge clk => (q : d)) = (3:3:3);
    $setup(d, posedge clk, 1);
    $hold(d, posedge clk, 1);
  endspecify
endmodule
