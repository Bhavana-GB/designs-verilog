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
        (posedge clk => (q : d)) = (1:2:3); 
        $setup(d, posedge clk, 2);
        $hold(d, posedge clk, 1);
    endspecify
endmodule
"""

def gev_v_levels2(levels=2, width=3):
    codev = []
    codev.append(f"module multi_level_circuit (\n    input clk,\n    input [{width-1}:0] in,\n    output [{width-1}:0] out\n);")

    # Level 1 Flip-Flops
    for i in range(width):
        codev.append(f"    wire q1_{i};")
    for i in range(width):
        codev.append(f"    dff_spec ff1_{i} (.clk(clk), .d(in[{i}]), .q(q1_{i}));")

    codev.append(f"    wire and1_out = " + " & ".join([f"q1_{i}" for i in range(width)]) + ";")

    # Level 2 Flip-Flops
    for i in range(width):
        codev.append(f"    wire q2_{i};")
    for i in range(width):
        codev.append(f"    dff_spec ff2_{i} (.clk(clk), .d(and1_out), .q(q2_{i}));")

    codev.append(f"    assign out = {{ {', '.join([f'q2_{i}' for i in reversed(range(width))])} }};")
    codev.append("endmodule")

    return "\n".join(codev)

def main():
    with open("Python_Generated/generated_design.v", "w") as f:
        f.write("// Code generated using Python\n\n")
        f.write(generate_dff_module())
        f.write("\n\n")
        f.write(gev_v_levels2())

if __name__ == "__main__":
    main()
