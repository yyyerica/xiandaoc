    //singal of sm3-sm4
    wire [31 : 0]  msg_input;   
    wire [127: 0]  sm4_input_encode;  
	wire [127: 0]  sm4_input_decode; 
	wire 		   encdc_sel_decode;
	wire 		   encode_sel_encode;
	wire [31:0]    temp_result;
    wire [127: 0]  result_encode;   
	wire [31: 0]  result_decode;
	//end of singal of sm3-sm4
	wire [31:0 ] data_wr_out;
	//wire [31:0 ] data_rd_in;


	//start of assignment of singal
    assign msg_input = 32'h61626364; // random data from PUF
	assign encdc_sel_decode = 0; 
	assign sm4_input_decode = mem_d_data_rd_i;
	

	assign sm4_input_encode = mem_d_data_wr_o;
	assign encode_sel_encode = 1;
	
	assign temp_result = result_decode[31:0];
	
	//add module
    link_top U_LT1(
        .clk(clk_i),
        .reset_n(rst_i),
        .msg_input(msg_input),
		.encde_sel(encdc_sel_decode),
        .result_out(result_decode),
        .sm4_msg(sm4_input_decode)
    );
	link_top U_LT2(
        .clk(clk_i),
        .reset_n(rst_i),
        .msg_input(msg_input),
		.encde_sel(encode_sel_encode),
        .result_out(result_encode),
        .sm4_msg(sm4_input_encode)
    );
    //add module finish
