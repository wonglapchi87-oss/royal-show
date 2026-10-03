import asyncio,sys
from playwright.async_api import async_playwright
URL=sys.argv[1] if len(sys.argv)>1 else 'http://localhost:8765/'
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch()
    c=await b.new_context(viewport={'width':390,'height':844},device_scale_factor=2,is_mobile=True,has_touch=True,timezone_id='Australia/Perth',geolocation={'latitude':-31.9778,'longitude':115.7846},permissions=['geolocation'])
    pg=await c.new_page(); errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e))); pg.on('console',lambda m: m.type=='error' and errs.append(m.text))
    await pg.goto(URL,wait_until='networkidle'); await pg.wait_for_timeout(800)
    await pg.screenshot(path='screens/1-events.png')
    await pg.click('nav button[data-v=route]'); await pg.select_option('#dst','Global Stage'); await pg.wait_for_timeout(200)
    await pg.screenshot(path='screens/2-picker.png')
    await pg.click('#showroute'); await pg.wait_for_timeout(2500)
    await pg.screenshot(path='screens/3-map-route.png')
    print('dir:',await pg.text_content('#dirtxt'),'|',await pg.text_content('#dirsub'),'|',await pg.text_content('#gpsnote'))
    print('errors:',errs); await b.close()
asyncio.run(main())
