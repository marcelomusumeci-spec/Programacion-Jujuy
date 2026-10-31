"""Interacciones de la portada visual en un perfil temporal, sin datos de usuarios."""
from playwright.sync_api import sync_playwright
from pathlib import Path
import os,json
BASE=os.environ.get('JUJUY_TEST_URL','http://127.0.0.1:8000')
ARTIFACTS=Path('/tmp/jujuy-home-artifacts');ARTIFACTS.mkdir(exist_ok=True)
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path=os.environ.get('CHROMIUM_PATH','/usr/bin/chromium'),headless=True,args=['--no-sandbox'])
 context=browser.new_context(viewport={'width':390,'height':844},is_mobile=True,has_touch=True)
 page=context.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto(BASE);page.wait_for_selector('.visual-hero');page.locator('#cutoff').fill('2026-10-31');page.locator('#cutoff').dispatch_event('change')
 assert not page.locator('#view-options').evaluate('(e)=>e.open')
 assert page.locator('.mobile-company img').evaluate('(i)=>i.complete&&i.naturalWidth>0')
 page.locator('#view-options summary').click();page.locator('#level').select_option('N1');assert page.locator('#view-options').evaluate('(e)=>e.open');assert 'N1' in page.locator('#view-options summary').inner_text()
 page.locator('#clear').click();page.locator('#view-options summary').click()
 # Es una muestra local para validar la prioridad, no un parte publicado.
 state={'version':1,'project':'jujuy-a0','reports':[{'taskId':43,'date':'2026-10-31','progress':25,'owner':'Prueba','note':'Prueba de interfaz','savedAt':'2026-10-31T15:00:00.000Z'}],'restrictions':[{'id':'test-home','taskId':44,'opened':'2026-10-29','due':'2026-10-30','resolved':None,'cause':'Material de prueba pendiente','owner':'Prueba','category':'Materiales'}]}
 page.evaluate('(s)=>localStorage.setItem("jujuy-control-v1",JSON.stringify(s))',state);page.reload();page.wait_for_selector('.visual-hero');page.locator('#cutoff').fill('2026-10-31');page.locator('#cutoff').dispatch_event('change')
 assert page.locator('.stat-card.blocked strong').inner_text()=='01';assert page.locator('.stat-card.late strong').inner_text()=='01'
 assert page.locator('.focus-row').first.get_attribute('data-task')=='44'
 assert page.locator('.focus-row').nth(1).get_attribute('data-task')=='43'
 page.locator('.focus-row').first.click();assert page.locator('.dialog-heading .badge').inner_text()=='Restringido';page.locator('[data-close=task-dialog]').click()
 page.locator('.stat-card.blocked').click();assert page.locator('.trade-card').count()==1;assert 'Albañilería' in page.locator('.trade-card').inner_text()
 page.locator('.trade-card').click();assert page.locator('.task-row').count()>0;assert page.locator('#trade').input_value()=='Albañilería'
 page.locator('.mobile-company').click();page.locator('#clear').click() if page.locator('#view-options').evaluate('(e)=>e.open') else None
 # Capturas sin el toast ni foco de fecha, mostrando sólo este perfil de prueba.
 page.locator('#view-options summary').click();page.locator('#clear').click();page.locator('#view-options summary').click()
 page.wait_for_timeout(5200)
 for width,height,name in [(390,844,'mobile'),(768,1024,'tablet'),(1440,1000,'desktop'),(320,740,'small-mobile')]:
  page.set_viewport_size({'width':width,'height':height});assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
  page.screenshot(path=str(ARTIFACTS/(name+'.png')))
 assert not errors,errors
 browser.close();print('PASS: logo oficial, filtros desplegables, prioridad restricciones/atrasos, filtro por semáforo, acceso a actividades, navegación de marca y 4 tamaños sin desborde.')
