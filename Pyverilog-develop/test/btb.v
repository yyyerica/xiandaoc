`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2019/05/28 16:23:22
// Design Name: 
// Module Name: btb
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


module btb(
    input clk,
    input pe,
    input BranchE,
    input [31:0]PCE,
    input [31:0]BrNPC,
    input [2:0]BranchTypeE,
    input [31:0]addr,
    output reg [31:0]paddr,
    output reg [31:0]branchaddr,
    output reg pd,
    output reg exist,
    output  reg notflush
    );
    
    reg  [26:0]bramp[7:0];
     reg  [31:0]bram[7:0];
    reg  [7:0]valid;
        reg [31:0]hit;
    reg [31:0]nothit;
    
     initial valid = 0;
      initial pd = 0;
        initial hit= 0;
          initial nothit = 0;

   
   always@(*)
   begin
      if(pe&BranchE==1)
      notflush<=1;
      else if(BranchTypeE!=0&pe==0&BranchE==0)
       notflush<=1;
       else 
        notflush<=0;
   end   
      
   
    always@(*)
    begin
    if(PCE==addr&BranchTypeE!=0)
       begin
        if(BranchE)
         begin
         paddr<=BrNPC;
         branchaddr<=BrNPC;
         pd<=1;  
         end
         else 
         begin
         paddr<=PCE+4;
         branchaddr<=BrNPC;
         pd<=0;
         end
       end
    else
    begin
        if(valid[addr[4:2]]==1&bramp[addr[4:2]]==addr[31:5])
        begin
            paddr<=bram[addr[4:2]];
            branchaddr<=bram[addr[4:2]];
            pd<=1;
        end
        else if(BranchTypeE!=0&pe==1&BranchE==0)
        begin
           pd=0;
           paddr<=PCE+4;
           branchaddr<=bram[addr[4:2]];
            end
            else
            begin
            paddr<=addr+4;
            end
            
    end
    end
    
    
      always@(posedge clk)
      begin
          if(BranchTypeE!=0)
          begin
             if(pe==0)
             begin
             bramp[PCE[4:2]]<=PCE[31:5];
             bram[PCE[4:2]]<=BrNPC;
             valid[PCE[4:2]]<=1;
             end
             else
             begin
             if(BranchE)
             begin
                bramp[PCE[4:2]]<=PCE[31:5];
                 bram[PCE[4:2]]<=BrNPC;
                  valid[PCE[4:2]]<=1;   
             end
             else
             begin
            //  valid[PCE[4:2]]<=0;            
             end
             end     
          end
      end
      
    always@(*)
    begin
    if(valid[PCE[4:2]]==1&bramp[PCE[4:2]]==PCE[31:5])
    exist<=1;
    else
    exist<=0;  
    end
    
    
   always@(negedge clk)
    begin
    if(BranchTypeE!=0)
    begin
    if(notflush)
    hit<=hit+1;
    else
    nothit<=nothit+1;
    end
    end
      

endmodule