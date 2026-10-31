"""Verifica actualización de una instalación A0 sin perder partes privados."""
from pathlib import Path
from tempfile import TemporaryDirectory
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
import subprocess,tarfile,io,threading,json,os
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parent.parent
with TemporaryDirectory(prefix='jujuy-update-') as temp:
    archive=subprocess.check_output(['git','archive','32c8845'],cwd=ROOT)
    with tarfile.open(fileobj=io.BytesIO(archive)) as tar:tar.extractall(temp,filter='data')
    active={'directory':temp}
    class Handler(SimpleHTTPRequestHandler):
        def __init__(self,*args,**kwargs):super().__init__(*args,directory=active['directory'],**kwargs)
        def log_message(self,*args):pass
        def end_headers(self):self.send_header('Cache-Control','no-cache');super().end_headers()
    server=ThreadingHTTPServer(('127.0.0.1',0),Handler)
    thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
    try:
        with sync_playwright() as p:
            browser=p.chromium.launch(executable_path=os.environ.get('CHROMIUM_PATH','/usr/bin/chromium'),headless=True,args=['--no-sandbox'])
            context=browser.new_context(viewport={'width':390,'height':844},is_mobile=True,has_touch=True)
            page=context.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
            url=f'http://127.0.0.1:{server.server_port}/'
            page.goto(url);page.wait_for_selector('.trade-card');page.evaluate('navigator.serviceWorker.ready');page.reload();page.wait_for_function('navigator.serviceWorker.controller !== null')
            part={'version':1,'project':'jujuy-a0','reports':[{'taskId':43,'date':'2026-10-31','progress':43,'owner':'Jefe original','note':'Conservar este parte','savedAt':'2026-10-31T14:00:00.000Z'}],'restrictions':[]}
            page.evaluate('(s)=>localStorage.setItem("jujuy-control-v1",s)',json.dumps(part))
            active['directory']=str(ROOT)
            page.reload();page.wait_for_selector('#apply-update',timeout=20000);page.locator('#apply-update').click();page.wait_for_function("navigator.serviceWorker.controller && document.querySelector('.sidebar-bottom strong')?.textContent.includes('R1')")
            page.wait_for_timeout(500)
            assert page.evaluate('JSON.parse(localStorage.getItem("jujuy-control-v1"))')==part
            assert page.evaluate("fetch('data/schedule.json?v=r1').then(r=>r.json()).then(d=>d.revision)")=='r1'
            assert page.evaluate("caches.keys()") == ['jujuy-app-oddino-v1']
            context.set_offline(True);page.reload();page.wait_for_selector('.trade-card')
            assert page.locator('.sidebar-bottom strong').inner_text()=='R1 · Base real 30/10/2026'
            assert page.evaluate('JSON.parse(localStorage.getItem("jujuy-control-v1"))')==part
            assert not errors,errors
            browser.close()
            print('PASS: actualización A0 → R1 en celular, partes intactos y portada Oddino disponible offline.')
    finally:server.shutdown();server.server_close()
