import os;
import shutil;
# f = open(file_name, "r+");
# count = 0;
# file_context = f.read();
# # for i in file_context:
#     # line =  	
# print(file_context);
# for line in file_context:
#     line = line.strip('\n')
#     print(line)
#     if((line.find('output'))!=-1):
#         count = count + 1;
#         print('yes');
# print(count);
# f.write(file_context);
# f.close();
# target = ''
# source = ''
# shutil.copytree(source, target)

def modifyFile(fileName, copyFile, name1, templateContent):
    point = 0 ;
    with open(fileName, "r+") as ModifyFile:
        with open(copyFile, "r+") as CFile:
            lines = ModifyFile.readlines();
            for line in lines:
                point = point + 1;
                # print(line);
                if "endmodule" in line:  #插入例化模块
                    print("this line need change", line);
                    line = line.replace(line, (templateContent + '\n' + line));
                    print(line);
                    CFile.write(line);
                elif name1 in line and ("assign" not in line and "input" not in line):#修改之后调用的信号名称
                    newline = line;
                    strline = newline.split("(");
                    #print()
                    print(strline);
                    line = line.replace(line, strline[0]+"(temp_result)\n");
                    CFile.write(line);
                elif name1 in line and "input" in line:
                    newline = line;
                    strline = newline.split("[");
                    line = line.replace(line, strline[0] + " [ 127:0 ] " + name1 + '\n');
                    print(line);
                    CFile.write(line);
                else:
                    CFile.write(line);
                                   
                    
def modifyTamplate(templateName, bakFile, name1, num1, clkname, rstname):
    point = 0 ;
    fd = open(templateName, mode="w");
    fd.close();
    with open(bakFile, "r") as ModifyFile:
        with open(templateName, "r+") as CFile:
            lines = ModifyFile.readlines();
            for line in lines:
                point = point + 1;
                # print(line);
                if "sm4_input" in line and "assign" in line:#将sm4输入信号改为对应的读取数据的信号
                     strline = "\tassign sm4_input = " + name1 + ";\n";
                     print(strline);
                     line = line.replace(line, strline);
                     CFile.write(line);
                # wire [31:0]    temp_result;
                elif "temp_result" in line and "wire" in line:
                    print('htidshafasdjfasjdfhasdjkhfaskjhfajsdhfkjahsdkjfa');
                    strline = line;
                    tempStr = strline.split("[");
                    tempStr2 = tempStr[1].split(":");
                    strline = tempStr[0] +'['+str(num1)+':'+tempStr2[1];
                    line = line.replace(line, strline);
                    print(line);
                    CFile.write(line);
                # assigh temp_result = result_decode[31:0];
                elif "temp_result" in line and "assign" in line:
                    print('dsafsdfasdfas            dfsderwerd     ');
                    strline = line;
                    tempStr = strline.split("[");
                    tempStr2 = tempStr[1].split(":");
                    strline = tempStr[0] +'['+str(num1)+':'+tempStr2[1];
                    line = line.replace(line, strline);
                    print(line);
                    CFile.write(line);
                elif "clk" in line:
                    newline = line;
                    strline = newline.split("(");
                    strline1 = strline[0] + "(" + clkname + "),\n";
                    line = line.replace(line, strline1);
                    print(strline1);
                    CFile.write(line);
                elif "reset_n" in line:
                    newline = line;
                    strline = newline.split("(");
                    strline1 = strline[0] + "(" + rstname + "),\n";
                    line = line.replace(line, strline1);
                    print(strline1);
                    CFile.write(line);
                elif "data" in line and "rd" in line and "wire" in line:
                    newline = line;
                    strline = newline.split("[");
                    # strline2 = strline[1].split(":");
                    strline1 = strline[0] + "[" + str(num1) +  ':0 ]' + name1 + ';\n';
                    line = line.replace(line, strline1);
                    print(strline1);
                    CFile.write(line);
                else:
                    CFile.write(line);
        
