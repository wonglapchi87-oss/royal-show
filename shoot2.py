import asyncio,sys
from playwright.async_api import async_playwright
URL=sys.argv[1] if len(sys.argv)>1 else 'http://localhost:8765/'
OUT=sys.argv[2] if len(sys.argv)>2 else 'screens'
async def ctx(b,lat,lng):
    return await b.new_context(viewport={'width':390,'height':844},device_scale_factor=2,is_mobile=True,has_touch=True,timezone_id='Australia/Perth',geolocation={'latitude':lat,'longitude':lng},permissions=['geolocation'],service_workers='block')
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(); errs=[]
    c=await ctx(b,-31.9779,115.7849)  # just inside Gate 1
    pg=await c.new_page(); pg.on('pageerror',lambda e:errs.append(str(e))); pg.on('console',lambda m: m.type=='error' and errs.append(m.text))
    await pg.goto(URL,wait_until='networkidle'); await pg.wait_for_timeout(800)
    await pg.screenshot(path=f'{OUT}/v2-1-events.png')
    await pg.fill('#q','woodchop'); await pg.wait_for_timeout(200); n=await pg.locator('.ev').count(); print('search woodchop ->',n); await pg.fill('#q','')
    await pg.click('nav button[data-v=route]'); await pg.select_option('#dst','Global Stage'); await pg.wait_for_timeout(200)
    await pg.screenshot(path=f'{OUT}/v2-2-picker.png')
    await pg.click('#showroute'); await pg.wait_for_timeout(2500)
    await pg.screenshot(path=f'{OUT}/v2-3-footpath-route.png')
    print('IN:',await pg.text_content('#dirtxt'),'|',await pg.text_content('#dirsub'))
    await pg.click('#hintsbox summary'); await pg.wait_for_timeout(300)
    print('hints:',await pg.inner_text('#hints'))
    await pg.screenshot(path=f'{OUT}/v2-4-route-steps.png')
    # tap event Go here
    await pg.click('nav button[data-v=events]'); await pg.fill('#q','Fireworks'); await pg.click('.go'); await pg.wait_for_timeout(1500)
    print('EV:',await pg.text_content('#dirtxt'),'|',await pg.text_content('#dirsub'))
    c2=await ctx(b,-31.9807,115.7814)  # Claremont station, outside
    p2=await c2.new_page(); p2.on('pageerror',lambda e:errs.append(str(e)))
    await p2.goto(URL,wait_until='networkidle'); await p2.wait_for_timeout(500)
    await p2.fill('#q','Fireworks'); await p2.click('.go'); await p2.wait_for_timeout(2500)
    await p2.screenshot(path=f'{OUT}/v2-5-outside-showground.png')
    print('OUT:',await p2.text_content('#warn'),'|',await p2.text_content('#dirtxt'),'|',await p2.text_content('#dirsub'),'|',await p2.get_attribute('#gmaps','href'))
    t=await p2.evaluate("()=>{const t0=performance.now();for(let i=0;i<20;i++)buildRoute({lat:-31.9719,lng:115.7867},{lat:-31.9780,lng:115.7857});return (performance.now()-t0)/20}")
    print('route ms',round(t,1))
    print('errors:',errs); await b.close()
asyncio.run(main())
