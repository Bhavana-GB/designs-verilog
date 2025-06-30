def generate_testbench_from_graph(G, module_name="multi_level_circuit"):
    codetb = []
    codetb.append(f"module {module_name}_tb;")

    # Clock
    codetb.append("  reg clk;")

    # Inputs and outputs
    inputs = sorted([n for n in G.nodes if G.nodes[n]["type"] == "input"])
    outputs = sorted([n for n in G.nodes if G.nodes[n]["type"] == "output"])

    if inputs:
        codetb.append(f"  reg {', '.join(inputs)};")
    if outputs:
        codetb.append(f"  wire {', '.join(outputs)};")

    # Instantiate DUT
    port_bindings = [f".{p}({p})" for p in inputs + ['clk'] + outputs]
    codetb.append(f"  {module_name} uut ({', '.join(port_bindings)});")

    # Clock process
    codetb.append("  initial clk = 0;")
    codetb.append("  always #5 clk = ~clk;")

    # Stimulus
    codetb.append("  initial begin")
    codetb.append("    $dumpfile(\"wave.vcd\");")
    codetb.append("    $dumpvars(0, uut);")

    # Reset all inputs
    codetb.append("    " + "; ".join(f"{i} = 0" for i in inputs) + "; #10;")

    # Sample test vectors
    for cycle in range(4):
        values = [(f"{i} = {((cycle >> idx) & 1)}") for idx, i in enumerate(inputs)]
        codetb.append("    " + "; ".join(values) + "; #10;")

    codetb.append("    $finish;")
    codetb.append("  end")
    codetb.append("endmodule")

    return "\n".join(codetb)


from tb_gen import generate_testbench_from_graph

# ... existing graph and Verilog generation ...
with open("multi_level_circuit_tb.v", "w") as f:
    f.write(generate_testbench_from_graph(G))
