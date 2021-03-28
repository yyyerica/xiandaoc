`timescale 1ns / 1ps








module ram1(clk,rst,indata,outdata);
           input clk;
           input rst;
           input CIN;
           input[31:0]indata;
           output[31:0]outdata;
           
           ram u1(
                  .clk(clk&&x),
                  .rst(rst),
                  .in(indata),
                  .out(outdata)
                  );
          reg x1; 
          reg qqq; reg qx,qqx,fx;
          always@(*)
           begin
          qx<=x1;
            end



function [1:0] ADD; 
input A, B, CIN;
reg S, COUT;
begin
S = A ^ B ^ CIN; 
COUT = (A&B) | (A&CIN) | (B&CIN); 
ADD = {COUT, S};
end
endfunction

endmodule

module ram(clk,rst,in,out);
           input clk;
           input rst;
           input[31:0]in;
           output[31:0]out;
           assign out= in;
           reg x1;
           reg qx;

endmodule
