"""LPS planificado: filtros, correcciones, PPC pendiente y no mutación de partes."""
from playwright.sync_api import sync_playwright
from pathlib import Path
import os,json,csv
BASE=os.environ.get('JUJUY_TEST_URL','http://127.0.0.1:8000')
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path=os.environ.get('CHROMIUM_PATH','/usr/bin/chromium'),headless=True,args=['--no-sandbox'])
 context=browser.new_context(viewport={'width':390,'height':844},is_mobile=True,has_touch=True,accept_downloads=True)
 page=context.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto(BASE);page.wait_for_selector('.trade-card')
 state={'version':1,'project':'jujuy-a0','reports':[{'taskId':44,'date':'2026-11-03','progress':25,'owner':'Prueba','note':'Conservar el parte','savedAt':'2026-11-03T12:00:00Z'}],'restrictions':[]}
 page.evaluate('(s)=>localStorage.setItem("jujuy-control-v1",JSON.stringify(s))',state);page.reload();page.wait_for_selector('.trade-card')
 page.get_by_role('button',name='Compromisos LPS',exact=True).click();assert page.locator('.lps-card').count()==20
 assert page.locator('#view-options').is_hidden();assert page.locator('.lps-summary>div').nth(2).locator('strong').inner_text()=='—'
 for week,count in [('0',3),('1',9),('2',4),('3',4)]:page.locator('#lps-week').select_option(week);assert page.locator('.lps-card').count()==count
 page.locator('#lps-week').select_option('2');gas=page.locator('.lps-card').filter(has_text='Inspección ocular de instalación de gas');assert gas.count()==1;assert 'SAN-02' in gas.inner_text();assert 'Gas' in gas.inner_text()
 assert 'Hormigón de sala de máquinas y tanques' in page.locator('#content').inner_text()
 page.locator('#lps-week').select_option('all')
 assert page.evaluate('JSON.parse(localStorage.getItem("jujuy-control-v1"))')==state
 with page.expect_download() as dl:page.get_by_role('link',name='Descargar compromisos CSV').click()
 with open(dl.value.path(),encoding='utf-8-sig') as f:rows=list(csv.reader(f))
 assert len(rows)==21 and all('planificado' in r for r in rows[1:])
 assert all('/codex-remote-attachments/' not in src for src in page.locator('img').evaluate_all('(nodes)=>nodes.map(i=>i.src)'))
 out=Path('/tmp/jujuy-lps-artifacts');out.mkdir(exist_ok=True)
 for width,height in [(390,844),(768,1024),(320,740)]:
  page.set_viewport_size({'width':width,'height':height});assert page.evaluate('document.documentElement.scrollWidth<=innerWidth');page.screenshot(path=str(out/f'lps-{width}.png'))
 page.evaluate('navigator.serviceWorker.ready');page.reload();page.wait_for_function('navigator.serviceWorker.controller!==null');context.set_offline(True);page.reload();page.wait_for_selector('.trade-card');page.get_by_role('button',name='Compromisos LPS',exact=True).click();assert page.locator('.lps-card').count()==20
 assert page.evaluate('JSON.parse(localStorage.getItem("jujuy-control-v1"))')==state;assert not errors,errors
 browser.close();print('PASS: LPS 20 compromisos, filtros 3/9/4/4, correcciones confirmadas, PPC pendiente, CSV, offline y partes privados intactos.')
