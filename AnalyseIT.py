import matplotlib.pyplot as plt
import numpy as np
from pyautocad import Autocad, APoint
import math
class Node:
  def __init__(self, x, y, fx, fy, s, disx, disy, dx, dy,mz):
    self.x = x
    self.y = y
    self.fx = fx
    self.fy = fy
    self.s = s
    self.disx=disx
    self.disy=disy  
    self.dx = dx
    self.dy = dy
    self.mz=mz

class Member:
      def __init__(self, n, f, l, cx, cy, qf):
        self.n = n
        self.f = f
        self.l = l
        self.cx =cx
        self.cy =cy
        self.qf=qf 
bp =2
ln=8
n= []
m= []
unconstrained=[]
constrained= []
gd = 0
lsum=0.0
p=int(input("Enter the no. of nodes you want to add:  "))
for i in range(p):
   n.append(Node(0.0,0.0,0.0,0.0,' ',-1.0,-1.0, 0, 0,-1.0))
   print("Enter X & Y coordinates of node", (i+1), ", seperated by space") 
   n[i].x, n[i].y=map(float,input().split())
ln=len(n)*2
ssm = [[0 for col in range(ln)] for row in range(ln)];
Q= [0.0 for i in range(ln)]
D= [0.0 for i in range(ln)]
for i in range(p):
  unconstrained.append(i)
nm=int(input("Enter the no. of Members you want to add:  "))
for i in range(nm):
    print("Add Members by giving nodes seperated by space") 
    near, far=map(int,input().split())
    m.append(Member(n[near-1],n[far-1],0.0,0.0,0.0,0.0))
    xd=(m[i].f.x-m[i].n.x)
    yd=(m[i].f.y-m[i].n.y)
    l=math.sqrt( (xd**2)+(yd**2) )
    lsum+=l;
    cx=xd/l
    cy=yd/l
    m[i].l=l
    m[i].cx=cx
    m[i].cy=cy
    print('cx=', cx)
    print('cy=', cy)
lavg=lsum/nm
p=int(input("Enter no. of Nodes with Horizontal Force-"))
if p>0:
    print("Apply Horizontal force on Members")
else:
    print("OK")
for i in range(p):
    node=int(input("Node No.: "))
    Fx=float(input("Fx= "))
    n[node-1].fx=Fx
    unconstrained.remove(node-1)
    constrained.append(node-1)
p=int(input("Enter no. of Nodes with Vertical Force-"))
if p>0:
    print("Apply Vertical force on Members")
else:
    print("OK")
try:
  for i in range(p):
      node=int(input("Node No.: "))
      Fy=float(input("Fy= "))
      n[node-1].fy=Fy
      for i in range(len(unconstrained)):
        if(unconstrained[i]==node-1):
          unconstrained.remove(node-1)
          constrained.append(node-1)
except:
  pass
#A=int(input("Enter Cross-Sectional Area of Members-"))
#E=int(input("Enter Modulus of Elasticity of Members-"))
p=int(input("Enter no. of Horizontal Roller Support-"))
if p>0:
    print("Apply Roller Support on nodes")
else:
    print("OK")
for i in range(p):
    node=int(input("Node No.: "))
    n[node-1].fx=0.0
    n[node-1].fy=-1.0
    n[node-1].disy=0.0
    n[node-1].s='rh'
    unconstrained.remove(node-1)
    constrained.append(node-1)
p=int(input("Enter no. of Vertical Roller Support-"))
if p>0:
    print("Apply Roller Support on nodes")
else:
    print("OK")
for i in range(p):
    node=int(input("Node No.: "))
    n[node-1].fx=-1.0
    n[node-1].fy=0.0
    n[node-1].disx=0.0
    n[node-1].s='rv'
    unconstrained.remove(node-1)
    constrained.append(node-1)
p=int(input("Enter no. of Nodes Pin Support-"))
if p>0:
    print("Apply Pin Support on nodes")
else:
    print("OK")
