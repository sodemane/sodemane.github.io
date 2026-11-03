#!/usr/bin/env python3
"""機能ページ（features/*.html）用の着せ替えを index.html から作る（2026-11-03）。

使い方: python3 tools/make_kei_sub.py

- 色・書体の定義と、最初に系を当てるスクリプトは index.html を正本にして写す（手で二重に持たない）。
- 出力: assets/kei-sub.css / assets/kei-sub.js
- index.html の系スキン定義を変えたら、これを実行してから公開する。
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = (ROOT / "index.html").read_text(encoding="utf-8")


def between(start: str, end: str) -> str:
    i = INDEX.index(start)
    return INDEX[i:INDEX.index(end, i)]


tokens = between('html[data-kei="neon"]{color-scheme:dark', "html[data-kei] .field input::placeholder")
menu = between("/* 世界観の切替ボタン", ".hero .shot-wrap{")
head = re.search(r"\(function\(\)\{\n  var KEIS=.*?\n\}\)\(\);", INDEX, re.S).group(0)

OVERRIDES = """
/* ここから機能ページ専用（色を直書きしている部品をトークンへ寄せる） */
html[data-kei] body{background:var(--page-bg,var(--cream))}
html[data-kei] .topbar{background:var(--topbar-bg,var(--cream))}
html[data-kei] .btn-primary,html[data-kei] .step .n{color:var(--on-accent,#fff)}
html[data-kei] .btn-ghost,html[data-kei] .sec.white,html[data-kei] .frow,html[data-kei] .step{background:var(--surface,#fff)}
html[data-kei] .sec.white .frow,html[data-kei] .view{background:var(--band,var(--cream))}
html[data-kei] .honest{border-color:var(--line)}
.topbar .in{position:relative}
.topbar .brand{margin-left:auto}
.topbar .kei-menu{margin-left:10px;order:3}
@media(max-width:400px){.topbar .brand{font-size:0;gap:0}}
"""

JS = (
    "// 生成物: tools/make_kei_sub.py（直接編集しない）\n"
    + head
    + r"""
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
"""
)

(ROOT / "assets/kei-sub.css").write_text(
    "/* 生成物: tools/make_kei_sub.py（直接編集しない） */\n" + tokens + "\n" + menu + OVERRIDES, encoding="utf-8"
)
(ROOT / "assets/kei-sub.js").write_text(JS, encoding="utf-8")
print("ok", len(tokens), len(menu), len(JS))
