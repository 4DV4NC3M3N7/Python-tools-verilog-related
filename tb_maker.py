"""
##########################################################
#       Khaip python test bench script generator         #
#       version 1                                        #
#       Created 2022.12.10                               #
##########################################################
"""
import sys
from sys import getsizeof 
from array import *
import re
#file read=============================================================
#rtl = str(sys.argv[1]);
#testbench = str(sys.argv[2]);
rtl = "alu.v";
module = open(rtl,'r');
#======================================================================
tb_read = open('testbench.v','r');
current_line_tb = tb_read.readlines();
user_main_code = [];
#======================================================================
#User main testbench code retain after regeneration
def retained_code_lines():
    finish_line = 0;
    start_line = 0;
    for i in range(len(current_line_tb)):
        #tokens = re.split('      //your test bench code here',current_line[i]);
        if((start_line==1)and(re.search('finish;',current_line_tb[i])==None)):
            user_main_code.append(current_line_tb[i]);
        if((re.search('//your test bench code here',current_line_tb[i])!=None)):
            start_line += 1;
        if(re.search('finish;',current_line_tb[i])!=None):
            start_line += 1;
#Store user code domain inside a lists
retained_code_lines();
tb_read.close();
#======================================================================
tb = open('testbench.v','w');
current_line = module.readlines();
#Ports record lists
#======================================================================
input_ports = [];
output_ports = [];
#======================================================================
#Tokenize strings
#======================================================================
#Read input port
def input_search(line,keyword):
    tokens = re.split(keyword,current_line[line]);
    if((re.search(keyword,current_line[line])!=None) and (re.search("//",current_line[line])==None)):
        token_len = len(tokens);
        name_vector = tokens[token_len-1].replace("\n", "").replace(",", "");
        name_split = name_vector.split();
        input_ports.append(name_split[len(name_split)-1]);
        #print(input_ports);
        tb.write("   reg  "+name_vector+";\n");
    else:
        return ;
#======================================================================
#Read output port
def output_search(line,keyword):
    tokens = re.split(keyword,current_line[line]);
    if((re.search(keyword,current_line[line])!=None) and (re.search("//",current_line[line])==None)):
        token_len = len(tokens);
        name_vector = tokens[token_len-1].replace(",", "").replace("\n","");
        name_split = name_vector.split();
        output_ports.append(name_split[len(name_split)-1]);
        #print(output_ports);
        tb.write("   wire "+name_vector+";\n");    
    else:
        return ;
#======================================================================
#Read module name
def module_name_search(line,keyword):
    tokens = re.split(keyword,current_line[line]);
    if(re.search(keyword,current_line[line])!=None):
        token_len = len(tokens);
        name = tokens[token_len-1].replace("(","").strip();
        tb.write("   "+name+" u_"+name+"(\n");
        tb.write('   //your instance connection here\n');
        port_instantiation();        
        tb.write('   );\n');
    else:
        return ;
#======================================================================
#Moudule port instantiation
def port_instantiation():
    for i in range(len(input_ports)):
        tb.write("      ."+input_ports[i]+"("+input_ports[i]+"),\n");
    for i in range(len(output_ports)):
        if(i<len(output_ports)-1):
            tb.write("      ."+output_ports[i]+"("+output_ports[i]+"),\n");
        else:
            tb.write("      ."+output_ports[i]+"("+output_ports[i]+")\n");
#======================================================================
#Main Testbench maker
#======================================================================
#Time scale and testbench module
tb.write("`timescale 1ns/10ps\n");
tb.write("module testbench;\n");
#======================================================================
#Port declaration
#tb.write("   reg         clk;\n");
#tb.write("   reg         rstn;\n");
#======================================================================
#Port declaration
for i in range(len(current_line)):
    input_search(i,'(input wire) ');
    output_search(i,'(output reg) ');
tb.write("\n");
#======================================================================
#Instantiation for top module
for i in range(len(current_line)):
    module_name_search(i,'module ');
#======================================================================
tb.write("\n");
tb.write("   initial begin\n");
tb.write('      $fsdbAutoSwitchDumpfile(1024,"dump.fsdb",0);\n');
tb.write('      $fsdbDumpfile("dump.fsdb");\n');
tb.write("      $fsdbDumpvars(0,testbench);\n");
tb.write("   end\n");
tb.write("\n");
tb.write("\n");
tb.write("   initial begin\n");
tb.write("      clk = 1;\n");
tb.write("      forever\n");
tb.write("         #10 clk = ~clk;\n");
tb.write("   end\n");
tb.write("\n");
tb.write("\n");
tb.write("   initial begin\n");
tb.write("   //your test bench code here\n");
#======================================================================
#Insert the previous user code domain
for i in range(len(user_main_code)):
    tb.write(user_main_code[i]);
#======================================================================
tb.write("      $finish;\n");
tb.write("   end\n");
tb.write("\n");
tb.write("endmodule\n");


