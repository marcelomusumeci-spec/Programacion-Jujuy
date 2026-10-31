"""Genera R1 siempre desde A0: nunca acumula desplazamientos."""
from pathlib import Path
from datetime import date,timedelta
import json,csv
ROOT=Path(__file__).resolve().parent.parent
TARGET=date(2026,10,30)
def shift(value,days):
    d=date.fromisoformat(value);step=1 if days>=0 else -1
    for _ in range(abs(days)):
        d+=timedelta(days=step)
        while d.weekday()>4:d+=timedelta(days=step)
    return d.isoformat()
def distance(start,end):
    d=date.fromisoformat(start);step=1 if d<end else -1;n=0
    while d!=end:
        d+=timedelta(days=step)
        if d.weekday()<5:n+=step
    return n

def generate():
    data=json.loads((ROOT/'data/schedule-a0.json').read_text())
    original={t['id']:dict(t) for t in data['tasks']}
    general=distance(original[135]['start'],TARGET)
    floor4=distance(original[181]['start'],TARGET)
    for task in data['tasks']:
        # N4: su secuencia completa y su resumen. El hito de coordinación
        # N4-5-6 se lleva al arranque de la tanda (N4), sin certificar N5/N6.
        delta=floor4 if (task['level']=='N4' and task['trade']!='Estructura y preliminares') or task['id'] in [172,170] else general
        task.update(originalStart=task['start'],originalEnd=task['end'],shiftWorkdays=delta)
        task['start']=shift(task['start'],delta);task['end']=shift(task['end'],delta)
    tasks={t['id']:t for t in data['tasks']}
    for id in [135,181]:
        assert tasks[id]['start']==TARGET.isoformat()==tasks[id]['end']
        tasks[id]['confirmedReport']={'taskId':id,'date':TARGET.isoformat(),'progress':100,'owner':'','note':'Bombeo realizado el 30/10/2026, confirmado expresamente por el comitente en la reprogramación R1.','savedAt':'2026-10-31T12:00:00.000Z'}
    # El resumen de bombeos abarca todas las fechas de bombeo por nivel.
    pumping=[t for t in data['tasks'] if t['trade']=='Bombeo de contrapiso' and t['kind']=='milestone']
    tasks[168]['start']=min(t['start'] for t in pumping);tasks[168]['end']=max(t['end'] for t in pumping)
    data['start']=tasks[0]['start'];data['end']=tasks[0]['end']
    data['version']='R1 · Referencia real 30/10/2026'
    data['revision']='r1'
    data['reprogramming']={'referenceDate':TARGET.isoformat(),'anchorIds':[135,181],'generalShiftWorkdays':general,'n4ShiftWorkdays':floor4,'calendar':'lunes a viernes, sin feriados','originalStart':original[0]['start'],'originalEnd':original[0]['end'],'method':'Desplazamiento general respecto de N3; secuencia N4 con desplazamiento propio. No es un recálculo de red de predecesoras.'}
    (ROOT/'data/schedule.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    with (ROOT/'docs/programacion.csv').open('w',newline='',encoding='utf-8-sig') as f:
        w=csv.writer(f,lineterminator='\n');w.writerow(['ID PDF','Actividad','Tipo','Nivel','Rubro','Etapa','Inicio R1','Fin R1','Inicio original A0','Fin original A0','Desplazamiento laborable','Duración documental (días)','Duración LB original (días)','Página fuente original','Real confirmado'])
        for t in data['tasks']:w.writerow([t[k] for k in ['id','code','kind','level','trade','stage','start','end','originalStart','originalEnd','shiftWorkdays','duration','baselineDuration','sourcePage']]+[TARGET.isoformat() if t.get('confirmedReport') else ''])
    print('R1:',data['start'],'—',data['end'],'General:',general,'días laborables; N4:',floor4)
    for t in data['tasks']:
        if t['id'] in [42,84,126,172,214,256,298,340,382,423,443,448]:print(t['code'],t['start'],t['end'])
if __name__=='__main__':generate()
