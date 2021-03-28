module EXAMPLE (A, B, CIN, S, COUT); 
 
input [3:0] A, B; 
input CIN; 
output [3:0] S; 
output COUT; 
 
wire [3:0] S; 
wire COUT; 
reg [1:0] S0, S1, S2, S3; 
reg  [10:0]x[10:0] ;
assign COUT=S[0];
assign COUT=S[1];
assign COUT=S[2];
assign COUT=S[3];
assign S1=x[2][1-1:0];
endmodule
