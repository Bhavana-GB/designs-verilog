def generate_dff_module():
    return """\
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
"""

def generate_and_gate_module(input_count=3):
    assert input_count >= 2, "AND gate needs at least 2 inputs"
    inputs = ", ".join([f"in{i}" for i in range(input_count)])
    delays = "\n    ".join([f"({f'in{i}'} => y) = (1:1:1);" for i in range(input_count)])
    and_expr = " & ".join([f"in{i}" for i in range(input_count)])

    return f"""\
`celldefine
module and_gate_{input_count} (
    input {inputs},
    output y
);
    assign y = {and_expr};

    specify
        {delays}
    endspecify
endmodule
`endcelldefine
"""

def generate_multi_level_circuit(levels=2, width=3):
    codev = []
    codev.append("module multi_level_circuit (\n    input clk,")

    # input ports
    for i in range(width):
        codev.append(f"    input d{i},")
    # output ports
    for i in range(width):
        comma = ',' if i < width - 1 else ''
        codev.append(f"    output q{i}{comma}")
    codev.append(");")

    # Declaring all wires (grouped)
    for lvl in range(1, levels + 1):
        wire_list = ", ".join([f"q{lvl}_{i}" for i in range(width)])
        codev.append(f"    wire {wire_list};")

    if levels >= 2:
        for lvl in range(2, levels + 1):
            codev.append(f"    wire and{lvl - 1}_out;")

    # Level 1 Flip-Flops 
    for i in range(width):
        codev.append(f"    dff_spec ff1_{i} (.clk(clk), .d(d{i}), .q(q1_{i}));")

    # Intermediate levels
    for lvl in range(2, levels + 1):
        # Instantiate AND gate
        inputs = ", ".join([f"q{lvl - 1}_{i}" for i in range(width)])
        and_gate_ports = ", ".join([f".in{i}(q{lvl - 1}_{i})" for i in range(width)])
        codev.append(f"    and_gate_{width} and_inst_{lvl - 1} (.y(and{lvl - 1}_out), {and_gate_ports});")
        for i in range(width):
            codev.append(f"    dff_spec ff{lvl}_{i} (.clk(clk), .d(and{lvl - 1}_out), .q(q{lvl}_{i}));")

    # Output assignment
    for i in range(width):
        codev.append(f"    assign q{i} = q{levels}_{i};")

    codev.append("endmodule")
    return "\n".join(codev)

def main():
    levels = 3
    width = 3

    with open("Python_Generated/levels3_3.v", "w") as f:
        f.write("// Auto-generated Verilog design\n\n")
        f.write(generate_dff_module())
        f.write("\n\n")
        f.write(generate_and_gate_module(width))
        f.write("\n\n")
        f.write(generate_multi_level_circuit(levels=levels, width=width))

if __name__ == "__main__":
    main()