for i in range(p):
    node=int(input("Node No.: "))
    n[node-1].fx=-1.0
    n[node-1].fy=-1.0
    n[node-1].disx=0.0
    n[node-1].disy=0.0
    n[node-1].s='pin'
    unconstrained.remove(node-1)
    constrained.append(node-1)
##    p=int(input("Enter no. of Fixed Support-"))
##    if p>0:
##        print("Apply on Fixed Nodes")
##    else:
##        print("OK")
##    for i in range(p):
##        node=int(input("Node No.: "))
##        n[node-1].fx=-1.0
##        n[node-1].fy=-1.0
##        n[node-1].mz=-1.0
##        n[node-1].disx=0.0
##        n[node-1].disy=0.0
##        n[node-1].s='f'
##        unconstrained.remove(node-1)
##        constrained.append(node-1)

###################################################################
acad = Autocad(create_if_not_exists=True)
acad.prompt("Please open AutoCAD and create a new file to view your structure, press Enter when done\n")
input()
print(acad.doc.Name)
sc=lavg/10
#####################################################
LayerObj = acad.ActiveDocument.Layers.Add("Node no.")
acad.ActiveDocument.ActiveLayer = LayerObj
ClrNum = 150#blue
LayerObj.color = ClrNum
for i in range(len(n)):
  p1 = APoint(n[i].x, n[i].y)
  text = acad.model.AddText('N%s' % (i+1),p1, .5*sc)
#####################################################
LayerObj = acad.ActiveDocument.Layers.Add("Members")
acad.ActiveDocument.ActiveLayer = LayerObj
ClrNum = 30#orange
LayerObj.color = ClrNum
#LayerObj.Lineweight = 30
for i in range(nm):
    p1 = APoint(m[i].n.x, m[i].n.y)
    p2 = APoint(m[i].f.x, m[i].f.y)
    acad.model.AddLine(p1, p2)
    x1=(m[i].n.x+m[i].f.x)/2.0
    y1=(m[i].n.y+m[i].f.y)/2.0+.2
    text = acad.model.AddText('M%s' % (i+1), APoint(x1,y1), .08*lavg)
#####################################################
for i in range(len(n)):
  LayerObj = acad.ActiveDocument.Layers.Add("Force")
  acad.ActiveDocument.ActiveLayer = LayerObj
  ClrNum = 82#dark green
  LayerObj.color = ClrNum
  #LayerObj.Lineweight = 25
  if n[i].fx!=0.0 and n[i].fx!=-1.0:
    p1 = APoint(n[i].x, n[i].y)
    p2 = APoint(n[i].x-n[i].fx*sc, n[i].y)
    acad.model.AddLine(p1, p2)
    text = acad.model.AddText('F=%0.1fk'%n[i].fx,p2, .04*lavg)
    p1 = APoint(n[i].x-0.215*n[i].fx*sc, n[i].y+0.125*n[i].fx*sc)
    p2 = APoint(n[i].x, n[i].y)
    acad.model.AddLine(p1, p2)
    p1 = APoint(n[i].x-0.215*n[i].fx*sc, n[i].y-0.125*n[i].fx*sc)
    p2 = APoint(n[i].x, n[i].y)
    acad.model.AddLine(p1, p2)
  if n[i].fy!=0 and n[i].fy!=-1.0:
    p1 = APoint(n[i].x, n[i].y)
    p2 = APoint(n[i].x, n[i].y-n[i].fy*sc)
    acad.model.AddLine(p1, p2)
    text = acad.model.AddText('F=%0.1fk'%n[i].fy,p2, .04*lavg)
    p1 = APoint(n[i].x+0.125*n[i].fy*sc, n[i].y-0.215*n[i].fy*sc)
    p2 = APoint(n[i].x, n[i].y)
    acad.model.AddLine(p1, p2)
    p1 = APoint(n[i].x-0.125*n[i].fy*sc, n[i].y-0.215*n[i].fy*sc)
    p2 = APoint(n[i].x, n[i].y)
    acad.model.AddLine(p1, p2)
