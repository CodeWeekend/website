// Render native SVG masters and the guide using the local Chrome installation.
// Usage: node render.cjs /path/to/playwright-core
const { chromium } = require(process.argv[2] || 'playwright-core');
const fs = require('fs');
const path = require('path');
const { pathToFileURL } = require('url');
const root = path.resolve(__dirname, '..');
(async () => {
  const browser = await chromium.launch({ executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless: true });
  const page = await browser.newPage({ viewport: { width: 1320, height: 850 }, deviceScaleFactor: 1 });
  await page.goto(pathToFileURL(path.join(root, 'brand-guide.html')).href);
  await page.evaluate(() => document.fonts.ready);
  const broken = await page.locator('img').evaluateAll(imgs => imgs.filter(i => !i.complete || !i.naturalWidth).map(i => i.src));
  if (broken.length) throw new Error('Broken guide images: ' + broken.join(', '));
  const overflow = await page.locator('.page').evaluateAll(pages => pages.flatMap((p,idx) => {
    const box=p.getBoundingClientRect();
    return [...p.querySelectorAll('h1,h2,h3,h4,p,img,.swatch,footer')].filter(e=> {
      const r=e.getBoundingClientRect(); return r.left<box.left || r.right>box.right+1 || r.top<box.top || r.bottom>box.bottom+1;
    }).map(e=>({page:idx+1,tag:e.tagName,text:e.textContent.slice(0,60)}));
  }));
  const pages=await page.locator('.page').count();
  const footerCollisions=await page.locator('.page').evaluateAll(pages=>pages.flatMap((p,i)=>{
    const top=p.querySelector('footer').getBoundingClientRect().top;
    return [...p.querySelectorAll('p,h1,h2,h3,h4,img,.rule-strip,.token-notes,.rtl-rules,.screening-note')].filter(e=>e.getBoundingClientRect().bottom>top-8).map(e=>({page:i+1,tag:e.tagName,text:e.textContent.slice(0,80)}));
  }));
  await page.pdf({path:path.join(root,'codeweekend-brand-guide.pdf'),preferCSSPageSize:true,printBackground:true,tagged:true});
  require('child_process').execFileSync('/opt/homebrew/bin/pdftoppm',['-scale-to','1200','-png',path.join(root,'codeweekend-brand-guide.pdf'),path.join(root,'previews/page')]);
  const exports=[];
  const logoBounds=[];
  for(const folder of ['logos','applications','imagery','research']){
    for(const name of fs.readdirSync(path.join(root,folder)).filter(n=>n.endsWith('.svg'))){
      const source=fs.readFileSync(path.join(root,folder,name),'utf8');
      const match=source.match(/viewBox="[^"]*? ([\d.]+) ([\d.]+)"/);
      const rawW=Number(match[1]), rawH=Number(match[2]);
      const w=folder==='logos' ? (name==='favicon.svg'?32:name==='avatar.svg'?800:name.startsWith('mark')?512:1600) : rawW;
      const h=Math.round(rawH*w/rawW);
      await page.setViewportSize({width:Math.ceil(w),height:h});
      await page.setContent(`<html><body style="margin:0;background:transparent"><div style="width:${w}px;height:${h}px">${source.replace(/width="[^"]+" height="[^"]+"/,`width="${w}" height="${h}"`)}</div></body></html>`);
      if(folder==='logos') logoBounds.push(await page.locator('svg').evaluate((e,file)=>{
        const b=e.getBBox(),v=e.viewBox.baseVal;
        return {file,inside:b.x>=v.x-.1&&b.y>=v.y-.1&&b.x+b.width<=v.width+.1&&b.y+b.height<=v.height+.1,bounds:{x:b.x,y:b.y,width:b.width,height:b.height}};
      },name));
      const output=path.join(root,folder,name.replace('.svg','.png'));
      // Rasterize the SVG itself. This avoids screenshot compositor tiling after
      // repeated viewport changes, and preserves exact alpha and dimensions.
      const png=await page.evaluate(async ({source,w,h})=>{
        const img=new Image(); img.src='data:image/svg+xml;base64,'+btoa(unescape(encodeURIComponent(source)));
        await img.decode();
        const canvas=document.createElement('canvas');canvas.width=w;canvas.height=h;
        canvas.getContext('2d').drawImage(img,0,0,w,h);
        return canvas.toDataURL('image/png').split(',')[1];
      },{source,w,h});
      fs.writeFileSync(output,Buffer.from(png,'base64'));
      exports.push({file:path.relative(root,output),width:w,height:h});
    }
  }
  // A transparent icon size strip is useful for checking the mark at actual pixels.
  const icon=fs.readFileSync(path.join(root,'logos/favicon.svg'),'utf8');
  await page.setViewportSize({width:600,height:170});
  await page.setContent(`<body style="margin:0;padding:32px;background:#F7F4EC;display:flex;gap:28px;align-items:center">${[16,24,32,48,64].map(n=>`<div>${icon.replace('width="32" height="32"',`width="${n}" height="${n}"`)}<p style="font:12px sans-serif">${n}px</p></div>`).join('')}</body>`);
  await page.screenshot({path:path.join(root,'previews/size-check.png')});
  const specimen=await browser.newPage({viewport:{width:1200,height:1600},deviceScaleFactor:1});
  await specimen.goto(pathToFileURL(path.join(root,'web-preview.html')).href);
  await specimen.evaluate(()=>document.fonts.ready);
  const rtl=await specimen.locator('[data-script]').evaluateAll(es=>es.map(e=>({script:e.dataset.script,font:getComputedStyle(e).fontFamily,direction:getComputedStyle(e).direction,logoDirection:getComputedStyle(e.querySelector('.cw-logo')).direction})));
  await specimen.getByRole('button',{name:'Join the community'}).focus();
  const focus=await specimen.getByRole('button',{name:'Join the community'}).evaluate(e=>({width:getComputedStyle(e).outlineWidth,offset:getComputedStyle(e).outlineOffset}));
  const codeFont=await specimen.locator('code').evaluate(e=>({font:getComputedStyle(e).fontFamily,direction:getComputedStyle(e).direction}));
  if(!codeFont.font.includes('Atkinson')||codeFont.direction!=='ltr') throw new Error('Code specimen must use its LTR mono font');
  await specimen.screenshot({path:path.join(root,'previews/web-preview.png'),fullPage:true});
  fs.writeFileSync(path.join(root,'source/render-checks.json'),JSON.stringify({pages,brokenImages:broken,guideOverflow:overflow,footerCollisions,logoBounds,rtl,codeFont,focus,exports},null,2));
  await browser.close();
  console.log(JSON.stringify({pages,brokenImages:broken,guideOverflow:overflow,footerCollisions,logoBoundsPass:logoBounds.every(l=>l.inside),rtl,focus,exports:exports.length}));
  if(overflow.length||footerCollisions.length||logoBounds.some(l=>!l.inside)||rtl.some(r=>!r.font.includes('Vazirmatn')||r.direction!=='rtl'||r.logoDirection!=='ltr')||focus.width!=='3px') process.exitCode=1;
})().catch(e=>{console.error(e);process.exit(1)});
