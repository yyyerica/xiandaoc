//-----------------------------------------------------------------
//                         RISC-V Core
//                            V1.0
//                     Ultra-Embedded.com
//                     Copyright 2014-2019
//
//                   admin@ultra-embedded.com
//
//                       License: BSD
//-----------------------------------------------------------------
//
// Copyright (c) 2014-2019, Ultra-Embedded.com
// All rights reserved.
// 
// Redistribution and use in source and binary forms, with or without
// modification, are permitted provided that the following conditions 
// are met:
//   - Redistributions of source code must retain the above copyright
//     notice, this list of conditions and the following disclaimer.
//   - Redistributions in binary form must reproduce the above copyright
//     notice, this list of conditions and the following disclaimer 
//     in the documentation and/or other materials provided with the 
//     distribution.
//   - Neither the name of the author nor the names of its contributors 
//     may be used to endorse or promote products derived from this 
//     software without specific prior written permission.
// 
// THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS 
// "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT 
// LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR 
// A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE AUTHOR BE 
// LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR 
// CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF 
// SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR 
// BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF 
// LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
// (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF 
// THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF 
// SUCH DAMAGE.
//-----------------------------------------------------------------
`timescale 1ns / 100ps
module riscv_csr
//-----------------------------------------------------------------
// Params
//-----------------------------------------------------------------
#(
     parameter SUPPORT_MULDIV   = 1
    ,parameter SUPPORT_SUPER    = 1
)
//-----------------------------------------------------------------
// Ports
//-----------------------------------------------------------------
(
    // Inputs
     input           clk_i
    ,input           rst_i
    ,input           intr_i
    ,input           opcode_valid_i
    ,input  [ 31:0]  opcode_opcode_i
    ,input  [ 31:0]  opcode_pc_i
    ,input           opcode_invalid_i
    ,input  [  4:0]  opcode_rd_idx_i
    ,input  [  4:0]  opcode_ra_idx_i
    ,input  [  4:0]  opcode_rb_idx_i
    ,input  [ 31:0]  opcode_ra_operand_i
    ,input  [ 31:0]  opcode_rb_operand_i
    ,input           csr_writeback_write_i
    ,input  [ 11:0]  csr_writeback_waddr_i
    ,input  [ 31:0]  csr_writeback_wdata_i
    ,input  [  5:0]  csr_writeback_exception_i
    ,input  [ 31:0]  csr_writeback_exception_pc_i
    ,input  [ 31:0]  csr_writeback_exception_addr_i
    ,input  [ 31:0]  cpu_id_i
    ,input  [ 31:0]  reset_vector_i
    ,input           interrupt_inhibit_i

    // Outputs
    ,output [ 31:0]  csr_result_e1_value_o
    ,output          csr_result_e1_write_o
    ,output [ 31:0]  csr_result_e1_wdata_o
    ,output [  5:0]  csr_result_e1_exception_o
    ,output          branch_csr_request_o
    ,output [ 31:0]  branch_csr_pc_o
    ,output [  1:0]  branch_csr_priv_o
    ,output          take_interrupt_o
    ,output          ifence_o
    ,output [  1:0]  mmu_priv_d_o
    ,output          mmu_sum_o
    ,output          mmu_mxr_o
    ,output          mmu_flush_o
    ,output [ 31:0]  mmu_satp_o
);



//-----------------------------------------------------------------
// Includes
//-----------------------------------------------------------------
`include "riscv_defs.v"

