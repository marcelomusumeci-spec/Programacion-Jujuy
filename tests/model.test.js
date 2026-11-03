import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {expected,inspect,summarize,emptyState,validateState,upsertReport,validDate,csvCell,workdays,reportAt} from '../model.js';
const data=JSON.parse(readFileSync(new URL('../data/schedule.json',import.meta.url)));
const original=JSON.parse(readFileSync(new URL('../data/schedule-a0.json',import.meta.url)));
const r1=JSON.parse(readFileSync(new URL('../data/schedule-r1.json',import.meta.url)));
const tasks=data.tasks.filter(t=>t.active&&['activity','milestone'].includes(t.kind));
const t={id:1000,start:'2027-03-04',end:'2027-03-10',duration:5};
const report=(date,progress)=>({taskId:1000,date,progress,owner:'Cuadrilla A',note:'Ejecutado',savedAt:'2027-03-10T12:00:00.000Z'});
test('R2: 395 actividades activas, 491 antecedentes y 10 IDs nuevos compatibles',()=>{
 assert.equal(original.tasks.length,491);assert.equal(data.tasks.length,501);assert.equal(new Set(data.tasks.map(t=>t.id)).size,501);assert.equal(tasks.length,395);assert.equal(data.sources.length,10);
 for(const task of data.tasks){assert.ok(validDate(task.start));assert.ok(validDate(task.end));assert.ok(task.end>=task.start);assert.ok(task.sourcePage>=1&&task.sourcePage<=40);}
 assert.equal(data.tasks.find(t=>t.id===391).start,'2027-02-12');assert.equal(data.tasks.find(t=>t.id===490).end,'2027-10-13');
 assert.equal(data.tasks.filter(t=>t.active===false).length,106);
});
test('Plan interpolado con fines de semana y límites inclusivos',()=>{
 assert.equal(workdays(t.start,t.end),5);assert.equal(expected(t,'2027-03-03'),0);assert.equal(expected(t,'2027-03-04'),20);assert.equal(expected(t,'2027-03-07'),40);assert.equal(expected(t,'2027-03-10'),100);assert.equal(expected(t,'2027-03-20'),100);
 assert.equal(expected({...t,duration:0,start:t.end},'2027-03-09'),0);assert.equal(expected({...t,duration:0,start:t.end},t.end),100);
});
test('Sin parte no significa atraso ni 0 real; futuro sigue programado',()=>{
 assert.equal(inspect(t,emptyState(),t.end).status,'missing');assert.equal(inspect(t,emptyState(),t.end).actual,null);assert.equal(inspect(t,emptyState(),'2027-03-01').status,'future');assert.equal(summarize([t],emptyState(),t.end).actual,null);
});
test('Corte ignora partes posteriores y reemplaza sólo mismo día',()=>{
 let s=upsertReport(emptyState(),report('2027-03-04',20));s=upsertReport(s,report('2027-03-10',100));
 assert.equal(inspect(t,s,'2027-03-04').actual,20);assert.equal(inspect(t,s,'2027-03-09').status,'late');assert.equal(inspect(t,s,'2027-03-10').status,'done');
 s=upsertReport(s,report('2027-03-04',25));assert.equal(s.reports.length,2);assert.equal(inspect(t,s,'2027-03-04').actual,25);
});
test('Restricción prevalece; alta y resolución respetan el corte histórico',()=>{
 const s={...upsertReport(emptyState(),report('2027-03-04',0)),restrictions:[{taskId:1000,id:'r',opened:'2027-03-05',due:'2027-03-08',resolved:'2027-03-09',cause:'Material',owner:'Compras',category:'Materiales'}]};
 assert.equal(inspect(t,s,'2027-03-04').status,'late');assert.equal(inspect(t,s,'2027-03-05').status,'blocked');assert.equal(inspect(t,s,'2027-03-08').status,'blocked');assert.equal(inspect(t,s,'2027-03-09').status,'late');
});
test('Resumen informa cobertura y prioriza atrasos sobre partes en plan',()=>{
 const u={...t,id:1001};const s=upsertReport(emptyState(),report(t.end,100));const result=summarize([t,u],s,t.end);
 assert.equal(result.reported,1);assert.equal(result.due,2);assert.equal(result.actual,null);assert.equal(result.status,'missing');
 const all=upsertReport(s,{...report(t.end,50),taskId:1001});assert.equal(summarize([t,u],all,t.end).actual,75);assert.equal(summarize([t,u],all,t.end).status,'late');
});
test('Restauración rechaza IDs ajenos, progreso inválido, duplicados y fechas imposibles',()=>{
 const good=upsertReport(emptyState(),report(t.end,50));assert.equal(validateState(good,[t]).reports.length,1);
 assert.throws(()=>validateState(good,tasks));assert.throws(()=>validateState({...good,reports:[report(t.end,101)]},[t]));assert.throws(()=>validateState({...good,reports:[report(t.end,NaN)]},[t]));assert.throws(()=>validateState({...good,reports:[report(t.end,20),report(t.end,40)]},[t]));assert.equal(validDate('2027-02-30'),false);
 assert.throws(()=>validateState({...good,restrictions:[{id:'r',taskId:1000,opened:t.end,due:t.start,resolved:null,cause:'Bloqueo',owner:'Jefe',category:'Otro'}]},[t]));
});
test('CSV escapa comillas y neutraliza fórmulas de observaciones',()=>{assert.equal(csvCell('=1+1'),'"\'=1+1"');assert.equal(csvCell('a,"b"'),'"a,""b"""');});

