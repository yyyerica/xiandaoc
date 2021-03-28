`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2020/11/16 21:49:22
// Design Name: 
// Module Name: link_top
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


module link_top(
    input clk,
    input reset_n,
    input [31:0] msg_input,
    input [127:0] sm4_msg,
    input  encde_sel,
    output [127:0] result_out
    );
    
    //reg [31:0]  msg_input;
    
    reg                    SM3_en_in;
   
    reg    [31 : 0]         msg_in;    
    reg                     msg_valid_in;
    reg                     is_last_word_in;    
    reg    [1:0]            last_word_byte_in;    
    wire    [127 : 0]       sm3_result;        
    wire                    sm3_finished;    
   
    reg [3:0] T_S;
    reg [11:0] cnt; 
    reg sm4_enable_in;
    reg encdec_enable_in;
    reg valid_in;
    reg encdec_sel_in;
    reg [127: 0] data_in;
    reg enable_key_exp_in;
    reg user_key_valid_in;
    reg [127: 0] user_key_in;
    wire key_exp_ready_out;
    wire ready_out;
     //(*mark_debug = "true"*) wire [127: 0] result_out;  
     
     //user_key_valid_in <= sm3_finished;
     //user_key_in <= sm3_result;
     
     parameter S3_START = 0;
     parameter S3_PROGRESS1 = 1;
     parameter S3_PROGRESS = 2;
     parameter S3_END  = 3;
     parameter S4_START = 4;
     parameter S4_PROGRESS = 5;
     parameter S4_END  = 6;
      
   always @(posedge clk)
      begin
      if(!reset_n)begin
            T_S <= 0; 
            msg_valid_in <= 0 ;
            cnt <= 0 ;
            //T_S <= 0; 
            //sm4
            enable_key_exp_in <= 0;
            encdec_enable_in <= 0 ;
            encdec_sel_in <= 0 ;
            user_key_valid_in <= 0 ;
            valid_in <= 0 ;
            sm4_enable_in <= 0 ;
            //cnt <= 0 ;
        end 
        else begin   
         case(T_S)
           S3_START:begin
               SM3_en_in <= 1;
               if(clk) cnt <= cnt +12'd1;
               if(cnt == 12'd12) begin
                    cnt <= 0;
                    T_S <= S3_PROGRESS1;
               end
               
           end
           S3_PROGRESS1:begin
               msg_valid_in <= 1;
               cnt <= 0;
               msg_in <= 32'h0;
               //data_in <= 128'h9338375e82eec1cbbef65edf8757a631;
              // data_in <= 128'h0123456789abcdeffedcba9876543210;
               if(clk) cnt <= cnt + 12'd1;
               if(cnt == 12'd15)begin
                  is_last_word_in <= 1;
                  T_S <= S3_PROGRESS;
                  last_word_byte_in <= 2'b11;
                  cnt <= cnt + 12'd1;
                  msg_valid_in <= 1;
                  msg_in <= msg_input;//32'h61626364;
               end
               else if (cnt < 12'd15)begin
                   is_last_word_in <= 0;
                   last_word_byte_in <= 0;
                   cnt <= cnt + 12'd1;
                   msg_valid_in <= 1;
                   msg_in <= msg_input;//32'h61626364;
               end
            end
            S3_PROGRESS:begin
                  is_last_word_in <= 0;
                  last_word_byte_in <= 0;
                  cnt <= 0;
                  msg_in <= 0;
                  msg_valid_in <= 0;
                // if(clk_in) cnt <= cnt + 12'd1;
                // if(cnt == 12'd138 && sm3_finished)begin
                 if(sm3_finished)begin
                      T_S <= S3_END;
                      cnt <= 0 ;
                  end
                  
            end
            S3_END: begin
                     T_S <= S4_START;

            end    
             S4_START:begin
                      //enable_key_exp_in <= 1;
                      sm4_enable_in <= 1 ;
                      encdec_enable_in <= 1 ;
                      encdec_sel_in <= encde_sel ;

                      if(clk) cnt <=cnt + 12'd1;
                      if(cnt == 12'd20)begin
                         T_S <= S4_PROGRESS;
                         cnt <= 12'd0;
                      end
        
                   end
              S4_PROGRESS:begin
                         //enable_key_exp_in <= 1;   
                       enable_key_exp_in <= 1;  
                       user_key_valid_in <= 1; 
                       //user_key_in <= 128'h0123456789abcdeffedcba9876543210;
                       user_key_in <= sm3_result;
                       valid_in <= 1 ;
                       data_in <= sm4_msg;//128'h0123456789abcdeffedcba9876543210;//681edf34d206965e86b3e94f536e4246
                       //data_in <= 128'h8f8a24f6c1b69fd7df46c0fcf655cc3e;//h0123456789abcdeffedcba9876543210;
                       //data_in <= 128'h8f8a24f6c1b69fd7df46c0fcf655cc3e;//h0123456789abcdeffedcba9876543210;
                       //data_in <= 128'h0123456789abcdeffedcba9876543210;
                       //data_in <= 128'h9338375e82eec1cbbef65edf8757a631;
                      // data_in <= 128'h0123456789abcdeffedcba9876543210;
                       if(clk) cnt <=cnt + 12'd1;
                       if(cnt == 12'd100)begin
                          T_S <= S4_END;
                          cnt <= 12'd0;
                       end
                   end
              S4_END: begin
                       //enable_key_exp_in <= 1;
                       if(clk) cnt <= cnt + 12'd1;
                       if(cnt == 12'd100)
                            cnt <= 12'd0;
                            
                      T_S <= S3_START;
                   end    
                   
          endcase
      end
      
   end
    
    
        SM3_top usm3
        (
            .clk_in(clk),
            .reset_n_in(reset_n),
            .SM3_en_in(SM3_en_in),
            .msg_in(msg_in),
            .msg_valid_in(msg_valid_in),
            .is_last_word_in(is_last_word_in),
            .last_word_byte_in(last_word_byte_in),
            .sm3_result(sm3_result),
            .sm3_finished(sm3_finished)
        );
        
        
        sm4_top U_sm4(
                .clk(clk)                    ,
                .reset_n(reset_n)               ,
                .sm4_enable_in(sm4_enable_in)       ,
                .encdec_enable_in(encdec_enable_in)    ,
                .encdec_sel_in(encdec_sel_in)       ,
                .valid_in(valid_in)            ,
                .data_in(data_in)             ,
                .enable_key_exp_in(enable_key_exp_in)   ,
                .user_key_valid_in(user_key_valid_in)   ,
                .user_key_in (user_key_in)        ,
                .key_exp_ready_out(key_exp_ready_out)   ,
                .ready(ready_out)           ,
                .result_out(result_out)         
            ); 
        
        
    
endmodule