def readFile(fileName, bakFile, name1, templateName, num1, clkname, rstname):
    # count = 0;
    # countEnd = 0;
    # point = 0;
    # countPort = 0;
    # with open(fileName, "r") as ModifyFile:
    #     lines = ModifyFile.readlines();
    #     for line in lines:
    #         point = point + 1;
    #         if "input" in line:
    #             count = count + 1;
    #         if "endmodule" in line:
    #             countEnd = point;
    #         if name1 in line and "input" in line:
    #             countPort = point;
    # print(count);
    # print(countEnd);
    # print(countPort);
    templateName1 = templateName +'.bak';
    print(templateName1, templateName);
    hasFile(templateName,templateName1);
    bakFileFunction(templateName1,templateName);######测试时使用
    bakFileFunction(templateName,templateName1);
    modifyTamplate(templateName, templateName1, name1, num1, clkname, rstname);
    # templateName, bakFile, name1, num1, clkname, rstname
    with open(templateName, "r") as templateFile:
        templateContent = templateFile.read();
    print(templateContent)
    modifyFile(fileName, bakFile, name1, templateContent);

#拷贝目录下文件到目的目录
def copyFiles(templatePath,DestPath):
    hasDir(templatePath, DestPath);
    src_files = os.listdir(templatePath);
    for file_name in src_files:
        full_file_name = os.path.join(templatePath, file_name);
        if os.path.isfile(full_file_name):
            shutil.copy(full_file_name, DestPath);#拷贝
            # print("copy file" + full_file_name);

#是否有该文件
def hasFile(templateFile, DestFile):
    template1 =  os.path.exists(DestFile);
    template2 =  os.path.exists(templateFile);    
    if template1 and template2 :
        print('yes');
    elif template2 :
        print('yes2');
        # os.makedirs(DestFile); 
        fd = open(DestFile, mode="w");
        fd.close();
    elif  template1 :
        print('yes3');  
        # os.makedirs(templateFile); 
        fd = open(templateFile, mode="w");
        fd.close();

#是否存在该文件夹
def hasDir(templatePath, DestPath):
    template1 =  os.path.exists(templatePath);
    template2 =  os.path.exists(DestPath);    
    if template1 and template2 :
        print('yes');
    elif template2 :
        print('yes2');
        os.makedirs(templatePath); 
    elif  template1 :
        print('yes3');  
        os.makedirs(DestPath);    

#备份文件
def bakFileFunction(fileName,bakFileName):
    shutil.copy(fileName, bakFileName)
   
#检查输出端口
def inputPort(fileName):
    count = 0 ;
    with open(fileName, "r+") as file:
        fileContent = file.readlines()
        for line in fileContent:
            if 'input' in line:
                count = count + 1;
                test = line.split();
                a = len(test)-1;
                if "data" in test[a] and "rd" in test[a]:
                    name1 = test[a];
                    print(test);
        print(count)
    return name1;

#检查总线位宽
def inputNum(fileName):
    count = 0 ;
    with open(fileName, "r+") as file:
        fileContent = file.readlines()
        for line in fileContent:
            if 'input' in line:
                count = count + 1;
                test = line.split();
                a = len(test)-1;
                if "data" in test[a] and "rd" in test[a]:
                    testM = line.split("[");
                    tempM = testM[1].split(":");
                    num1 = int(tempM[0]);
                    print(num1);
        print(count)
    return num1;

#检查clk端口
def clkPort(fileName):
    count = 0 ;
    clkname = '';
    with open(fileName, "r+") as file:
        fileContent = file.readlines()
        for line in fileContent:
            if 'clk' in line and 'input' in line:
                count = count + 1;
                test = line.split();
                a = len(test)-1;
                if "clk" in test[a]:
                    clkname = test[a];
                    print(test);
        print(count)
    return clkname;


#检查rst_n端口
def rstPort(fileName):
    count = 0 ;
    rstName = '';
    with open(fileName, "r+") as file:
        fileContent = file.readlines()
        for line in fileContent:
            if 'rst' in line and 'input' in line:
                count = count + 1;
                test = line.split();
                a = len(test)-1;
                if "rst" in test[a]:
                    rstName = test[a];
                    print(test);
        print(count)
    return rstName;
    
