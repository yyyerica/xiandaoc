
    //add code start  ------ single zuc
    wire [127 : 0]  input_key;  
    wire [127: 0]   input_iv;  
    wire [127: 0]   input_data_for_decode;   
    wire [31: 0]   out_data_decode;
    
    wire [127: 0]   input_data_for_encode;   
    wire [127: 0]   result_encode;
    wire [31:0]     temp_result;
    //end of singal of single zuc

	wire [31:0 ] mem_d_data_wr_o;

	//start of assignment of singal
    assign input_key = 128'h3d4c_4be9_6a82_fdae_b58f_641d_b17b_455b;  // init_key_data
    assign input_iv =  128'h8431_9aa8_de69_15ca_1f6b_da6b_fbd8_c766;  // init_vector
	assign input_data_for_decode = mem_d_data_rd_i;
    assign temp_result = out_data_decode[31:0];
    //input_data=128'h15d28715bbd209f6b5521e857a9c3a73;     decode : 0123456789abcdeffedcba9876543210
    
	assign input_data_for_encode = mem_d_data_wr_o;

	//add module
    top_zuc_ddr U_zuc_decode(
        .clk        (clk_i),
        .reset_n    (rst_i),
        .input_key  (input_key  ),
        .input_iv   (input_iv   ),
        .input_data (input_data_for_decode ),
        .out_data   (out_data_decode   )
        );
    top_zuc_ddr U_zuc_encode(
        .clk        (clk_i),
        .reset_n    (rst_i),
        .input_key  (input_key  ),
        .input_iv   (input_iv   ),
        .input_data (input_data_for_encode ),
        .out_data   (result_encode   )
        );
        
    //add module finish
