`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2019/05/28 16:25:00
// Design Name: 
// Module Name: bht
// Project Name: 
// Target Devices: 
// Tool Versions: 
// Description: 
// 
// Dependencies: 
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
//////////////////////////////////////////////////////////////////////////////////


module bht(
input clk,
input pe,
input BranchE,
input [31:0]PCE,
input [31:0]BrNPC,
input [2:0]BranchTypeE,
input [31:0]addr,
output reg [31:0]paddrf,
output reg pdf,
output   notflush
    );
   wire[31:0]paddr;
   wire pd;
   wire [31:0]branchaddr;
        wire exist;
     btb btb1 (
    .clk(clk),
    .pe(pe),
    .BranchE( BranchE),
    .PCE(PCE),
    .BrNPC(BrNPC),
    .BranchTypeE(BranchTypeE),
   .addr(addr),
   .paddr(paddr),
   .branchaddr(branchaddr),
   .pd(pd),
   .exist(exist),
   .notflush(notflush)
     );
     reg [1:0]bhtbuffer[7:0];
      initial 
        begin
      bhtbuffer[0]=0;
      bhtbuffer[1]=0;
      bhtbuffer[2]=0;
      bhtbuffer[3]=0;
      bhtbuffer[4]=0;
      bhtbuffer[5]=0;
      bhtbuffer[6]=0;
       bhtbuffer[7]=0;
      end
      
     always@(posedge clk)
     begin
     if(BranchTypeE!=0)
        if(exist)
         begin
           case(bhtbuffer[PCE[4:2]])
           0: bhtbuffer[PCE[4:2]]<=(BranchE)?1:0;
           1: bhtbuffer[PCE[4:2]]<=(BranchE)?3:0;
           2: bhtbuffer[PCE[4:2]]<=(BranchE)?3:0;
           3: bhtbuffer[PCE[4:2]]<=(BranchE)?3:2;
            default:bhtbuffer[PCE[4:2]]<=0;
           endcase
         end
        else
          bhtbuffer[PCE[4:2]]<=(BranchE)?1:0;
     end
     
     
      always@(*)
      begin  
      case(bhtbuffer[addr[4:2]]) 
      0: pdf<=0;
      1: pdf<=0;
      2: pdf<=pd;
      3: pdf<=pd;
     endcase 
     end
     
     
   always@(*)
     begin 
     if(BranchE==0&BranchTypeE!=0&notflush==0)
      paddrf<=PCE+4;
     else
      if(pdf)
      paddrf<=branchaddr;
      else
      paddrf<=addr+4;
    end
 
 
endmodule