#####################################################
  LayerObj = acad.ActiveDocument.Layers.Add("Support")
  acad.ActiveDocument.ActiveLayer = LayerObj
  ClrNum = 240#brown
  LayerObj.color = ClrNum
  #LayerObj.Lineweight = 18
  if n[i].s=='pin':
    p1 = APoint(n[i].x, n[i].y)
    p2 = APoint(n[i].x+0.65*sc, n[i].y-0.75*sc)
    acad.model.AddLine(p1, p2)
    p1 = APoint(n[i].x-0.65*sc, n[i].y-0.75*sc)
    p2 = APoint(n[i].x, n[i].y)
    acad.model.AddLine(p1, p2)
    p1 = APoint(n[i].x+0.65*sc, n[i].y-0.75*sc)
    p2 = APoint(n[i].x-0.65*sc, n[i].y-0.75*sc)
    acad.model.AddLine(p1, p2)
  if n[i].s=='rh':
    p1 = APoint(n[i].x, n[i].y-0.4*sc)
    acad.model.AddCircle(p1, 0.4*sc)
    p1 = APoint(n[i].x+1*sc, n[i].y-0.8*sc)
    p2=APoint(n[i].x-1*sc, n[i].y-0.8*sc)
    acad.model.AddLine(p1, p2) 
  if n[i].s=='rv':
    p1 = APoint(n[i].x+0.4*sc, n[i].y)
    acad.model.AddCircle(p1, 0.4*sc)
    p1 = APoint(n[i].x+0.8*sc, n[i].y-1*sc)
    p2=APoint(n[i].x+0.8*sc, n[i].y+1*sc) 
    acad.model.AddLine(p1, p2)
#########################################################################
    
gd=0
for i in range (len(unconstrained)):
    n[unconstrained[i]].dx=gd
    gd=gd+1
    n[unconstrained[i]].dy=gd
    gd=gd+1
for i in range (len(constrained)):
    if n[constrained[i]].s=='rv':
      n[constrained[i]].dy=gd
      gd=gd+1
      n[constrained[i]].dx=gd
      gd=gd+1
    else:
      n[constrained[i]].dx=gd
      gd=gd+1
      n[constrained[i]].dy=gd
      gd=gd+1
#################################################
sc=sc*0.5
LayerObj = acad.ActiveDocument.Layers.Add("Node Direction Vectors")
acad.ActiveDocument.ActiveLayer = LayerObj
ClrNum = 6#magenta
LayerObj.color = ClrNum
#LayerObj.Lineweight = 5
for i in range(len(n)):
    p1 = APoint(n[i].x+0.2*sc, n[i].y)
    p2 = APoint(n[i].x+2.2*sc, n[i].y)
    acad.model.AddLine(p1, p2)
    p3 = APoint(p2.x-0.4*sc, p2.y+0.25*sc)
    p4 = APoint(p2.x-0.4*sc, p2.y-0.25*sc)
    acad.model.AddLine(p2, p3)
    acad.model.AddLine(p2, p4)
    text = acad.model.AddText(int(n[i].dx+1), APoint(p2.x+0.2*sc,p2.y), .02*lavg)
    p1 = APoint(n[i].x, n[i].y+0.2*sc)
    p2 = APoint(n[i].x, n[i].y+2.2*sc)
    acad.model.AddLine(p1, p2)
    p3 = APoint(p2.x+0.25*sc, p2.y-0.4*sc)
    p4 = APoint(p2.x-0.25*sc, p2.y-0.4*sc)
    acad.model.AddLine(p2, p3)
    acad.model.AddLine(p2, p4)
    text = acad.model.AddText(int(n[i].dy+1), APoint(p2.x,p2.y+0.2*sc), .02*lavg)
print("PLOTTED SUCCESSFULLY:)");
#####################################################
for i in range(ln):
  for j in range(ln):
    ssm[i][j]=0.0

