
==================================================
TOP‑LEVEL LAYOUT (pr5/)
==================================================

Directory:

```
pr5/
│
├── programs/
│   ├── asms/        ← your hand‑written assembly programs
│   └── custom/      ← crt.S, encoding.h, test.ld
│
└── src/
    └── Processors/
        ├── Single_cycle/  ← single‑cycle RISC‑V CPU simulator
        └── Pipeline/      ← 5‑stage pipeline RISC‑V CPU simulator
```

==================================================
README SECTION — programs/
==================================================

### programs/asms/
Contains **your own RISC‑V assembly programs** written as part of Lab‑1 and other labs.  
These files are assembled and linked using the custom startup code (crt.S) and linker script (test.ld).  
Running `make all` collects these assembly files and produces binary `.o` or ELF files inside `programs/bins/`.

These binaries are used as:

• input to Spike simulator, and  
• input to your custom RISC‑V CPU simulator in `src/Processors`.

### programs/custom/
Contains low‑level runtime support files required to produce valid RISC‑V executables for Spike and your simulator:

| File | Description |
|------|-------------|
| **crt.S** | Startup code (C runtime). Initializes registers, FPU, trap handler, sets `gp`, allocates stack, calls `main`, handles exit via Spike `tohost`. Required before any RISC‑V assembly runs. |
| **encoding.h** | RISC‑V privileged architecture constants. Defines CSR bit masks (mstatus, mip, mie), interrupt IDs, PMP bits, SATP modes, PTE flags, and helpers like `read_csr()`. Used by crt.S and assembly programs. |
| **test.ld** | Linker script describing where text/data/bss should be placed in memory. Places code at 0x80000000 (Spike DRAM base), defines `.text.init`, `.text`, `.tohost`, `.data`, `.bss`, TLS, and sets entry `_start`. Required to produce correct ELF layout. |

==================================================
README SECTION — src/Processors/
==================================================

This folder contains two RISC‑V CPU simulators:

### 1. Single‑cycle processor (Single_cycle/)
Simulates each RISC‑V instruction in **one cycle**.  
Used for simpler testing, debugging, and comparison with the pipeline.

Important files:

| File | Purpose |
|------|---------|
| **main.py** | Loads ELF, parses memory, and runs the single‑cycle CPU for N cycles. |
| **Processor.py** | Implements one‑cycle execute loop: fetch → decode → execute → memory → writeback. |
| **Hardware.py** | ALU, control unit, immediate generator. |
| **RegisterFile.py** | 32 architectural registers (x0–x31). |
| **Memory.py** | Simulated RAM for instructions & data (supports loads/stores). |
| **LoadSection.py** | Loads `.text.init`, `.text`, `.data` into RAM. |
| **Disassemble.py** | Decodes binary instructions into human‑readable form. |
| **readElf.py** | Extracts ELF sections. |
| **SupportedFun.py** | Helper functions: binary↔int, two's complement, sign‑extend, etc. |
| **observation.txt** | Notes/outputs recorded during development. |

==================================================
README SECTION — Pipeline processor (Pipeline/)
==================================================

A full **5‑stage pipelined RISC‑V processor simulator**:

Stages & their files:
- IF → **FetchDecodeReg.py**
- ID → **DecodeExecuteReg.py**
- EX → **ExecuteMemReg.py**
- MEM → **MemWbReg.py**
- WB → handled inside Processor.writeBack()

Pipeline features implemented:
• Forwarding unit  
• Stall handling (load‑use hazard)  
• Branch flush logic  
• Separate pipeline registers  
• ALU + control unit logic  

Description of each file:

| File | Purpose |
|------|---------|
| **main.py** | Loads ELF sections, initializes memory, runs the pipelined simulation for N cycles. |
| **Processor.py** | Core CPU pipeline: orchestrates IF → ID → EX → MEM → WB per cycle, manages hazards, flushes, forwarding, and program counter updates. Prints execution trace. |
| **Clock.py** | Maintains global cycle counter; provides posEdgeClk (clock tick). |
| **FetchDecodeReg.py** | Pipeline register between IF and ID. Holds fetched instruction and PC. |
| **DecodeExecuteReg.py** | Pipeline register between ID and EX. Stores decoded fields, control signals, immediates, register values. |
| **ExecuteMemReg.py** | EX/MEM pipeline register. Stores ALU results, branch targets, memory addresses. |
| **MemWbReg.py** | MEM/WB pipeline register. Stores values to be written back to registers. |
| **StallHardware.py** | Provides logic for stalling pipeline on hazards (load‑use). |
| **Hardware.py** | ALU, control unit, immediate generator, forwarding unit, ALU‑control logic. |
| **Memory.py** | Simulated RAM for instructions and data (maps ELF addresses to arrays). |
| **LoadSection.py** | Loads ELF segments into memory—identical to single‑cycle version. |
| **registerFile.py** | Implements the 32 registers with appropriate RISC‑V semantics. |
| **Disassemble.py** | Human‑readable decoding of instructions for output. |
| **readElf.py** | Reads `.text.init`, `.text`, `.data` from compiled ELF. |

==================================================
README SECTION — How Simulation Works
==================================================

1. You write assembly in `programs/asms/`.
2. `make all` compiles it using:
   - custom crt.S  
   - custom encoding.h  
   - custom test.ld  
3. It produces ELF files in:
   ```
   programs/bins/
   ```
4. These ELF files can be executed in *two ways*:

#### A. On Spike (ISA simulator)
```
spike --isa=rv32im test.elf
```

#### B. On your Python RISC‑V processor simulator
```
cd src/Processors/Pipeline/
python main.py <binary-name-without-extension>
```
Example:
```
python main.py add
```

==================================================
README SECTION — Summary
==================================================

Use the following text as your README summary:

**This project implements a complete RISC‑V simulation environment**, including:

• Custom startup/runtime environment (crt.S, linking, encoding)  
• ELF loading and memory mapping  
• A working **single‑cycle RISC‑V CPU** simulator  
• A fully functional **5‑stage pipelined RISC‑V CPU** with hazards, forwarding, stalls  
• Programs written in pure assembly that run both on **Spike** and on the custom CPU  

The simulator executes real ELF binaries, not hardcoded instructions—making it a true model of the hardware.

