export const labels = {plan:'En plan',late:'Atrasado',blocked:'Restringido',missing:'Sin parte',future:'Programado',done:'Completado'};
export const emptyState = () => ({version:1,project:'jujuy-a0',reports:[],restrictions:[]});
export function validDate(s) {return typeof s==='string' && /^\d{4}-\d{2}-\d{2}$/.test(s) && !Number.isNaN(Date.parse(s+'T12:00:00Z')) && new Date(s+'T12:00:00Z').toISOString().slice(0,10)===s;}
export function addDays(date,n) {const d=new Date(date+'T12:00:00Z');d.setUTCDate(d.getUTCDate()+n);return d.toISOString().slice(0,10);}
export function workdays(start,end) {if(end<start)return 0;let n=0;for(let d=start;d<=end;d=addDays(d,1)){const day=new Date(d+'T12:00:00Z').getUTCDay();if(day!==0&&day!==6)n++;}return n;}
export function expected(task,date) {
 if(date<task.start)return 0;
 if(date>=task.end)return 100;
 return 100*workdays(task.start,date)/Math.max(1,workdays(task.start,task.end));
}
export function reportAt(task,state,date) {
 const local=state.reports.filter(r=>r.taskId===task.id&&r.date<=date);
 const confirmed=task.confirmedReport;
 if(confirmed&&confirmed.date<=date&&!local.some(r=>r.date===confirmed.date))local.push(confirmed);
 return local.sort((a,b)=>b.date.localeCompare(a.date)||b.savedAt.localeCompare(a.savedAt))[0]||null;
}
export function activeRestrictions(task,state,date) {return state.restrictions.filter(r=>r.taskId===task.id&&r.opened<=date&&(!r.resolved||r.resolved>date));}
export function inspect(task,state,date) {
 const report=reportAt(task,state,date),planned=expected(task,date),blocks=activeRestrictions(task,state,date);
 const actual=report?report.progress:null;
 const status=blocks.length?'blocked':actual===100?'done':actual===null?(date<task.start?'future':'missing'):actual+0.5<planned?'late':date<task.start&&actual===0?'future':'plan';
 return {task,report,planned,actual,blocks,status};
}
export function summarize(tasks,state,date) {
 const rows=tasks.map(t=>inspect(t,state,date));const counts=Object.fromEntries(Object.keys(labels).map(k=>[k,rows.filter(r=>r.status===k).length]));
 const weight=t=>Math.max(1,t.duration);
 const total=tasks.reduce((s,t)=>s+weight(t),0);
 const planned=total?rows.reduce((s,r)=>s+r.planned*weight(r.task),0)/total:0;
 const due=rows.filter(r=>r.task.start<=date),missing=due.filter(r=>!r.report);
 const actual=missing.length||!rows.some(r=>r.report)?null:total?rows.reduce((s,r)=>s+(r.actual??0)*weight(r.task),0)/total:0;
 const status=['blocked','late','missing','plan'].find(k=>counts[k])||(counts.future?'future':'done');
 return {rows,counts,planned,actual,due:due.length,reported:due.length-missing.length,status};
}
export function validateState(s,tasks) {
 const ids=new Set(tasks.map(t=>t.id));const string=(v,max=4000)=>typeof v==='string'&&v.length<=max;
 if(!s||s.version!==1||s.project!=='jujuy-a0'||!Array.isArray(s.reports)||!Array.isArray(s.restrictions)||s.reports.length>50000||s.restrictions.length>20000)throw Error('El archivo no es una copia válida de Jujuy.');
 const seen=new Set();
 for(const r of s.reports){if(!r||!ids.has(r.taskId)||!validDate(r.date)||!Number.isFinite(r.progress)||r.progress<0||r.progress>100||!string(r.owner,160)||!string(r.note)||!string(r.savedAt,40)||Number.isNaN(Date.parse(r.savedAt)))throw Error('Hay un parte inválido en la copia.');const key=`${r.taskId}:${r.date}`;if(seen.has(key))throw Error('Hay partes duplicados para una misma fecha.');seen.add(key);}
 const keys=new Set();
 for(const r of s.restrictions){if(!r||!string(r.id,100)||!r.id||keys.has(r.id)||!ids.has(r.taskId)||!validDate(r.opened)||!validDate(r.due)||r.due<r.opened||(r.resolved!==null&&(!validDate(r.resolved)||r.resolved<r.opened))||!string(r.cause)||!r.cause.trim()||!string(r.owner,160)||!r.owner.trim()||!string(r.category,100))throw Error('Hay una restricción inválida en la copia.');keys.add(r.id);}
 return {version:1,project:'jujuy-a0',reports:s.reports.map(r=>({taskId:r.taskId,date:r.date,progress:r.progress,owner:r.owner,note:r.note,savedAt:r.savedAt})),restrictions:s.restrictions.map(r=>({id:r.id,taskId:r.taskId,opened:r.opened,due:r.due,resolved:r.resolved,cause:r.cause,owner:r.owner,category:r.category}))};
}
export function upsertReport(state,report) {return {...state,reports:[...state.reports.filter(r=>!(r.taskId===report.taskId&&r.date===report.date)),report]};}
export function csvCell(value){const s=String(value??'');return '"'+(/^[=+\-@\t\r]/.test(s)?"'"+s:s).replaceAll('"','""')+'"';}
