var Zt=Object.defineProperty;var Xt=(e,r,i)=>r in e?Zt(e,r,{enumerable:!0,configurable:!0,writable:!0,value:i}):e[r]=i;var ft=(e,r,i)=>Xt(e,typeof r!="symbol"?r+"":r,i);import{f as Kt,e as lt}from"./index.DDgd0KB9.js";import"./disclose-version.R4vLOQNQ.js";import"./legacy.2nIxhB3F.js";import{U as At,N as Qt,P as en,b as tn,c as Et,e as ct,d as nn,p as rn,i as St,f as Oe,h as Ze,a as ye,w as J,j as sn,k as Ce,g as an}from"./entry.jyiokiFF.js";import{ai as He,aS as Me}from"./index-client.rJPuloIY.js";import{p as be,n as dt}from"./stores.BB7RgSSW.js";const on=!0;class Ve extends Error{constructor(r,i){super(r),this.name="DevalueError",this.path=i.join("")}}function pt(e){return Object(e)!==e}const un=Object.getOwnPropertyNames(Object.prototype).sort().join("\0");function fn(e){const r=Object.getPrototypeOf(e);return r===Object.prototype||r===null||Object.getOwnPropertyNames(r).sort().join("\0")===un}function ln(e){return Object.prototype.toString.call(e).slice(8,-1)}function cn(e){switch(e){case'"':return'\\"';case"<":return"\\u003C";case"\\":return"\\\\";case`
`:return"\\n";case"\r":return"\\r";case"	":return"\\t";case"\b":return"\\b";case"\f":return"\\f";case"\u2028":return"\\u2028";case"\u2029":return"\\u2029";default:return e<" "?`\\u${e.charCodeAt(0).toString(16).padStart(4,"0")}`:""}}function de(e){let r="",i=0;const t=e.length;for(let o=0;o<t;o+=1){const u=e[o],a=cn(u);a&&(r+=e.slice(i,o)+a,i=o+1)}return`"${i===0?e:r+e.slice(i)}"`}function dn(e){return Object.getOwnPropertySymbols(e).filter(r=>Object.getOwnPropertyDescriptor(e,r).enumerable)}const pn=/^[a-zA-Z_$][a-zA-Z_$0-9]*$/;function mt(e){return pn.test(e)?"."+e:"["+JSON.stringify(e)+"]"}function mn(e,r){const i=[],t=new Map,o=[],u=[];let a=0;function c(d){if(typeof d=="function")throw new Ve("Cannot stringify a function",u);if(t.has(d))return t.get(d);if(d===void 0)return At;if(Number.isNaN(d))return Qt;if(d===1/0)return en;if(d===-1/0)return tn;if(d===0&&1/d<0)return Et;const A=a++;t.set(d,A);for(const{key:L,fn:V}of o){const E=V(d);if(E)return i[A]=`["${L}",${c(E)}]`,A}let y="";if(pt(d))y=$e(d);else{const L=ln(d);switch(L){case"Number":case"String":case"Boolean":y=`["Object",${$e(d)}]`;break;case"BigInt":y=`["BigInt",${d}]`;break;case"Date":y=`["Date","${!isNaN(d.getDate())?d.toISOString():""}"]`;break;case"RegExp":const{source:E,flags:Z}=d;y=Z?`["RegExp",${de(E)},"${Z}"]`:`["RegExp",${de(E)}]`;break;case"Array":y="[";for(let b=0;b<d.length;b+=1)b>0&&(y+=","),b in d?(u.push(`[${b}]`),y+=c(d[b]),u.pop()):y+=nn;y+="]";break;case"Set":y='["Set"';for(const b of d)y+=`,${c(b)}`;y+="]";break;case"Map":y='["Map"';for(const[b,_]of d)u.push(`.get(${pt(b)?$e(b):"..."})`),y+=`,${c(b)},${c(_)}`,u.pop();y+="]";break;case"Int8Array":case"Uint8Array":case"Uint8ClampedArray":case"Int16Array":case"Uint16Array":case"Int32Array":case"Uint32Array":case"Float32Array":case"Float64Array":case"BigInt64Array":case"BigUint64Array":{const _=ct(d.buffer);y='["'+L+'","'+_+'"]';break}case"ArrayBuffer":{y=`["ArrayBuffer","${ct(d)}"]`;break}default:if(!fn(d))throw new Ve("Cannot stringify arbitrary non-POJOs",u);if(dn(d).length>0)throw new Ve("Cannot stringify POJOs with symbolic keys",u);if(Object.getPrototypeOf(d)===null){y='["null"';for(const b in d)u.push(mt(b)),y+=`,${de(b)},${c(d[b])}`,u.pop();y+="]"}else{y="{";let b=!1;for(const _ in d)b&&(y+=","),b=!0,u.push(mt(_)),y+=`${de(_)}:${c(d[_])}`,u.pop();y+="}"}}}return i[A]=y,A}const m=c(e);return m<0?`${m}`:`[${i.join(",")}]`}function $e(e){const r=typeof e;return r==="string"?de(e):e instanceof String?de(e.toString()):e===void 0?At.toString():e===0&&1/e<0?Et.toString():r==="bigint"?`["BigInt","${e}"]`:String(e)}const Tt=on;function qe(e,r,i){return e[r]=i,"skip"}function yn(e,r){return r.value!==void 0&&typeof r.value!="object"&&r.path.length<e.length}function ne(e,r,i={}){i.modifier||(i.modifier=o=>yn(r,o)?void 0:o.value);const t=W(e,r,i.modifier);if(t)return i.value===void 0||i.value(t.value)?t:void 0}function W(e,r,i){if(!r.length)return;const t=[r[0]];let o=e;for(;o&&t.length<r.length;){const a=t[t.length-1],c=i?i({parent:o,key:String(a),value:o[a],path:t.map(m=>String(m)),isLeaf:!1,set:m=>qe(o,a,m)}):o[a];if(c===void 0)return;o=c,t.push(r[t.length])}if(!o)return;const u=r[r.length-1];return{parent:o,key:String(u),value:o[u],path:r.map(a=>String(a)),isLeaf:!0,set:a=>qe(o,u,a)}}function ee(e,r,i=[]){for(const t in e){const o=e[t],u=o===null||typeof o!="object",a={parent:e,key:t,value:o,path:i.concat([t]),isLeaf:u,set:m=>qe(e,t,m)},c=r(a);if(c==="abort")return c;if(c==="skip")continue;if(!u){const m=ee(o,r,a.path);if(m==="abort")return m}}}function bn(e,r){return e===r||e.size===r.size&&[...e].every(i=>r.has(i))}function yt(e,r){const i=new Map;function t(a,c){return a instanceof Date&&c instanceof Date&&a.getTime()!==c.getTime()||a instanceof Set&&c instanceof Set&&!bn(a,c)||a instanceof File&&c instanceof File&&a!==c}function o(a){return a instanceof Date||a instanceof Set||a instanceof File}function u(a,c){const m=c?W(c,a.path):void 0;function d(){return i.set(a.path.join(" "),a.path),"skip"}if(o(a.value)&&(!o(m==null?void 0:m.value)||t(a.value,m.value)))return d();a.isLeaf&&(!m||a.value!==m.value)&&d()}return ee(e,a=>u(a,r)),ee(r,a=>u(a,e)),Array.from(i.values())}function X(e,r,i){const t=typeof i=="function";for(const o of r){const u=W(e,o,({parent:a,key:c,value:m})=>((m===void 0||typeof m!="object")&&(a[c]={}),a[c]));u&&(u.parent[u.key]=t?i(o,u):i)}}function oe(e){return e.toString().split(/[[\].]+/).filter(r=>r)}function he(e){return e.reduce((r,i)=>{const t=String(i);return typeof i=="number"||/^\d+$/.test(t)?r+=`[${t}]`:r?r+=`.${t}`:r+=t,r},"")}var hn=ge;function ge(e){let r=e;var i={}.toString.call(e).slice(8,-1);if(i=="Set")return new Set([...e].map(o=>ge(o)));if(i=="Map")return new Map([...e].map(o=>[ge(o[0]),ge(o[1])]));if(i=="Date")return new Date(e.getTime());if(i=="RegExp")return RegExp(e.source,gn(e));if(i=="Array"||i=="Object"){r=Array.isArray(e)?[]:{};for(var t in e)r[t]=ge(e[t])}return r}function gn(e){if(typeof e.source.flags=="string")return e.source.flags;var r=[];return e.global&&r.push("g"),e.ignoreCase&&r.push("i"),e.multiline&&r.push("m"),e.sticky&&r.push("y"),e.unicode&&r.push("u"),r.join("")}function B(e){return e&&typeof e=="object"?hn(e):e}function Xe(e,r){if(typeof e=="boolean")throw new je("Schema property cannot be defined as boolean.",r)}const bt=e=>{if(typeof e=="object"&&e!==null){if(typeof Object.getPrototypeOf=="function"){const r=Object.getPrototypeOf(e);return r===Object.prototype||r===null}return Object.prototype.toString.call(e)==="[object Object]"}return!1},K=(...e)=>e.reduce((r,i)=>{if(Array.isArray(i))throw new TypeError("Arguments provided to ts-deepmerge must be objects, not arrays.");return Object.keys(i).forEach(t=>{["__proto__","constructor","prototype"].includes(t)||(Array.isArray(r[t])&&Array.isArray(i[t])?r[t]=K.options.mergeArrays?K.options.uniqueArrayItems?Array.from(new Set(r[t].concat(i[t]))):[...r[t],...i[t]]:i[t]:bt(r[t])&&bt(i[t])?r[t]=K(r[t],i[t]):r[t]=i[t]===void 0?K.options.allowUndefinedOverrides?i[t]:r[t]:i[t])}),r},{}),Be={allowUndefinedOverrides:!0,mergeArrays:!0,uniqueArrayItems:!0};K.options=Be;K.withOptions=(e,...r)=>{K.options=Object.assign(Object.assign({},Be),e);const i=K(...r);return K.options=Be,i};const wn=["unix-time","bigint","any","symbol","set"];function _t(e,r,i){var m;if(Xe(e,i),e.allOf&&e.allOf.length)return{...K.withOptions({allowUndefinedOverrides:!1},...e.allOf.map(d=>_t(d,!1,[]))),schema:e};const t=Ot(e,i),o=e.items&&t.includes("array")?(Array.isArray(e.items)?e.items:[e.items]).filter(d=>typeof d!="boolean"):void 0,u=e.additionalProperties&&typeof e.additionalProperties=="object"&&t.includes("object")?Object.fromEntries(Object.entries(e.additionalProperties).filter(([,d])=>typeof d!="boolean")):void 0,a=e.properties&&t.includes("object")?Object.fromEntries(Object.entries(e.properties).filter(([,d])=>typeof d!="boolean")):void 0,c=(m=vn(e))==null?void 0:m.filter(d=>d.type!=="null"&&d.const!==null);return{types:t.filter(d=>d!=="null"),isOptional:r,isNullable:t.includes("null"),schema:e,union:c!=null&&c.length?c:void 0,array:o,properties:a,additionalProperties:u,required:e.required}}function Ot(e,r){Xe(e,r);let i=e.const===null?["null"]:[];if(e.type&&(i=Array.isArray(e.type)?e.type:[e.type]),e.anyOf&&(i=e.anyOf.flatMap(t=>Ot(t,r))),i.includes("array")&&e.uniqueItems){const t=i.findIndex(o=>o!="array");i[t]="set"}else if(e.format&&wn.includes(e.format)&&(i.unshift(e.format),e.format=="unix-time")){const t=i.findIndex(o=>o=="integer");i.splice(t,1)}return e.const&&e.const!==null&&typeof e.const!="function"&&i.push(typeof e.const),Array.from(new Set(i))}function vn(e){if(!(!e.anyOf||!e.anyOf.length))return e.anyOf.filter(r=>typeof r!="boolean")}class k extends Error{constructor(r){super(r),Object.setPrototypeOf(this,k.prototype)}}class je extends k{constructor(i,t){super((t&&t.length?`[${Array.isArray(t)?t.join("."):t}] `:"")+i);ft(this,"path");this.path=Array.isArray(t)?t.join("."):t,Object.setPrototypeOf(this,je.prototype)}}function An(e,r){var o;const i={};function t(u){if("_errors"in i||(i._errors=[]),!Array.isArray(i._errors))if(typeof i._errors=="string")i._errors=[i._errors];else throw new k("Form-level error was not an array.");i._errors.push(u.message)}for(const u of e){if(!u.path||u.path.length==1&&!u.path[0]){t(u);continue}const c=!/^\d$/.test(String(u.path[u.path.length-1]))&&((o=ne(r,u.path.filter(y=>/\D/.test(String(y)))))==null?void 0:o.value),m=W(i,u.path,({value:y,parent:L,key:V})=>(y===void 0&&(L[V]={}),L[V]));if(!m){t(u);continue}const{parent:d,key:A}=m;c?(A in d||(d[A]={}),"_errors"in d[A]?d[A]._errors.push(u.message):d[A]._errors=[u.message]):A in d?d[A].push(u.message):d[A]=[u.message]}return i}function ht(e,r,i){return i?e:(ee(r,t=>{Array.isArray(t.value)&&t.set(void 0)}),ee(e,t=>{!Array.isArray(t.value)&&t.value!==void 0||X(r,[t.path],t.value)}),r)}function En(e){return Mt(e,[])}function Mt(e,r){return Object.entries(e).filter(([,t])=>t!==void 0).flatMap(([t,o])=>{if(Array.isArray(o)&&o.length>0){const u=r.concat([t]);return{path:he(u),messages:o}}else return Mt(e[t],r.concat([t]))})}function gt(e){!e.flashMessage||!Tt||Ye(e)&&(document.cookie=`flash=; Max-Age=0; Path=${e.flashMessage.cookiePath??"/"};`)}function Ye(e){return!e.flashMessage||!Tt?!1:e.syncFlashMessage}function ze(e){const r=JSON.parse(e);return r.data&&(r.data=rn(r.data)),r}function Ue(e){return HTMLElement.prototype.cloneNode.call(e)}function Sn(e,r=()=>{}){const i=async({action:o,result:u,reset:a=!0,invalidateAll:c=!0})=>{u.type==="success"&&(a&&HTMLFormElement.prototype.reset.call(e),c&&await St()),(location.origin+location.pathname===o.origin+o.pathname||u.type==="redirect"||u.type==="error")&&Oe(u)};async function t(o){var Z,b,_,we,ve;if(((Z=o.submitter)!=null&&Z.hasAttribute("formmethod")?o.submitter.formMethod:Ue(e).method)!=="post")return;o.preventDefault();const a=new URL((b=o.submitter)!=null&&b.hasAttribute("formaction")?o.submitter.formAction:Ue(e).action),c=(_=o.submitter)!=null&&_.hasAttribute("formenctype")?o.submitter.formEnctype:Ue(e).enctype,m=new FormData(e),d=(we=o.submitter)==null?void 0:we.getAttribute("name");d&&m.append(d,((ve=o.submitter)==null?void 0:ve.getAttribute("value"))??"");const A=new AbortController;let y=!1;const V=await r({action:a,cancel:()=>y=!0,controller:A,formData:m,formElement:e,submitter:o.submitter})??i;if(y)return;let E;try{const O=new Headers({accept:"application/json","x-sveltekit-action":"true"});c!=="multipart/form-data"&&O.set("Content-Type",/^(:?application\/x-www-form-urlencoded|text\/plain)$/.test(c)?c:"application/x-www-form-urlencoded");const Ie=c==="multipart/form-data"?m:new URLSearchParams(m),pe=await fetch(a,{method:"POST",headers:O,cache:"no-store",body:Ie,signal:A.signal});E=ze(await pe.text()),E.type==="error"&&(E.status=pe.status)}catch(O){if((O==null?void 0:O.name)==="AbortError")return;E={type:"error",error:O}}V({action:a,formData:m,formElement:e,update:O=>i({action:a,result:E,reset:O==null?void 0:O.reset,invalidateAll:O==null?void 0:O.invalidateAll}),result:E})}return HTMLFormElement.prototype.addEventListener.call(e,"submit",t),{destroy(){HTMLFormElement.prototype.removeEventListener.call(e,"submit",t)}}}const Ft="noCustomValidity";async function wt(e,r){"setCustomValidity"in e&&e.setCustomValidity(""),!(Ft in e.dataset)&&jt(e,r)}function Tn(e,r){for(const i of e.querySelectorAll("input,select,textarea,button")){if("dataset"in i&&Ft in i.dataset||!i.name)continue;const t=W(r,oe(i.name)),o=t&&typeof t.value=="object"&&"_errors"in t.value?t.value._errors:t==null?void 0:t.value;if(jt(i,o),o)return}}function jt(e,r){const i=r&&r.length?r.join(`
`):"";e.setCustomValidity(i),i&&e.reportValidity()}const _n=(e,r=0)=>{const i=e.getBoundingClientRect();return i.top>=r&&i.left>=0&&i.bottom<=(window.innerHeight||document.documentElement.clientHeight)&&i.right<=(window.innerWidth||document.documentElement.clientWidth)},On=(e,r=1.125,i="smooth")=>{const u=e.getBoundingClientRect().top+window.pageYOffset-window.innerHeight/(2*r);window.scrollTo({left:0,top:u,behavior:i})},Mn=["checkbox","radio","range","file"];function vt(e){const r=!!e&&(e instanceof HTMLSelectElement||e instanceof HTMLInputElement&&Mn.includes(e.type)),i=!!e&&e instanceof HTMLSelectElement&&e.multiple,t=!!e&&e instanceof HTMLInputElement&&e.type=="file";return{immediate:r,multiple:i,file:t}}var N;(function(e){e[e.Idle=0]="Idle",e[e.Submitting=1]="Submitting",e[e.Delayed=2]="Delayed",e[e.Timeout=3]="Timeout"})(N||(N={}));const Fn=new Set;function jn(e,r,i){let t=N.Idle,o,u;const a=Fn;function c(){m(),A(t!=N.Delayed?N.Submitting:N.Delayed),o=window.setTimeout(()=>{o&&t==N.Submitting&&A(N.Delayed)},i.delayMs),u=window.setTimeout(()=>{u&&t==N.Delayed&&A(N.Timeout)},i.timeoutMs),a.add(m)}function m(){clearTimeout(o),clearTimeout(u),o=u=0,a.delete(m),A(N.Idle)}function d(){a.forEach(b=>b()),a.clear()}function A(b){t=b,r.submitting.set(t>=N.Submitting),r.delayed.set(t>=N.Delayed),r.timeout.set(t>=N.Timeout)}const y=e;function L(b){const _=b.target;i.selectErrorText&&_.select()}function V(){i.selectErrorText&&y.querySelectorAll("input").forEach(b=>{b.addEventListener("invalid",L)})}function E(){i.selectErrorText&&y.querySelectorAll("input").forEach(b=>b.removeEventListener("invalid",L))}const Z=e;{V();const b=_=>{_.clearAll?d():m(),_.cancelled||setTimeout(()=>Ge(Z,i),1)};return Me(()=>{E(),b({cancelled:!0})}),{submitting(){c()},completed:b,scrollToFirstError(){setTimeout(()=>Ge(Z,i),1)},isSubmitting:()=>t===N.Submitting||t===N.Delayed}}}const Ge=async(e,r)=>{if(r.scrollToError=="off")return;const i=r.errorSelector;if(!i)return;await He();let t;if(t=e.querySelector(i),!t)return;t=t.querySelector(i)??t;const o=r.stickyNavbar?document.querySelector(r.stickyNavbar):null;typeof r.scrollToError!="string"?t.scrollIntoView(r.scrollToError):_n(t,(o==null?void 0:o.offsetHeight)??0)||On(t,void 0,r.scrollToError);function u(c){return typeof r.autoFocusOnError=="boolean"?r.autoFocusOnError:!/iPhone|iPad|iPod|Android/i.test(c)}if(!u(navigator.userAgent))return;let a;if(a=t,["INPUT","SELECT","BUTTON","TEXTAREA"].includes(a.tagName)||(a=a.querySelector('input:not([type="hidden"]):not(.flatpickr-input), select, textarea')),a)try{a.focus({preventScroll:!0}),r.selectErrorText&&a.tagName=="INPUT"&&a.select()}catch{}};function Fe(e,r,i){const t=W(e,r,({parent:o,key:u,value:a})=>(a===void 0&&(o[u]=/\D/.test(u)?{}:[]),o[u]));if(t){const o=i(t.value);t.parent[t.key]=o}return e}function In(e,r,i){const t=e.form,o=oe(r),u=Ze(t,a=>{const c=W(a,o);return c==null?void 0:c.value});return{subscribe(...a){const c=u.subscribe(...a);return()=>c()},update(a,c){t.update(m=>Fe(m,o,a),c??i)},set(a,c){t.update(m=>Fe(m,o,()=>a),c??i)}}}function Pn(e,r){const i="form"in e;if(!i&&(r==null?void 0:r.taint)!==void 0)throw new k("If options.taint is set, the whole superForm object must be used as a proxy.");return i}function Te(e,r,i){const t=oe(r);if(Pn(e,i))return In(e,r,i);const o=Ze(e,u=>{const a=W(u,t);return a==null?void 0:a.value});return{subscribe(...u){const a=o.subscribe(...u);return()=>a()},update(u){e.update(a=>Fe(a,t,u))},set(u){e.update(a=>Fe(a,t,()=>u))}}}function Bn(e,r=[]){const i=Je(e,r);if(!i)throw new je("No shape could be created for schema.",r);return i}function Je(e,r){Xe(e,r);const i=_t(e,!1,r);if(i.array||i.union){const t=i.array||[],o=i.union||[];return t.concat(o).reduce((u,a)=>{const c=Je(a,r);return c&&(u={...u??{},...c}),u},t.length?{}:void 0)}if(i.properties){const t={};for(const[o,u]of Object.entries(i.properties)){const a=Je(u,[...r,o]);a&&(t[o]=a)}return t}return i.types.includes("array")||i.types.includes("object")?{}:void 0}function We(e){let r={};const i=Array.isArray(e);for(const[t,o]of Object.entries(e))!o||typeof o!="object"||(i?r={...r,...We(o)}:r[t]=We(o));return r}const _e=new WeakMap,le=new WeakMap,It=e=>{throw e.result.error},kn={applyAction:!0,invalidateAll:!0,resetForm:!0,autoFocusOnError:"detect",scrollToError:"smooth",errorSelector:'[aria-invalid="true"],[data-invalid]',selectErrorText:!1,stickyNavbar:void 0,taintedMessage:!1,onSubmit:void 0,onResult:void 0,onUpdate:void 0,onUpdated:void 0,onError:It,dataType:"form",validators:void 0,customValidity:!1,clearOnSubmit:"message",delayMs:500,timeoutMs:8e3,multipleSubmits:"prevent",SPA:void 0,validationMethod:"auto"};function Dn(e){return`Duplicate form id's found: "${e}". Multiple forms will receive the same data. Use the id option to differentiate between them, or if this is intended, set the warnings.duplicateId option to false in superForm to disable this warning. More information: https://superforms.rocks/concepts/multiple-forms`}let Pt=!1;try{SUPERFORMS_LEGACY&&(Pt=!0)}catch{}let ce=!1;try{globalThis.STORIES&&(ce=!0)}catch{}function Yn(e,r){var ut;let i,t=r??{},o;{if((t.legacy??Pt)&&(t.resetForm===void 0&&(t.resetForm=!1),t.taintedMessage===void 0&&(t.taintedMessage=!0)),ce&&t.applyAction===void 0&&(t.applyAction=!1),typeof t.SPA=="string"&&(t.invalidateAll===void 0&&(t.invalidateAll=!1),t.applyAction===void 0&&(t.applyAction=!1)),o=t.validators,t={...kn,...t},(t.SPA===!0||typeof t.SPA=="object")&&t.validators===void 0&&console.warn("No validators set for superForm in SPA mode. Add a validation adapter to the validators option, or set it to false to disable this warning."),!e)throw new k("No form data sent to superForm. Make sure the output from superValidate is used (usually data.form) and that it's not null or undefined. Alternatively, an object with default values for the form can also be used, but then constraints won't be available.");d(e)===!1&&(e={id:t.id??Math.random().toString(36).slice(2,10),valid:!1,posted:!1,errors:{},data:e,shape:We(e)}),e=e;const n=e.id=t.id??e.id,s=ye(be)??(ce?{}:void 0);if(((ut=t.warnings)==null?void 0:ut.duplicateId)!==!1)if(!_e.has(s))_e.set(s,new Set([n]));else{const f=_e.get(s);f!=null&&f.has(n)?console.warn(Dn(n)):f==null||f.add(n)}if(le.has(e)||le.set(e,e),i=le.get(e),e=B(i),Me(()=>{var f;qt(),Nt(),zt();for(const l of Object.values(U))l.length=0;(f=_e.get(s))==null||f.delete(n)}),t.dataType!=="json"){const f=(l,p)=>{if(!(!p||typeof p!="object")){if(Array.isArray(p))p.length>0&&f(l,p[0]);else if(!(p instanceof Date)&&!(p instanceof File)&&!(p instanceof FileList))throw new k(`Object found in form field "${l}". Set the dataType option to "json" and add use:enhance to use nested data structures. More information: https://superforms.rocks/concepts/nested-data`)}};for(const[l,p]of Object.entries(e.data))f(l,p)}}const u={formId:e.id,form:B(e.data),constraints:e.constraints??{},posted:e.posted,errors:B(e.errors),message:B(e.message),tainted:void 0,valid:e.valid,submitting:!1,shape:e.shape},a=u,c=J(t.id??e.id);function m(n){return Object.values(n).filter(f=>d(f)!==!1)}function d(n){return!n||typeof n!="object"||!("valid"in n&&"errors"in n&&typeof n.valid=="boolean")?!1:"id"in n&&typeof n.id=="string"?n.id:!1}const A=J(e.data),y={subscribe:A.subscribe,set:(n,s={})=>{const f=B(n);return rt(f,s.taint??!0),A.set(f)},update:(n,s={})=>A.update(f=>{const l=n(f);return rt(l,s.taint??!0),l})};function L(){return t.SPA===!0||typeof t.SPA=="object"}function V(n){var s;return n>400?n:(typeof t.SPA=="boolean"||typeof t.SPA=="string"||(s=t.SPA)==null?void 0:s.failStatus)||n}async function E(n={}){const s=n.formData??a.form;let f={},l;const p=n.adapter??t.validators;if(typeof p=="object"){if(p!=o&&!("jsonSchema"in p))throw new k('Client validation adapter found in options.validators. A full adapter must be used when changing validators dynamically, for example "zod" instead of "zodClient".');if(l=await p.validate(s),!l.success)f=An(l.issues,p.shape??a.shape??{});else if(n.recheckValidData!==!1)return E({...n,recheckValidData:!1})}else l={success:!0,data:{}};const g={...a.form,...s,...l.success?l.data:{}};return{valid:l.success,posted:!1,errors:f,data:g,constraints:a.constraints,message:void 0,id:a.formId,shape:a.shape}}function Z(n){if(!t.onChange||!n.paths.length||n.type=="blur")return;let s;const f=n.paths.map(he);n.type&&n.paths.length==1&&n.formElement&&n.target instanceof Element?s={path:f[0],paths:f,formElement:n.formElement,target:n.target,set(l,p,g){Te({form:y},l,g).set(p)},get(l){return ye(Te(y,l))}}:s={paths:f,target:void 0,set(l,p,g){Te({form:y},l,g).set(p)},get(l){return ye(Te(y,l))}},t.onChange(s)}async function b(n,s=!1,f){n&&(t.validators=="clear"&&z.update(g=>(X(g,n.paths,void 0),g)),setTimeout(()=>Z(n)));let l=!1;if(s||(t.validationMethod=="onsubmit"||t.validationMethod=="submit-only"||t.validationMethod=="onblur"&&(n==null?void 0:n.type)=="input"||t.validationMethod=="oninput"&&(n==null?void 0:n.type)=="blur")&&(l=!0),l||!n||!t.validators||t.validators=="clear"){if(n!=null&&n.paths){const g=(n==null?void 0:n.formElement)??me();g&&_(g)}return}const p=await E({adapter:f});return p.valid&&(n.immediate||n.type!="input")&&y.set(p.data,{taint:"ignore"}),await He(),we(p.errors,n,s),p}function _(n){const s=new Map;if(t.customValidity&&n)for(const f of n.querySelectorAll("[name]")){if(typeof f.name!="string"||!f.name.length)continue;const l="validationMessage"in f?String(f.validationMessage):"";s.set(f.name,{el:f,message:l}),wt(f,void 0)}return s}async function we(n,s,f){const{type:l,immediate:p,multiple:g,paths:H}=s,te=a.errors,re={};let R=new Map;const D=s.formElement??me();D&&(R=_(D)),ee(n,S=>{if(!Array.isArray(S.value))return;const j=[...S.path];j[j.length-1]=="_errors"&&j.pop();const fe=j.join(".");function q(){if(X(re,[S.path],S.value),t.customValidity&&ie&&R.has(fe)){const{el:C,message:se}=R.get(fe);se!=S.value&&(setTimeout(()=>wt(C,S.value)),R.clear())}}if(f)return q();const Se=S.path[S.path.length-1]=="_errors",ie=S.value&&H.some(C=>Se?j&&C&&j.length>0&&j[0]==C[0]:fe==C.join("."));if(ie&&t.validationMethod=="oninput"||p&&!g&&ie)return q();if(g){const C=ne(ye(z),S.path.slice(0,-1));if(C!=null&&C.value&&typeof(C==null?void 0:C.value)=="object"){for(const se of Object.values(C.value))if(Array.isArray(se))return q()}}const Q=ne(te,S.path);if(Q&&Q.key in Q.parent)return q();if(Se){if(t.validationMethod=="oninput"||l=="blur"&&$t(he(S.path.slice(0,-1))))return q()}else if(l=="blur"&&ie)return q()}),z.set(re)}function ve(n,s={}){return s.keepFiles&&ee(a.form,f=>{if(!(f.parent instanceof FileList)&&(f.value instanceof File||f.value instanceof FileList)){const l=ne(n,f.path);(!l||!(l.key in l.parent))&&X(n,[f.path],f.value)}}),y.set(n,s)}function O(n,s){return n&&s&&t.resetForm&&(t.resetForm===!0||t.resetForm())}function Ie(n=!0){let s=a.form,f=a.tainted;if(n){const l=Jt(a.form);s=l.data;const p=l.paths;p.length&&(f=B(f)??{},X(f,p,!1))}return{valid:a.valid,posted:a.posted,errors:a.errors,data:s,constraints:a.constraints,message:a.message,id:a.formId,tainted:f,shape:a.shape}}async function pe(n,s){n.valid&&s&&O(n.valid,s)?Pe({message:n.message,posted:!0}):Ee({form:n,untaint:s,keepFiles:!0,skipFormData:t.invalidateAll=="force"}),U.onUpdated.length&&await He();for(const f of U.onUpdated)f({form:n})}function Pe(n={}){n.newState&&(i.data={...i.data,...n.newState});const s=B(i);s.data={...s.data,...n.data},n.id!==void 0&&(s.id=n.id),Ee({form:s,untaint:!0,message:n.message,keepFiles:!1,posted:n.posted,resetted:!0})}async function Dt(n){if(n.type=="error")throw new k(`ActionResult of type "${n.type}" cannot be passed to update function.`);if(n.type=="redirect"){O(!0,!0)&&Pe({posted:!0});return}if(typeof n.data!="object")throw new k("Non-object validation data returned from ActionResult.");const s=m(n.data);if(!s.length)throw new k("No form data returned from ActionResult. Make sure you return { form } in the form actions.");for(const f of s)f.id===a.formId&&await pe(f,n.status>=200&&n.status<300)}const ue=J(u.message),ke=J(u.constraints),De=J(u.posted),Ke=J(u.shape),xe=J(e.errors),z={subscribe:xe.subscribe,set(n,s){return xe.set(ht(n,a.errors,s==null?void 0:s.force))},update(n,s){return xe.update(f=>ht(n(f),a.errors,s==null?void 0:s.force))},clear:()=>z.set({})};let F=null;function xt(n){var s;F&&n&&Object.keys(n).length==1&&((s=n.paths)!=null&&s.length)&&F.target&&F.target instanceof HTMLInputElement&&F.target.type.toLowerCase()=="file"?F.paths=n.paths:F=n,setTimeout(()=>{b(F)},0)}function Rt(n,s,f,l,p){F===null&&(F={paths:[]}),F.type=n,F.immediate=s,F.multiple=f,F.formElement=l,F.target=p}function Qe(){return(F==null?void 0:F.paths)??[]}function Nt(){F=null}const x={defaultMessage:"Leave page? Changes that you made may not be saved.",state:J(),message:t.taintedMessage,clean:B(e.data),forceRedirection:!1};function et(){return t.taintedMessage&&!a.submitting&&!x.forceRedirection&&nt()}function tt(n){if(!et())return;n.preventDefault(),n.returnValue="";const{taintedMessage:s}=t,l=typeof s=="function"||s===!0?x.defaultMessage:s;return(n||window.event).returnValue=l||x.defaultMessage,l}async function Lt(n){if(!et())return;const{taintedMessage:s}=t,f=typeof s=="function";if(f&&n.cancel(),n.type==="leave")return;const l=f||s===!0?x.defaultMessage:s;let p;try{p=f?await s():window.confirm(l||x.defaultMessage)}catch{p=!1}if(p&&n.to)try{x.forceRedirection=!0,await an(n.to.url,{...n.to.params});return}finally{x.forceRedirection=!1}else!p&&!f&&n.cancel()}function Ct(){t.taintedMessage=x.message}function Vt(){return x.state}function $t(n){if(!a.tainted)return!1;if(!n)return!!a.tainted;const s=ne(a.tainted,oe(n));return!!s&&s.key in s.parent}function nt(n){if(!arguments.length)return Ae(a.tainted);if(typeof n=="boolean")return n;if(typeof n=="object")return Ae(n);if(!a.tainted||n===void 0)return!1;const s=ne(a.tainted,oe(n));return Ae(s==null?void 0:s.value)}function Ae(n){if(!n)return!1;if(typeof n=="object"){for(const s of Object.values(n))if(Ae(s))return!0}return n===!0}function rt(n,s){if(s=="ignore")return;const f=yt(n,a.form),l=yt(n,x.clean).map(p=>p.join());f.length&&(s=="untaint-all"||s=="untaint-form"?x.state.set(void 0):x.state.update(p=>(p||(p={}),X(p,f,(g,H)=>{if(!l.includes(g.join()))return;const te=W(n,g),re=W(x.clean,g);return te&&re&&te.value===re.value?void 0:s===!0?!0:s==="untaint"?void 0:H.value}),p)),xt({paths:f}))}function Ut(n,s){x.state.set(n),s&&(x.clean=s)}const Re=J(!1),it=J(!1),st=J(!1),at=[x.state.subscribe(n=>u.tainted=B(n)),y.subscribe(n=>u.form=B(n)),z.subscribe(n=>u.errors=B(n)),c.subscribe(n=>u.formId=n),ke.subscribe(n=>u.constraints=n),De.subscribe(n=>u.posted=n),ue.subscribe(n=>u.message=n),Re.subscribe(n=>u.submitting=n),Ke.subscribe(n=>u.shape=n)];function Ht(n){at.push(n)}function qt(){at.forEach(n=>n())}let $;function me(){return $}function Bt(n){$=document.createElement("form"),$.method="POST",$.action=n,ot($),document.body.appendChild($)}function Yt(n){$&&($.action=n)}function zt(){$!=null&&$.parentElement&&$.remove(),$=void 0}const Gt=Ze(z,n=>n?En(n):[]);t.taintedMessage=void 0;function Ee(n){const s=n.form,f=n.message??s.message;if((n.untaint||n.resetted)&&Ut(typeof n.untaint=="boolean"?void 0:n.untaint,s.data),n.skipFormData!==!0&&ve(s.data,{taint:"ignore",keepFiles:n.keepFiles}),ue.set(f),n.resetted?z.update(()=>({}),{force:!0}):z.set(s.errors),c.set(s.id),De.set(n.posted??s.posted),s.constraints&&ke.set(s.constraints),s.shape&&Ke.set(s.shape),u.valid=s.valid,t.flashMessage&&Ye(t)){const l=t.flashMessage.module.getFlash(be);f&&ye(l)===void 0&&l.set(f)}}const U={onSubmit:t.onSubmit?[t.onSubmit]:[],onResult:t.onResult?[t.onResult]:[],onUpdate:t.onUpdate?[t.onUpdate]:[],onUpdated:t.onUpdated?[t.onUpdated]:[],onError:t.onError?[t.onError]:[]};window.addEventListener("beforeunload",tt),Me(()=>{window.removeEventListener("beforeunload",tt)}),sn(Lt),Ht(be.subscribe(async n=>{ce&&n===void 0&&(n={status:200});const s=n.status>=200&&n.status<300;if(t.applyAction&&n.form&&typeof n.form=="object"){const f=n.form;if(f.type==="error")return;for(const l of m(f)){const p=le.has(l);l.id!==a.formId||p||(le.set(l,l),await pe(l,s))}}else if(n.data&&typeof n.data=="object")for(const f of m(n.data)){const l=le.has(f);if(f.id!==a.formId||l)continue;t.invalidateAll==="force"&&(i.data=f.data);const p=O(f.valid,!0);Ee({form:f,untaint:s,keepFiles:!p,resetted:p})}})),typeof t.SPA=="string"&&Bt(t.SPA);function ot(n,s){if(t.SPA!==void 0&&n.method=="get"&&(n.method="post"),typeof t.SPA=="string"?t.SPA.length&&n.action==document.location.href&&(n.action=t.SPA):$=n,s){if(s.onError){if(t.onError==="apply")throw new k('options.onError is set to "apply", cannot add any onError events.');if(s.onError==="apply")throw new k('Cannot add "apply" as onError event in use:enhance.');U.onError.push(s.onError)}s.onResult&&U.onResult.push(s.onResult),s.onSubmit&&U.onSubmit.push(s.onSubmit),s.onUpdate&&U.onUpdate.push(s.onUpdate),s.onUpdated&&U.onUpdated.push(s.onUpdated)}Ct();let f;async function l(R){const D=vt(R.target);D.immediate&&!D.file&&await new Promise(S=>setTimeout(S,0)),f=Qe(),Rt("input",D.immediate,D.multiple,n,R.target??void 0)}async function p(R){if(a.submitting||!f||Qe()!=f)return;const D=vt(R.target);D.immediate&&!D.file&&await new Promise(S=>setTimeout(S,0)),b({paths:f,immediate:D.multiple,multiple:D.multiple,type:"blur",formElement:n,target:R.target??void 0}),f=void 0}n.addEventListener("focusout",p),n.addEventListener("input",l),Me(()=>{n.removeEventListener("focusout",p),n.removeEventListener("input",l)});const g=jn(n,{submitting:Re,delayed:it,timeout:st},t);let H,te;const re=Sn(n,async R=>{let D,S=t.validators;const j={...R,jsonData(w){if(t.dataType!=="json")throw new k("options.dataType must be set to 'json' to use jsonData.");D=w},validators(w){S=w},customRequest(w){te=w}},fe=j.cancel;let q=!1;function Ne(w){const h={...w,posted:!0},v=h.valid?200:V(400),I={form:h},T=h.valid?{type:"success",status:v,data:I}:{type:"failure",status:v,data:I};setTimeout(()=>se({result:T}),0)}function Se(){switch(t.clearOnSubmit){case"errors-and-message":z.clear(),ue.set(void 0);break;case"errors":z.clear();break;case"message":ue.set(void 0);break}}async function ie(w,h){var v;if(w.status=h,t.onError!=="apply"){const I={result:w,message:ue,form:e};for(const T of U.onError)T!=="apply"&&(T!=It||!((v=t.flashMessage)!=null&&v.onError))&&await T(I)}t.flashMessage&&t.flashMessage.onError&&await t.flashMessage.onError({result:w,flashMessage:t.flashMessage.module.getFlash(be)}),t.applyAction&&(t.onError=="apply"?await Oe(w):await Oe({type:"failure",status:V(w.status),data:w}))}function Q(w={resetTimers:!0}){return q=!0,w.resetTimers&&g.isSubmitting()&&g.completed({cancelled:q}),fe()}if(j.cancel=Q,g.isSubmitting()&&t.multipleSubmits=="prevent")Q({resetTimers:!1});else{g.isSubmitting()&&t.multipleSubmits=="abort"&&H&&H.abort(),g.submitting(),H=j.controller;for(const w of U.onSubmit)try{await w(j)}catch(h){Q(),ie({type:"error",error:h},500)}}if(q&&t.flashMessage&&gt(t),!q){const w=!L()&&(n.noValidate||(j.submitter instanceof HTMLButtonElement||j.submitter instanceof HTMLInputElement)&&j.submitter.formNoValidate);let h;const v=async()=>await E({adapter:S});if(Se(),w||(h=await v(),h.valid||(Q({resetTimers:!1}),Ne(h))),!q){t.flashMessage&&(t.clearOnSubmit=="errors-and-message"||t.clearOnSubmit=="message")&&Ye(t)&&t.flashMessage.module.getFlash(be).set(void 0);const I="formData"in j?j.formData:j.data;if(f=void 0,L())h||(h=await v()),Q({resetTimers:!1}),Ne(h);else if(t.dataType==="json"){h||(h=await v());const T=B(D??h.data);ee(T,P=>{if(P.value instanceof File){const M="__superform_file_"+he(P.path);return I.append(M,P.value),P.set(void 0)}else if(Array.isArray(P.value)&&P.value.length&&P.value.every(M=>M instanceof File)){const M="__superform_files_"+he(P.path);for(const Y of P.value)I.append(M,Y);return P.set(void 0)}}),Object.keys(T).forEach(P=>{typeof I.get(P)=="string"&&I.delete(P)});const ae=C(mn(T),t.jsonChunkSize??5e5);for(const P of ae)I.append("__superform_json",P)}if(!I.has("__superform_id")){const T=a.formId;T!==void 0&&I.set("__superform_id",T)}typeof t.SPA=="string"&&Yt(t.SPA)}}function C(w,h){const v=Math.ceil(w.length/h),I=new Array(v);for(let T=0,ae=0;T<v;++T,ae+=h)I[T]=w.substring(ae,ae+h);return I}async function se(w){let h=!1;H=null;let v="type"in w.result&&"status"in w.result?w.result:{type:"error",status:V(parseInt(String(w.result.status))||500),error:w.result.error instanceof Error?w.result.error:w.result};const I=()=>h=!0,T={result:v,formEl:n,formElement:n,cancel:I},ae=ce||!L()?()=>{}:dt.subscribe(M=>{var Y,G;!M||((Y=M.from)==null?void 0:Y.route.id)===((G=M.to)==null?void 0:G.route.id)||I()});function P(M,Y,G){Y.result={type:"error",error:M,status:V(G)}}for(const M of U.onResult)try{await M(T)}catch(Y){P(Y,T,Math.max(v.status??500,400))}if(v=T.result,!h){if((v.type==="success"||v.type==="failure")&&v.data){const M=m(v.data);if(!M.length)throw new k("No form data returned from ActionResult. Make sure you return { form } in the form actions.");for(const Y of M){if(Y.id!==a.formId)continue;const G={form:Y,formEl:n,formElement:n,cancel:()=>h=!0,result:v};for(const Le of U.onUpdate)try{await Le(G)}catch(Wt){P(Wt,G,Math.max(v.status??500,400))}v=G.result,h||(t.customValidity&&Tn(n,G.form.errors),O(G.form.valid,v.type=="success")&&G.formElement.querySelectorAll('input[type="file"]').forEach(Le=>Le.value=""))}}h||(v.type!=="error"?(v.type==="success"&&t.invalidateAll&&await St(),t.applyAction?await Oe(v):await Dt(v)):await ie(v,Math.max(v.status??500,400)))}if(h&&t.flashMessage&&gt(t),h||v.type!="redirect")g.completed({cancelled:h});else if(ce)g.completed({cancelled:h,clearAll:!0});else{const M=dt.subscribe(Y=>{Y||(setTimeout(()=>{try{M&&M()}catch{}}),g.isSubmitting()&&g.completed({cancelled:h,clearAll:!0}))})}ae()}if(!q&&te){fe();const w=await te(R);let h;w instanceof Response?h=ze(await w.text()):w instanceof XMLHttpRequest?h=ze(w.responseText):h=w,h.type==="error"&&(h.status=w.status),se({result:h})}return se});return{destroy:()=>{for(const[R,D]of Object.entries(U))U[R]=D.filter(S=>S===t[R]);re.destroy()}}}function Jt(n){const s=[];if(ee(n,l=>{if(l.value instanceof File)return s.push(l.path),"skip";if(Array.isArray(l.value)&&l.value.length&&l.value.every(p=>p instanceof File))return s.push(l.path),"skip"}),!s.length)return{data:n,paths:s};const f=B(n);return X(f,s,l=>{var p;return(p=ne(i.data,l))==null?void 0:p.value}),{data:f,paths:s}}return{form:y,formId:c,errors:z,message:ue,constraints:ke,tainted:Vt(),submitting:Ce(Re),delayed:Ce(it),timeout:Ce(st),options:t,capture:Ie,restore:n=>{Ee({form:n,untaint:n.tainted??!0})},async validate(n,s={}){if(!t.validators)throw new k("options.validators must be set to use the validate method.");s.update===void 0&&(s.update=!0),s.taint===void 0&&(s.taint=!1),typeof s.errors=="string"&&(s.errors=[s.errors]);let f;const l=oe(n);"value"in s?s.update===!0||s.update==="value"?(y.update(H=>(X(H,[l],s.value),H),{taint:s.taint}),f=a.form):(f=B(a.form),X(f,[l],s.value)):f=a.form;const p=await E({formData:f}),g=ne(p.errors,l);return g&&g.value&&s.errors&&(g.value=s.errors),(s.update===!0||s.update=="errors")&&z.update(H=>(X(H,[l],g==null?void 0:g.value),H)),g==null?void 0:g.value},async validateForm(n={}){if(!t.validators&&!n.schema)throw new k("options.validators or the schema option must be set to use the validateForm method.");const s=n.update?await b({paths:[]},!0,n.schema):E({adapter:n.schema}),f=me();return n.update&&f&&setTimeout(()=>{f&&Ge(f,{...t,scrollToError:n.focusOnError===!1?"off":t.scrollToError})},1),s||E({adapter:n.schema})},allErrors:Gt,posted:De,reset(n){return Pe({message:n!=null&&n.keepMessage?a.message:void 0,data:n==null?void 0:n.data,id:n==null?void 0:n.id,newState:n==null?void 0:n.newState})},submit(n){const s=me()?me():n&&n instanceof HTMLElement?n.closest("form"):void 0;if(!s)throw new k("use:enhance must be added to the form to use submit, or pass a HTMLElement inside the form (or the form itself) as an argument.");if(!s.requestSubmit)return s.submit();const f=n&&(n instanceof HTMLButtonElement&&n.type=="submit"||n instanceof HTMLInputElement&&["submit","image"].includes(n.type));s.requestSubmit(f?n:void 0)},isTainted:nt,enhance:ot}}let xn=!1;try{SUPERFORMS_LEGACY&&(xn=!0)}catch{}function Rn(e,r,i,t){t===void 0&&(t={});const o=Array.isArray(i)?i:[i];if(e.errors||(e.errors={}),r===null||r==="")e.errors._errors||(e.errors._errors=[]),e.errors._errors=t.overwrite?o:e.errors._errors.concat(o);else{const a=oe(r),c=W(e.errors,a,({parent:m,key:d,value:A})=>(A===void 0&&(m[d]={}),m[d]));c&&(c.parent[c.key]=Array.isArray(c.value)&&!t.overwrite?c.value.concat(o):o)}e.valid=!1;const u=t.removeFiles===!1?{form:e}:kt({form:e});return Kt(t.status??400,u)}function kt(e){if(typeof e!="object")return e;for(const r in e){const i=e[r];i instanceof File?delete e[r]:i&&typeof i=="object"&&kt(i)}return e}function zn(e){return e&&e.__esModule&&Object.prototype.hasOwnProperty.call(e,"default")?e.default:e}async function Gn(e,r){const i=await e("/api/testruns/"+r).then(o=>(o.ok||lt(o.status,o.statusText),o.json())),t=await e("/api/testruns/measurements/"+i.id).then(o=>(o.ok||lt(o.status,o.statusText),o.json()));return{run:i,measurements:t}}async function Jn(e,r,i){let t="POST";return r.data.id&&(e+="/"+r.data.id,t="PUT"),await Nn(t,e,r,i)}async function Nn(e,r,i,t){let o="/api/"+r;const u=await fetch(o,{headers:{"Content-Type":"application/json"},method:e,body:JSON.stringify(t||i.data)}),a=await u.json();if(!u.ok)if(u.status==422)"error"in a&&"type"in a.error&&(a.error.type=="unique_violation"?Rn(i,a.error.field,"An entry with this value already exists"):console.log("TODO: implement this error type"));else throw new Error("TODO");return a}export{je as S,Xe as a,k as b,Bn as c,zn as d,Yn as e,Jn as f,Gn as g,Nn as h,K as m,_t as s};
