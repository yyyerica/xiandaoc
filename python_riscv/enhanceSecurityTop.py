# -*- coding: utf-8 -*-
"""
Created on Mon Jan 11 18:22:21 2021

@author: Administrator
"""
import os;

# import enhanceInOutSecurity
from de_encodeScript import enhanceInOutSecurity
# import encodeScript
from decodeScript import enhanceInputSecurity
from encodeScript import enhanceOutputSecurity

from n_de_encodeScript import n_enhanceInOutSecurity
# import encodeScript
from n_decodeScript import n_enhanceInputSecurity
from n_encodeScript import n_enhanceOutputSecurity



def use(args, label, topFileName, projectDir, destDir):  # 0  ,   0
    # topFileName = 'riscv_core.v';
    # destDir = 'E:\python-project\python_riscv-light-v1\zuc\ll3';
    # args = 1;

    if label == 0 :# 0  ,   0     normal
        if args == 0 :#双向模块加密lll3
            n_enhanceInOutSecurity(topFileName, projectDir, destDir)
        elif args == 1:#加密输出lll2
            n_enhanceOutputSecurity(topFileName, projectDir, destDir)
        elif args == 2:#输入解密ll1
            n_enhanceInputSecurity(topFileName, projectDir, destDir)
    else:# 0  ,   1     light
        if args == 0 :#双向模块加密lll3
            enhanceInOutSecurity(topFileName, projectDir, destDir)
        elif args == 1:#加密输出lll2
            enhanceOutputSecurity(topFileName, projectDir, destDir)
        elif args == 2:#输入解密ll1
            enhanceInputSecurity(topFileName, projectDir, destDir)

    
if __name__ == '__main__':
     topFileName = 'riscv_core.v';
     destDir = 'E:\python-project\ee';
     src_files = os.listdir('E:\python-project\ee');
     print(src_files)
     ProjectDir = " ".join(src_files);
     print(ProjectDir)
     use(0, 0, topFileName, ProjectDir, destDir)
