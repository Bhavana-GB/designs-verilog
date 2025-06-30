def generate_tb_cascade(rows, module_name="cascading_and"):
    # print("Inside generate_tb_cascade")

    codetb = []
    codetb.append("`timescale 1ns / 1ps\n")
    codetb.append(f"module tb_{module_name};\n")

    # Inputs
    codetb.append("    // Inputs")
    codetb.append("    reg clk;")
    d_regs = ", ".join([f"d{i}" for i in range(rows)]) + ";"
    codetb.append(f"    reg {d_regs}")

    # Outputs
    codetb.append("\n    // Outputs")
    out_wires = ", ".join([f"q{i}" for i in range(rows)]) + ";"
    codetb.append(f"    wire {out_wires}")

    # Instantiate DUT
    codetb.append(f"\n    // Instantiate DUT")
    codetb.append(f"    {module_name} uut (")
    codetb.append("        .clk(clk),")
    for i in range(rows):
        codetb.append(f"        .d{i}(d{i}),")
    for i in range(rows):
        comma = "," if i < rows - 1 else ""
        codetb.append(f"        .q{i}(q{i}){comma}")
    codetb.append("    );\n")

    # Clock gen
    codetb.append("    // Clock gen")
    codetb.append("    initial begin")
    codetb.append("        clk = 0;")
    codetb.append("        forever #5 clk = ~clk;")
    codetb.append("    end\n")

    # Stimulus block
    codetb.append("    // Stimulus")
    codetb.append("    initial begin")
    codetb.append(f'        $display("Time\\tclk\\t{" ".join([f"d{i}" for i in range(rows)])}\\t{" ".join([f"q{i}" for i in range(rows)])}");')
    monitor_fmt = "%0t\t%b\t" + "  %b" * rows + "\t" + "  %b" * rows
    monitor_vars = ", ".join(["$time", "clk"] + [f"d{i}" for i in range(rows)] + [f"q{i}" for i in range(rows)])
    codetb.append(f'        $monitor("{monitor_fmt}", {monitor_vars});\n')

    # Test
    vectors = [
        [0] * rows,
        [1 if i == 0 else 0 for i in range(rows)],
        [1 if i < rows // 2 else 0 for i in range(rows)],
        [1] * rows,
        [1 if i % 2 == 0 else 0 for i in range(rows)],
        [0 if i % 2 == 0 else 1 for i in range(rows)],
    ]

    for vec in vectors:
        for i, bit in enumerate(vec):
            codetb.append(f"        d{i} = {bit};")
        codetb.append("        #20;\n")

    codetb.append("        $finish;")
    codetb.append("    end\nendmodule")
    return "\n".join(codetb)

    