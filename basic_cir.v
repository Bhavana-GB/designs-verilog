// Auto-generated logic circuit: AND followed by OR

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


`celldefine
module or_gate_2 (
    input a, b,
    output y
);
    assign y = a | b;

    specify
        (a => y) = (1:1:1);
        (b => y) = (1:1:1);
    endspecify
endmodule
`endcelldefine


module logic_gate_test (
    input a, b, c,
    output y
);
    wire and1, or1;
    and_gate_2 and1_inst (.a(a), .b(b), .y(and1));
    or_gate_2 or1_inst (.a(and1), .b(c), .y(or1));
    assign y = or1;
endmodule