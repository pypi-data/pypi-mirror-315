import{at as m,ab as A,au as O,ae as D,av as g,Z as h,S as N,U as I,O as u,ac as L,aw as V,ax as C,a8 as H,W as Y,ay as M,T as W,J as $,p as j,N as w,C as k,a as J,i as P}from"./runtime.B40kIuYm.js";import{a as U,r as R,h as v}from"./events.DTvxUH_b.js";import{b as Z}from"./disclose-version.hHXjza9X.js";const q=["touchstart","touchmove"];function z(t){return q.includes(t)}function Q(t,e){var n=e==null?"":typeof e=="object"?e+"":e;n!==(t.__t??(t.__t=t.nodeValue))&&(t.__t=n,t.nodeValue=n==null?"":n+"")}function B(t,e){return S(t,e)}function X(t,e){m(),e.intro=e.intro??!1;const n=e.target,_=w,l=u;try{for(var a=A(n);a&&(a.nodeType!==8||a.data!==O);)a=D(a);if(!a)throw g;h(!0),N(a),I();const d=S(t,{...e,anchor:a});if(u===null||u.nodeType!==8||u.data!==L)throw V(),g;return h(!1),d}catch(d){if(d===g)return e.recover===!1&&C(),m(),H(n),h(!1),B(t,e);throw d}finally{h(_),N(l)}}const i=new Map;function S(t,{target:e,anchor:n,props:_={},events:l,context:a,intro:d=!0}){m();var y=new Set,p=o=>{for(var r=0;r<o.length;r++){var s=o[r];if(!y.has(s)){y.add(s);var f=z(s);e.addEventListener(s,v,{passive:f});var T=i.get(s);T===void 0?(document.addEventListener(s,v,{passive:f}),i.set(s,1)):i.set(s,T+1)}}};p(Y(U)),R.add(p);var c=void 0,b=M(()=>{var o=n??e.appendChild(W());return $(()=>{if(a){j({});var r=P;r.c=a}l&&(_.$$events=l),w&&Z(o,null),c=t(o,_)||{},w&&(k.nodes_end=u),a&&J()}),()=>{var f;for(var r of y){e.removeEventListener(r,v);var s=i.get(r);--s===0?(document.removeEventListener(r,v),i.delete(r)):i.set(r,s)}R.delete(p),E.delete(c),o!==n&&((f=o.parentNode)==null||f.removeChild(o))}});return E.set(c,b),c}let E=new WeakMap;function x(t){const e=E.get(t);e&&e()}export{X as h,B as m,Q as s,x as u};