def copyvFiles(templatePath, ProjectDir,  DestPath):
    hasDir(templatePath, DestPath);
    print('this is copyvfille', templatePath, ProjectDir);
    s2 = ProjectDir.split(' ')
    print(s2)
    for file_name in s2:
        full_file_name = os.path.join(templatePath, file_name);
        if os.path.isfile(full_file_name):
            shutil.copy(full_file_name, DestPath);#拷贝
#            print("copy file" + full_file_name);
                  
#总体函数
def n_enhanceInputSecurity(topFileName, projectDir, destDir):
    print('this is my main!');
    workDir = os.getcwd();
    
    # print(workDir  +'\n' +destDir);
    topFile = destDir + '\\' + topFileName;
    topFilName1 = topFileName.split(".");
    # bakFile = destDir + '\\' + topFilName1[0] + '_1.v' ;
    # workCopyDir = workDir + '\\sm3_4decode\\ll1';
    # bakFile1 = workCopyDir + '\\' + topFilName1[0] + '_1.v' ;
    # bakFile = workCopyDir + '\\' + topFileName;
    # print("fdsfasdfa " + bakFile);
    workCopyDir = os.path.join(workDir, 'sm3_4decode', 'll1');
    bakFile = os.path.join(workDir, 'sm3_4decode', 'll1', topFileName)
    bakFile1 = os.path.join(workDir, 'sm3_4decode', 'll1', topFilName1[0])
    bakFile1 = bakFile1 + '_1.v'
    
    hasFile(bakFile1, bakFile);
    bakFileFunction(topFile, bakFile);
    bakFileFunction(topFile, bakFile1);

    copyvFiles(destDir, projectDir, workCopyDir)

    name1 = inputPort(bakFile);
    print(name1);
    num1 = inputNum(bakFile);
    print(num1);
    templateName = os.path.join(workDir, 'sm3_4decode', 'sm3_sm4_decode_code', 'sm34_decode.v');
    # templateName = workDir + '\\sm3_4decode\\sm3_sm4_decode_code\\sm34_decode.v';
    rstname = rstPort(bakFile);
    clkname = clkPort(bakFile);
    # print(clkname, rstname);
    # print(workDir   + '\t' + templateName);
    print('starting read file and modify!');
    readFile(bakFile, bakFile1, name1, templateName, num1, clkname, rstname);
    # topFile, bakFile, name1, templateName, num1, clkname, rstname
    print('Modify finish copy file to dest Project!');
    templatePath = os.path.join(workDir, 'sm3_4decode', 'sm3_sm4_decode_code', 'sm3_sm4_decode_code');
    # templatePath = workDir + '\\sm3_4decode\\sm3_sm4_decode_code\\sm3_sm4_decode_code';
    # '\\sm3_4decode\\sm3_sm4_decode_code\\sm3_sm4_decode_code'
    copyFiles(templatePath, workCopyDir);

# if __name__ == '__main__':
#     topFileName = 'riscv_core.v';
#     destDir = 'E:\python-project';
#     enhanceInputSecurity(topFileName, destDir);
 
    
 
#     print('this is my main!');
#     os.chdir("E:\\python-project\\python-changeFile\\")
#     fileName = 'c4-0105.v';
#     bakFileName = 'c4-0105.v.bak';
#     bakFile(bakFileName,fileName);
#     bakFile(fileName,bakFileName);
#     templateName = 'sm3_4decode\\sm34_decode.v';
#     print('starting read file and modify!');
#     readFile(fileName, templateName);
#     print('Modify finish copy file to dest Project!');
#     templatePath = 'E:\python-project\python-changeFile\sm3_4decode\sm3_sm4_decode_code';
#     DestPath = 'E:\python-project\python-changeFile\sm3_4decode\ll1';
#     #copyFiles(templatePath, DestPath);