`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: USTC ESLAB（Embeded System Lab）
// Engineer: Haojun Xia
// Create Date: 2019/02/08
// Design Name: RISCV-Pipline CPU
// Module Name: ControlUnit
// Target Devices: Nexys4
// Tool Versions: Vivado 2017.4.1
// Description: RISC-V Instruction Decoder
//////////////////////////////////////////////////////////////////////////////////
`include "Parameters.v"   
module ControlUnit(
    input  [6:0] Op,
    input  [2:0] Fn3,
    input  [6:0] Fn7,
    output  JalD,
    output  JalrD,
    output reg [2:0] RegWriteD,
    output  MemToRegD,
    output reg [3:0] MemWriteD,
    output  LoadNpcD,
    output reg [1:0] RegReadD,
    output reg [2:0] BranchTypeD,
    output reg [3:0] AluContrlD,
    output  [1:0] AluSrc2D,
    output  AluSrc1D,
    output reg [2:0] ImmType        
    );
    //
    wire [6:0] x,y;
    assign AluSrc1D=x[0];
  
    
endmodule
