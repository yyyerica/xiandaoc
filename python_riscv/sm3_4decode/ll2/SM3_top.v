`timescale 1ns / 100ps
/*
 * File: SM3_top.v
 * Project: rtl
 * File Created: Sunday, 5th August 2018 9:03:57 am
 * Author: Chen Rui (raymond.rui.chen@qq.com>)
 * -----
 * Last Modified: Sunday, 5th August 2018 9:12:50 am
 * Modified By: Chen Rui (raymond.rui.chen@qq.com>)
 * -----
 * Copyright (c) 2018 - Chen Rui
 * All rights reserved.
 */
module SM3_top
	(
		clk_in,
		reset_n_in,
		SM3_en_in,
		msg_in,
		msg_valid_in,
		is_last_word_in,
		last_word_byte_in,
		sm3_result,
		sm3_finished
	);
	
`define		IDLE		2'b00
`define		PADDING		2'b01
`define		ITERATION	2'b10	

localparam	WIDTH = 32;	

input					clk_in,
						reset_n_in,
						SM3_en_in;
input	[WIDTH - 1 : 0]	msg_in;	
input					msg_valid_in;
input					is_last_word_in;	
input	[1:0]			last_word_byte_in;	
output	[127 : 0]		sm3_result;		
output					sm3_finished;	

   reg sm3_finished;
//wire sm3_finished_out;
//wire [127:0] tmp1,tmp2;
   reg [127:0] sm3_result;
   wire [255:0] sm3_result_out;
   wire [127:0] tmp1,tmp2;
   reg xor_finish;
   reg  [127:0] b;
// assign finish = 0;

//assign  {tmp1,tmp2} = sm3_result_out;
//assign sm3_result = tmp1^tmp2;

reg						padding_en,
						iteration_en;
   (*mark_debug = "true"*) reg						sm3_finished_out;

reg		[1:0]			current_state,
						next_state;		
reg		[5:0]			index_j;
wire					padding_1_block_finished;
wire	[511:0]			msg_padded;
wire					padding_all_finished;
wire	[31:0]			word_expanded_p;
wire	[31:0]			word_expanded;
wire					msg_exp_finished;
reg						is_last_block;
wire					is_1st_msg_block;



assign tmp1 = sm3_result_out[255:128];
assign tmp2 = sm3_result_out[127:0];


always@(posedge clk_in)
	if(!reset_n_in)
		is_last_block 	<=	1'b0;
	else if(padding_all_finished)	
		is_last_block	<=	1'b1;
	else if(SM3_en_in == 1'b0)
		is_last_block	<=	1'b0;
	else
		is_last_block	<=	is_last_block;

always@(posedge clk_in)					
	if(!reset_n_in)
		current_state	<=	`IDLE;
	else
		current_state	<=	next_state;
		
always@(*)
	begin	
		next_state	=	`IDLE;
		case(current_state)
			`IDLE:
				if(SM3_en_in == 1'b1 && is_last_block != 1'b1)	
					next_state = `PADDING;
				else
					next_state = `IDLE;
			`PADDING:
				if(padding_1_block_finished)
					next_state = `ITERATION;
				else
					next_state = `PADDING;
			`ITERATION:
				if(msg_exp_finished)
					next_state = `IDLE;
				else
					next_state = `ITERATION;
			default:
					next_state = `IDLE;
		endcase
	end
	
	
always@(posedge clk_in)
        if(sm3_finished_out)
            begin
                sm3_result = tmp1 ^tmp2;
                sm3_finished <= 1;
            end
            
            
            
always@(posedge clk_in)
	if(!reset_n_in)
		begin
			padding_en			<=	1'b0;
			iteration_en		<=	1'b0;
			sm3_finished_out	<=	1'b0;
		end
	else
		begin

			if(next_state == `PADDING)
				padding_en		<=	1'b1;
			else
				padding_en		<=	1'b0;
			
			if(current_state == `ITERATION)
				iteration_en	<=	1'b1;
			else
				iteration_en	<=	1'b0;
			
			if(current_state == `ITERATION && next_state == `IDLE && is_last_block ==  1'b1)
				sm3_finished_out	<=	1'b1;
				
			else
				sm3_finished_out	<=	1'b0;								
		end

always@(posedge clk_in)
	if(!reset_n_in)
		index_j	<=	'd0;
	else if(iteration_en)
		index_j	<=	index_j	+	1'b1;
	else
		index_j	<=	'd0;

msg_padding #(WIDTH) U_pad
	(
		.clk_in(						clk_in),
		.reset_n_in(					reset_n_in),
		.SM3_en_in(						SM3_en_in),
		.padding_en_in(					padding_en),
		.msg_in(						msg_in),
		.msg_valid_in(					msg_valid_in),
		.is_last_word_in(				is_last_word_in),
		.last_word_byte_in(				last_word_byte_in),
		.is_1st_msg_block_out(			is_1st_msg_block),
		.msg_padded_out(				msg_padded),
		.padding_1_block_finished_out(	padding_1_block_finished),
		.padding_all_finished_out(		padding_all_finished)
	);
	
msg_expansion U_exp
	(
		.clk_in(						clk_in),
		.reset_n_in(					reset_n_in),
		.start_in(						padding_1_block_finished),
		.index_j_in(					index_j),
		.message_in(					msg_padded),
		.word_p_out(					word_expanded_p),
		.word_out(						word_expanded),
		.msg_exp_finished_out(			msg_exp_finished)
	);	

compression_function U_cf
	(
		.clk_in(						clk_in),
		.reset_n_in(					reset_n_in),
		.start_in(						padding_1_block_finished),
		.index_j_in(					index_j),
		.is_1st_msg_block_in(			is_1st_msg_block),
		.word_expanded_p_in(			word_expanded_p),
		.word_expanded_in(				word_expanded),		
		.data_after_cf_out(				sm3_result_out)
	);	
	
		
endmodule		