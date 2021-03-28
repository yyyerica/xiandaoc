`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Engineer: Haojun Xia
// Create Date: 2019/02/08
// Design Name: RISCV-Pipline CPU
// Module Name: testBench
// Target Devices: Nexys4
// Tool Versions: Vivado 2017.4.1
// Description: This testBench Help users to initial the bram content, by loading .data file and .inst file.
//				Then give signals to start the execution of our cpu
//				When all instructions finish their executions, this testBench will dump the Instruction Bram and Data Bram's content to .txt files 
// !!! ALL YOU NEED TO CHANGE IS 4 FILE PATH BELOW !!!	
//				(they are all optional, you can run cpu without change paths here,if files are failed to open, we will not dump the content to .txt and will not try to initial your bram)
//////////////////////////////////////////////////////////////////////////////////
`define DataRamContentLoadPath "E:\\data\\btb.data"
`define InstRamContentLoadPath "E:\\data\\btb.inst"
`define DataRamContentSavePath "E:\\data\\DataRamContent.txt"
`define InstRamContentSavePath "E:\\data\\InstRamContent.txt"
`define BRAMWORDS 4096  //a word is 32bit, so our bram is 4096*32bit

module testBench(
    );
    //
    wire [31:0]PCF;
     wire [31:0]PCE;
    wire [31:0]Instr;
     wire [31:0]paddr;
     wire pd;
     wire pe;
     wire notflush;
     wire [31:0]BrNPC;
     wire  BranchE;
    reg CPU_CLK;
    reg CPU_RST;
    reg [31:0] CPU_Debug_DataRAM_A2;
    reg [31:0] CPU_Debug_DataRAM_WD2;
    reg [3:0] CPU_Debug_DataRAM_WE2;
    wire [31:0] CPU_Debug_DataRAM_RD2;
    reg [31:0] CPU_Debug_InstRAM_A2;
    reg [31:0] CPU_Debug_InstRAM_WD2;
    reg [3:0] CPU_Debug_InstRAM_WE2;
    wire [31:0] CPU_Debug_InstRAM_RD2;
    //generate clock signal
    
    // Connect the CPU core
    RV32Core RV32Core1(
        .CPU_CLK(CPU_CLK),
        .CPU_RST(CPU_RST),
        .CPU_Debug_DataRAM_A2(CPU_Debug_DataRAM_A2),
        .CPU_Debug_DataRAM_WD2(CPU_Debug_DataRAM_WD2),
        .CPU_Debug_DataRAM_WE2(CPU_Debug_DataRAM_WE2),
        .CPU_Debug_DataRAM_RD2(CPU_Debug_DataRAM_RD2),
        .CPU_Debug_InstRAM_A2(CPU_Debug_InstRAM_A2),
        .CPU_Debug_InstRAM_WD2(CPU_Debug_InstRAM_WD2),
        .CPU_Debug_InstRAM_WE2(CPU_Debug_InstRAM_WE2),
        .CPU_Debug_InstRAM_RD2(CPU_Debug_InstRAM_RD2),
        .PCF1(PCF),
         .Instr1(Instr),
          .paddr(paddr),
          .pd(pd),
          .pe(pe),
          .notflush(notflush),
          .PCE(PCE),
          .BrNPC(BrNPC),
          .BranchE( BranchE)
        );
    //define file handles
;
    //
    initial  
       begin
    forever #1 CPU_CLK = ~CPU_CLK;
    end
    
     initial  
     begin
              CPU_RST = 1'b1;
              CPU_CLK =1; 
            #10;   
          CPU_RST = 1'b0;
      end
      
  endmodule
