import{a as g,t as m}from"../chunks/disclose-version.hHXjza9X.js";import{p as v,t as _,a as b,c as d,s as u,r as f,Q as y,u as $}from"../chunks/runtime.B40kIuYm.js";import{s as w}from"../chunks/snippet.BlUAN25S.js";import{s as j,a as O,p as S}from"../chunks/stores.jAWgkzgh.js";import{a as p}from"../chunks/attributes.faLUl4vZ.js";import{i as C}from"../chunks/lifecycle.BHVFZquU.js";import{b as s}from"../chunks/fetcher.CABHu9Eq.js";import{p as M}from"../chunks/plugins.svelte.D9-d_f1D.js";const N=!0,D=Object.freeze(Object.defineProperty({__proto__:null,prerender:N},Symbol.toStringTag,{value:"Module"}));var P=m('<nav class="flex flex-row justify-between bg-bg1 p-3"><a class="text-lg font-bold hover:bg-bg2 px-2 py-1 rounded transition duration-300">SCANEO</a> <div class="flex flex-row gap-6"><a class="hover:bg-bg2 px-2 py-1 rounded transition duration-300">Campaigns</a> <a class="hover:bg-bg2 px-2 py-1 rounded transition duration-300">Models</a> <a class="hover:bg-bg2 px-2 py-1 rounded transition duration-300">Plugins</a></div> <div class="flex flex-row gap-3"><a href="https://github.com/earthpulse/scaneo" target="_blank" class="hover:bg-bg2 px-2 py-1 rounded transition duration-300">Github</a></div></nav>');function U(c,n){v(n,!1),C();var t=P(),o=d(t),e=u(o,2),r=d(e),i=u(r,2),l=u(i,2);f(e),y(2),f(t),_(()=>{p(o,"href",s.url),p(r,"href",`${s.url??""}/campaigns`),p(i,"href",`${s.url??""}/models`),p(l,"href",`${s.url??""}/plugins`)}),g(c,t),b()}var k=m('<div class="min-h-screen flex flex-col"><!> <main class="flex flex-col flex-1"><!></main></div>');function F(c,n){v(n,!0);const t=j(),o=()=>O(S,"$page",t),e=(a,x)=>a.split(x)[0];$(()=>{let a=o().url.origin+o().url.pathname;a.includes("/campaigns")?a=e(a,"/campaigns"):a.includes("/models")?a=e(a,"/models"):a.includes("/plugins")&&(a=e(a,"/plugins")),a=a.replace(/\/+$/,""),s.url=a,s.api_url=a,M.retrieve()});var r=k(),i=d(r);U(i,{});var l=u(i,2),h=d(l);w(h,()=>n.children),f(l),f(r),g(c,r),b()}export{F as component,D as universal};
