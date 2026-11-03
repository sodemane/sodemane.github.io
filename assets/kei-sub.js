// 生成物: tools/make_kei_sub.py（直接編集しない）
(function(){
  var KEIS=["star","neon","noir","dream","splash"], KEY="sodemane_lp_kei";
  var FONTS={
    neon:"family=Zen+Kaku+Gothic+New:wght@500;700;900&family=Orbitron:wght@700",
    noir:"family=Shippori+Mincho+B1:wght@500;700;800&family=Noto+Serif+JP:wght@500;700;900&family=Cinzel:wght@700",
    star:"family=RocknRoll+One&family=M+PLUS+Rounded+1c:wght@500;700;800;900&family=Poppins:wght@700",
    dream:"family=Hachi+Maru+Pop&family=Kosugi+Maru&family=Quicksand:wght@700",
    splash:"family=Mochiy+Pop+One&family=M+PLUS+Rounded+1c:wght@500;700;800;900"
  };
  // 各系の 2 つ目の書体（アプリの fontChoices と同じ・skin_packs.dart）。選ばれたときだけ読み込む
  var ALT_FONTS={
    neon:"family=DotGothic16",
    noir:"family=Zen+Old+Mincho:wght@500;700;900",
    star:"family=Mochiy+Pop+One",
    dream:"family=Yusei+Magic",
    splash:"family=Reggae+One"
  }, FKEY="sodemane_lp_kei_font";
  var loaded={};
  function altFont(k){
    if(!ALT_FONTS[k]||loaded["alt_"+k]) return; loaded["alt_"+k]=true;
    var l=document.createElement("link"); l.rel="stylesheet";
    l.href="https://fonts.googleapis.com/css2?"+ALT_FONTS[k]+"&display=swap";
    document.head.appendChild(l);
  }
  function font(k){
    if(!FONTS[k]||loaded[k]) return; loaded[k]=true;
    var l=document.createElement("link"); l.rel="stylesheet";
    l.href="https://fonts.googleapis.com/css2?"+FONTS[k]+"&display=swap";
    document.head.appendChild(l);
  }
  var k=null;
  try{
    var q=new URLSearchParams(location.search).get("kei");
    if(q!==null){ q=q.toLowerCase(); if(q==="default") k=""; else if(KEIS.indexOf(q)>=0) k=q; }
  }catch(e){}
  if(k===null){ try{ var v=localStorage.getItem(KEY); if(v&&KEIS.indexOf(v)>=0) k=v; }catch(e){} }
  var alt=false;
  if(k){
    document.documentElement.setAttribute("data-kei",k); font(k); altFont(k);
    try{ alt=localStorage.getItem(FKEY)===k; }catch(e){}
    if(alt) document.documentElement.setAttribute("data-kei-font","alt");
  }
  window.__sodeKei={ list:KEIS, key:KEY, font:font, altFont:altFont, fontKey:FKEY, initial:k||"", initialAlt:alt };
})();
(function(){
  var K=window.__sodeKei, root=document.documentElement;
  var LIST=[["","いつもの","linear-gradient(120deg,#ff5fa2,#8b5cf6)"],
    ["star","STAR","linear-gradient(120deg,#FF4488,#FFD700)"],
    ["neon","NEON","linear-gradient(120deg,#120025,#00E5FF)"],
    ["noir","NOIR","linear-gradient(120deg,#4B0082,#D4AF6A)"],
    ["dream","DREAM","linear-gradient(120deg,#FFD6EC,#C5E0FC,#B06BF0)"],
    ["splash","SPLASH","linear-gradient(120deg,#FF2D95,#DBFF9E)"]];
  function ready(){
    var imgs=Array.prototype.slice.call(document.querySelectorAll('img[src*="assets/screens/app-"]'));
    imgs.forEach(function(i){ i.setAttribute("data-default-src", i.getAttribute("src")); });
    var meta=document.querySelector('meta[name="theme-color"]'), metaDefault=meta&&meta.getAttribute("content");
    var bar=document.querySelector(".topbar .in");
    var wrap,toggle,pop;
    function apply(k, persist){
      if(k){ root.setAttribute("data-kei",k); K.font(k); K.altFont(k); } else { root.removeAttribute("data-kei"); root.removeAttribute("data-kei-font"); }
      imgs.forEach(function(i){
        var d=i.getAttribute("data-default-src");
        i.setAttribute("src", k ? d.replace("assets/screens/", "assets/screens/skins/"+k+"/") : d);
      });
      if(meta) meta.setAttribute("content", k ? getComputedStyle(root).getPropertyValue("--theme").trim() : metaDefault);
      if(pop) pop.querySelectorAll("button[data-kei]").forEach(function(b){
        var on=b.getAttribute("data-kei")===k;
        b.setAttribute("aria-pressed", on?"true":"false");
        if(on) toggle.querySelector("i").style.setProperty("--g", b.querySelector("i").style.getPropertyValue("--g"));
      });
      if(persist){
        try{ localStorage.removeItem(K.fontKey); if(k) localStorage.setItem(K.key,k); else localStorage.removeItem(K.key); }catch(e){}
        root.removeAttribute("data-kei-font");
      }
    }
    function open(on){ pop.hidden=!on; toggle.setAttribute("aria-expanded", on?"true":"false"); }
    if(bar){
      wrap=document.createElement("div"); wrap.className="kei-menu";
      wrap.innerHTML='<button type="button" class="kei-toggle" aria-expanded="false" aria-controls="keiPop"><i></i>着せ替え</button>';
      toggle=wrap.firstChild;
      pop=document.createElement("div"); pop.className="kei-pop"; pop.id="keiPop"; pop.hidden=true;
      pop.innerHTML='<div class="kei-pick" role="group" aria-label="このページの見た目を、アプリの系スキン（世界観）で着せ替える"><span class="kp-lbl">このページを、アプリの世界観で着せ替え</span><div class="kp-row">'
        +LIST.map(function(x){ return '<button type="button" data-kei="'+x[0]+'" aria-pressed="false"><i style="--g:'+x[2]+'"></i><b>'+x[1]+'</b></button>'; }).join("")
        +'</div></div>';
      wrap.appendChild(pop); bar.appendChild(wrap);
      toggle.addEventListener("click", function(ev){ ev.stopPropagation(); open(pop.hidden); });
      pop.addEventListener("click", function(ev){
        ev.stopPropagation();
        var b=ev.target.closest("button[data-kei]"); if(!b) return;
        apply(b.getAttribute("data-kei"), true);
      });
      document.addEventListener("click", function(){ open(false); });
      document.addEventListener("keydown", function(ev){ if(ev.key==="Escape"){ open(false); toggle.focus(); } });
    }
    apply(K.initial, false);
    if(K.initialAlt) root.setAttribute("data-kei-font","alt");
  }
  if(document.readyState==="loading") document.addEventListener("DOMContentLoaded", ready); else ready();
})();
