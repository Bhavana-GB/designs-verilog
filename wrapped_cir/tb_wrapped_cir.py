def generate_wrapped_testbench(G, module_name="multi_level_circuit"):
    codetb = []
    codetb.append(f"module {module_name}_tb;")

    # Clock signal
    codetb.append("  reg clk;")

    # Input and output signals (sorted for clean naming)
    inputs = sorted([n for n in G.nodes if G.nodes[n]["type"] == "input"])
    outputs = sorted([n for n in G.nodes if G.nodes[n]["type"] == "output"])

    if inputs:
        codetb.append(f"  reg {', '.join(inputs)};")
    if outputs:
        codetb.append(f"  wire {', '.join(outputs)};")

    # DUT instantiation
    port_bindings = [f".{sig}({sig})" for sig in inputs + ['clk'] + outputs]
    codetb.append(f"  {module_name} uut ({', '.join(port_bindings)});")

    # Clock generator
    codetb.append("  initial clk = 0;")
    codetb.append("  always #5 clk = ~clk;")

    # Stimulus
    codetb.append("  initial begin")
    # codetb.append("    $dumpfile(\"wave.vcd\");")
    # codetb.append("    $dumpvars(0, uut);")

    # Reset all inputs
    codetb.append("    " + "; ".join(f"{i} = 0" for i in inputs) + "; #10;")

    # generate test cases 
    max_patterns = min(2 ** len(inputs), 8) 
    for pattern in range(max_patterns):
        values = [f"{sig} = {((pattern >> idx) & 1)}" for idx, sig in enumerate(inputs)]
        codetb.append("    " + "; ".join(values) + "; #10;")

    codetb.append("    $finish;")
    codetb.append("  end")

    codetb.append("endmodule")
    return "\n".join(codetb)