test('Histórico R1 conserva las anclas y el desplazamiento original',()=>{
 const data=r1,tasks=r1.tasks.filter(t=>['activity','milestone'].includes(t.kind));
 assert.equal(data.revision,'r1');assert.equal(data.start,'2026-01-28');assert.equal(data.end,'2027-07-05');
 assert.equal(data.reprogramming.generalShiftWorkdays,-148);assert.equal(data.reprogramming.n4ShiftWorkdays,-178);
 for(const task of data.tasks){
  const old=original.tasks.find(t=>t.id===task.id);
  assert.equal(task.originalStart,old.start);assert.equal(task.originalEnd,old.end);assert.equal(task.duration,old.duration);assert.equal(task.baselineDuration,old.baselineDuration);
  assert.equal(workdays(task.start,task.end),workdays(old.start,old.end));
  const count=workdays(task.start,old.start)-1;assert.equal(count,-task.shiftWorkdays,task.code);
  assert.equal(task.shiftWorkdays,(task.level==='N4'&&task.trade!=='Estructura y preliminares')||[172,170].includes(task.id)?-178:-148);
 }
 for(const id of [135,181]){const task=data.tasks.find(t=>t.id===id);assert.equal(task.start,'2026-10-30');assert.equal(task.end,'2026-10-30');assert.equal(inspect(task,emptyState(),'2026-10-30').status,'done');assert.equal(inspect(task,emptyState(),'2026-10-29').actual,null);}
 assert.equal(tasks.filter(t=>t.confirmedReport).length,2);
 const structure=data.tasks.filter(t=>t.id>=26&&t.id<=39);for(let i=1;i<structure.length;i++)assert.ok(structure[i].start>structure[i-1].end);
 assert.ok(data.tasks.find(t=>t.id===173).start>data.tasks.find(t=>t.id===33).end);
});
test('Histórico R1 respeta partes y restricciones anteriores',()=>{
 const data=r1,tasks=r1.tasks.filter(t=>['activity','milestone'].includes(t.kind));
 const task=data.tasks.find(t=>t.id===135);
 const local={...emptyState(),reports:[{taskId:135,date:'2026-10-30',progress:80,owner:'Jefatura',note:'Dato local a revisar',savedAt:'2026-10-31T15:00:00.000Z'}],restrictions:[{id:'r-original',taskId:135,opened:'2026-10-29',due:'2026-11-02',resolved:null,cause:'Prueba pendiente',owner:'Jefe',category:'Inspección'}]};
 const before=JSON.stringify(local);const safe=validateState(local,tasks);
 assert.equal(reportAt(task,safe,'2026-10-30').progress,80);assert.equal(inspect(task,safe,'2026-10-30').status,'blocked');assert.equal(JSON.stringify(local),before);
 assert.equal(safe.restrictions[0].due,'2026-11-02');assert.equal(safe.reports[0].date,'2026-10-30');
 assert.equal(reportAt(task,emptyState(),'2026-10-30').progress,100);
 const other=tasks.find(t=>t.id===134);assert.equal(inspect(other,emptyState(),'2026-10-30').actual,null);
});

