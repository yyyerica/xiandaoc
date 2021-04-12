import shutil
import os
import math

def findname(nameindex,name,stri):
    if(nameindex!=-1 and isit(stri,nameindex-1) and isit(stri,nameindex+len(name))):
        return True
    return False



def onebitenhance(regname,filename,modulenum): 
    f=open(filename,'r')
    contentx = f.read()
    content = contentx.split(';')
    for i in range(0,len(content)-1):
        listi=list(content[i])
        listi.append(';')
        content[i]=''.join(listi)
    iindex=0
    find=0
    listi=[]
    nummodule=-1
    findstart=-1
    findend=-1
    for i in range(len(content)):
        moduleat=content[i].find('module')
        if(findname(moduleat,'module',content[i])):
            nummodule=nummodule+1
        if(nummodule==modulenum):
            findstart=i
            for j in range(i,len(content)):
                endmoduleat=content[j].find('endmodule')
                if(findname(endmoduleat,'endmodule',content[j])):
                    findend=j
                    break
            break


        
    infunction=0    
    for i in range(findstart,findend+1):
        functionstart=content[i].find('function')
        functionend=content[i].find('endfunction')

        if(findname(functionstart,'function',content[i])): 
            infunction=1
        if(infunction==1):
            if(findname(functionend,'endfunction',content[i])):
                infunction=0
            else:
                continue

                   
        regindex=content[i].find('reg')
        if(findname(regindex,'reg',content[i])):
            regnameindex=content[i].find(regname,regindex,len(content[i]))
            while(regnameindex!=-1):
                if(isit(content[i],regnameindex-1) and isit(content[i],regnameindex+len(regname))):
                    iindex=i
                    commaindex=content[i].find(',',regindex,len(content[i]))
                    listi=list(content[i])
                    if(commaindex==-1):
                        x=regindex
                        while(x<len(content[i])):
                              listi[x]=' '
                              x=x+1
                    else:
                        if(commaindex<regnameindex):
                            x=regnameindex-1+len(regname)
                            while(content[i][x]!=','):
                                  listi[x]=' '
                                  x=x-1
                            listi[x]=' '
                        else:
                            x=regnameindex
                            while(x<=commaindex):
                                listi[x]=' '
                                x=x+1
                    find=1
                    listi=''.join(listi)
                    break;
                else:
                    regnameindex=content[i].find(regname,regnameindex+len(regname),len(content[i]))
        if(find==1):
            break
    if(find==0):
        print('error,cannot find ',regname,' in ',filename)
    else:
        del content[iindex]
        content.insert(iindex,'\nvote3 vote3module_'+regname+'(.r3(vote3_'+regname+'),.r('+regname+'));')
        content.insert(iindex,'\nreg [3:0]vote3_'+regname+';')
        content.insert(iindex,'\nwire '+regname+';')
        content.insert(iindex,str(listi))




    for i in range(findstart,findend+1): 
        functionstart=content[i].find('function')
        functionend=content[i].find('endfunction')

        if(findname(functionstart,'function',content[i])): 
            infunction=1
        if(infunction==1):
            if(findname(functionend,'endfunction',content[i])):
                infunction=0
            else:
                continue
        eq=content[i].find('<=')
        if(eq!=-1):
            x=1;
            while(content[i][eq-x]==' ' or content[i][eq-x]=='\n' or content[i][eq-x]=='\t'):
                x=x+1;
            if(content[i][eq-x-len(regname)+1:eq-x+1]==regname): 
                regnameindex=eq-x-len(regname)+1
                contentx=content[i][:regnameindex]+'vote3_'+regname+' <= {3{'+content[i][eq+2:-1]+'}};'
                content[i]=list(content[i])
                content[i]=contentx
               


    for i in range(findstart,findend+1):
        functionstart=content[i].find('function')
        functionend=content[i].find('endfunction')

        if(findname(functionstart,'function',content[i])): 
            infunction=1
        if(infunction==1):
            if(findname(functionend,'endfunction',content[i])):
                infunction=0
            else:
                continue
        begin=0
        end=len(content[i])
        eq=0        
        while(eq!=-1):
            eq=content[i].find('=',begin,end)

            if(eq!=-1):
                if(content[i][eq-1]=='<' or content[i][eq+1]=='=' or content[i][eq-1]=='='):
                    begin=eq+2
                    eq=-2
            if(eq>=0):
                x=1;
                while(content[i][eq-x]==' ' or content[i][eq-x]=='\n' or content[i][eq-x]=='\t'):
                    x=x+1;
                if(content[i][eq-x-len(regname)+1:eq-x+1]==regname): 
                    regnameindex=eq-x-len(regname)+1
                    contentx=content[i][:regnameindex]+'vote3_'+regname+' = {3{'+content[i][eq+1:-1]+'}};'
                    content[i]=list(content[i])
                    content[i]=contentx
                break
            
    i=0 
    while(i<len(content)):
        if(content[i]==''):
           del content[i]
        else:
           i=i+1
    f=open(filename,'w')
    for i in range(len(content)):
            f.write(content[i]) 
 
    
def nummodulec(filename):
    f=open(filename,'r')
    content = f.read()
    x=content.find('module')
    num=0
    nowindex=0
    while(x!=-1):
        if(isit(content,x-1) and isit(content,x+len('module'))):
            num=num+1
        x=content.find('module',x+len('module'),len(content))

    return num
               
    
    
def changeindex(reg_num_list,filenamelist):

    nummodule=[]
    numindexrange=[]
    for i in filenamelist:
        nummodule.append(nummodulec(i))
        numindexrange.append(-1)   
    for i in range(len(nummodule)):
        for j in range(0,i+1):
            numindexrange[i]=numindexrange[i]+nummodule[j]
    for i in reg_num_list:
        for j in range(len(numindexrange)):
            if(i[1]<=numindexrange[0]):
                i.append(i[1]-0)
                break
            elif(i[1]<=numindexrange[j] and i[1]>numindexrange[j-1]):
                i.append((i[1]-numindexrange[j-1]-1))
                i[1]=j
                break


def isit(strx,index):
    if(index<0 or index>=len(strx)): 
        return True
    achar=strx[index]
    if((achar<='Z' and achar>='A') or (achar<='z' and achar>='a') or(achar<='9' and achar>='0') or  achar=='_'):
        return False
    return True



def enhanceall(reg_num_list,filelist,num):
    rate=[0.3,0.6,1]
    filepath=os.getcwd()
    filepath=os.path.join(filepath,'new_verilog')
    if  os.path.exists(filepath):
        shutil.rmtree(filepath)
    os.makedirs(filepath)
    for i in filelist:
        srcfile = os.path.join(i) 
        dstfile = os.path.join(filepath,os.path.basename(i)) 
        shutil.copyfile(srcfile, dstfile)
    endnum=math.ceil(len(reg_num_list)*rate[num])
    for i in range(endnum):
        onebitenhance(reg_num_list[i][0],os.path.join(filepath,filelist[reg_num_list[i][1]]),reg_num_list[i][3])
    
    srcfile = os.path.join('vote3.v') 
    dstfile = os.path.join(filepath,'vote3.v') 
    shutil.copyfile(srcfile, dstfile)    




