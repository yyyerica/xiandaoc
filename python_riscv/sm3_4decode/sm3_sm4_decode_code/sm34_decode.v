    //singal of sm3-sm4decode
    wire [31 : 0]  msg_input;  
    wire [127: 0]  result_out;  
    wire [127: 0]  sm4_input;  
	wire 		   encdc_sel;
	wire [31:0]    temp_result;
	//end of singal of sm3-sm4decode
	//wire [31:0 ]mem_d_data_rd_i;

	//start of assignment of singal
    assign msg_input = 32'h61626364; // random data from PUF
	assign encdc_sel = 0; 
	assign sm4_input = mem_d_data_rd_i;
	assign temp_result = result_out[31:0];
	

	//add module
    link_top U_LT1(
        .clk(clk_i),
        .reset_n(rst_i),
        .msg_input(msg_input),
		.encde_sel(encdc_sel),
        .result_out(result_out),
        .sm4_msg(sm4_input)
        );
    //add module finish
