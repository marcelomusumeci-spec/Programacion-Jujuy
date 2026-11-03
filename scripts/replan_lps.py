"""R3: recalcular la red R2 por el 09/11 no laborable confirmado en LPS.
Comprueba que el motor reproduce tanto pase hacia delante como atrás de R2.
No modifica partes reales ni toma compromisos LPS como trabajo ejecutado.
"""
from pathlib import Path
from datetime import date,timedelta
import json,re,csv,hashlib,copy
ROOT=Path(__file__).resolve().parent.parent
R3_PDF='Jujuy_Programacion_R3_LPS.pdf'

def calendar_days(calendar):
 d=date(2026,1,1);days=[]
 while d<=date(2028,12,31):
  text=d.isoformat()
  if d.weekday()<5 and not any(r['start']<=text<=r['end'] for r in calendar['excludedRanges']):days.append(text)
  d+=timedelta(days=1)
 return days

def solve(tasks,calendar):
 days=calendar_days(calendar);byid={t['sourceId']:t for t in tasks};values={};visiting=set();edges={};order=[]
 for id,t in byid.items():
  edges[id]=[]
  for token in t['predecessors'].split(';'):
   if not token.strip():continue
   m=re.fullmatch(r'([A-Z0-9]+):(FS|SS)([+-]\d+)?',token.strip());assert m,token
   other,relation,lag=m.groups();assert other in byid;edges[id].append((other,relation,int(lag or 0)))
 def before(day):return sum(d<day for d in days)
 def through(day):return sum(d<=day for d in days)
 def early(id):
  if id in values:return values[id]
  assert id not in visiting, 'Dependencia circular: '+id
  visiting.add(id);t=byid[id];limits=[]
  for other,relation,lag in edges[id]:
   a,b=early(other);limits.append((b if relation=='FS' else a)+lag)
  if t['availability']:
   # Disponibilidad es comienzo de día para actividades/LIB; los otros
   # hitos raíz representan fin del día de su fecha explícita en R2.
   limits.append(before(t['availability']) if t['duration']>0 or id=='LIB' else through(t['start']))
  assert limits, 'Falta ancla para '+id
  start=max(limits);end=start+t['duration'];assert start>=1 and end<len(days)
  values[id]=(start,end);visiting.remove(id);order.append(id);return start,end
 for id in byid:early(id)
 finish=max(end for start,end in values.values());successors={id:[] for id in byid}
 for to,links in edges.items():
  for other,rel,lag in links:successors[other].append((to,rel,lag))
 latest={}
 for id in reversed(order):
  duration=byid[id]['duration'];limits=[finish-duration]
  for other,rel,lag in successors[id]:limits.append(latest[other]-lag-(duration if rel=='FS' else 0))
  latest[id]=min(limits);assert latest[id]>=values[id][0]
 result={}
 for id,t in byid.items():
  start,end=values[id]
  display_start=days[start] if t['duration']>0 or id=='LIB' else days[start-1]
  display_end=days[end-1] if t['duration']>0 else display_start
  result[id]={'startIndex':start,'endIndex':end,'start':display_start,'end':display_end,'lateStartIndex':latest[id],'floatDays':latest[id]-start}
 return result

