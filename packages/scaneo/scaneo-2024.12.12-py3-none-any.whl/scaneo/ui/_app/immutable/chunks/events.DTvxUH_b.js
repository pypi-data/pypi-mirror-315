import{am as b,a1 as y,an as v,V as k}from"./runtime.B40kIuYm.js";const E=new Set,L=new Set;function S(r,a,e,n){function i(t){if(n.capture||q.call(a,t),!t.cancelBubble)return e.call(this,t)}return r.startsWith("pointer")||r.startsWith("touch")||r==="wheel"?y(()=>{a.addEventListener(r,i,n)}):a.addEventListener(r,i,n),i}function O(r,a,e,n,i){var t={capture:n,passive:i},o=S(r,a,e,t);(a===document.body||a===window||a===document)&&b(()=>{a.removeEventListener(r,o,t)})}function T(r){for(var a=0;a<r.length;a++)E.add(r[a]);for(var e of L)e(r)}function q(r){var _;var a=this,e=a.ownerDocument,n=r.type,i=((_=r.composedPath)==null?void 0:_.call(r))||[],t=i[0]||r.target,o=0,d=r.__root;if(d){var f=i.indexOf(d);if(f!==-1&&(a===document||a===window)){r.__root=a;return}var h=i.indexOf(a);if(h===-1)return;f<=h&&(o=f)}if(t=i[o]||r.target,t!==a){v(r,"currentTarget",{configurable:!0,get(){return t||e}});try{for(var l,p=[];t!==null;){var s=t.assignedSlot||t.parentNode||t.host||null;try{var u=t["__"+n];if(u!==void 0&&!t.disabled)if(k(u)){var[g,...w]=u;g.apply(t,[r,...w])}else u.call(t,r)}catch(c){l?p.push(c):l=c}if(r.cancelBubble||s===a||s===null)break;t=s}if(l){for(let c of p)queueMicrotask(()=>{throw c});throw l}}finally{r.__root=a,delete r.currentTarget}}}export{E as a,T as d,O as e,q as h,L as r};
