import{K as n,am as i,F as c,g as o,b as a}from"./runtime.B40kIuYm.js";import{s as f}from"./entry.1R3Ceel4.js";function g(s,u,r){if(s==null)return u(void 0),n;const e=s.subscribe(u,r);return e.unsubscribe?()=>e.unsubscribe():e}function v(s,u,r){const e=r[u]??(r[u]={store:null,source:c(void 0),unsubscribe:n});if(e.store!==s)if(e.unsubscribe(),e.store=s??null,s==null)e.source.v=void 0,e.unsubscribe=n;else{var t=!0;e.unsubscribe=g(s,b=>{t?e.source.v=b:a(e.source,b)}),t=!1}return o(e.source)}function m(){const s={};return i(()=>{for(var u in s)s[u].unsubscribe()}),s}const p=()=>{const s=f;return{page:{subscribe:s.page.subscribe},navigating:{subscribe:s.navigating.subscribe},updated:s.updated}},w={subscribe(s){return p().page.subscribe(s)}};export{v as a,w as p,m as s};