for i in range(nm):        
    ssm[int(m[i].n.dx)][int(m[i].n.dx)]+=(m[i].cx**2)/m[i].l
    ssm[int(m[i].n.dx)][int(m[i].n.dy)]+=(m[i].cx*m[i].cy)/m[i].l
    ssm[int(m[i].n.dx)][int(m[i].f.dx)]+=(-1*m[i].cx**2)/m[i].l
    ssm[int(m[i].n.dx)][int(m[i].f.dy)]+=(-1*m[i].cx*m[i].cy)/m[i].l

    ssm[int(m[i].n.dy)][int(m[i].n.dx)]+=(m[i].cx*m[i].cy)/m[i].l
    ssm[int(m[i].n.dy)][int(m[i].n.dy)]+=(m[i].cy**2)/m[i].l
    ssm[int(m[i].n.dy)][int(m[i].f.dx)]+=(-1*m[i].cx*m[i].cy)/m[i].l
    ssm[int(m[i].n.dy)][int(m[i].f.dy)]+=(-1*m[i].cy**2)/m[i].l

    ssm[int(m[i].f.dx)][int(m[i].n.dx)]=(-1*m[i].cx**2)/m[i].l
    ssm[int(m[i].f.dx)][int(m[i].n.dy)]=(-1*m[i].cx*m[i].cy)/m[i].l
    ssm[int(m[i].f.dx)][int(m[i].f.dx)]=(m[i].cx**2)/m[i].l
    ssm[int(m[i].f.dx)][int(m[i].f.dy)]=(m[i].cx*m[i].cy)/m[i].l

    ssm[int(m[i].f.dy)][int(m[i].n.dx)]=(-1*m[i].cx*m[i].cy)/m[i].l
    ssm[int(m[i].f.dy)][int(m[i].n.dy)]=(-1*m[i].cy**2)/m[i].l
    ssm[int(m[i].f.dy)][int(m[i].f.dx)]=(m[i].cx*m[i].cy)/m[i].l
    ssm[int(m[i].f.dy)][int(m[i].f.dy)]=(m[i].cy**2)/m[i].l
##print('constrained')
##for i in range(len(constrained)):    
##    print(constrained[i])
##print('unconstrained')
##for i in range(len(unconstrained)):
##    print(unconstrained[i])
print("STRUCTURE STIFFNESS MATRIX")
for i in range(ln):
  for j in range(ln):
    print('%.3f' % ssm[i][j], end ="\t")
  print()
for i in range(len(n)):
    Q[n[i].dx]=n[i].fx
    Q[n[i].dy]=n[i].fy
    D[n[i].dx]=n[i].disx
    D[n[i].dy]=n[i].disy
for i in range(ln):
    if(Q[i]==-1.0):
      bp=i
      break;
sQ= []
sD= []
sM= [[0 for col in range(bp)] for row in range(bp)];
sM1= [[0 for col in range(bp)] for row in range(ln-bp)];
for i in range(bp):
    sQ.append(Q[i])
    for j in range(bp):
      sM[i][j]=ssm[i][j]
x= np.linalg.solve(sM, sQ)
for i in range(bp):
    D[i]=x[i]
for i in range(len(n)):
    n[i].disx=D[n[i].dx]
    n[i].disy=D[n[i].dy]
for i in range(bp,ln):
  for j in range(bp):
    sM1[i-bp][j]=ssm[i][j]
for i in range(ln-bp):
  Q[bp+i]=0.0
  for j in range(bp):
    Q[bp+i]+=sM1[i][j]*D[j]
for i in range(ln):
  print('Q',(i+1),'=%.3f'%Q[i],'k\t','D',(i+1),'=%.3f'%D[i],'/AE')
for i in range(nm):
  m[i].qf=(-m[i].cx*m[i].n.disx-m[i].cy*m[i].n.disy+m[i].cx*m[i].f.disx+m[i].cy*m[i].f.disy)/m[i].l
  print('Force in M',(i+1),'=%.3f' %(m[i].qf),'k')
import pandas as pd
import matplotlib
from pylab import title, figure, xlabel, ylabel, xticks, bar, legend, axis, savefig
from fpdf import FPDF
import webbrowser as wb
from pyautocad import Autocad, APoint


df = pd.DataFrame()
df['Code No.'] = []
df['Q'] = []
df['D'] = []
columns = list(df)
data = []

for i in range(4, 10, 3):
  values = [i, i+1, i+2]
  zipped = zip(columns, values)
  a_dictionary = dict(zipped)
  data.append(a_dictionary)
