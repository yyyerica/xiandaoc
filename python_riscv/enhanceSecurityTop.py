# -*- coding: utf-8 -*-
"""
Created on Mon Jan 11 18:22:21 2021

@author: Administrator
"""


# import enhanceInOutSecurity
from de_encodeScript import enhanceInOutSecurity
# import encodeScript
from decodeScript import enhanceInputSecurity
from encodeScript import enhanceOutputSecurity
import shutil
import os


def use(args,topFileName,destDir):  # 0
    # topFileName = 'riscv_core.v';
    # destDir = 'E:\python-project\python-changeFile\sm3_4decode\ll3';
    # args = 1;
    if args == 0 :#双向模块加密
        shutil.rmtree('sm3_4decode/ll3/', True)  # 若为文件夹，则删除该文件夹及文件夹内所有文件
        os.makedirs('sm3_4decode/ll3/')
        enhanceInOutSecurity(topFileName, destDir)
    elif args == 1:#加密输出
        shutil.rmtree('sm3_4decode/ll2/', True)  # 若为文件夹，则删除该文件夹及文件夹内所有文件
        os.makedirs('sm3_4decode/ll2/')
        enhanceOutputSecurity(topFileName, destDir)
    elif args == 2:#输入解密
        shutil.rmtree('sm3_4decode/ll1/', True)  # 若为文件夹，则删除该文件夹及文件夹内所有文件
        os.makedirs('sm3_4decode/ll1/')
        enhanceInputSecurity(topFileName, destDir)
 
    
 
    
# if __name__ == '__main__':
#     topFileName = 'riscv_core.v';
#     destDir = 'E:\python-project';
#     use(2, topFileName, destDir)
