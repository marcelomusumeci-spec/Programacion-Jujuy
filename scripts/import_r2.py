"""Importa las tablas R2 del PDF, contrastando programación y trazabilidad.
Requiere pdftotext. No calcula nuevas fechas ni acumula desplazamientos.
"""
from pathlib import Path
from datetime import datetime,date,timedelta
import re,json,csv,subprocess,hashlib
ROOT=Path(__file__).resolve().parent.parent
FILE='Jujuy_Programacion_completa_revisada.pdf'
CALENDAR={'workingWeekdays':[1,2,3,4,5],'excludedRanges':[{'start':'2026-12-24','end':'2027-01-10','reason':'Cierre por vacaciones R2'}]}
def iso(s):return datetime.strptime(s,'%d/%m/%y').date().isoformat() if s else None
def working(a,b):
 a=date.fromisoformat(a);b=date.fromisoformat(b);n=0
 while a<=b:
  if a.weekday()<5 and not date(2026,12,24)<=a<=date(2027,1,10):n+=1
  a+=timedelta(days=1)
 return n

def extract(text):
 rows=[];section=False
 for page,chunk in enumerate(text.split('\f'),1):
  if '2. Programación completa' in chunk:section=True
  if '3. Gantt semanal completo' in chunk:break
  if not section:continue
  lines=chunk.splitlines();header=next(l for l in lines if re.match(r'\s*ID\s+Sector',l));obs=header.index('Observación');last=None
  for line in lines:
   if line.startswith('JUJUY |'):last=None;continue
   id=line[:10].strip()
   if re.fullmatch(r'\d+|H16|LIB|L[1-8]',id) and re.fullmatch(r'\d{2}/\d{2}/\d{2}',line[122:133].strip()):
    last={'sourceId':id,'sector':line[10:28].strip(),'code':line[28:76].strip(),'duration':int(line[76:88].strip()),'availability':iso(line[88:104].strip()),'startIndex':int(line[104:113].strip()),'endIndex':int(line[113:122].strip()),'start':iso(line[122:133].strip()),'end':iso(line[133:144].strip()),'lateStartIndex':int(line[144:153].strip()),'floatDays':int(line[153:160].strip()),'critical':line[160:177].strip(),'predecessors':line[177:obs].strip(),'note':line[obs:].strip(),'sourcePage':page}
    rows.append(last)
   elif last and not id:
    for field,a,b in [('sector',10,28),('code',28,76),('predecessors',177,obs),('note',obs,None)]:
     extra=line[a:b].strip()
     if extra:last[field]+=' '+extra
 assert len(rows)==395==len(set(r['sourceId'] for r in rows)), 'Extracción incompleta o duplicada'
 # Contrastar con las otras 491 filas de la sección Base original.
 trace={};section=False
 for page,chunk in enumerate(text.split('\f'),1):
  if '4. Base original' in chunk:section=True
  if not section or not chunk.strip():continue
  lines=chunk.splitlines();header=next(l for l in lines if 'ID ori' in l)
  starts=[m.start() for m in re.finditer(r'Inicio',header)];revision=starts[-1];fin=header.index('Fin revisión');obs=header.index('Observación');last=None
  for line in lines:
   id=line[:12].strip()
   if id.isdigit() and line[96:114].strip():
    last={'id':int(id),'treatment':line[129:revision].strip(),'start':iso(line[revision:fin].strip()),'end':iso(line[fin:obs].strip()),'note':line[obs:].strip(),'page':page};trace[int(id)]=last
   elif last and not id and not line.startswith('JUJUY |'):
    extra=line[obs:].strip()
    if extra:last['note']+=' '+extra
 assert len(trace)==491, f'Trazabilidad incompleta: {len(trace)}'
 for r in rows:
  assert r['end']>=r['start']
  if r['duration']:assert working(r['start'],r['end'])==r['duration'],r
  if r['sourceId'].isdigit():
   t=trace[int(r['sourceId'])];assert (r['start'],r['end'])==(t['start'],t['end']),r
  for pred in re.findall(r'([A-Z0-9]+):(FS|SS)',r['predecessors']):assert pred[0] in {x['sourceId'] for x in rows},pred
 return rows,trace

