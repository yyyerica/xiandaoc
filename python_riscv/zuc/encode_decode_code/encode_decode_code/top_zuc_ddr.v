`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2021/02/22 16:57:25
// Design Name: 
// Module Name: top_zuc_ddr
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

module top_zuc_ddr(
	input				clk,
    input               reset_n,
    input	[127:0]		input_key,
    input   [127:0]     input_iv,
    input   [127:0]     input_data,
    output  [127:0]     out_data
    
    );
    reg [127:0]     out_data;
    //reg     [127:0]     input_data;
    (*mark_debug = "true"*)  reg                  i_ready;
    (*mark_debug = "true"*)  reg                  i_reset_n;
    (*mark_debug = "true"*)  wire                 s_valid;
    
    (*mark_debug = "true"*)  reg     [127:0]     key_data;
    
    (*mark_debug = "true"*)  reg                 i_init;
    (*mark_debug = "true"*)  reg 	   [127:0]	   i_key;
    (*mark_debug = "true"*)  reg     [127:0]     i_iv;
    
    (*mark_debug = "true"*)  reg     [31:0]      o_data1;
    (*mark_debug = "true"*)  reg     [31:0]      o_data2;
    (*mark_debug = "true"*)  reg     [31:0]      o_data3;
    (*mark_debug = "true"*)  reg     [31:0]      o_data4;
    (*mark_debug = "true"*)  wire    [31:0]      s_data;
    //(*mark_debug = "true"*)   
    (*mark_debug = "true"*)  reg     [3:0]          T_S;
    (*mark_debug = "true"*)  reg     [11:0]         cnt; 
    
     parameter ZUC_START = 0;
     parameter ZUC_PROGRESS = 1;
     parameter ZUC_PROCESS1 = 2;
     parameter ZUC_PROCESS2 = 3;
     parameter ZUC_END  = 4;
    
     //i_ready <= s_valid & i_ready;
    
   always @(posedge clk)
      begin
      if(!reset_n)begin
            T_S     <=  0 ; 
            i_key   <=  0 ;
            i_iv    <=  0 ;
            cnt     <=  0 ;
            i_ready =  0 ;
            i_init  <=  0 ;
            i_reset_n <= 1;
        end 
        else begin   
         case(T_S)
           ZUC_START:begin
               cnt <= cnt + 12'd1;
               if(cnt == 12'd10) begin
                   i_reset_n <= 0;
                   
               end
               //if(clk)   cnt <= cnt + 12'd1;
               if(cnt == 12'd20) begin
                   i_init <= 1;
                   //i_reset_n <= 0;
                   cnt <= 0; 
                   i_key  <= input_key;//128'h3d4c_4be9_6a82_fdae_b58f_641d_b17b_455b;//input_key;
                   i_iv   <=  input_iv;//128'h8431_9aa8_de69_15ca_1f6b_da6b_fbd8_c766;//input_iv;
                   T_S <= ZUC_PROGRESS;
               end
           end
           ZUC_PROGRESS:begin
                //cnt <= cnt + 12'd1;
                //if(cnt == 12'd1) begin
                     cnt <= 0;
                     i_ready = 1 ;
                     i_key  <= input_key;//128'h3d4c_4be9_6a82_fdae_b58f_641d_b17b_455b;//input_key;
                     i_iv   <= input_iv;//128'h8431_9aa8_de69_15ca_1f6b_da6b_fbd8_c766;//input_iv;
                     i_init <= 0;
                     T_S <= ZUC_PROCESS1;
                  //end  
                 //i_key  <= input_key;//128'h3d4c_4be9_6a82_fdae_b58f_641d_b17b_455b;//input_key;
                 //i_iv   <=  input_iv;//128'h8431_9aa8_de69_15ca_1f6b_da6b_fbd8_c766;//input_iv;
           end
           ZUC_PROCESS1: begin
                 if(s_valid)begin
                     i_ready = 0;
                     cnt <= cnt + 12'd1;
                    if(cnt == 12'd2) begin
                       i_ready = 1;
                       cnt <= cnt + 12'd1;
                    end
                     if(cnt == 12'd3) begin
                        o_data1 <= s_data;
                        i_ready = 1;
                        cnt <= cnt + 12'd1;
                     end
                     if(cnt == 12'd4) begin
                        cnt <= cnt + 12'd1;
                        i_ready = 1;
                        o_data2 <= s_data;
                     end
                     if(cnt == 12'd5) begin
                        o_data3 <= s_data;
                        i_ready = 1;
                        cnt <= cnt + 12'd1;
                     end                   
                     if(cnt == 12'd6) begin
                        cnt <= 0;
                        i_ready = 1;
                        o_data4 <= s_data;   
               
                        T_S <= ZUC_PROCESS2;
                     end
                 end
            end
           ZUC_PROCESS2:begin
                 //i_ready <= 0;
                 key_data <= {o_data1,o_data2,o_data3,o_data4};
                 T_S <= ZUC_END;
            end
           ZUC_END:begin
                  //i_ready <= 0;
                  out_data <= key_data ^ input_data;
                  i_reset_n <= 1;
                  i_ready =  0 ;
                  T_S <= ZUC_START;
             end    
          endcase
      end
      
   end  
    
    zuc_core u_core(
        .i_clk      (clk      ),
        .i_rst      (i_reset_n  ),
        .i_init     (i_init     ),
        .i_key      (i_key      ),
        .i_iv       (i_iv       ),
        .i_ready    (i_ready    ),
        .o_valid    (s_valid    ),
        .o_data     (s_data     )
    );    
        
endmodule