def make_pdf(data):
 from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,PageBreak,Flowable
 from reportlab.lib.pagesizes import A3,landscape
 from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
 from reportlab.lib import colors
 from reportlab.pdfbase import pdfmetrics
 from reportlab.pdfbase.ttfonts import TTFont
 from reportlab.pdfgen.canvas import Canvas
 from xml.sax.saxutils import escape
 font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
 pdfmetrics.registerFont(TTFont('Jujuy',font));styles=getSampleStyleSheet()
 styles.add(ParagraphStyle(name='CellJ',fontName='Jujuy',fontSize=7,leading=10));styles.add(ParagraphStyle(name='BodyJ',fontName='Jujuy',fontSize=10,leading=15));styles.add(ParagraphStyle(name='TitleJ',fontName='Jujuy',fontSize=23,leading=30,spaceAfter=15))
 def p(text,style='CellJ'):return Paragraph(escape(str(text)),styles[style])
 domain_start=date(2026,11,1);domain_end=date(2027,11,1);span=(domain_end-domain_start).days
 class Bar(Flowable):
  def __init__(self,t):Flowable.__init__(self);self.t=t;self.width=350;self.height=15
  def draw(self):
   c=self.canv;c.setStrokeColor(colors.HexColor('#d9e2e8'));c.setLineWidth(.3)
   for n in range(0,span,28):x=n/span*self.width;c.line(x,0,x,self.height)
   a=(date.fromisoformat(self.t['start'])-domain_start).days/span*self.width;b=(date.fromisoformat(self.t['end'])-domain_start).days/span*self.width
   c.setFillColor(colors.HexColor('#bd5047' if self.t['floatDays']==0 else '#456f85'))
   if not self.t['duration']:
    path=c.beginPath();path.moveTo(a,3);path.lineTo(a+3,7);path.lineTo(a,11);path.lineTo(a-3,7);path.close();c.drawPath(path,fill=1,stroke=0)
   else:c.roundRect(a,4,max(2,b-a),7,2,stroke=0,fill=1)
 path=ROOT/'docs'/R3_PDF
 doc=SimpleDocTemplate(str(path),pagesize=landscape(A3),rightMargin=35,leftMargin=35,topMargin=32,bottomMargin=32,title='Jujuy R3 · Ajuste LPS 09/11 no laborable',author='Oddino Arquitectura')
 story=[p('JUJUY · Programación R3 · Ajuste LPS','TitleJ'),p(f"Plan recalculado: {data['start']} — {data['end']}. Base: Gantt R2 y confirmaciones LPS del usuario.",'BodyJ'),Spacer(1,12)]
 for text in ['09/11/2026 no laborable confirmado. Se mantiene el cierre de vacaciones 24/12/2026–10/01/2027 inclusive. Otros feriados no descontados.','Red FS/SS y duraciones de R2 conservadas, incluido el vínculo SS+2. Antes del ajuste el motor reprodujo exactamente las 395 fechas y todas las holguras R2.','Contrapisos P5/P6 del 27/11/2026 y límite de medianeras 20/02/2027 se mantienen. No se trasladan todos los hitos indiscriminadamente.','ET1 hasta P8: fin previsto 10/11/2026, corrigiendo la referencia 10/10 de R2. No se da por ejecutada una promesa.','Los partes y restricciones privados no se modifican. Compromisos LPS sin cumplimiento confirmado; PPC pendiente.']:
  story.extend([p(text,'BodyJ'),Spacer(1,8)])
 story.extend([Spacer(1,12),p('Compromisos fijos y variaciones','TitleJ')])
 audit=[['Referencia','R2','R3']]+[[str(r['reference']),r['before'],r['after']] for r in data['reprogramming']['keyDates']]
 table=Table([[p(c) for c in row] for row in audit],colWidths=[330,140,140],repeatRows=1);table.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e6eef2')),('BOTTOMPADDING',(0,0),(-1,-1),8),('LINEBELOW',(0,0),(-1,-1),.3,colors.HexColor('#d8e0e5'))]));story.extend([table,PageBreak(),p('395 actividades e hitos · Red FS/SS y Gantt','TitleJ'),p('Barras: rojo = HT cero de la red recalculada; azul = resto. No representan avance real. Escala noviembre 2026 a octubre 2027.','BodyJ'),Spacer(1,8)])
 headers=['ID','Frente','Actividad','Inicio','Fin','Dur.','HT','Nov 26      Ene 27      Mar 27      May 27      Jul 27      Sep 27']
 rows=[[p(c) for c in headers]]
 for t in sorted((t for t in data['tasks'] if t['active']),key=lambda t:(t['start'],t['end'],t['id'])):
  rows.append([p(t['sourceId']),p(t['level']),p(t['code']),p(t['start']),p(t['end']),p(t['duration']),p(t['floatDays']),Bar(t)])
 table=Table(rows,colWidths=[35,48,340,73,73,35,35,350],repeatRows=1,hAlign='LEFT');table.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e6eef2')),('VALIGN',(0,0),(-1,-1),'MIDDLE'),('LINEBELOW',(0,0),(-1,-1),.2,colors.HexColor('#e1e7eb')),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]));story.append(table)
 story.extend([PageBreak(),p('LPS · Noviembre 2026 · Compromisos, no ejecución','TitleJ'),p(data['lps']['publicationNote'],'BodyJ'),Spacer(1,10)])
 rows=[[p(c) for c in ['Fecha','Código','Rubro / frente','Compromiso','Observación']]]
 for r in data['lps']['items']:rows.append([p(r['date']),p(r['code']),p(r['actor']+' · '+r['levels']),p(r['text']),p(r['note'])])
 table=Table(rows,colWidths=[80,80,160,300,369],repeatRows=1);table.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e6eef2')),('VALIGN',(0,0),(-1,-1),'TOP'),('LINEBELOW',(0,0),(-1,-1),.3,colors.HexColor('#d8e0e5')),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7)]));story.append(table)
 def footer(canvas,doc):canvas.setFont('Jujuy',8);canvas.drawString(35,17,'ODDINO ARQUITECTURA · JUJUY R3 · Fechas calculadas; no certifican ejecución');canvas.drawRightString(1155,17,str(doc.page))
 doc.build(story,onFirstPage=footer,onLaterPages=footer,canvasmaker=lambda *a,**kw:Canvas(*a,**(kw|{'invariant':1})))
 return path

