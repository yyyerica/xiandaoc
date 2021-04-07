"""
   Copyright 2013, Shinya Takamaeda-Yamazaki and Contributors

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

from __future__ import absolute_import
from __future__ import print_function
from collections import Counter
import sys
import re
import copy
import numpy as np
import random
import networkx as nx
import matplotlib.pyplot as plt
nowmodulename='x'
topmodulename='x'
nodemodulename=0
nodename=1
granodemodulename=0
granodename=1
nodewide=2
nodegra=3
nodetype=4
nodethree=5
nodeuse=6
granodedeepgap=2
granodetype=3
deep = 0
castlist=[]
topinput=[]
topoutput=[]
listonereg=[]
modulelist=[]
valuesuse=[]
allvalues=[]
cdrate=4
randomrate=0.15
def xpass(grid): 
    A=grid         
    A = [[row[i] for row in A] for i in range(len(A[0]))]
    xrate=[]
    for i in range(len(A)):
        t=[1]*len(A)
        t[i]=0
        while(1):
            tx=t
            for j in range(len(A)):
                for k in range(len(A)):
                    if(t[j]==0 and A[j][k]==1):
                        t[k]=0
            if(t==tx):
                break
        num=0
        for j in t:
            if(j==0):
                num=num+1
        num=num/len(t)
        xrate.append(num)
    return xrate
            
def take2(elem):
    return elem[1]
#def opertorxy(a)
#    i=0
#    while(('a'<a[i] and a[i]<'z') or 'A'<a[i] and a[i]<'Z'):
        

class Node(object):
    """ Abstact class for every element in parser """

    def children(self):
        pass

    def show(self, buf=sys.stdout, offset=0, attrnames=False, showlineno=True):
        indent = 2
        lead = ' ' * offset

        buf.write(lead + self.__class__.__name__ + ': ')
        #if(self.__class__.__name__ == 'IfStatement'):
        #    buf.write('check it')

        if self.attr_names:
            if attrnames:
                nvlist = [(n, getattr(self, n)) for n in self.attr_names]
                attrstr = ', '.join('%s=%s' % (n, v) for (n, v) in nvlist)
            else:
                vlist = [getattr(self, n) for n in self.attr_names]
                attrstr = ', '.join('%s' % v for v in vlist)
            buf.write(attrstr)

        if showlineno:
            buf.write(' (at %s)' % self.lineno)

        buf.write('\n')

        for c in self.children():

            c.show(buf, offset + indent, attrnames, showlineno)

    def __eq__(self, other):
        if type(self) != type(other):
            return False

        self_attrs = tuple([getattr(self, a) for a in self.attr_names])
        other_attrs = tuple([getattr(other, a) for a in other.attr_names])

        if self_attrs != other_attrs:
            return False

        other_children = other.children()

        for i, c in enumerate(self.children()):
            if c != other_children[i]:
                return False

        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        s = hash(tuple([getattr(self, a) for a in self.attr_names]))
        c = hash(self.children())
        return hash((s, c))

   



    def checkvalues(self,allvalues,buf=sys.stdout):
        global listonereg,modulelist,nowmodulename,modulelist
        if(self.__class__.__name__ == 'ModuleDef'):
            modulelist.append(self.name)
            storemodulename=nowmodulename
            nowmodulename=self.name
            for c in self.children():
                c.checkvalues(allvalues,buf)
            nowmodulename=storemodulename
        else:              
            if(self.__class__.__base__.__name__ == 'Variable'):
                ex=0
                for i in allvalues:
                    if(i[nodemodulename]==nowmodulename and i[nodename]==self.name):
                        if(self.__class__.__name__=='Reg'):
                            i[nodetype]=str('Reg'+i[nodetype])
                        ex=1
                        break
                if(ex==0):    
                    value=[]
                    wi=[]
                    if(self.width!=None):
                        value.append(nowmodulename)
                        value.append(self.name)
                        if(self.width.msb.__class__.__base__.__name__=='Operator'):
                            wi.append('x')
                        else:
                            wi.append(int(str(self.width.msb)))
                        wi.append(int(str(self.width.lsb)))
                        value.append(wi)
                        value.append([])       
                        value.append(self.__class__.__name__ )
                        value.append([])       
                    else:
                        value.append(nowmodulename)
                        value.append(self.name)
                        wi.append(0)
                        wi.append(0)
                        value.append(wi)
                        value.append([])
                        value.append(self.__class__.__name__ )   
                        value.append([])   
                    allvalues.append(value)
            for c in self.children():
                c.checkvalues(allvalues,buf)
                

                
     






    def findinout(self, buf=sys.stdout):
        global topinput,topoutput
        if(self.__class__.__name__ == 'Input'):
            topinput.append(str(self.name))
        if(self.__class__.__name__ == 'Output'):
            topoutput.append(str(self.name))
        for c in self.children():
            c.findinout(buf)



    def keymodule(self,pr):
        modulescorelist=modulelist.copy()
        for i in range(len(modulescorelist)):
            modulescorelist[i]=[modulescorelist[i],0]
        for i in allvalues:
            if(i[nodetype]=='Output' or i[nodetype]=='RegOutput'):
                name=str(i[nodemodulename]+'+'+i[nodename])
                for j in pr:
                    if(j[0]==name):
                        for k in modulescorelist:
                            if(k[0]==i[nodemodulename]):
                                k[1]=k[1]+j[1]
                                break
        modulescorelist.sort(key=take2,reverse=True)
        return modulescorelist
                         
 
            

    def checksignals(self, buf=sys.stdout):
        global namelist,topmodulename,nowmodulename,listonereg,allvalues
        allvalues=[]
        topmodulename=((self.description).children())[0].name
        print('*******************************') 
        ((self.description).children())[0].findinout(buf)
        nowmodulename=topmodulename
        self.description.checkvalues(allvalues, buf)
        print('bianliang shengcheng over')
        nowmodulename=topmodulename



 







        ((self.description).children())[0].checkkeyvalues(self.description,[],allvalues, buf)       
        print('yufa fenxi over')

      
       
        for i in allvalues:
            if(len(i[nodegra])==1 and i[nodetype]=='Wire'):
                cast=[]
                cast.append([i[nodemodulename],i[nodename]])
                cast.append([i[nodegra][0][nodemodulename],i[nodegra][0][nodename]])
                castlist.append(cast)
        topallput=topinput+topoutput
        i=0
        while(i<len(castlist)):
            for j in topallput:
                if(castlist[i][0][nodemodulename]==topmodulename and castlist[i][0][nodename]==j):
                    del castlist[i]
                    i=i-1
                    break
            i=i+1

        
        for i in castlist:
            for j in allvalues:
                if(i[0][nodemodulename]==j[nodemodulename] and i[0][nodename]==j[nodename]):
                    k=0
                    while(k<len(j[nodegra])):
                        if(i[1][nodemodulename]==j[nodegra][k][nodename] and i[1][nodename]==j[nodegra][k][nodename]):
                            del j[nodegra][k]

                        else:
                            k=k+1

            self.castatob(allvalues,i[0][nodemodulename],i[1][nodemodulename],i[0][nodename],i[1][nodename])
        print('touying over')


        for i in allvalues:
            j=0
            while j <len(i[nodegra]):
                k=j+1              
                while k < len(i[nodegra]):
                  if(i[nodegra][j][granodename]==i[nodegra][k][granodename]):
                      del i[nodegra][k]
                      
                  else:
                      k=k+1
                j=j+1          
           
        num=len(allvalues)


        for i in  allvalues:   
            if(i[nodetype][:2]=='Reg' and i[nodewide][0]==0):
                listonereg.append([i[nodemodulename],i[nodename]])


#        self.description.finddontcare()
#        self.description.searchdontcare()
#        for i in allvalues:
#            print(i)
        DG = nx.DiGraph()
        for i in range(num):
            clist=[]
            dlist=[]
            for j in allvalues[i][nodethree]:
                for k in j[0]:
                    find=0
                    for l in clist:
                        if(l[nodemodulename]==k[nodemodulename] and l[nodename]==k[nodename]):
                            find=1
                            l[2]=l[2]+1
                            break
                    if(find==0):
                        clist.append([k[nodemodulename],k[nodename],1])
                for k in j[1]:
                    find=0
                    for l in dlist:
                        if(l[nodemodulename]==k[nodemodulename] and l[nodename]==k[nodename]):
                            find=1
                            l[2]=l[2]+1
                            break
                    if(find==0):
                        dlist.append([k[nodemodulename],k[nodename],1])
                        break  
            numc=0
            for j in clist:
                numc=numc+j[2] 
            numd=0
            for j in dlist:
                numd=numd+j[2]
            allscores=0           
            for j in clist:
                DG.add_weighted_edges_from([(str(allvalues[i][nodemodulename]+'+'+allvalues[i][nodename]),j[granodemodulename]+'+'+j[granodename],j[2]*(cdrate)*(numd/numc))])
                allscores=allscores+j[2]*(cdrate)*(numd/numc)
            for j in dlist:
                DG.add_weighted_edges_from([(str(allvalues[i][nodemodulename]+'+'+allvalues[i][nodename]),j[granodemodulename]+'+'+j[granodename],j[2])])
                allscores=allscores+j[2]
            pscore=(allscores/len(topoutput))*randomrate
        #    if(allscores!=0):
         #       for j in topoutput:
         #           DG.add_weighted_edges_from([(str(allvalues[i][nodemodulename]+'+'+allvalues[i][nodename]),modulelist[0]+'+'+j,pscore)])

        personalpr={}
        pr = nx.pagerank(DG,alpha=0.85,max_iter=100000)
        print('pagerank over')

        listpr=[]
        listvalues=[]
        listcompare=[]
        for key,value in pr.items():
            x=[key,value]
            listpr.append(x)
            listvalues.append(value)
            listcompare.append(x)
                  
        
        listpr.sort(key=take2,reverse=True)
   #     for i in range(50):
   #         print(listpr[i])
  #      modulescorelist=self.keymodule(listpr)

        listoneregrank=[]
        listprprint=[]
        listoneprint=[]
        listnotuse=[]
        for i in listpr:
            listx = i[0].split('+')
            #for k in allvalues:
            #    if(listx[nodemodulename]==k[nodemodulename] and listx[nodename]==k[nodename]):
            #        listprprint.append([i[0],k[nodetype],i[1]])
            #        if(k[nodeuse+1]=='notall'):
            #            listnotuse.append([i[0],k[nodetype],i[1]])             
            for j in listonereg:
                if(listx[nodemodulename]==j[nodemodulename] and listx[nodename]==j[nodename]):
                    listoneregrank.append([listx[1],modulelist.index(listx[0]),i[1]])
                    listoneprint.append([i[0],i[1]])
                    break
        print('\n\n\n')

#        for i in range(len(listoneregrank)):
#            print(listoneregrank[i])
        print('\n\n\n')

        print('\n\n\n')

        A=nx.to_numpy_matrix(DG)
        A=A.tolist()
        for i in A:
            for j in range(len(i)):
                if(i[j]>1):
                    i[j]=1.0
        gnamelist=[]
        for i in DG:
            gnamelist.append(str(i)) 
#        for i in listonereg:
#            print(i)
#         listx=xpass(A)
#         for i in range(len(listcompare)):
#             listcompare[i].append(listx[i])
#         # for i in modulescorelist:
#         #     print(i)
#         listcompare.sort(key=take2,reverse=True)
#        for i in listcompare:
#            print(i[0])
#            print(round(i[1],6),round(i[2],6))               

        return A,gnamelist,listvalues,listoneregrank


        


    def finddontcare(self):          
        global allvalues
        for i in allvalues:
             i.append([])
        self.findused()

   
    def findused(self):
        global allvalues,nowmodulename
        if(self.__class__.__name__ == 'ModuleDef'):
            nowmodulename=self.name
        if(self.__class__.__name__ == 'Decl'):
            return 

        if(self.__class__.__name__ == 'Identifier'):
            idat=-1
            for i in range(len(allvalues)):
                if(allvalues[i][nodemodulename]==nowmodulename and allvalues[i][nodename]==self.name):
                    idat=i
            allvalues[idat][nodeuse].append('all')

        if(len(self.children())!=0):  
            if(self.__class__.__name__ == 'Pointer' and self.children()[0].__class__.__name__=='Identifier'):
                idat=-1
                for i in range(len(allvalues)):
                    if(allvalues[i][nodemodulename]==nowmodulename and allvalues[i][nodename]==self.children()[0].name):
                        idat=i
                if(self.children()[1].__class__.__name__=='IntConst'):
                    allvalues[idat][nodeuse].append([self.children()[1].value,self.children()[1].value])   
                else:
                    allvalues[idat][nodeuse].append('unknown')

            elif(self.__class__.__name__ == 'Partselect' and self.children()[0].__class__.__name__=='Identifier'):
                idat=-1
                for i in range(len(allvalues)):
                    if(allvalues[i][nodemodulename]==nowmodulename and allvalues[i][nodename]==self.children()[0].name):
                        idat=i
                if(self.children()[1].__class__.__name__=='IntConst' and self.children()[2].__class__.__name__=='Intconst'):
                    allvalues[idat][nodeuse].append([min([self.children()[1].value,self.children()[2].value]),max([self.children()[1].value,self.children()[2].value])])
                else:
                    allvalues[idat][nodeuse].append('unknown')
            else:
                for c in self.children():
                    c.findused()
                
        
    def searchdontcare(self):
        for i in allvalues:
            if(i[nodewide][0]=='x'):
                i.append('unknown')
                continue
            finish=0
            usemap=[0]*(i[nodewide][0]-i[nodewide][1]+1)
            if(len(i[nodeuse])==0):
                    i.append('notall')
                    continue       
            for j in i[nodeuse]:
                if(j=='all'):
                    i.append('all')
                    finish=1
                    break
                elif(j=='unknown'):
                    i.append('unknown')
                    finish=1
                    break
                else:
                    for k in range(int(j[0]),int(j[1])+1):
                        usemap[k]=1
            if(finish==0):
                no=0
                for l in usemap:
                    if(l==0):
                        no=1
                        break
                if(no==0):
                    i.append('all') 
                else:
                    i.append('notall')                      
         

                    
                        
                
 
      


        
    def changereg(self,regname,modulenum):
        modulelo=self.findmodule(modulelist[modulenum])
        modulelo.declchange(regname)
         

    def declchange(self,regname):
        for c in self.children():
            if(c.__class__.__name__ == 'Decl'):
                c.changereg(regname)

    def findmodule(self,modulename):
        if(self.__class__.__name__ == 'ModuleDef' and self.name==modulename):
            return self
        else:
            for i in self.children():
                modulep=i.findmodule(modulename)
                if(modulep!=None):
                    return modulep
        return None




    def findvalues(self, valueslist,buf=sys.stdout):
        if(self.__class__.__name__ == 'Identifier'):
            valueslist.append([nowmodulename,self.name,deep]);
        for c in self.children():
            c.findvalues(valueslist,buf)
  
    def castatob(self,allvalues,pnodemodulename,nnodemodulename,pnodename,nnodename):
        delv=-1
        num=0
        for j in allvalues:
            if(j[nodemodulename]==nnodemodulename and j[nodename]==nnodename):
               for k in allvalues:
                   if(k[nodemodulename]==pnodemodulename and k[nodename]==pnodename):
                       delv=num                    
                   for l in k[nodegra]:
                       if(l[nodemodulename]==pnodemodulename and l[nodename]==pnodename):
                           l[nodemodulename]=nnodemodulename
                           l[nodename]=nnodename
                   for m in k[nodethree]:
                       for n in m:
                           for o in n:
                               
                               if(o[nodemodulename]==pnodemodulename and o[nodename]==pnodename):
                                   o[nodemodulename]=nnodemodulename
                                   o[nodename]=nnodename
                   num=num+1
        for j in castlist:
            if(j[0][0]==pnodemodulename and j[0][1]==pnodename):
                j[0][0]=nnodemodulename
                j[0][1]=nnodename
            if(j[1][0]==pnodemodulename and j[1][1]==pnodename):
                j[1][0]=nnodemodulename
                j[1][1]=nnodename
        if(delv!=-1):
            del allvalues[delv]
                    

    def checkkeyvalues(self,description,infstack, allvalues,buf=sys.stdout):
        global deep,nowmodulename

        if(self.__class__.__name__ == 'Instance'):
           storemodulename=nowmodulename
           find=0
           m=description.findmodule(self.module)
           if(m!=None):
               find=1
               nowmodulename=self.module
               m.checkkeyvalues(description,[], allvalues,buf)


           if(find==0):
               print('do not find module ' ,self.module)
           else:
               for i in self.children():
                   if(i.__class__.__name__!= 'ParamArg'):
                       valueslist=[]
                       nowinfstack=copy.deepcopy(infstack)
                       i.findvalues(valueslist,buf)
                       for n in valueslist:
                           n[nodemodulename]=storemodulename
                           n.append(0)
                       porttype='x'
                       for j in allvalues:
                           if(j[nodemodulename]==nowmodulename and j[nodename]==str(i.portname)):
                              porttype=j[nodetype]
                       if(porttype=='Input'):
                           for k in allvalues:
                               if(k[nodemodulename]==nowmodulename and k[nodename]==str(i.portname)):
                                   for o in valueslist:
                                       k[nodegra].append(o)
                                   k[nodethree].append([nowinfstack,valueslist])

                       if(porttype=='Output'):
                           for l in valueslist:
                               for m in allvalues:
                                   if(m[nodemodulename]==l[nodemodulename] and m[nodename]==l[nodename]):
                                       m[nodegra].append([nowmodulename,str(i.portname),0,0])
                                       m[nodethree].append([nowinfstack,[[nowmodulename,str(i.portname),0,0]]])    
                                                             
           nowmodulename= storemodulename

        elif(self.__class__.__name__ == 'Assign' or self.__class__.__base__.__name__ == 'Assign' or self.__class__.__base__.__name__ == 'Substitution'):

            lvalues=[];
            (self.children())[0].findvalues(lvalues,buf)
            rvalues=[];
            (self.children())[1].findvalues(rvalues,buf)

            for i in rvalues:
                i.append(1)
            for i in rvalues:
                i[granodedeepgap]=0
            nowinfstack=copy.deepcopy(infstack)
            for i in nowinfstack:
                i[granodedeepgap]=deep-i[granodedeepgap]
            for c in range(len(allvalues)):
                for i in lvalues:
                    if( allvalues[c][nodemodulename]==i[granodemodulename] and allvalues[c][nodename]==i[granodename]):
                      allvalues[c][nodegra]=allvalues[c][nodegra]+rvalues+nowinfstack
                      allvalues[c][nodethree].append([nowinfstack,rvalues])



        elif(self.__class__.__name__ == 'IfStatement'):
            rvalues=[];
            (self.children())[0].findvalues(rvalues,buf)
            for i in rvalues:
                i.append(0)
            infstack=infstack+rvalues
            deep=deep+1;

            for k in range(1,len(self.children())):
                (self.children())[k].checkkeyvalues(description,infstack,allvalues,buf)
            deep=deep-1;
            for i in range(len(infstack)-1,0,-1):
                if(infstack[i][granodedeepgap]==deep):
                    infstack.remove(infstack[i])        
        elif(self.__class__.__name__ == 'CaseStatement'):    
            rvalues=[];
            (self.children())[0].findvalues(rvalues,buf)
            for i in rvalues:
                i.append(0)
            for k in range(1,len(self.children())): 
                infstack=infstack+rvalues
                rvaluesc=[]
                if(len(((self.children())[k]).children())>1):
                    ((self.children())[k]).children()[0].findvalues(rvaluesc,buf)
                for i in rvaluesc:
                    i.append(0);
                infstack=infstack+rvaluesc;
   
                deep=deep+1;
                for l in range(len(((self.children())[k]).children())):
                    ((self.children())[k]).children()[l].checkkeyvalues(description,infstack,allvalues,buf)
                deep=deep-1;
                x=0 
                while x<len(infstack):
                    if(infstack[x][granodedeepgap]==deep):
                       del(infstack[x])
                    else:
                       x=x+1                      
        elif(self.__class__.__name__ == 'Function'):
            pass;
        else:
            for c in self.children():
                c.checkkeyvalues(description,infstack, allvalues,buf)

# ------------------------------------------------------------------------------
class Source(Node):
    attr_names = ('name',)

    def __init__(self, name, description, lineno=0):
        self.lineno = lineno
        self.name = name
        self.description = description

    def children(self):
        nodelist = []
        if self.description:
            nodelist.append(self.description)
        return tuple(nodelist)


class Description(Node):
    attr_names = ()

    def __init__(self, definitions, lineno=0):
        self.lineno = lineno
        self.definitions = definitions

    def children(self):
        nodelist = []
        if self.definitions:
            nodelist.extend(self.definitions)
        return tuple(nodelist)


class ModuleDef(Node):
    attr_names = ('name',)

    def __init__(self, name, paramlist, portlist, items, default_nettype='wire', lineno=0):
        self.lineno = lineno
        self.name = name
        self.paramlist = paramlist
        self.portlist = portlist
        self.items = items
        self.default_nettype = default_nettype

    def children(self):
        nodelist = []
        if self.paramlist:
            nodelist.append(self.paramlist)
        if self.portlist:
            nodelist.append(self.portlist)
        if self.items:
            nodelist.extend(self.items)
        return tuple(nodelist)


class Paramlist(Node):
    attr_names = ()

    def __init__(self, params, lineno=0):
        self.lineno = lineno
        self.params = params

    def children(self):
        nodelist = []
        if self.params:
            nodelist.extend(self.params)
        return tuple(nodelist)


class Portlist(Node):
    attr_names = ()

    def __init__(self, ports, lineno=0):
        self.lineno = lineno
        self.ports = ports

    def children(self):
        nodelist = []
        if self.ports:
            nodelist.extend(self.ports)
        return tuple(nodelist)


class Port(Node):
    attr_names = ('name', 'type',)

    def __init__(self, name, width, dimensions, type, lineno=0):
        self.lineno = lineno
        self.name = name
        self.width = width
        self.dimensions = dimensions
        self.type = type

    def children(self):
        nodelist = []
        if self.width:
            nodelist.append(self.width)
        return tuple(nodelist)


class Width(Node):
    attr_names = ()

    def __init__(self, msb, lsb, lineno=0):
        self.lineno = lineno
        self.msb = msb
        self.lsb = lsb

    def children(self):
        nodelist = []
        if self.msb:
            nodelist.append(self.msb)
        if self.lsb:
            nodelist.append(self.lsb)
        return tuple(nodelist)


class Length(Width):
    pass


class Dimensions(Node):
    attr_names = ()

    def __init__(self, lengths, lineno=0):
        self.lineno = lineno
        self.lengths = lengths

    def children(self):
        nodelist = []
        if self.lengths:
            nodelist.extend(self.lengths)
        return tuple(nodelist)


class Identifier(Node):
    attr_names = ('name',)

    def __init__(self, name, scope=None, lineno=0):
        self.lineno = lineno
        self.name = name
        self.scope = scope

    def children(self):
        nodelist = []
        if self.scope:
            nodelist.append(self.scope)
        return tuple(nodelist)

    def __repr__(self):
        if self.scope is None:
            return self.name
        return self.scope.__repr__() + '.' + self.name


class Value(Node):
    attr_names = ()

    def __init__(self, value, lineno=0):
        self.lineno = lineno
        self.value = value

    def children(self):
        nodelist = []
        if self.value:
            nodelist.append(self.value)
        return tuple(nodelist)


class Constant(Value):
    attr_names = ('value',)

    def __init__(self, value, lineno=0):
        self.lineno = lineno
        self.value = value

    def children(self):
        nodelist = []
        return tuple(nodelist)

    def __repr__(self):
        return str(self.value)


class IntConst(Constant):
    pass


class FloatConst(Constant):
    pass


class StringConst(Constant):
    pass


class Variable(Value):
    attr_names = ('name', 'signed')

    def __init__(self, name, width=None, signed=False, dimensions=None, value=None, lineno=0):
        self.lineno = lineno
        self.name = name
        self.width = width
        self.signed = signed
        self.dimensions = dimensions
        self.value = value

    def children(self):
        nodelist = []
        if self.width:
            nodelist.append(self.width)
        if self.dimensions:
            nodelist.append(self.dimensions)
        if self.value:
            nodelist.append(self.value)
        return tuple(nodelist)


class Input(Variable):
    pass


class Output(Variable):
    pass


class Inout(Variable):
    pass


class Tri(Variable):
    pass


class Wire(Variable):
    pass


class Reg(Variable):
    pass


class Integer(Variable):
    pass


class Real(Variable):
    pass


class Genvar(Variable):
    pass


class Ioport(Node):
    attr_names = ()

    def __init__(self, first, second=None, lineno=0):
        self.lineno = lineno
        self.first = first
        self.second = second

    def children(self):
        nodelist = []
        if self.first:
            nodelist.append(self.first)
        if self.second:
            nodelist.append(self.second)
        return tuple(nodelist)


class Parameter(Node):
    attr_names = ('name', 'signed')

    def __init__(self, name, value, width=None, signed=False, lineno=0):
        self.lineno = lineno
        self.name = name
        self.value = value
        self.width = width
        self.signed = signed
        self.dimensions = None

    def children(self):
        nodelist = []
        if self.value:
            nodelist.append(self.value)
        if self.width:
            nodelist.append(self.width)
        return tuple(nodelist)


class Localparam(Parameter):
    pass


class Supply(Parameter):
    pass


class Decl(Node):
    attr_names = ()

    def __init__(self, list, lineno=0):
        self.lineno = lineno
        self.list = list

    def children(self):
        nodelist = []
        if self.list:
            nodelist.extend(self.list)
        return tuple(nodelist)

    def changereg(self,regname):
        for i in range(len(self.children())):
            c=self.children()[i]
            if(c.__class__.__name__ == 'Reg' and c.name==regname):
                x=Wire(c.name, None, c.signed, c.dimensions, c.value, c.lineno)
                self.list=list(self.list)
                self.list[i]=x
                tuple(self.list)



class Concat(Node):
    attr_names = ()

    def __init__(self, list, lineno=0):
        self.lineno = lineno
        self.list = list

    def children(self):
        nodelist = []
        if self.list:
            nodelist.extend(self.list)
        return tuple(nodelist)


class LConcat(Concat):
    pass


class Repeat(Node):
    attr_names = ()

    def __init__(self, value, times, lineno=0):
        self.lineno = lineno
        self.value = value
        self.times = times

    def children(self):
        nodelist = []
        if self.value:
            nodelist.append(self.value)
        if self.times:
            nodelist.append(self.times)
        return tuple(nodelist)


class Partselect(Node):
    attr_names = ()

    def __init__(self, var, msb, lsb, lineno=0):
        self.lineno = lineno
        self.var = var
        self.msb = msb
        self.lsb = lsb

    def children(self):
        nodelist = []
        if self.var:
            nodelist.append(self.var)
        if self.msb:
            nodelist.append(self.msb)
        if self.lsb:
            nodelist.append(self.lsb)
        return tuple(nodelist)


class Pointer(Node):
    attr_names = ()

    def __init__(self, var, ptr, lineno=0):
        self.lineno = lineno
        self.var = var
        self.ptr = ptr

    def children(self):
        nodelist = []
        if self.var:
            nodelist.append(self.var)
        if self.ptr:
            nodelist.append(self.ptr)
        return tuple(nodelist)


class Lvalue(Node):
    attr_names = ()

    def __init__(self, var, lineno=0):
        self.lineno = lineno
        self.var = var

    def children(self):
        nodelist = []
        if self.var:
            nodelist.append(self.var)
        return tuple(nodelist)


class Rvalue(Node):
    attr_names = ()

    def __init__(self, var, lineno=0):
        self.lineno = lineno
        self.var = var

    def children(self):
        nodelist = []
        if self.var:
            nodelist.append(self.var)
        return tuple(nodelist)


# ------------------------------------------------------------------------------
class Operator(Node):
    attr_names = ()

    def __init__(self, left, right, lineno=0):
        self.lineno = lineno
        self.left = left
        self.right = right

    def children(self):
        nodelist = []
        if self.left:
            nodelist.append(self.left)
        if self.right:
            nodelist.append(self.right)
        return tuple(nodelist)

    def __repr__(self):
        ret = '(' + self.__class__.__name__
        for c in self.children():
            ret += ' ' + c.__repr__()
        ret += ')'
        return ret


class UnaryOperator(Operator):
    attr_names = ()

    def __init__(self, right, lineno=0):
        self.lineno = lineno
        self.right = right

    def children(self):
        nodelist = []
        if self.right:
            nodelist.append(self.right)
        return tuple(nodelist)


# Level 1 (Highest Priority)
class Uplus(UnaryOperator):
    pass


class Uminus(UnaryOperator):
    pass


class Ulnot(UnaryOperator):
    pass


class Unot(UnaryOperator):
    pass


class Uand(UnaryOperator):
    pass


class Unand(UnaryOperator):
    pass


class Uor(UnaryOperator):
    pass


class Unor(UnaryOperator):
    pass


class Uxor(UnaryOperator):
    pass


class Uxnor(UnaryOperator):
    pass


# Level 2
class Power(Operator):
    pass


class Times(Operator):
    pass


class Divide(Operator):
    pass


class Mod(Operator):
    pass


# Level 3
class Plus(Operator):
    pass


class Minus(Operator):
    pass


# Level 4
class Sll(Operator):
    pass


class Srl(Operator):
    pass


class Sla(Operator):
    pass


class Sra(Operator):
    pass


# Level 5
class LessThan(Operator):
    pass


class GreaterThan(Operator):
    pass


class LessEq(Operator):
    pass


class GreaterEq(Operator):
    pass


# Level 6
class Eq(Operator):
    pass


class NotEq(Operator):
    pass


class Eql(Operator):
    pass  # ===


class NotEql(Operator):
    pass  # !==


# Level 7
class And(Operator):
    pass


class Xor(Operator):
    pass


class Xnor(Operator):
    pass


# Level 8
class Or(Operator):
    pass


# Level 9
class Land(Operator):
    pass


# Level 10
class Lor(Operator):
    pass


# Level 11
class Cond(Operator):
    attr_names = ()

    def __init__(self, cond, true_value, false_value, lineno=0):
        self.lineno = lineno
        self.cond = cond
        self.true_value = true_value
        self.false_value = false_value

    def children(self):
        nodelist = []
        if self.cond:
            nodelist.append(self.cond)
        if self.true_value:
            nodelist.append(self.true_value)
        if self.false_value:
            nodelist.append(self.false_value)
        return tuple(nodelist)


class Assign(Node):
    attr_names = ()

    def __init__(self, left, right, ldelay=None, rdelay=None, lineno=0):
        self.lineno = lineno
        self.left = left
        self.right = right
        self.ldelay = ldelay
        self.rdelay = rdelay

    def children(self):
        nodelist = []
        if self.left:
            nodelist.append(self.left)
        if self.right:
            nodelist.append(self.right)
        if self.ldelay:
            nodelist.append(self.ldelay)
        if self.rdelay:
            nodelist.append(self.rdelay)
        return tuple(nodelist)


class Always(Node):
    attr_names = ()

    def __init__(self, sens_list, statement, lineno=0):
        self.lineno = lineno
        self.sens_list = sens_list
        self.statement = statement

    def children(self):
        nodelist = []
        if self.sens_list:
            nodelist.append(self.sens_list)
        if self.statement:
            nodelist.append(self.statement)
        return tuple(nodelist)


class AlwaysFF(Always):
    pass


class AlwaysComb(Always):
    pass


class AlwaysLatch(Always):
    pass


class SensList(Node):
    attr_names = ()

    def __init__(self, list, lineno=0):
        self.lineno = lineno
        self.list = list

    def children(self):
        nodelist = []
        if self.list:
            nodelist.extend(self.list)
        return tuple(nodelist)


class Sens(Node):
    attr_names = ('type',)

    def __init__(self, sig, type='posedge', lineno=0):
        self.lineno = lineno
        self.sig = sig
        self.type = type  # 'posedge', 'negedge', 'level', 'all' (*)

    def children(self):
        nodelist = []
        if self.sig:
            nodelist.append(self.sig)
        return tuple(nodelist)


class Substitution(Node):
    attr_names = ()

    def __init__(self, left, right, ldelay=None, rdelay=None, lineno=0):
        self.lineno = lineno
        self.left = left
        self.right = right
        self.ldelay = ldelay
        self.rdelay = rdelay

    def children(self):
        nodelist = []
        if self.left:
            nodelist.append(self.left)
        if self.right:
            nodelist.append(self.right)
        if self.ldelay:
            nodelist.append(self.ldelay)
        if self.rdelay:
            nodelist.append(self.rdelay)
        return tuple(nodelist)


class BlockingSubstitution(Substitution):
    pass


class NonblockingSubstitution(Substitution):
    pass


class IfStatement(Node):
    attr_names = ()

    def __init__(self, cond, true_statement, false_statement, lineno=0):
        self.lineno = lineno
        self.cond = cond
        self.true_statement = true_statement
        self.false_statement = false_statement

    def children(self):
        nodelist = []
        if self.cond:
            nodelist.append(self.cond)
        if self.true_statement:
            nodelist.append(self.true_statement)
        if self.false_statement:
            nodelist.append(self.false_statement)
        return tuple(nodelist)


class ForStatement(Node):
    attr_names = ()

    def __init__(self, pre, cond, post, statement, lineno=0):
        self.lineno = lineno
        self.pre = pre
        self.cond = cond
        self.post = post
        self.statement = statement

    def children(self):
        nodelist = []
        if self.pre:
            nodelist.append(self.pre)
        if self.cond:
            nodelist.append(self.cond)
        if self.post:
            nodelist.append(self.post)
        if self.statement:
            nodelist.append(self.statement)
        return tuple(nodelist)


class WhileStatement(Node):
    attr_names = ()

    def __init__(self, cond, statement, lineno=0):
        self.lineno = lineno
        self.cond = cond
        self.statement = statement

    def children(self):
        nodelist = []
        if self.cond:
            nodelist.append(self.cond)
        if self.statement:
            nodelist.append(self.statement)
        return tuple(nodelist)


class CaseStatement(Node):
    attr_names = ()

    def __init__(self, comp, caselist, lineno=0):
        self.lineno = lineno
        self.comp = comp
        self.caselist = caselist

    def children(self):
        nodelist = []
        if self.comp:
            nodelist.append(self.comp)
        if self.caselist:
            nodelist.extend(self.caselist)
        return tuple(nodelist)


class CasexStatement(CaseStatement):
    pass


class CasezStatement(CaseStatement):
    pass


class UniqueCaseStatement(CaseStatement):
    pass


class Case(Node):
    attr_names = ()

    def __init__(self, cond, statement, lineno=0):
        self.lineno = lineno
        self.cond = cond
        self.statement = statement

    def children(self):
        nodelist = []
        if self.cond:
            nodelist.extend(self.cond)
        if self.statement:
            nodelist.append(self.statement)
        return tuple(nodelist)


class Block(Node):
    attr_names = ('scope',)

    def __init__(self, statements, scope=None, lineno=0):
        self.lineno = lineno
        self.statements = statements
        self.scope = scope

    def children(self):
        nodelist = []
        if self.statements:
            nodelist.extend(self.statements)
        return tuple(nodelist)


class Initial(Node):
    attr_names = ()

    def __init__(self, statement, lineno=0):
        self.lineno = lineno
        self.statement = statement

    def children(self):
        nodelist = []
        if self.statement:
            nodelist.append(self.statement)
        return tuple(nodelist)


class EventStatement(Node):
    attr_names = ()

    def __init__(self, senslist, lineno=0):
        self.lineno = lineno
        self.senslist = senslist

    def children(self):
        nodelist = []
        if self.senslist:
            nodelist.append(self.senslist)
        return tuple(nodelist)


class WaitStatement(Node):
    attr_names = ()

    def __init__(self, cond, statement, lineno=0):
        self.lineno = lineno
        self.cond = cond
        self.statement = statement

    def children(self):
        nodelist = []
        if self.cond:
            nodelist.append(self.cond)
        if self.statement:
            nodelist.append(self.statement)
        return tuple(nodelist)


class ForeverStatement(Node):
    attr_names = ()

    def __init__(self, statement, lineno=0):
        self.lineno = lineno
        self.statement = statement

    def children(self):
        nodelist = []
        if self.statement:
            nodelist.append(self.statement)
        return tuple(nodelist)


class DelayStatement(Node):
    attr_names = ()

    def __init__(self, delay, lineno=0):
        self.lineno = lineno
        self.delay = delay

    def children(self):
        nodelist = []
        if self.delay:
            nodelist.append(self.delay)
        return tuple(nodelist)


class InstanceList(Node):
    attr_names = ('module',)

    def __init__(self, module, parameterlist, instances, lineno=0):
        self.lineno = lineno
        self.module = module
        self.parameterlist = parameterlist
        self.instances = instances

    def children(self):
        nodelist = []
        if self.parameterlist:
            nodelist.extend(self.parameterlist)
        if self.instances:
            nodelist.extend(self.instances)
        return tuple(nodelist)


class Instance(Node):
    attr_names = ('name', 'module')

    def __init__(self, module, name, portlist, parameterlist, array=None, lineno=0):
        self.lineno = lineno
        self.module = module
        self.name = name
        self.portlist = portlist
        self.parameterlist = parameterlist
        self.array = array

    def children(self):
        nodelist = []
        if self.array:
            nodelist.append(self.array)
        if self.parameterlist:
            nodelist.extend(self.parameterlist)
        if self.portlist:
            nodelist.extend(self.portlist)
        return tuple(nodelist)


class ParamArg(Node):
    attr_names = ('paramname',)

    def __init__(self, paramname, argname, lineno=0):
        self.lineno = lineno
        self.paramname = paramname
        self.argname = argname

    def children(self):
        nodelist = []
        if self.argname:
            nodelist.append(self.argname)
        return tuple(nodelist)


class PortArg(Node):
    attr_names = ('portname',)

    def __init__(self, portname, argname, lineno=0):
        self.lineno = lineno
        self.portname = portname
        self.argname = argname

    def children(self):
        nodelist = []
        if self.argname:
            nodelist.append(self.argname)
        return tuple(nodelist)


class Function(Node):
    attr_names = ('name',)

    def __init__(self, name, retwidth, statement, lineno=0):
        self.lineno = lineno
        self.name = name
        self.retwidth = retwidth
        self.statement = statement

    def children(self):
        nodelist = []
        if self.retwidth:
            nodelist.append(self.retwidth)
        if self.statement:
            nodelist.extend(self.statement)
        return tuple(nodelist)

    def __repr__(self):
        return self.name.__repr__()


class FunctionCall(Node):
    attr_names = ()

    def __init__(self, name, args, lineno=0):
        self.lineno = lineno
        self.name = name
        self.args = args

    def children(self):
        nodelist = []
        if self.name:
            nodelist.append(self.name)
        if self.args:
            nodelist.extend(self.args)
        return tuple(nodelist)

    def __repr__(self):
        return self.name.__repr__()


class Task(Node):
    attr_names = ('name',)

    def __init__(self, name, statement, lineno=0):
        self.lineno = lineno
        self.name = name
        self.statement = statement

    def children(self):
        nodelist = []
        if self.statement:
            nodelist.extend(self.statement)
        return tuple(nodelist)


class TaskCall(Node):
    attr_names = ()

    def __init__(self, name, args, lineno=0):
        self.lineno = lineno
        self.name = name
        self.args = args

    def children(self):
        nodelist = []
        if self.name:
            nodelist.append(self.name)
        if self.args:
            nodelist.extend(self.args)
        return tuple(nodelist)


class GenerateStatement(Node):
    attr_names = ()

    def __init__(self, items, lineno=0):
        self.lineno = lineno
        self.items = items

    def children(self):
        nodelist = []
        if self.items:
            nodelist.extend(self.items)
        return tuple(nodelist)


class SystemCall(Node):
    attr_names = ('syscall',)

    def __init__(self, syscall, args, lineno=0):
        self.lineno = lineno
        self.syscall = syscall
        self.args = args

    def children(self):
        nodelist = []
        if self.args:
            nodelist.extend(self.args)
        return tuple(nodelist)

    def __repr__(self):
        ret = []
        ret.append('(')
        ret.append('$')
        ret.append(self.syscall)
        for a in self.args:
            ret.append(' ')
            ret.append(str(a))
        ret.append(')')
        return ''.join(ret)


class IdentifierScopeLabel(Node):
    attr_names = ('name', 'loop')

    def __init__(self, name, loop=None, lineno=0):
        self.lineno = lineno
        self.name = name
        self.loop = loop

    def children(self):
        nodelist = []
        return tuple(nodelist)


class IdentifierScope(Node):
    attr_names = ()

    def __init__(self, labellist, lineno=0):
        self.lineno = lineno
        self.labellist = labellist

    def children(self):
        nodelist = []
        if self.labellist:
            nodelist.extend(self.labellist)
        return tuple(nodelist)


class Pragma(Node):
    attr_names = ()

    def __init__(self, entry, lineno=0):
        self.lineno = lineno
        self.entry = entry

    def children(self):
        nodelist = []
        if self.entry:
            nodelist.append(self.entry)
        return tuple(nodelist)


class PragmaEntry(Node):
    attr_names = ('name', )

    def __init__(self, name, value=None, lineno=0):
        self.lineno = lineno
        self.name = name
        self.value = value

    def children(self):
        nodelist = []
        if self.value:
            nodelist.append(self.value)
        return tuple(nodelist)


class Disable(Node):
    attr_names = ('dest',)

    def __init__(self, dest, lineno=0):
        self.lineno = lineno
        self.dest = dest

    def children(self):
        nodelist = []
        return tuple(nodelist)


class ParallelBlock(Node):
    attr_names = ('scope',)

    def __init__(self, statements, scope=None, lineno=0):
        self.lineno = lineno
        self.statements = statements
        self.scope = scope

    def children(self):
        nodelist = []
        if self.statements:
            nodelist.extend(self.statements)
        return tuple(nodelist)


class SingleStatement(Node):
    attr_names = ()

    def __init__(self, statement, lineno=0):
        self.lineno = lineno
        self.statement = statement

    def children(self):
        nodelist = []
        if self.statement:
            nodelist.append(self.statement)
        return tuple(nodelist)


class EmbeddedCode(Node):
    attr_names = ('code',)

    def __init__(self, code, lineno=0):
        self.code = code

    def children(self):
        nodelist = []
        return tuple(nodelist)