def generate():
 pdf=ROOT/'docs'/FILE
 text=subprocess.check_output(['pdftotext','-layout',str(pdf),'-']).decode()
 rows,trace=extract(text)
 data=json.loads((ROOT/'data/schedule-r1.json').read_text());old={t['id']:dict(t) for t in data['tasks']}
 active_numeric={int(r['sourceId']) for r in rows if r['sourceId'].isdigit()}
 for t in data['tasks']:
  t['active']=t['id'] in active_numeric
  t['r2Treatment']=trace[t['id']]['treatment'];t['r2TraceNote']=trace[t['id']]['note'];t['r2TracePage']=trace[t['id']]['page']
  if not t['active']:t['archiveReason']='Fuera de las 395 actividades activas de R2. '+t['r2Treatment']
 lookup={t['id']:t for t in data['tasks']}
 synthetic={'H16':10001,**{f'L{i}':10001+i for i in range(1,9)},'LIB':10010}
 for r in rows:
  id=int(r['sourceId']) if r['sourceId'].isdigit() else synthetic[r['sourceId']]
  t=lookup.get(id)
  if t is None:
   t={'id':id,'originalStart':None,'originalEnd':None,'baselineDuration':None,'finishVariance':None,'trade':'Estructura y preliminares' if r['sourceId']=='H16' else 'Liberación de instalaciones' if r['sourceId'].startswith('L') and r['sourceId']!='LIB' else 'Liberación de frentes','stage':''};data['tasks'].append(t)
  else:
   t['previousPlan']={'revision':'r1','start':t['start'],'end':t['end'],'duration':t['duration'],'code':t['code']}
  for field in ['code','duration','start','end','sourceId','sector','availability','startIndex','endIndex','lateStartIndex','floatDays','critical','predecessors','note','sourcePage']:t[field]=r[field]
  t.update(active=True,kind='milestone' if r['duration']==0 else 'activity',source='r2',sourceFile=FILE,calendar=CALENDAR)
  sector=r['sector'];t['level']='N'+sector[1:] if re.fullmatch(r'P[1-8]',sector) else 'P9' if sector.startswith('P9') else 'PB' if sector=='Planta baja' else 'EC' if sector=='Comunes' else 'Medianeras' if id in range(444,448) else 'General'
  if r['sourceId'] in ['135','181']:
   t['previousConfirmedReport']=t.pop('confirmedReport',None)
   t['scopeReview']='Antecedente R1: bombeo realizado el 30/10/2026. R2 programa contrapiso terminado con otra fecha; no se certifica automáticamente su terminación. Los partes locales permanecen intactos.'
 data.update(revision='r2',version='R2 · Programación completa revisada',start=min(r['start'] for r in rows),end=max(r['end'] for r in rows),calendar=CALENDAR,currentSource={'file':FILE,'sha256':hashlib.sha256(pdf.read_bytes()).hexdigest(),'pages':text.count('\f')},activeCount=len(rows))
 data['sources'].append({'file':FILE,'sha256':data['currentSource']['sha256'],'revision':'r2'})
 data['historyNotes']=['A0 original y R1 se conservan por separado. R2 sustituye fechas del plan, no fechas reales de partes.','ET1 terminada hasta P8 al 10/10/2026 según el PDF, sin fechas reales individuales.','Instalaciones iniciales P1–P8 agrupadas en L1–L8; los partes originales no se transfieren automáticamente a estos hitos.']
 data['reprogramming']={'method':'Fechas transcritas de la sección 2 del PDF R2 y cotejadas con su sección 4. No se recalculan fechas ni holguras.'}
 (ROOT/'data/schedule.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
 with (ROOT/'docs/programacion.csv').open('w',newline='',encoding='utf-8-sig') as f:
  w=csv.writer(f,lineterminator='\n');w.writerow(['ID R2','ID interno compatible','Sector','Actividad','Rubro','Inicio R2','Fin R2','Duración restante','HT PDF (días)','Criticidad del modelo','Predecesoras PDF','Disponibilidad mínima PDF','Observación','Página PDF'])
  for t in data['tasks']:
   if t['active']:w.writerow([t[k] for k in ['sourceId','id','sector','code','trade','start','end','duration','floatDays','critical','predecessors','availability','note','sourcePage']])
 print('R2:',data['start'],data['end'],'activos',len(rows),'archivados',sum(not t['active'] for t in data['tasks']),'registros totales',len(data['tasks']))
 return data
if __name__=='__main__':generate()