def generate():
 data=json.loads((ROOT/'data/schedule-r2.json').read_text());active=[t for t in data['tasks'] if t['active']];base_by_id={t['sourceId']:copy.deepcopy(t) for t in active}
 baseline=solve(active,data['calendar'])
 for t in active:
  for field in ['startIndex','endIndex','start','end','lateStartIndex','floatDays']:assert baseline[t['sourceId']][field]==t[field],(t['sourceId'],field)
 calendar=copy.deepcopy(data['calendar']);calendar['excludedRanges'].insert(0,{'start':'2026-11-09','end':'2026-11-09','reason':'No laborable confirmado por el usuario en LPS'})
 result=solve(active,calendar)
 for t in active:
  t['r2Plan']={k:t[k] for k in ['start','end','startIndex','endIndex','lateStartIndex','floatDays','critical']};t.update(result[t['sourceId']]);t['calendar']=calendar;t['planRevision']='r3';t['critical']='Crítica R3' if t['floatDays']==0 else 'No crítica';t['pdfCritical']=t['r2Plan']['critical'];t['pdfFloatDays']=t['r2Plan']['floatDays']
 byid={t['sourceId']:t for t in active}
 for id in ['223','265']:assert byid[id]['end']=='2026-11-27'
 assert byid['445']['end']<='2027-02-19';assert byid['H16']['start']=='2026-11-16';assert byid['LIB']['start']=='2026-11-30'
 data.update(revision='r3',version='R3 · Ajuste LPS · 09/11 no laborable',calendar=calendar,start=min(t['start'] for t in active),end=max(t['end'] for t in active),lps=json.loads((ROOT/'data/lps-noviembre-2026.json').read_text()))
 key=[('ET2 P1','44'),('ET2 P8','342'),('Contrapiso P5','223'),('Contrapiso P6','265'),('Medianera Norte','445'),('Hormigón sala máquinas / azotea','H16'),('Liberación P9','LIB'),('Entrega general','490')]
 data['reprogramming']={'method':'Recalculado por red FS/SS R2, conservando duraciones, restricciones mínimas y anclas fijas; calendario con 09/11 no laborable confirmado. Motor cotejado contra todas las fechas y holguras originales de R2.','referenceCalendarChange':'2026-11-09','changedTasks':sum(t['start']!=t['r2Plan']['start'] or t['end']!=t['r2Plan']['end'] for t in active),'keyDates':[{'reference':name,'sourceId':id,'before':base_by_id[id]['end'],'after':byid[id]['end']} for name,id in key]}
 data['historyNotes']=[('Corrección LPS: ET1 hasta P8, fin previsto 10/11/2026. La referencia 10/10 del PDF R2 se corrigió por el usuario; no acredita ejecución.' if 'ET1' in note and '10/10' in note else note) for note in data['historyNotes']]
 data['historyNotes'].append('Usuario corrigió fin previsto ET1 hasta P8 a 10/11/2026 (no 10/10). Se conserva como compromiso, no como ejecución certificada.')
 for t in data['tasks']:
  if not t['active'] and t['id'] in [43,85,127,173,215,257,299,341]:t['operationalNote']='Corrección del usuario: fin previsto de ET1 hasta P8 el 10/11/2026, no 10/10. No se inventan fechas reales por piso ni se certifica ejecución.'
 pdf=make_pdf(data);data['previousSource']=data['currentSource'];data['currentSource']={'file':R3_PDF,'revision':'r3','sha256':hashlib.sha256(pdf.read_bytes()).hexdigest()};data['sources'].append(copy.deepcopy(data['currentSource']))
 (ROOT/'data/schedule.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
 with (ROOT/'docs/programacion.csv').open('w',newline='',encoding='utf-8-sig') as f:
  w=csv.writer(f,lineterminator='\n');w.writerow(['ID PDF','ID interno','Frente','Actividad','Rubro','Inicio R3','Fin R3','Inicio R2','Fin R2','Duración','HT R3','HT PDF R2','Predecesoras','Observación PDF'])
  for t in active:w.writerow([t['sourceId'],t['id'],t['level'],t['code'],t['trade'],t['start'],t['end'],t['r2Plan']['start'],t['r2Plan']['end'],t['duration'],t['floatDays'],t['pdfFloatDays'],t['predecessors'],t['note']])
 print('R3:',data['start'],data['end'],'actividades con fechas ajustadas:',data['reprogramming']['changedTasks'])
 print(json.dumps(data['reprogramming']['keyDates'],ensure_ascii=False,indent=2))
 return data
if __name__=='__main__':generate()
