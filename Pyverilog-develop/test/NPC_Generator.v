`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////?
// Engineer: Haojun Xia
// Create Date: 2019/03/14 11:21:33
// Design Name: RISCV-Pipline CPU
// Module Name: NPC_Generator
// Target Devices: Nexys4
// Tool Versions: Vivado 2017.4.1
// Description: Choose Next PC value
//////////////////////////////////////////////////////////////////////////////////
module NPC_Generator(
    input wire [2:0]BranchTypeE,
    input wire notflush,
    input wire [31:0]paddr,
    input wire p,
    input wire [31:0] PCF,JalrTarget, BranchTarget, JalTarget,
    input wire BranchE,JalD,JalrE,
    output reg [31:0] PC_In
    );
    always @(*)
    begin
        if(JalrE)
            PC_In <= JalrTarget;
        else if(BranchE&notflush==0)
            PC_In <= BranchTarget;
        else if(JalD)
            PC_In <= JalTarget;
        else
          if(p|(BranchE==0&BranchTypeE!=0&notflush==0))
       PC_In <=paddr;
         else
            PC_In <= PCF+4;
    end
endmodule