test('R2 pausa el avance esperado durante vacaciones y retoma el 11/01',()=>{
 const t=data.tasks.find(t=>t.id===300);
 assert.equal(t.start,'2026-12-21');assert.equal(t.end,'2027-01-12');assert.equal(workdays(t.start,t.end,t.calendar),5);
 for(const date of ['2026-12-23','2026-12-24','2026-12-31','2027-01-08','2027-01-10'])assert.equal(expected(t,date),60,date);
 assert.equal(expected(t,'2027-01-11'),80);assert.equal(expected(t,'2027-01-12'),100);
 for(const t of tasks){if(t.duration)assert.equal(workdays(t.start,t.end,t.calendar),t.duration,t.code);}
});
test('R2 conserva datos privados de tareas archivadas y permite partes de hitos nuevos',()=>{
 const state={...emptyState(),reports:[{taskId:43,date:'2026-10-31',progress:43,owner:'Jefatura',note:'Parte anterior',savedAt:'2026-10-31T12:00:00Z'}],restrictions:[{taskId:45,id:'old',opened:'2026-10-30',due:'2026-11-05',resolved:null,cause:'Pendiente anterior',owner:'Compras',category:'Materiales'}]};
 assert.equal(data.tasks.find(t=>t.id===43).active,false);assert.equal(data.tasks.find(t=>t.id===45).active,false);
 assert.deepEqual(validateState(state,data.tasks),state);
 const h=data.tasks.find(t=>t.sourceId==='H16');const next=upsertReport(state,{taskId:h.id,date:'2026-11-16',progress:100,owner:'Jefe',note:'Hito',savedAt:'2026-11-16T12:00:00Z'});assert.equal(validateState(next,data.tasks).reports.length,2);
 assert.equal(inspect(data.tasks.find(t=>t.sourceId==='L1'),state,'2026-11-16').actual,null);
});
test('R2 preserva fechas definitivas, compromisos y antecedentes de bombeo sin certificar otro alcance',()=>{
 assert.equal(data.revision,'r2');assert.equal(data.start,'2026-11-09');assert.equal(data.end,'2027-10-13');
 for(const id of [223,265])assert.equal(data.tasks.find(t=>t.id===id).end,'2026-11-27');
 assert.equal(data.tasks.find(t=>t.id===445).end,'2027-02-19');
 for(const [id,planned] of [[135,'2026-11-27'],[181,'2026-12-04']]){const t=data.tasks.find(t=>t.id===id);assert.equal(t.end,planned);assert.equal(t.previousConfirmedReport.date,'2026-10-30');assert.equal(t.confirmedReport,undefined);assert.equal(inspect(t,emptyState(),'2026-11-03').actual,null);}
 const ids=new Set(tasks.map(t=>t.sourceId));for(const t of tasks)for(const [,id,relation] of t.predecessors.matchAll(/([A-Z0-9]+):(FS|SS)/g)){assert.ok(ids.has(id));assert.ok(['FS','SS'].includes(relation));}
});
