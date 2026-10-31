from playwright.sync_api import sync_playwright
import json,os
from pathlib import Path
BASE=os.environ.get("JUJUY_TEST_URL","http://127.0.0.1:8000")
ARTIFACTS=Path(os.environ.get("JUJUY_TEST_ARTIFACTS","/tmp/jujuy-browser-artifacts"))
ARTIFACTS.mkdir(parents=True,exist_ok=True)
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path=os.environ.get('CHROMIUM_PATH','/usr/bin/chromium'),headless=True,args=['--no-sandbox'])
 context=browser.new_context(viewport={'width':1440,'height':1050},accept_downloads=True)
 page=context.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto(BASE);page.wait_for_selector('.trade-card');page.locator('#cutoff').fill('2026-10-31');page.locator('#cutoff').dispatch_event('change');page.screenshot(path=str(ARTIFACTS/'jujuy-desktop.png'),full_page=True)
 assert page.locator('.stat-card.missing strong').inner_text()=='06'
 page.locator('#cutoff').fill('2027-03-10');page.locator('#cutoff').dispatch_event('change')
 page.get_by_role('button',name='Programación',exact=True).click();page.locator('#search').fill('N1-ALB_ET1');page.locator('[data-task="43"]').click()
 f=page.locator('#report-form');f.locator('[name=progress]').fill('50');f.locator('[name=owner]').fill('Jefatura');f.locator('[name=note]').fill('Parte de prueba');f.get_by_role('button',name='Guardar parte',exact=True).click()
 assert page.locator('.dialog-heading .badge').inner_text()=='Atrasado'
 page.locator('.add-restriction summary').click();rf=page.locator('#restriction-form');rf.locator('[name=cause]').fill('Falta material de prueba');rf.locator('[name=owner]').fill('Compras');rf.locator('[name=due]').fill('2027-03-12');rf.get_by_role('button',name='Guardar restricción',exact=True).click()
 assert page.locator('.dialog-heading .badge').inner_text()=='Restringido'
 page.locator('[data-resolve] button').click();assert page.locator('.dialog-heading .badge').inner_text()=='Atrasado'
 page.locator('[data-close=task-dialog]').click();page.reload();page.wait_for_selector('.task-row, .trade-card');page.locator('#cutoff').fill('2027-03-10');page.locator('#cutoff').dispatch_event('change');page.get_by_role('button',name='Programación',exact=True).click();page.locator('#search').fill('N1-ALB_ET1')
 assert page.locator('[data-task="43"] .badge').inner_text()=='Atrasado'
 with page.expect_download() as download:page.locator('#backup').click()
 path=download.value.path();backup=json.load(open(path));assert backup['reports'][0]['progress']==50;assert backup['restrictions'][0]['resolved']=='2027-03-10'
 with page.expect_download() as download:page.locator('#export-cut').click()
 assert 'N1-ALB_ET1' in open(download.value.path(),encoding='utf-8-sig').read()
 # Restoration and its confirmation are exercised with the exported copy.
 page.on('dialog',lambda d:d.accept());page.locator('#restore').set_input_files({'name':'copia.json','mimeType':'application/json','buffer':json.dumps(backup).encode()});page.wait_for_timeout(250)
 assert page.locator('[data-task="43"] .badge').inner_text()=='Atrasado'
 # Real viewport, touch/mobile, no horizontal overflow; exercise the modal.
 mobile=browser.new_context(viewport={'width':390,'height':844},is_mobile=True,has_touch=True,device_scale_factor=1)
 m=mobile.new_page();m.on('pageerror',lambda e:errors.append(str(e)));m.goto(BASE);m.wait_for_selector('.trade-card');assert m.evaluate('document.documentElement.scrollWidth <= innerWidth')
 m.screenshot(path=str(ARTIFACTS/'jujuy-mobile.png'),full_page=True);m.get_by_role('button',name='Programación',exact=True).click();m.locator('#search').fill('N1-ALB_ET1');m.locator('[data-task="43"]').click();assert m.locator('#task-dialog').is_visible();assert m.evaluate('document.documentElement.scrollWidth <= innerWidth');m.screenshot(path=str(ARTIFACTS/'jujuy-mobile-detail.png'),full_page=True);m.locator('[data-close=task-dialog]').click()
 m.get_by_role('button',name='Base documental',exact=True).click();assert m.locator('.source-list a').count()==9
 # Complete first install, control reload, then offline cold navigation and data entry.
 page.evaluate('navigator.serviceWorker.ready');page.reload();page.wait_for_selector('.trade-card');page.wait_for_function('navigator.serviceWorker.controller !== null');context.set_offline(True);page.reload();page.wait_for_selector('.trade-card');page.get_by_role('button',name='Programación',exact=True).click();page.locator('#search').fill('N1-ALB_ET1');page.locator('[data-task="43"]').click();f=page.locator('#report-form');f.locator('[name=date]').fill('2027-03-11');f.locator('[name=progress]').fill('70');f.get_by_role('button',name='Guardar parte',exact=True).click();assert page.evaluate('JSON.parse(localStorage.getItem("jujuy-control-v1")).reports.length')==2
 assert not errors,errors
 # Tablet portrait and narrow mobile.
 for width,height in [(768,1024),(320,740)]:
  m.set_viewport_size({'width':width,'height':height});m.get_by_role('button',name='Tablero',exact=True).click();assert m.evaluate('document.documentElement.scrollWidth <= innerWidth'),width
 print('PASS: desktop, mobile 390/320, tablet 768, avance, restricción/resolución, persistencia, CSV, respaldo/restauración, corte histórico, offline y cero errores JS')
 browser.close()
