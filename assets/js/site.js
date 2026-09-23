(function(){
  window.__5to9=1;
  var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

  var all=[].slice.call(document.querySelectorAll('.reveal'));
  function showAll(){ all.forEach(function(el){ el.classList.add('in'); }); }
  try{
    if(reduce || !window.IntersectionObserver){ showAll(); }
    else{
      var io = new IntersectionObserver(function(es){
        es.forEach(function(e){ if(e.isIntersecting){ e.target.classList.add('in'); io.unobserve(e.target); } });
      },{threshold:.14});
      all.forEach(function(el){ io.observe(el); });
      /* safety net: nothing stays invisible for longer than 3s */
      setTimeout(function(){
        all.forEach(function(el){
          var r=el.getBoundingClientRect();
          if(r.top < innerHeight*1.5) el.classList.add('in');
        });
      },3000);
    }
  }catch(err){ showAll(); }

  try{
  /* phone menu */
  var burger=document.getElementById('burger'), mmenu=document.getElementById('mobilemenu');
  function setMenu(open){
    document.body.classList.toggle('menu-open',open);
    document.body.style.overflow=open?'hidden':'';
    burger.setAttribute('aria-expanded',open?'true':'false');
    burger.setAttribute('aria-label',open?burger.dataset.close:burger.dataset.open);
  }
  burger.addEventListener('click',function(){ setMenu(!document.body.classList.contains('menu-open')); });
  [].slice.call(mmenu.querySelectorAll('a')).forEach(function(a){ a.addEventListener('click',function(){ setMenu(false); }); });
  addEventListener('keydown',function(e){ if(e.key==='Escape' && document.body.classList.contains('menu-open')) setMenu(false); });
  }catch(err){}

  try{
  /* ticker: driven in JS so it keeps moving whatever the CSS is doing */
  (function(){
    var track=document.querySelector('.ticker-track');
    if(!track) return;
    var setSize=track.children.length/2;           // markup holds two identical sets
    function fill(){
      var guard=0;
      while(track.scrollWidth < innerWidth*2 && guard++ < 12){
        for(var i=0;i<setSize;i++) track.appendChild(track.children[i].cloneNode(true));
      }
    }
    fill();
    track.classList.add('js');
    var loop=track.children[setSize].offsetLeft, x=0, prev=null, speed=42; // px per second
    addEventListener('resize',function(){ fill(); loop=track.children[setSize].offsetLeft; });
    function step(t){
      if(prev===null) prev=t;
      var dt=Math.min((t-prev)/1000,.05); prev=t;
      x-=speed*dt;
      if(loop && -x>=loop) x+=loop;
      track.style.transform='translateX('+x.toFixed(2)+'px)';
      requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  })();
  }catch(err){}

  try{
  /* nav: orange indicator follows the section you are in (home) or sits under the current page (landing) */
  var navLinks=[].slice.call(document.querySelectorAll('.nav-links a')),
      ind=document.getElementById('nav-ind');
  function place(target){
    if(target && target.offsetWidth){
      ind.style.width=target.offsetWidth+'px';
      ind.style.transform='translateX('+target.offsetLeft+'px)';
      ind.style.opacity='1';
    } else { ind.style.opacity='0'; }
  }
  addEventListener('resize',function(){ place(document.querySelector('.nav-links a.active')); });

  var rail=document.getElementById('rail');
  if(!rail){
    place(document.querySelector('.nav-links a.active'));
  } else {
    var navFor={top:null,offer:'#offer',about:'#about',sports:'#sports',fitness:'#fitness',digital:'#digital',
                playgrounds:'#playgrounds',process:'#process',contact:null};
    var markNav=function(id){
      var href=navFor[id], target=null;
      navLinks.forEach(function(a){
        var on = href && a.getAttribute('href')===href;
        a.classList.toggle('active', !!on);
        if(on) target=a;
      });
      place(target);
    };
    var links=[].slice.call(rail.querySelectorAll('a'));
    var lightIds=['about','sports','fitness','process'];
    var railObserver=new IntersectionObserver(function(es){
      es.forEach(function(e){
        if(!e.isIntersecting) return;
        var id=e.target.id;
        markNav(id);
        links.forEach(function(a){
          a.classList.toggle('active', a.dataset.t===id);
          a.classList.toggle('on-light', lightIds.indexOf(id)>-1);
        });
      });
    },{threshold:.5});
    [].slice.call(document.querySelectorAll('.band[id]')).forEach(function(s){ railObserver.observe(s); });
  }
  }catch(err){}

  try{
  /* product detail sheet */
  var sheet=document.getElementById('sheet'), sPhoto=document.getElementById('sheet-photo'),
      sTitle=document.getElementById('sheet-title'), sKind=document.getElementById('sheet-kind'),
      sSpecs=document.getElementById('sheet-specs'), lastFocus=null;
  function openSheet(card){
    lastFocus=card;
    sPhoto.src=card.dataset.img;
    sTitle.textContent=card.querySelector('h4').textContent;
    sPhoto.alt=sTitle.textContent;
    var kind=card.querySelector('.kind');
    sKind.textContent=kind?kind.textContent:'';
    sSpecs.innerHTML=card.querySelector('ul').innerHTML;
    sheet.classList.add('open');
    document.body.style.overflow='hidden';
    document.getElementById('sheet-close').focus();
  }
  function closeSheet(){
    sheet.classList.remove('open');
    document.body.style.overflow='';
    if(lastFocus) lastFocus.focus();
  }
  [].slice.call(document.querySelectorAll('.model[data-img]')).forEach(function(card){
    card.addEventListener('click',function(){ openSheet(card); });
    card.addEventListener('keydown',function(e){
      if(e.key==='Enter'||e.key===' '){ e.preventDefault(); openSheet(card); }
    });
  });
  document.getElementById('sheet-close').addEventListener('click',closeSheet);
  document.getElementById('sheet-ask').addEventListener('click',closeSheet);
  sheet.addEventListener('click',function(e){ if(e.target===sheet) closeSheet(); });
  addEventListener('keydown',function(e){ if(e.key==='Escape' && sheet.classList.contains('open')) closeSheet(); });
  }catch(err){}

  try{
  var bar=document.getElementById('progress');
  addEventListener('scroll',function(){
    var y=scrollY, h=document.body.scrollHeight-innerHeight;
    bar.style.width=(h>0? y/h*100:0)+'%';
  },{passive:true});
  }catch(err){}
})();
