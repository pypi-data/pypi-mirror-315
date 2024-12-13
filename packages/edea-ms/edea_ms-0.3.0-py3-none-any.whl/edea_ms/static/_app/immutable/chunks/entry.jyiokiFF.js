import{ap as M,aR as Ke,aW as wt,o as vt,ai as we,ah as bt}from"./index-client.rJPuloIY.js";new URL("sveltekit-internal://");function At(e,n){return e==="/"||n==="ignore"?e:n==="never"?e.endsWith("/")?e.slice(0,-1):e:n==="always"&&!e.endsWith("/")?e+"/":e}function St(e){return e.split("%25").map(decodeURI).join("%25")}function kt(e){for(const n in e)e[n]=decodeURIComponent(e[n]);return e}function ge({href:e}){return e.split("#")[0]}const Et=["href","pathname","search","toString","toJSON"];function Rt(e,n,t){const r=new URL(e);Object.defineProperty(r,"searchParams",{value:new Proxy(r.searchParams,{get(a,o){if(o==="get"||o==="getAll"||o==="has")return s=>(t(s),a[o](s));n();const i=Reflect.get(a,o);return typeof i=="function"?i.bind(a):i}}),enumerable:!0,configurable:!0});for(const a of Et)Object.defineProperty(r,a,{get(){return n(),e[a]},enumerable:!0,configurable:!0});return r}const It="/__data.json",Ut=".html__data.json";function xt(e){return e.endsWith(".html")?e.replace(/\.html$/,Ut):e.replace(/\/$/,"")+It}function Tt(...e){let n=5381;for(const t of e)if(typeof t=="string"){let r=t.length;for(;r;)n=n*33^t.charCodeAt(--r)}else if(ArrayBuffer.isView(t)){const r=new Uint8Array(t.buffer,t.byteOffset,t.byteLength);let a=r.length;for(;a;)n=n*33^r[--a]}else throw new TypeError("value must be a string or TypedArray");return(n>>>0).toString(36)}function Lt(e){const n=atob(e),t=new Uint8Array(n.length);for(let r=0;r<n.length;r++)t[r]=n.charCodeAt(r);return t.buffer}const We=window.fetch;window.fetch=(e,n)=>((e instanceof Request?e.method:(n==null?void 0:n.method)||"GET")!=="GET"&&H.delete(ke(e)),We(e,n));const H=new Map;function Ct(e,n){const t=ke(e,n),r=document.querySelector(t);if(r!=null&&r.textContent){let{body:a,...o}=JSON.parse(r.textContent);const i=r.getAttribute("data-ttl");return i&&H.set(t,{body:a,init:o,ttl:1e3*Number(i)}),r.getAttribute("data-b64")!==null&&(a=Lt(a)),Promise.resolve(new Response(a,o))}return window.fetch(e,n)}function Pt(e,n,t){if(H.size>0){const r=ke(e,t),a=H.get(r);if(a){if(performance.now()<a.ttl&&["default","force-cache","only-if-cached",void 0].includes(t==null?void 0:t.cache))return new Response(a.body,a.init);H.delete(r)}}return window.fetch(n,t)}function ke(e,n){let r=`script[data-sveltekit-fetched][data-url=${JSON.stringify(e instanceof Request?e.url:e)}]`;if(n!=null&&n.headers||n!=null&&n.body){const a=[];n.headers&&a.push([...new Headers(n.headers)].join(",")),n.body&&(typeof n.body=="string"||ArrayBuffer.isView(n.body))&&a.push(n.body),r+=`[data-hash="${Tt(...a)}"]`}return r}const Nt=/^(\[)?(\.\.\.)?(\w+)(?:=(\w+))?(\])?$/;function Ot(e){const n=[];return{pattern:e==="/"?/^\/$/:new RegExp(`^${$t(e).map(r=>{const a=/^\[\.\.\.(\w+)(?:=(\w+))?\]$/.exec(r);if(a)return n.push({name:a[1],matcher:a[2],optional:!1,rest:!0,chained:!0}),"(?:/(.*))?";const o=/^\[\[(\w+)(?:=(\w+))?\]\]$/.exec(r);if(o)return n.push({name:o[1],matcher:o[2],optional:!0,rest:!1,chained:!0}),"(?:/([^/]+))?";if(!r)return;const i=r.split(/\[(.+?)\](?!\])/);return"/"+i.map((c,l)=>{if(l%2){if(c.startsWith("x+"))return me(String.fromCharCode(parseInt(c.slice(2),16)));if(c.startsWith("u+"))return me(String.fromCharCode(...c.slice(2).split("-").map(f=>parseInt(f,16))));const d=Nt.exec(c),[,h,m,u,p]=d;return n.push({name:u,matcher:p,optional:!!h,rest:!!m,chained:m?l===1&&i[0]==="":!1}),m?"(.*?)":h?"([^/]*)?":"([^/]+?)"}return me(c)}).join("")}).join("")}/?$`),params:n}}function jt(e){return!/^\([^)]+\)$/.test(e)}function $t(e){return e.slice(1).split("/").filter(jt)}function Dt(e,n,t){const r={},a=e.slice(1),o=a.filter(s=>s!==void 0);let i=0;for(let s=0;s<n.length;s+=1){const c=n[s];let l=a[s-i];if(c.chained&&c.rest&&i&&(l=a.slice(s-i,s+1).filter(d=>d).join("/"),i=0),l===void 0){c.rest&&(r[c.name]="");continue}if(!c.matcher||t[c.matcher](l)){r[c.name]=l;const d=n[s+1],h=a[s+1];d&&!d.rest&&d.optional&&h&&c.chained&&(i=0),!d&&!h&&Object.keys(r).length===o.length&&(i=0);continue}if(c.optional&&c.chained){i++;continue}return}if(!i)return r}function me(e){return e.normalize().replace(/[[\]]/g,"\\$&").replace(/%/g,"%25").replace(/\//g,"%2[Ff]").replace(/\?/g,"%3[Ff]").replace(/#/g,"%23").replace(/[.*+?^${}()|\\]/g,"\\$&")}function Ft({nodes:e,server_loads:n,dictionary:t,matchers:r}){const a=new Set(n);return Object.entries(t).map(([s,[c,l,d]])=>{const{pattern:h,params:m}=Ot(s),u={id:s,exec:p=>{const f=h.exec(p);if(f)return Dt(f,m,r)},errors:[1,...d||[]].map(p=>e[p]),layouts:[0,...l||[]].map(i),leaf:o(c)};return u.errors.length=u.layouts.length=Math.max(u.errors.length,u.layouts.length),u});function o(s){const c=s<0;return c&&(s=~s),[c,e[s]]}function i(s){return s===void 0?s:[a.has(s),e[s]]}}function Ye(e,n=JSON.parse){try{return n(sessionStorage[e])}catch{}}function Oe(e,n,t=JSON.stringify){const r=t(n);try{sessionStorage[e]=r}catch{}}const O=[];function Vt(e,n){return{subscribe:oe(e,n).subscribe}}function oe(e,n=M){let t=null;const r=new Set;function a(s){if(wt(e,s)&&(e=s,t)){const c=!O.length;for(const l of r)l[1](),O.push(l,e);if(c){for(let l=0;l<O.length;l+=2)O[l][0](O[l+1]);O.length=0}}}function o(s){a(s(e))}function i(s,c=M){const l=[s,c];return r.add(l),r.size===1&&(t=n(a,o)||M),s(e),()=>{r.delete(l),r.size===0&&t&&(t(),t=null)}}return{set:a,update:o,subscribe:i}}function yn(e,n,t){const r=!Array.isArray(e),a=r?[e]:e;if(!a.every(Boolean))throw new Error("derived() expects stores as input, got a falsy value");const o=n.length<2;return Vt(t,(i,s)=>{let c=!1;const l=[];let d=0,h=M;const m=()=>{if(d)return;h();const p=n(r?l[0]:l,i,s);o?i(p):h=typeof p=="function"?p:M},u=a.map((p,f)=>Ke(p,g=>{l[f]=g,d&=~(1<<f),c&&m()},()=>{d|=1<<f}));return c=!0,m(),function(){vt(u),h(),c=!1}})}function _n(e){return{subscribe:e.subscribe.bind(e)}}function wn(e){let n;return Ke(e,t=>n=t)(),n}var Me;const x=((Me=globalThis.__sveltekit_16rrod3)==null?void 0:Me.base)??"";var He;const Bt=((He=globalThis.__sveltekit_16rrod3)==null?void 0:He.assets)??x,qt="1734024351534",ze="sveltekit:snapshot",Je="sveltekit:scroll",Xe="sveltekit:states",Gt="sveltekit:pageurl",D="sveltekit:history",W="sveltekit:navigation",Q={tap:1,hover:2,viewport:3,eager:4,off:-1,false:-1},X=location.origin;function Ze(e){if(e instanceof URL)return e;let n=document.baseURI;if(!n){const t=document.getElementsByTagName("base");n=t.length?t[0].href:document.URL}return new URL(e,n)}function Ee(){return{x:pageXOffset,y:pageYOffset}}function j(e,n){return e.getAttribute(`data-sveltekit-${n}`)}const je={...Q,"":Q.hover};function Qe(e){let n=e.assignedSlot??e.parentNode;return(n==null?void 0:n.nodeType)===11&&(n=n.host),n}function et(e,n){for(;e&&e!==n;){if(e.nodeName.toUpperCase()==="A"&&e.hasAttribute("href"))return e;e=Qe(e)}}function ve(e,n){let t;try{t=new URL(e instanceof SVGAElement?e.href.baseVal:e.href,document.baseURI)}catch{}const r=e instanceof SVGAElement?e.target.baseVal:e.target,a=!t||!!r||se(t,n)||(e.getAttribute("rel")||"").split(/\s+/).includes("external"),o=(t==null?void 0:t.origin)===X&&e.hasAttribute("download");return{url:t,external:a,target:r,download:o}}function ee(e){let n=null,t=null,r=null,a=null,o=null,i=null,s=e;for(;s&&s!==document.documentElement;)r===null&&(r=j(s,"preload-code")),a===null&&(a=j(s,"preload-data")),n===null&&(n=j(s,"keepfocus")),t===null&&(t=j(s,"noscroll")),o===null&&(o=j(s,"reload")),i===null&&(i=j(s,"replacestate")),s=Qe(s);function c(l){switch(l){case"":case"true":return!0;case"off":case"false":return!1;default:return}}return{preload_code:je[r??"off"],preload_data:je[a??"off"],keepfocus:c(n),noscroll:c(t),reload:c(o),replace_state:c(i)}}function $e(e){const n=oe(e);let t=!0;function r(){t=!0,n.update(i=>i)}function a(i){t=!1,n.set(i)}function o(i){let s;return n.subscribe(c=>{(s===void 0||t&&c!==s)&&i(s=c)})}return{notify:r,set:a,subscribe:o}}function Mt(){const{set:e,subscribe:n}=oe(!1);let t;async function r(){clearTimeout(t);try{const a=await fetch(`${Bt}/_app/version.json`,{headers:{pragma:"no-cache","cache-control":"no-cache"}});if(!a.ok)return!1;const i=(await a.json()).version!==qt;return i&&(e(!0),clearTimeout(t)),i}catch{return!1}}return{subscribe:n,check:r}}function se(e,n){return e.origin!==X||!e.pathname.startsWith(n)}function vn(e){const n=new DataView(e);let t="";for(let r=0;r<e.byteLength;r++)t+=String.fromCharCode(n.getUint8(r));return Kt(t)}function De(e){const n=Ht(e),t=new ArrayBuffer(n.length),r=new DataView(t);for(let a=0;a<t.byteLength;a++)r.setUint8(a,n.charCodeAt(a));return t}const tt="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";function Ht(e){e.length%4===0&&(e=e.replace(/==?$/,""));let n="",t=0,r=0;for(let a=0;a<e.length;a++)t<<=6,t|=tt.indexOf(e[a]),r+=6,r===24&&(n+=String.fromCharCode((t&16711680)>>16),n+=String.fromCharCode((t&65280)>>8),n+=String.fromCharCode(t&255),t=r=0);return r===12?(t>>=4,n+=String.fromCharCode(t)):r===18&&(t>>=2,n+=String.fromCharCode((t&65280)>>8),n+=String.fromCharCode(t&255)),n}function Kt(e){let n="";for(let t=0;t<e.length;t+=3){const r=[void 0,void 0,void 0,void 0];r[0]=e.charCodeAt(t)>>2,r[1]=(e.charCodeAt(t)&3)<<4,e.length>t+1&&(r[1]|=e.charCodeAt(t+1)>>4,r[2]=(e.charCodeAt(t+1)&15)<<2),e.length>t+2&&(r[2]|=e.charCodeAt(t+2)>>6,r[3]=e.charCodeAt(t+2)&63);for(let a=0;a<r.length;a++)typeof r[a]>"u"?n+="=":n+=tt[r[a]]}return n}const Wt=-1,Yt=-2,zt=-3,Jt=-4,Xt=-5,Zt=-6;function bn(e,n){return nt(JSON.parse(e),n)}function nt(e,n){if(typeof e=="number")return a(e,!0);if(!Array.isArray(e)||e.length===0)throw new Error("Invalid input");const t=e,r=Array(t.length);function a(o,i=!1){if(o===Wt)return;if(o===zt)return NaN;if(o===Jt)return 1/0;if(o===Xt)return-1/0;if(o===Zt)return-0;if(i)throw new Error("Invalid input");if(o in r)return r[o];const s=t[o];if(!s||typeof s!="object")r[o]=s;else if(Array.isArray(s))if(typeof s[0]=="string"){const c=s[0],l=n==null?void 0:n[c];if(l)return r[o]=l(a(s[1]));switch(c){case"Date":r[o]=new Date(s[1]);break;case"Set":const d=new Set;r[o]=d;for(let u=1;u<s.length;u+=1)d.add(a(s[u]));break;case"Map":const h=new Map;r[o]=h;for(let u=1;u<s.length;u+=2)h.set(a(s[u]),a(s[u+1]));break;case"RegExp":r[o]=new RegExp(s[1],s[2]);break;case"Object":r[o]=Object(s[1]);break;case"BigInt":r[o]=BigInt(s[1]);break;case"null":const m=Object.create(null);r[o]=m;for(let u=1;u<s.length;u+=2)m[s[u]]=a(s[u+1]);break;case"Int8Array":case"Uint8Array":case"Uint8ClampedArray":case"Int16Array":case"Uint16Array":case"Int32Array":case"Uint32Array":case"Float32Array":case"Float64Array":case"BigInt64Array":case"BigUint64Array":{const u=globalThis[c],p=s[1],f=De(p),g=new u(f);r[o]=g;break}case"ArrayBuffer":{const u=s[1],p=De(u);r[o]=p;break}default:throw new Error(`Unknown type ${c}`)}}else{const c=new Array(s.length);r[o]=c;for(let l=0;l<s.length;l+=1){const d=s[l];d!==Yt&&(c[l]=a(d))}}else{const c={};r[o]=c;for(const l in s){const d=s[l];c[l]=a(d)}}return r[o]}return a(0)}const rt=new Set(["load","prerender","csr","ssr","trailingSlash","config"]);[...rt];const Qt=new Set([...rt]);[...Qt];function en(e){return e.filter(n=>n!=null)}class ie{constructor(n,t){this.status=n,typeof t=="string"?this.body={message:t}:t?this.body=t:this.body={message:`Error: ${n}`}}toString(){return JSON.stringify(this.body)}}class at{constructor(n,t){this.status=n,this.location=t}}class Re extends Error{constructor(n,t,r){super(r),this.status=n,this.text=t}}class An{constructor(n,t){this.status=n,this.data=t}}const tn="x-sveltekit-invalidated",nn="x-sveltekit-trailing-slash";function te(e){return e instanceof ie||e instanceof Re?e.status:500}function rn(e){return e instanceof Re?e.text:"Internal Error"}const an=new Set(["icon","shortcut icon","apple-touch-icon"]),N=Ye(Je)??{},Y=Ye(ze)??{},L={url:$e({}),page:$e({}),navigating:oe(null),updated:Mt()};function Ie(e){N[e]=Ee()}function on(e,n){let t=e+1;for(;N[t];)delete N[t],t+=1;for(t=n+1;Y[t];)delete Y[t],t+=1}function V(e){return location.href=e.href,new Promise(()=>{})}async function ot(){if("serviceWorker"in navigator){const e=await navigator.serviceWorker.getRegistration(x||"/");e&&await e.update()}}function Fe(){}let ce,be,ne,T,Ae,q;const st=[],re=[];let I=null;const Ue=[],sn=[];let $=[],_={branch:[],error:null,url:null},xe=!1,ae=!1,Ve=!0,z=!1,G=!1,it=!1,le=!1,P,E,U,R,B;const K=new Set;let ye;async function Sn(e,n,t){var a,o,i,s;document.URL!==location.href&&(location.href=location.href),q=e,await((o=(a=e.hooks).init)==null?void 0:o.call(a)),ce=Ft(e),T=document.documentElement,Ae=n,be=e.nodes[0],ne=e.nodes[1],be(),ne(),E=(i=history.state)==null?void 0:i[D],U=(s=history.state)==null?void 0:s[W],E||(E=U=Date.now(),history.replaceState({...history.state,[D]:E,[W]:U},""));const r=N[E];r&&(history.scrollRestoration="manual",scrollTo(r.x,r.y)),t?await gn(Ae,t):hn(location.href,{replaceState:!0}),pn()}async function cn(){if(await(ye||(ye=Promise.resolve())),!ye)return;ye=null;const e=de(_.url,!0);I=null;const n=B={},t=e&&await Ce(e);if(!(!t||n!==B)){if(t.type==="redirect")return fe(new URL(t.location,_.url).href,{},1,n);t.props.page&&(R=t.props.page),_=t.state,ct(),P.$set(t.props)}}function ct(){st.length=0,le=!1}function lt(e){re.some(n=>n==null?void 0:n.snapshot)&&(Y[e]=re.map(n=>{var t;return(t=n==null?void 0:n.snapshot)==null?void 0:t.capture()}))}function ft(e){var n;(n=Y[e])==null||n.forEach((t,r)=>{var a,o;(o=(a=re[r])==null?void 0:a.snapshot)==null||o.restore(t)})}function Be(){Ie(E),Oe(Je,N),lt(U),Oe(ze,Y)}async function fe(e,n,t,r){return Z({type:"goto",url:Ze(e),keepfocus:n.keepFocus,noscroll:n.noScroll,replace_state:n.replaceState,state:n.state,redirect_count:t,nav_token:r,accept:()=>{n.invalidateAll&&(le=!0)}})}async function ln(e){if(e.id!==(I==null?void 0:I.id)){const n={};K.add(n),I={id:e.id,token:n,promise:Ce({...e,preload:n}).then(t=>(K.delete(n),t.type==="loaded"&&t.state.error&&(I=null),t))}}return I.promise}async function _e(e){const n=ce.find(t=>t.exec(ht(e)));n&&await Promise.all([...n.layouts,n.leaf].map(t=>t==null?void 0:t[1]()))}function ut(e,n,t){var o;_=e.state;const r=document.querySelector("style[data-sveltekit]");r&&r.remove(),R=e.props.page,P=new q.root({target:n,props:{...e.props,stores:L,components:re},hydrate:t,sync:!1}),ft(U);const a={from:null,to:{params:_.params,route:{id:((o=_.route)==null?void 0:o.id)??null},url:new URL(location.href)},willUnload:!1,type:"enter",complete:Promise.resolve()};$.forEach(i=>i(a)),ae=!0}function J({url:e,params:n,branch:t,status:r,error:a,route:o,form:i}){let s="never";if(x&&(e.pathname===x||e.pathname===x+"/"))s="always";else for(const u of t)(u==null?void 0:u.slash)!==void 0&&(s=u.slash);e.pathname=At(e.pathname,s),e.search=e.search;const c={type:"loaded",state:{url:e,params:n,branch:t,error:a,route:o},props:{constructors:en(t).map(u=>u.node.component),page:R}};i!==void 0&&(c.props.form=i);let l={},d=!R,h=0;for(let u=0;u<Math.max(t.length,_.branch.length);u+=1){const p=t[u],f=_.branch[u];(p==null?void 0:p.data)!==(f==null?void 0:f.data)&&(d=!0),p&&(l={...l,...p.data},d&&(c.props[`data_${h}`]=l),h+=1)}return(!_.url||e.href!==_.url.href||_.error!==a||i!==void 0&&i!==R.form||d)&&(c.props.page={error:a,params:n,route:{id:(o==null?void 0:o.id)??null},state:{},status:r,url:new URL(e),form:i??null,data:d?l:R.data}),c}async function Te({loader:e,parent:n,url:t,params:r,route:a,server_data_node:o}){var d,h,m;let i=null,s=!0;const c={dependencies:new Set,params:new Set,parent:!1,route:!1,url:!1,search_params:new Set},l=await e();if((d=l.universal)!=null&&d.load){let u=function(...f){for(const g of f){const{href:b}=new URL(g,t);c.dependencies.add(b)}};const p={route:new Proxy(a,{get:(f,g)=>(s&&(c.route=!0),f[g])}),params:new Proxy(r,{get:(f,g)=>(s&&c.params.add(g),f[g])}),data:(o==null?void 0:o.data)??null,url:Rt(t,()=>{s&&(c.url=!0)},f=>{s&&c.search_params.add(f)}),async fetch(f,g){let b;f instanceof Request?(b=f.url,g={body:f.method==="GET"||f.method==="HEAD"?void 0:await f.blob(),cache:f.cache,credentials:f.credentials,headers:[...f.headers].length?f.headers:void 0,integrity:f.integrity,keepalive:f.keepalive,method:f.method,mode:f.mode,redirect:f.redirect,referrer:f.referrer,referrerPolicy:f.referrerPolicy,signal:f.signal,...g}):b=f;const S=new URL(b,t);return s&&u(S.href),S.origin===t.origin&&(b=S.href.slice(t.origin.length)),ae?Pt(b,S.href,g):Ct(b,g)},setHeaders:()=>{},depends:u,parent(){return s&&(c.parent=!0),n()},untrack(f){s=!1;try{return f()}finally{s=!0}}};i=await l.universal.load.call(null,p)??null}return{node:l,loader:e,server:o,universal:(h=l.universal)!=null&&h.load?{type:"data",data:i,uses:c}:null,data:i??(o==null?void 0:o.data)??null,slash:((m=l.universal)==null?void 0:m.trailingSlash)??(o==null?void 0:o.slash)}}function qe(e,n,t,r,a,o){if(le)return!0;if(!a)return!1;if(a.parent&&e||a.route&&n||a.url&&t)return!0;for(const i of a.search_params)if(r.has(i))return!0;for(const i of a.params)if(o[i]!==_.params[i])return!0;for(const i of a.dependencies)if(st.some(s=>s(new URL(i))))return!0;return!1}function Le(e,n){return(e==null?void 0:e.type)==="data"?e:(e==null?void 0:e.type)==="skip"?n??null:null}function fn(e,n){if(!e)return new Set(n.searchParams.keys());const t=new Set([...e.searchParams.keys(),...n.searchParams.keys()]);for(const r of t){const a=e.searchParams.getAll(r),o=n.searchParams.getAll(r);a.every(i=>o.includes(i))&&o.every(i=>a.includes(i))&&t.delete(r)}return t}function Ge({error:e,url:n,route:t,params:r}){return{type:"loaded",state:{error:e,url:n,route:t,params:r,branch:[]},props:{page:R,constructors:[]}}}async function Ce({id:e,invalidating:n,url:t,params:r,route:a,preload:o}){if((I==null?void 0:I.id)===e)return K.delete(I.token),I.promise;const{errors:i,layouts:s,leaf:c}=a,l=[...s,c];i.forEach(y=>y==null?void 0:y().catch(()=>{})),l.forEach(y=>y==null?void 0:y[1]().catch(()=>{}));let d=null;const h=_.url?e!==_.url.pathname+_.url.search:!1,m=_.route?a.id!==_.route.id:!1,u=fn(_.url,t);let p=!1;const f=l.map((y,v)=>{var C;const A=_.branch[v],k=!!(y!=null&&y[0])&&((A==null?void 0:A.loader)!==y[1]||qe(p,m,h,u,(C=A.server)==null?void 0:C.uses,r));return k&&(p=!0),k});if(f.some(Boolean)){try{d=await mt(t,f)}catch(y){const v=await F(y,{url:t,params:r,route:{id:e}});return K.has(o)?Ge({error:v,url:t,params:r,route:a}):ue({status:te(y),error:v,url:t,route:a})}if(d.type==="redirect")return d}const g=d==null?void 0:d.nodes;let b=!1;const S=l.map(async(y,v)=>{var he;if(!y)return;const A=_.branch[v],k=g==null?void 0:g[v];if((!k||k.type==="skip")&&y[1]===(A==null?void 0:A.loader)&&!qe(b,m,h,u,(he=A.universal)==null?void 0:he.uses,r))return A;if(b=!0,(k==null?void 0:k.type)==="error")throw k;return Te({loader:y[1],url:t,params:r,route:a,parent:async()=>{var Ne;const Pe={};for(let pe=0;pe<v;pe+=1)Object.assign(Pe,(Ne=await S[pe])==null?void 0:Ne.data);return Pe},server_data_node:Le(k===void 0&&y[0]?{type:"skip"}:k??null,y[0]?A==null?void 0:A.server:void 0)})});for(const y of S)y.catch(()=>{});const w=[];for(let y=0;y<l.length;y+=1)if(l[y])try{w.push(await S[y])}catch(v){if(v instanceof at)return{type:"redirect",location:v.location};if(K.has(o))return Ge({error:await F(v,{params:r,url:t,route:{id:a.id}}),url:t,params:r,route:a});let A=te(v),k;if(g!=null&&g.includes(v))A=v.status??A,k=v.error;else if(v instanceof ie)k=v.body;else{if(await L.updated.check())return await ot(),await V(t);k=await F(v,{params:r,url:t,route:{id:a.id}})}const C=await dt(y,w,i);return C?J({url:t,params:r,branch:w.slice(0,C.idx).concat(C.node),status:A,error:k,route:a}):await gt(t,{id:a.id},k,A)}else w.push(void 0);return J({url:t,params:r,branch:w,status:200,error:null,route:a,form:n?void 0:null})}async function dt(e,n,t){for(;e--;)if(t[e]){let r=e;for(;!n[r];)r-=1;try{return{idx:r+1,node:{node:await t[e](),loader:t[e],data:{},server:null,universal:null}}}catch{continue}}}async function ue({status:e,error:n,url:t,route:r}){const a={};let o=null;if(q.server_loads[0]===0)try{const l=await mt(t,[!0]);if(l.type!=="data"||l.nodes[0]&&l.nodes[0].type!=="data")throw 0;o=l.nodes[0]??null}catch{(t.origin!==X||t.pathname!==location.pathname||xe)&&await V(t)}const s=await Te({loader:be,url:t,params:a,route:r,parent:()=>Promise.resolve({}),server_data_node:Le(o)}),c={node:await ne(),loader:ne,universal:null,server:null,data:null};return J({url:t,params:a,branch:[s,c],status:e,error:n,route:null})}function de(e,n){if(!e||se(e,x))return;let t;try{t=q.hooks.reroute({url:new URL(e)})??e.pathname}catch{return}const r=ht(t);for(const a of ce){const o=a.exec(r);if(o)return{id:e.pathname+e.search,invalidating:n,route:a,params:kt(o),url:e}}}function ht(e){return St(e.slice(x.length)||"/")}function pt({url:e,type:n,intent:t,delta:r}){let a=!1;const o=_t(_,t,e,n);r!==void 0&&(o.navigation.delta=r);const i={...o.navigation,cancel:()=>{a=!0,o.reject(new Error("navigation cancelled"))}};return z||Ue.forEach(s=>s(i)),a?null:o}async function Z({type:e,url:n,popped:t,keepfocus:r,noscroll:a,replace_state:o,state:i={},redirect_count:s=0,nav_token:c={},accept:l=Fe,block:d=Fe}){const h=de(n,!1),m=pt({url:n,type:e,delta:t==null?void 0:t.delta,intent:h});if(!m){d();return}const u=E,p=U;l(),z=!0,ae&&L.navigating.set(m.navigation),B=c;let f=h&&await Ce(h);if(!f){if(se(n,x))return await V(n);f=await gt(n,{id:null},await F(new Re(404,"Not Found",`Not found: ${n.pathname}`),{url:n,params:{},route:{id:null}}),404)}if(n=(h==null?void 0:h.url)||n,B!==c)return m.reject(new Error("navigation aborted")),!1;if(f.type==="redirect")if(s>=20)f=await ue({status:500,error:await F(new Error("Redirect loop"),{url:n,params:{},route:{id:null}}),url:n,route:{id:null}});else return fe(new URL(f.location,n).href,{},s+1,c),!1;else f.props.page.status>=400&&await L.updated.check()&&(await ot(),await V(n));if(ct(),Ie(u),lt(p),f.props.page.url.pathname!==n.pathname&&(n.pathname=f.props.page.url.pathname),i=t?t.state:i,!t){const w=o?0:1,y={[D]:E+=w,[W]:U+=w,[Xe]:i};(o?history.replaceState:history.pushState).call(history,y,"",n),o||on(E,U)}if(I=null,f.props.page.state=i,ae){_=f.state,f.props.page&&(f.props.page.url=n);const w=(await Promise.all(sn.map(y=>y(m.navigation)))).filter(y=>typeof y=="function");if(w.length>0){let y=function(){$=$.filter(v=>!w.includes(v))};w.push(y),$.push(...w)}P.$set(f.props),it=!0}else ut(f,Ae,!1);const{activeElement:g}=document;await we();const b=t?t.scroll:a?Ee():null;if(Ve){const w=n.hash&&document.getElementById(decodeURIComponent(n.hash.slice(1)));b?scrollTo(b.x,b.y):w?w.scrollIntoView():scrollTo(0,0)}const S=document.activeElement!==g&&document.activeElement!==document.body;!r&&!S&&Se(),Ve=!0,f.props.page&&(R=f.props.page),z=!1,e==="popstate"&&ft(U),m.fulfil(void 0),$.forEach(w=>w(m.navigation)),L.navigating.set(null)}async function gt(e,n,t,r){return e.origin===X&&e.pathname===location.pathname&&!xe?await ue({status:r,error:t,url:e,route:n}):await V(e)}function un(){let e;T.addEventListener("mousemove",o=>{const i=o.target;clearTimeout(e),e=setTimeout(()=>{r(i,2)},20)});function n(o){o.defaultPrevented||r(o.composedPath()[0],1)}T.addEventListener("mousedown",n),T.addEventListener("touchstart",n,{passive:!0});const t=new IntersectionObserver(o=>{for(const i of o)i.isIntersecting&&(_e(i.target.href),t.unobserve(i.target))},{threshold:0});function r(o,i){const s=et(o,T);if(!s)return;const{url:c,external:l,download:d}=ve(s,x);if(l||d)return;const h=ee(s),m=c&&_.url.pathname+_.url.search===c.pathname+c.search;if(!h.reload&&!m)if(i<=h.preload_data){const u=de(c,!1);u&&ln(u)}else i<=h.preload_code&&_e(c.pathname)}function a(){t.disconnect();for(const o of T.querySelectorAll("a")){const{url:i,external:s,download:c}=ve(o,x);if(s||c)continue;const l=ee(o);l.reload||(l.preload_code===Q.viewport&&t.observe(o),l.preload_code===Q.eager&&_e(i.pathname))}}$.push(a),a()}function F(e,n){if(e instanceof ie)return e.body;const t=te(e),r=rn(e);return q.hooks.handleError({error:e,event:n,status:t,message:r})??{message:r}}function dn(e,n){bt(()=>(e.push(n),()=>{const t=e.indexOf(n);e.splice(t,1)}))}function kn(e){dn(Ue,e)}function hn(e,n={}){return e=Ze(e),e.origin!==X?Promise.reject(new Error("goto: invalid URL")):fe(e,n,0)}function En(){return le=!0,cn()}async function Rn(e){if(e.type==="error"){const n=new URL(location.href),{branch:t,route:r}=_;if(!r)return;const a=await dt(_.branch.length,t,r.errors);if(a){const o=J({url:n,params:_.params,branch:t.slice(0,a.idx).concat(a.node),status:e.status??500,error:e.error,route:r});_=o.state,P.$set(o.props),we().then(Se)}}else e.type==="redirect"?fe(e.location,{invalidateAll:!0},0):(P.$set({form:null,page:{...R,form:e.data,status:e.status}}),await we(),P.$set({form:e.data}),e.type==="success"&&Se())}function pn(){var n;history.scrollRestoration="manual",addEventListener("beforeunload",t=>{let r=!1;if(Be(),!z){const a=_t(_,void 0,null,"leave"),o={...a.navigation,cancel:()=>{r=!0,a.reject(new Error("navigation cancelled"))}};Ue.forEach(i=>i(o))}r?(t.preventDefault(),t.returnValue=""):history.scrollRestoration="auto"}),addEventListener("visibilitychange",()=>{document.visibilityState==="hidden"&&Be()}),(n=navigator.connection)!=null&&n.saveData||un(),T.addEventListener("click",async t=>{if(t.button||t.which!==1||t.metaKey||t.ctrlKey||t.shiftKey||t.altKey||t.defaultPrevented)return;const r=et(t.composedPath()[0],T);if(!r)return;const{url:a,external:o,target:i,download:s}=ve(r,x);if(!a)return;if(i==="_parent"||i==="_top"){if(window.parent!==window)return}else if(i&&i!=="_self")return;const c=ee(r);if(!(r instanceof SVGAElement)&&a.protocol!==location.protocol&&!(a.protocol==="https:"||a.protocol==="http:")||s)return;const[d,h]=a.href.split("#"),m=d===ge(location);if(o||c.reload&&(!m||!h)){pt({url:a,type:"link"})?z=!0:t.preventDefault();return}if(h!==void 0&&m){const[,u]=_.url.href.split("#");if(u===h){if(t.preventDefault(),h===""||h==="top"&&r.ownerDocument.getElementById("top")===null)window.scrollTo({top:0});else{const p=r.ownerDocument.getElementById(decodeURIComponent(h));p&&(p.scrollIntoView(),p.focus())}return}if(G=!0,Ie(E),e(a),!c.replace_state)return;G=!1}t.preventDefault(),await new Promise(u=>{requestAnimationFrame(()=>{setTimeout(u,0)}),setTimeout(u,100)}),Z({type:"link",url:a,keepfocus:c.keepfocus,noscroll:c.noscroll,replace_state:c.replace_state??a.href===location.href})}),T.addEventListener("submit",t=>{if(t.defaultPrevented)return;const r=HTMLFormElement.prototype.cloneNode.call(t.target),a=t.submitter;if(((a==null?void 0:a.formTarget)||r.target)==="_blank"||((a==null?void 0:a.formMethod)||r.method)!=="get")return;const s=new URL((a==null?void 0:a.hasAttribute("formaction"))&&(a==null?void 0:a.formAction)||r.action);if(se(s,x))return;const c=t.target,l=ee(c);if(l.reload)return;t.preventDefault(),t.stopPropagation();const d=new FormData(c),h=a==null?void 0:a.getAttribute("name");h&&d.append(h,(a==null?void 0:a.getAttribute("value"))??""),s.search=new URLSearchParams(d).toString(),Z({type:"form",url:s,keepfocus:l.keepfocus,noscroll:l.noscroll,replace_state:l.replace_state??s.href===location.href})}),addEventListener("popstate",async t=>{var r;if((r=t.state)!=null&&r[D]){const a=t.state[D];if(B={},a===E)return;const o=N[a],i=t.state[Xe]??{},s=new URL(t.state[Gt]??location.href),c=t.state[W],l=ge(location)===ge(_.url);if(c===U&&(it||l)){e(s),N[E]=Ee(),o&&scrollTo(o.x,o.y),i!==R.state&&(R={...R,state:i},P.$set({page:R})),E=a;return}const h=a-E;await Z({type:"popstate",url:s,popped:{state:i,scroll:o,delta:h},accept:()=>{E=a,U=c},block:()=>{history.go(-h)},nav_token:B})}else if(!G){const a=new URL(location.href);e(a)}}),addEventListener("hashchange",()=>{G&&(G=!1,history.replaceState({...history.state,[D]:++E,[W]:U},"",location.href))});for(const t of document.querySelectorAll("link"))an.has(t.rel)&&(t.href=t.href);addEventListener("pageshow",t=>{t.persisted&&L.navigating.set(null)});function e(t){_.url=t,L.page.set({...R,url:t}),L.page.notify()}}async function gn(e,{status:n=200,error:t,node_ids:r,params:a,route:o,data:i,form:s}){xe=!0;const c=new URL(location.href);({params:a={},route:o={id:null}}=de(c,!1)||{});let l,d=!0;try{const h=r.map(async(p,f)=>{const g=i[f];return g!=null&&g.uses&&(g.uses=yt(g.uses)),Te({loader:q.nodes[p],url:c,params:a,route:o,parent:async()=>{const b={};for(let S=0;S<f;S+=1)Object.assign(b,(await h[S]).data);return b},server_data_node:Le(g)})}),m=await Promise.all(h),u=ce.find(({id:p})=>p===o.id);if(u){const p=u.layouts;for(let f=0;f<p.length;f++)p[f]||m.splice(f,0,void 0)}l=J({url:c,params:a,branch:m,status:n,error:t,form:s,route:u??null})}catch(h){if(h instanceof at){await V(new URL(h.location,location.href));return}l=await ue({status:te(h),error:await F(h,{url:c,params:a,route:o}),url:c,route:o}),e.textContent="",d=!1}l.props.page&&(l.props.page.state={}),ut(l,e,d)}async function mt(e,n){var a;const t=new URL(e);t.pathname=xt(e.pathname),e.pathname.endsWith("/")&&t.searchParams.append(nn,"1"),t.searchParams.append(tn,n.map(o=>o?"1":"0").join(""));const r=await We(t.href);if(!r.ok){let o;throw(a=r.headers.get("content-type"))!=null&&a.includes("application/json")?o=await r.json():r.status===404?o="Not Found":r.status===500&&(o="Internal Error"),new ie(r.status,o)}return new Promise(async o=>{var h;const i=new Map,s=r.body.getReader(),c=new TextDecoder;function l(m){return nt(m,{Promise:u=>new Promise((p,f)=>{i.set(u,{fulfil:p,reject:f})})})}let d="";for(;;){const{done:m,value:u}=await s.read();if(m&&!d)break;for(d+=!u&&d?`
`:c.decode(u,{stream:!0});;){const p=d.indexOf(`
`);if(p===-1)break;const f=JSON.parse(d.slice(0,p));if(d=d.slice(p+1),f.type==="redirect")return o(f);if(f.type==="data")(h=f.nodes)==null||h.forEach(g=>{(g==null?void 0:g.type)==="data"&&(g.uses=yt(g.uses),g.data=l(g.data))}),o(f);else if(f.type==="chunk"){const{id:g,data:b,error:S}=f,w=i.get(g);i.delete(g),S?w.reject(l(S)):w.fulfil(l(b))}}}})}function yt(e){return{dependencies:new Set((e==null?void 0:e.dependencies)??[]),params:new Set((e==null?void 0:e.params)??[]),parent:!!(e!=null&&e.parent),route:!!(e!=null&&e.route),url:!!(e!=null&&e.url),search_params:new Set((e==null?void 0:e.search_params)??[])}}function Se(){const e=document.querySelector("[autofocus]");if(e)e.focus();else{const n=document.body,t=n.getAttribute("tabindex");n.tabIndex=-1,n.focus({preventScroll:!0,focusVisible:!1}),t!==null?n.setAttribute("tabindex",t):n.removeAttribute("tabindex");const r=getSelection();if(r&&r.type!=="None"){const a=[];for(let o=0;o<r.rangeCount;o+=1)a.push(r.getRangeAt(o));setTimeout(()=>{if(r.rangeCount===a.length){for(let o=0;o<r.rangeCount;o+=1){const i=a[o],s=r.getRangeAt(o);if(i.commonAncestorContainer!==s.commonAncestorContainer||i.startContainer!==s.startContainer||i.endContainer!==s.endContainer||i.startOffset!==s.startOffset||i.endOffset!==s.endOffset)return}r.removeAllRanges()}})}}}function _t(e,n,t,r){var c,l;let a,o;const i=new Promise((d,h)=>{a=d,o=h});return i.catch(()=>{}),{navigation:{from:{params:e.params,route:{id:((c=e.route)==null?void 0:c.id)??null},url:e.url},to:t&&{params:(n==null?void 0:n.params)??null,route:{id:((l=n==null?void 0:n.route)==null?void 0:l.id)??null},url:t},willUnload:!n,type:r,complete:i},fulfil:a,reject:o}}export{An as A,ie as H,zt as N,Jt as P,Wt as U,wn as a,Xt as b,Zt as c,Yt as d,vn as e,Rn as f,hn as g,yn as h,En as i,kn as j,_n as k,Sn as l,bn as p,Vt as r,L as s,oe as w};