//-----------------------------------------------------------------
// Registers / Wires
//-----------------------------------------------------------------
wire ecall_w             = opcode_valid_i && ((opcode_opcode_i & `INST_ECALL_MASK)      == `INST_ECALL);
wire ebreak_w            = opcode_valid_i && ((opcode_opcode_i & `INST_EBREAK_MASK)     == `INST_EBREAK);
wire eret_w              = opcode_valid_i && ((opcode_opcode_i & `INST_MRET_MASK)       == `INST_MRET);
wire csrrw_w             = opcode_valid_i && ((opcode_opcode_i & `INST_CSRRW_MASK)      == `INST_CSRRW);
wire csrrs_w             = opcode_valid_i && ((opcode_opcode_i & `INST_CSRRS_MASK)      == `INST_CSRRS);
wire csrrc_w             = opcode_valid_i && ((opcode_opcode_i & `INST_CSRRC_MASK)      == `INST_CSRRC);
wire csrrwi_w            = opcode_valid_i && ((opcode_opcode_i & `INST_CSRRWI_MASK)     == `INST_CSRRWI);
wire csrrsi_w            = opcode_valid_i && ((opcode_opcode_i & `INST_CSRRSI_MASK)     == `INST_CSRRSI);
wire csrrci_w            = opcode_valid_i && ((opcode_opcode_i & `INST_CSRRCI_MASK)     == `INST_CSRRCI);
wire wfi_w               = opcode_valid_i && ((opcode_opcode_i & `INST_WFI_MASK)        == `INST_WFI);
wire fence_w             = opcode_valid_i && ((opcode_opcode_i & `INST_FENCE_MASK)      == `INST_FENCE);
wire sfence_w            = opcode_valid_i && ((opcode_opcode_i & `INST_SFENCE_MASK)     == `INST_SFENCE);
wire ifence_w            = opcode_valid_i && ((opcode_opcode_i & `INST_IFENCE_MASK)     == `INST_IFENCE);

//-----------------------------------------------------------------
// CSR handling
//-----------------------------------------------------------------
wire [1:0]  current_priv_w;
reg [1:0]   csr_priv_r;
                           
wire csr_readonly_r;
reg [3:0]vote3_csr_readonly_r;
vote3 vote3module_csr_readonly_r(.r3(vote3_csr_readonly_r),.r(csr_readonly_r));
                        
wire csr_write_r;
reg [3:0]vote3_csr_write_r;
vote3 vote3module_csr_write_r(.r3(vote3_csr_write_r),.r(csr_write_r));
                  
wire set_r;
reg [3:0]vote3_set_r;
vote3 vote3module_set_r(.r3(vote3_set_r),.r(set_r));
                  
wire clr_r;
reg [3:0]vote3_clr_r;
vote3 vote3module_clr_r(.r3(vote3_clr_r),.r(clr_r));
                        
wire csr_fault_r;
reg [3:0]vote3_csr_fault_r;
vote3 vote3module_csr_fault_r(.r3(vote3_csr_fault_r),.r(csr_fault_r));

reg [31:0]  data_r;

always @ *
begin
    vote3_set_r = {3{ csrrw_w | csrrs_w | csrrwi_w | csrrsi_w}};
    vote3_clr_r = {3{ csrrw_w | csrrc_w | csrrwi_w | csrrci_w}};

    csr_priv_r      = opcode_opcode_i[29:28];
    vote3_csr_readonly_r = {3{ (opcode_opcode_i[31:30] == 2'd3)}};
    vote3_csr_write_r = {3{ (opcode_ra_idx_i != 5'b0) | csrrw_w | csrrwi_w}};

    data_r          = (csrrwi_w | 
                       csrrsi_w | 
                       csrrci_w) ?
                            {27'b0, opcode_ra_idx_i} : opcode_ra_operand_i;

    // Detect access fault on CSR access
    vote3_csr_fault_r = {3{ SUPPORT_SUPER ? (opcode_valid_i && (set_r | clr_r) && ((csr_write_r && csr_readonly_r) || (current_priv_w < csr_priv_r))) : 1'b0}};
end

wire satp_update_w = (opcode_valid_i && (set_r || clr_r) && csr_write_r && (opcode_opcode_i[31:20] == `CSR_SATP));

//-----------------------------------------------------------------
// CSR register file
//-----------------------------------------------------------------
wire timer_irq_w = 1'b0;

wire [31:0] misa_w = SUPPORT_MULDIV ? (`MISA_RV32 | `MISA_RVI | `MISA_RVM): (`MISA_RV32 | `MISA_RVI);

wire [31:0] csr_rdata_w;

wire        csr_branch_w;
wire [31:0] csr_target_w;

wire [31:0] interrupt_w;
wire [31:0] status_reg_w;
wire [31:0] satp_reg_w;

riscv_csr_regfile
#( .SUPPORT_MTIMECMP(1)
  ,.SUPPORT_SUPER(SUPPORT_SUPER) )
u_csrfile
(
     .clk_i(clk_i)
    ,.rst_i(rst_i)

    ,.ext_intr_i(intr_i)
    ,.timer_intr_i(timer_irq_w)
    ,.cpu_id_i(cpu_id_i)
    ,.misa_i(misa_w)

    // Issue
    ,.csr_ren_i(opcode_valid_i)
    ,.csr_raddr_i(opcode_opcode_i[31:20])
    ,.csr_rdata_o(csr_rdata_w)

    // Exception (WB)
    ,.exception_i(csr_writeback_exception_i)
    ,.exception_pc_i(csr_writeback_exception_pc_i)
    ,.exception_addr_i(csr_writeback_exception_addr_i)

    // CSR register writes (WB)
    ,.csr_waddr_i(csr_writeback_write_i ? csr_writeback_waddr_i : 12'b0)
    ,.csr_wdata_i(csr_writeback_wdata_i)

    // CSR branches
    ,.csr_branch_o(csr_branch_w)
    ,.csr_target_o(csr_target_w)

    // Various CSR registers
    ,.priv_o(current_priv_w)
    ,.status_o(status_reg_w)
    ,.satp_o(satp_reg_w)

    // Masked interrupt output
    ,.interrupt_o(interrupt_w)
);

//-----------------------------------------------------------------
// CSR Read Result (E1) / Early exceptions
//-----------------------------------------------------------------
                                      
wire rd_valid_e1_q;
reg [3:0]vote3_rd_valid_e1_q;
vote3 vote3module_rd_valid_e1_q(.r3(vote3_rd_valid_e1_q),.r(rd_valid_e1_q));
reg [ 31:0]             rd_result_e1_q;
reg [ 31:0]             csr_wdata_e1_q;
reg [`EXCEPTION_W-1:0]  exception_e1_q;

always @ (posedge clk_i or posedge rst_i)
if (rst_i)
begin
    vote3_rd_valid_e1_q <= {3{ 1'b0}};
    rd_result_e1_q  <= 32'b0;
    csr_wdata_e1_q  <= 32'b0;
    exception_e1_q  <= `EXCEPTION_W'b0;
end
else if (opcode_valid_i)
begin
    vote3_rd_valid_e1_q <= {3{ (set_r || clr_r) && ~csr_fault_r}};

    // Invalid instruction / CSR access fault?
    // Record opcode for writing to csr_xtval later.
    if (opcode_invalid_i || csr_fault_r)
        rd_result_e1_q  <= opcode_opcode_i;
    else    
        rd_result_e1_q  <= csr_rdata_w;

    // E1 CSR exceptions
    if ((opcode_opcode_i & `INST_ECALL_MASK) == `INST_ECALL)
        exception_e1_q  <= `EXCEPTION_ECALL + {4'b0, current_priv_w};
    else if ((opcode_opcode_i & `INST_MRET_MASK) == `INST_MRET)
        exception_e1_q  <= `EXCEPTION_ERET; // TODO: MPRIV
    else if ((opcode_opcode_i & `INST_EBREAK_MASK) == `INST_EBREAK)
        exception_e1_q  <= `EXCEPTION_BREAKPOINT;
    else if (opcode_invalid_i || csr_fault_r)
        exception_e1_q  <= `EXCEPTION_ILLEGAL_INSTRUCTION;
    // Fence / MMU settings cause a pipeline flush
    else if (satp_update_w || ifence_w || sfence_w)
        exception_e1_q  <= `EXCEPTION_FENCE;
    else
        exception_e1_q  <= `EXCEPTION_W'b0;

    // Value to be written to CSR registers
    if (set_r && clr_r)
        csr_wdata_e1_q <= data_r;
    else if (set_r)
        csr_wdata_e1_q <= csr_rdata_w | data_r;
    else if (clr_r)
        csr_wdata_e1_q <= csr_rdata_w & ~data_r;
end
else
begin
    vote3_rd_valid_e1_q <= {3{ 1'b0}};
    rd_result_e1_q  <= 32'b0;
    csr_wdata_e1_q  <= 32'b0;
    exception_e1_q  <= `EXCEPTION_W'b0;
end

assign csr_result_e1_value_o     = rd_result_e1_q;
assign csr_result_e1_write_o     = rd_valid_e1_q;
assign csr_result_e1_wdata_o     = csr_wdata_e1_q;
assign csr_result_e1_exception_o = exception_e1_q;

//-----------------------------------------------------------------
// Interrupt launch enable
//-----------------------------------------------------------------
                     
wire take_interrupt_q;
reg [3:0]vote3_take_interrupt_q;
vote3 vote3module_take_interrupt_q(.r3(vote3_take_interrupt_q),.r(take_interrupt_q));

always @ (posedge clk_i or posedge rst_i)
if (rst_i)
    vote3_take_interrupt_q <= {3{ 1'b0}};
else
    vote3_take_interrupt_q <= {3{ (|interrupt_w) & ~interrupt_inhibit_i}};

assign take_interrupt_o = take_interrupt_q;

//-----------------------------------------------------------------
// TLB flush
//-----------------------------------------------------------------
                
wire tlb_flush_q;
reg [3:0]vote3_tlb_flush_q;
vote3 vote3module_tlb_flush_q(.r3(vote3_tlb_flush_q),.r(tlb_flush_q));

always @ (posedge clk_i or posedge rst_i)
if (rst_i)
    vote3_tlb_flush_q <= {3{ 1'b0}};
else
    vote3_tlb_flush_q <= {3{ satp_update_w || sfence_w}};

//-----------------------------------------------------------------
// ifence
//-----------------------------------------------------------------
             
wire ifence_q;
reg [3:0]vote3_ifence_q;
vote3 vote3module_ifence_q(.r3(vote3_ifence_q),.r(ifence_q));

always @ (posedge clk_i or posedge rst_i)
if (rst_i)
    vote3_ifence_q <= {3{ 1'b0}};
else
    vote3_ifence_q <= {3{ ifence_w}};

assign ifence_o = ifence_q;

//-----------------------------------------------------------------
// Execute - Branch operations
//-----------------------------------------------------------------
                    
wire branch_q;
reg [3:0]vote3_branch_q;
vote3 vote3module_branch_q(.r3(vote3_branch_q),.r(branch_q));
reg [31:0] branch_target_q;
                   
wire reset_q;
reg [3:0]vote3_reset_q;
vote3 vote3module_reset_q(.r3(vote3_reset_q),.r(reset_q));

always @ (posedge clk_i or posedge rst_i)
if (rst_i)
begin
    branch_target_q <= 32'b0;
    vote3_branch_q <= {3{ 1'b0}};
    vote3_reset_q <= {3{ 1'b1}};
end
else if (reset_q)
begin
    branch_target_q <= reset_vector_i;
    vote3_branch_q <= {3{ 1'b1}};
    vote3_reset_q <= {3{ 1'b0}};
end
else
begin
    vote3_branch_q <= {3{ csr_branch_w}};
    branch_target_q <= csr_target_w;
end

assign branch_csr_request_o = branch_q;
assign branch_csr_pc_o      = branch_target_q;
assign branch_csr_priv_o    = satp_reg_w[`SATP_MODE_R] ? current_priv_w : `PRIV_MACHINE;

//-----------------------------------------------------------------
// MMU
//-----------------------------------------------------------------
assign mmu_priv_d_o     = status_reg_w[`SR_MPRV_R] ? status_reg_w[`SR_MPP_R] : current_priv_w;
assign mmu_satp_o       = satp_reg_w;
assign mmu_flush_o      = tlb_flush_q;
assign mmu_sum_o        = status_reg_w[`SR_SUM_R];
assign mmu_mxr_o        = status_reg_w[`SR_MXR_R];

endmodule