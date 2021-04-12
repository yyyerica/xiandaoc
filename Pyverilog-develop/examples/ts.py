
# -*- coding: utf-8 -*-  


from reportlab.pdfgen.canvas import Canvas  
from reportlab.pdfbase import pdfmetrics  
from reportlab.pdfbase.cidfonts import UnicodeCIDFont  
pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))
from reportlab.pdfbase.ttfonts import TTFont 
pdfmetrics.registerFont(TTFont('msyh', 'msyh.ttf'))  
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer,Image,Table,TableStyle
import time

def rpt(list2,filename):
    story=[]
    stylesheet=getSampleStyleSheet()
    normalStyle = stylesheet['Normal']

    curr_date = time.strftime("%Y-%m-%d", time.localtime())

    #标题：段落的用法详见reportlab-userguide.pdf中chapter 6 Paragraph
    rpt_title = '<para autoLeading="off" fontSize=15 align=center><b><font face="msyh">verilog代码层面关键信号检测报告</font></b><br/><br/><br/></para>' 
    story.append(Paragraph(rpt_title,normalStyle)) 


    text = '''<para autoLeading="off" fontSize=8><font face="msyh" >报告介绍：</font><br/>
    <font face="msyh" fontsize=7>本报告是关于在verilog代码层面对安全性进行检测的生成报告，对于verilog中命名的变量进行重要性排序，下列是代码中一位寄存器的重要性排序，并给出了他们所在的文件名,程序更改后代码另存于newverilog文件夹。</font><br/></para>'''
    
    story.append(Paragraph(text,normalStyle))
  



    #表格数据：用法详见reportlab-userguide.pdf中chapter 7 Table
    component_data= [
    ['单位寄存器变量'],
     ]
    for i in range(len(list2)):
        x=['','','','']
        x[0]=i
        x[1]=list2[i][0]
        x[3]=filename[list2[i][1]]
        x[2]=round(list2[i][2],6) 
        component_data.append(x)
    #创建表格对象，并设定各列宽度
    component_table = Table(component_data, colWidths=[ 20,150, 80,70])
    #添加表格样式
    component_table.setStyle(TableStyle([
    ('FONTNAME',(0,0),(-1,-1),'msyh'),#字体
    ('FONTSIZE',(0,0),(-1,-1),6),#字体大小
    ('SPAN',(0,0),(3,0)),#合并第一行前三列
    ('BACKGROUND',(0,0),(-1,0), colors.lightskyblue),#设置第一行背景颜色
    ('SPAN',(-1,0),(-2,0)), #合并第一行后两列
    ('ALIGN',(-1,0),(-2,0),'RIGHT'),#对齐
    ('VALIGN',(-1,0),(-2,0),'MIDDLE'),  #对齐
    ('LINEBEFORE',(0,0),(0,-1),0.1,colors.grey),#设置表格左边线颜色为灰色，线宽为0.1
    ('GRID',(0,0),(-1,-1),0.5,colors.red),#设置表格框线为红色，线宽为0.5
    ]))
    story.append(component_table)

    

    doc = SimpleDocTemplate('report.pdf')
    doc.build(story)