df = df.append(data, True)
df1 = pd.DataFrame()
df1['Member No.'] = ["Q1", "Q2", "Q3", "Q4","Q5"]
df1['Length'] = [3, 4, 5, 3,0]
df1['Force'] = [4.505, -19.003, 0, 0,0]
columns = list(df1)
data = []
############################################################################################################################
df = pd.DataFrame()
df['Code No.'] = []
df['Q'] = []
df['D'] = []
columns = list(df)
data = []

for i in range(ln):
  values = [i+1, Q[i], D[i]]
  zipped = zip(columns, values)
  a_dictionary = dict(zipped)
  data.append(a_dictionary)
df = df.append(data, True)

df1 = pd.DataFrame()
df1['Member No.'] = []
df1['Length'] = []
df1['Force'] = []
columns1 = list(df1)
data1 = []

for i in range(nm):
  values1 = [i+1, m[i].l, m[i].qf]
  zipped1 = zip(columns1, values1)
  a_dictionary1 = dict(zipped1)
  data1.append(a_dictionary1)
df1 = df1.append(data1, True)

acad = Autocad(create_if_not_exists=True)
acad.prompt("Please open AutoCAD and create a new file to view your structure\n")
print(acad.doc.Name)
acad.prompt("Click the save button in AutoCAD popup dialog box, Remember not to change the name")
acad.doc.SendCommand('_-PLOT'' ''N''\n''MODEL''\n''\n''PublishToWeb PNG.pc3' '\n''\n''\n')


pdf = FPDF()
pdf.add_page()
pdf.set_xy(0, 0)
pdf.set_font('times', 'B', 35)
pdf.set_text_color(0,90,0)
pdf.cell(60)
pdf.cell(90, 25, "Truss Analysis Report", 0, 2, 'C')
pdf.set_text_color(0,10,0)
pdf.cell(120, 80, " ", 0, 2, 'C')
pdf.cell(-40)
pdf.set_font('arial', 'B', 12)
pdf.cell(50, 10, 'Code No.', 1, 0, 'C')
pdf.cell(40, 10, 'Q', 1, 0, 'C')
pdf.cell(40, 10, 'D', 1, 2, 'C')
pdf.cell(-90)
pdf.set_font('arial', '', 12)
for i in range(0, len(df)):
    pdf.cell(50, 10, '%s' % (df['Code No.'].iloc[i]), 1, 0, 'C')
    pdf.cell(40, 10, '%s' % (str(df.D.iloc[i])), 1, 0, 'C')
    pdf.cell(40, 10, '%s' % (str(df.Q.iloc[i])), 1, 2, 'C')
    pdf.cell(-90)
pdf.set_font('times', 'B', 18)
pdf.image('Truss6m-Model.png', x = 25, y = 20, w =0, h = 75, type = '', link = '')
pdf.image('AnalyseIT1.png', x = 20, y = 2, w = 20, h = 20, type = '', link = '')

pdf.cell(150, 10, "_______________________Member Properties_________________________", 0, 2, 'C')

pdf.set_font('arial', 'B', 12)
pdf.cell(50, 10, 'Member No.', 1, 0, 'C')
pdf.cell(40, 10, 'Length', 1, 0, 'C')
pdf.cell(40, 10, 'Force', 1, 2, 'C')
pdf.cell(-90)
pdf.set_font('arial', '', 12)
for i in range(0, len(df1)):
    pdf.cell(50, 10, '%s' % (df1['Member No.'].iloc[i]), 1, 0, 'C')
    pdf.cell(40, 10, '%s' % (str(df1.Length.iloc[i])), 1, 0, 'C')
    pdf.cell(40, 10, '%s' % (str(df1.Force.iloc[i])), 1, 2, 'C')
    pdf.cell(-90)
pdf.cell(90, 10, " ", 0, 2, 'C')
pdf.cell(0)
pdf.output('Report.pdf', 'F')
wb.open_new(r'C:\Users\BK GAUTAM\Documents\Report.pdf')








  


