//Python Generated
module multi_level_circuit_tb;
  reg clk;
  reg d0, d1;
  wire q0, q1;
  multi_level_circuit uut (.d0(d0), .d1(d1), .clk(clk), .q0(q0), .q1(q1));
  initial clk = 0;
  always #5 clk = ~clk;
  initial begin
    d0 = 0; d1 = 0; #10;
    d0 = 0; d1 = 0; #10;
    d0 = 1; d1 = 0; #10;
    d0 = 0; d1 = 1; #10;
    d0 = 1; d1 = 1; #10;
    $finish;
  end
endmodule