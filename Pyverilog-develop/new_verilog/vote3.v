`timescale 1ns / 1ps







   module vote3(r3,r);
            input [2:0] r3;
            output r;
          
   assign r=(r3[0]&&r3[1]&&(~r3[2]))
            ||(r3[0]&&(~r3[1])&&r3[2])
            ||((~r3[0])&&r3[1]&&r3[2])
            ||(r3[0]&&r3[1]&&r3[2]);

   endmodule
