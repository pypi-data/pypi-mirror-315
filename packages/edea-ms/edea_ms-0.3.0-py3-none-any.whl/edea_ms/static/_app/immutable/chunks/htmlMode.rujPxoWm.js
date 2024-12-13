import{m as lt}from"./3.BIY6VRVe.js";/*!-----------------------------------------------------------------------------
 * Copyright (c) Microsoft Corporation. All rights reserved.
 * Version: 0.52.2(404545bded1df6ffa41ea0af4e8ddb219018c6c1)
 * Released under the MIT license
 * https://github.com/microsoft/monaco-editor/blob/main/LICENSE.txt
 *-----------------------------------------------------------------------------*/var ft=Object.defineProperty,gt=Object.getOwnPropertyDescriptor,ht=Object.getOwnPropertyNames,vt=Object.prototype.hasOwnProperty,pt=(e,n,i,r)=>{if(n&&typeof n=="object"||typeof n=="function")for(let t of ht(n))!vt.call(e,t)&&t!==i&&ft(e,t,{get:()=>n[t],enumerable:!(r=gt(n,t))||r.enumerable});return e},mt=(e,n,i)=>(pt(e,n,"default"),i),c={};mt(c,lt);var _t=2*60*1e3,Qe=class{constructor(e){this._defaults=e,this._worker=null,this._client=null,this._idleCheckInterval=window.setInterval(()=>this._checkIfIdle(),30*1e3),this._lastUsedTime=0,this._configChangeListener=this._defaults.onDidChange(()=>this._stopWorker())}_stopWorker(){this._worker&&(this._worker.dispose(),this._worker=null),this._client=null}dispose(){clearInterval(this._idleCheckInterval),this._configChangeListener.dispose(),this._stopWorker()}_checkIfIdle(){if(!this._worker)return;Date.now()-this._lastUsedTime>_t&&this._stopWorker()}_getClient(){return this._lastUsedTime=Date.now(),this._client||(this._worker=c.editor.createWebWorker({moduleId:"vs/language/html/htmlWorker",createData:{languageSettings:this._defaults.options,languageId:this._defaults.languageId},label:this._defaults.languageId}),this._client=this._worker.getProxy()),this._client}getLanguageServiceWorker(...e){let n;return this._getClient().then(i=>{n=i}).then(i=>{if(this._worker)return this._worker.withSyncedResources(e)}).then(i=>n)}},J;(function(e){function n(i){return typeof i=="string"}e.is=n})(J||(J={}));var S;(function(e){function n(i){return typeof i=="string"}e.is=n})(S||(S={}));var Y;(function(e){e.MIN_VALUE=-2147483648,e.MAX_VALUE=2147483647;function n(i){return typeof i=="number"&&e.MIN_VALUE<=i&&i<=e.MAX_VALUE}e.is=n})(Y||(Y={}));var M;(function(e){e.MIN_VALUE=0,e.MAX_VALUE=2147483647;function n(i){return typeof i=="number"&&e.MIN_VALUE<=i&&i<=e.MAX_VALUE}e.is=n})(M||(M={}));var b;(function(e){function n(r,t){return r===Number.MAX_VALUE&&(r=M.MAX_VALUE),t===Number.MAX_VALUE&&(t=M.MAX_VALUE),{line:r,character:t}}e.create=n;function i(r){let t=r;return a.objectLiteral(t)&&a.uinteger(t.line)&&a.uinteger(t.character)}e.is=i})(b||(b={}));var h;(function(e){function n(r,t,o,s){if(a.uinteger(r)&&a.uinteger(t)&&a.uinteger(o)&&a.uinteger(s))return{start:b.create(r,t),end:b.create(o,s)};if(b.is(r)&&b.is(t))return{start:r,end:t};throw new Error(`Range#create called with invalid arguments[${r}, ${t}, ${o}, ${s}]`)}e.create=n;function i(r){let t=r;return a.objectLiteral(t)&&b.is(t.start)&&b.is(t.end)}e.is=i})(h||(h={}));var C;(function(e){function n(r,t){return{uri:r,range:t}}e.create=n;function i(r){let t=r;return a.objectLiteral(t)&&h.is(t.range)&&(a.string(t.uri)||a.undefined(t.uri))}e.is=i})(C||(C={}));var Z;(function(e){function n(r,t,o,s){return{targetUri:r,targetRange:t,targetSelectionRange:o,originSelectionRange:s}}e.create=n;function i(r){let t=r;return a.objectLiteral(t)&&h.is(t.targetRange)&&a.string(t.targetUri)&&h.is(t.targetSelectionRange)&&(h.is(t.originSelectionRange)||a.undefined(t.originSelectionRange))}e.is=i})(Z||(Z={}));var O;(function(e){function n(r,t,o,s){return{red:r,green:t,blue:o,alpha:s}}e.create=n;function i(r){const t=r;return a.objectLiteral(t)&&a.numberRange(t.red,0,1)&&a.numberRange(t.green,0,1)&&a.numberRange(t.blue,0,1)&&a.numberRange(t.alpha,0,1)}e.is=i})(O||(O={}));var K;(function(e){function n(r,t){return{range:r,color:t}}e.create=n;function i(r){const t=r;return a.objectLiteral(t)&&h.is(t.range)&&O.is(t.color)}e.is=i})(K||(K={}));var ee;(function(e){function n(r,t,o){return{label:r,textEdit:t,additionalTextEdits:o}}e.create=n;function i(r){const t=r;return a.objectLiteral(t)&&a.string(t.label)&&(a.undefined(t.textEdit)||E.is(t))&&(a.undefined(t.additionalTextEdits)||a.typedArray(t.additionalTextEdits,E.is))}e.is=i})(ee||(ee={}));var A;(function(e){e.Comment="comment",e.Imports="imports",e.Region="region"})(A||(A={}));var te;(function(e){function n(r,t,o,s,u,f){const d={startLine:r,endLine:t};return a.defined(o)&&(d.startCharacter=o),a.defined(s)&&(d.endCharacter=s),a.defined(u)&&(d.kind=u),a.defined(f)&&(d.collapsedText=f),d}e.create=n;function i(r){const t=r;return a.objectLiteral(t)&&a.uinteger(t.startLine)&&a.uinteger(t.startLine)&&(a.undefined(t.startCharacter)||a.uinteger(t.startCharacter))&&(a.undefined(t.endCharacter)||a.uinteger(t.endCharacter))&&(a.undefined(t.kind)||a.string(t.kind))}e.is=i})(te||(te={}));var U;(function(e){function n(r,t){return{location:r,message:t}}e.create=n;function i(r){let t=r;return a.defined(t)&&C.is(t.location)&&a.string(t.message)}e.is=i})(U||(U={}));var x;(function(e){e.Error=1,e.Warning=2,e.Information=3,e.Hint=4})(x||(x={}));var re;(function(e){e.Unnecessary=1,e.Deprecated=2})(re||(re={}));var ne;(function(e){function n(i){const r=i;return a.objectLiteral(r)&&a.string(r.href)}e.is=n})(ne||(ne={}));var F;(function(e){function n(r,t,o,s,u,f){let d={range:r,message:t};return a.defined(o)&&(d.severity=o),a.defined(s)&&(d.code=s),a.defined(u)&&(d.source=u),a.defined(f)&&(d.relatedInformation=f),d}e.create=n;function i(r){var t;let o=r;return a.defined(o)&&h.is(o.range)&&a.string(o.message)&&(a.number(o.severity)||a.undefined(o.severity))&&(a.integer(o.code)||a.string(o.code)||a.undefined(o.code))&&(a.undefined(o.codeDescription)||a.string((t=o.codeDescription)===null||t===void 0?void 0:t.href))&&(a.string(o.source)||a.undefined(o.source))&&(a.undefined(o.relatedInformation)||a.typedArray(o.relatedInformation,U.is))}e.is=i})(F||(F={}));var I;(function(e){function n(r,t,...o){let s={title:r,command:t};return a.defined(o)&&o.length>0&&(s.arguments=o),s}e.create=n;function i(r){let t=r;return a.defined(t)&&a.string(t.title)&&a.string(t.command)}e.is=i})(I||(I={}));var E;(function(e){function n(o,s){return{range:o,newText:s}}e.replace=n;function i(o,s){return{range:{start:o,end:o},newText:s}}e.insert=i;function r(o){return{range:o,newText:""}}e.del=r;function t(o){const s=o;return a.objectLiteral(s)&&a.string(s.newText)&&h.is(s.range)}e.is=t})(E||(E={}));var V;(function(e){function n(r,t,o){const s={label:r};return t!==void 0&&(s.needsConfirmation=t),o!==void 0&&(s.description=o),s}e.create=n;function i(r){const t=r;return a.objectLiteral(t)&&a.string(t.label)&&(a.boolean(t.needsConfirmation)||t.needsConfirmation===void 0)&&(a.string(t.description)||t.description===void 0)}e.is=i})(V||(V={}));var L;(function(e){function n(i){const r=i;return a.string(r)}e.is=n})(L||(L={}));var ie;(function(e){function n(o,s,u){return{range:o,newText:s,annotationId:u}}e.replace=n;function i(o,s,u){return{range:{start:o,end:o},newText:s,annotationId:u}}e.insert=i;function r(o,s){return{range:o,newText:"",annotationId:s}}e.del=r;function t(o){const s=o;return E.is(s)&&(V.is(s.annotationId)||L.is(s.annotationId))}e.is=t})(ie||(ie={}));var W;(function(e){function n(r,t){return{textDocument:r,edits:t}}e.create=n;function i(r){let t=r;return a.defined(t)&&B.is(t.textDocument)&&Array.isArray(t.edits)}e.is=i})(W||(W={}));var H;(function(e){function n(r,t,o){let s={kind:"create",uri:r};return t!==void 0&&(t.overwrite!==void 0||t.ignoreIfExists!==void 0)&&(s.options=t),o!==void 0&&(s.annotationId=o),s}e.create=n;function i(r){let t=r;return t&&t.kind==="create"&&a.string(t.uri)&&(t.options===void 0||(t.options.overwrite===void 0||a.boolean(t.options.overwrite))&&(t.options.ignoreIfExists===void 0||a.boolean(t.options.ignoreIfExists)))&&(t.annotationId===void 0||L.is(t.annotationId))}e.is=i})(H||(H={}));var X;(function(e){function n(r,t,o,s){let u={kind:"rename",oldUri:r,newUri:t};return o!==void 0&&(o.overwrite!==void 0||o.ignoreIfExists!==void 0)&&(u.options=o),s!==void 0&&(u.annotationId=s),u}e.create=n;function i(r){let t=r;return t&&t.kind==="rename"&&a.string(t.oldUri)&&a.string(t.newUri)&&(t.options===void 0||(t.options.overwrite===void 0||a.boolean(t.options.overwrite))&&(t.options.ignoreIfExists===void 0||a.boolean(t.options.ignoreIfExists)))&&(t.annotationId===void 0||L.is(t.annotationId))}e.is=i})(X||(X={}));var $;(function(e){function n(r,t,o){let s={kind:"delete",uri:r};return t!==void 0&&(t.recursive!==void 0||t.ignoreIfNotExists!==void 0)&&(s.options=t),o!==void 0&&(s.annotationId=o),s}e.create=n;function i(r){let t=r;return t&&t.kind==="delete"&&a.string(t.uri)&&(t.options===void 0||(t.options.recursive===void 0||a.boolean(t.options.recursive))&&(t.options.ignoreIfNotExists===void 0||a.boolean(t.options.ignoreIfNotExists)))&&(t.annotationId===void 0||L.is(t.annotationId))}e.is=i})($||($={}));var z;(function(e){function n(i){let r=i;return r&&(r.changes!==void 0||r.documentChanges!==void 0)&&(r.documentChanges===void 0||r.documentChanges.every(t=>a.string(t.kind)?H.is(t)||X.is(t)||$.is(t):W.is(t)))}e.is=n})(z||(z={}));var oe;(function(e){function n(r){return{uri:r}}e.create=n;function i(r){let t=r;return a.defined(t)&&a.string(t.uri)}e.is=i})(oe||(oe={}));var ae;(function(e){function n(r,t){return{uri:r,version:t}}e.create=n;function i(r){let t=r;return a.defined(t)&&a.string(t.uri)&&a.integer(t.version)}e.is=i})(ae||(ae={}));var B;(function(e){function n(r,t){return{uri:r,version:t}}e.create=n;function i(r){let t=r;return a.defined(t)&&a.string(t.uri)&&(t.version===null||a.integer(t.version))}e.is=i})(B||(B={}));var se;(function(e){function n(r,t,o,s){return{uri:r,languageId:t,version:o,text:s}}e.create=n;function i(r){let t=r;return a.defined(t)&&a.string(t.uri)&&a.string(t.languageId)&&a.integer(t.version)&&a.string(t.text)}e.is=i})(se||(se={}));var q;(function(e){e.PlainText="plaintext",e.Markdown="markdown";function n(i){const r=i;return r===e.PlainText||r===e.Markdown}e.is=n})(q||(q={}));var P;(function(e){function n(i){const r=i;return a.objectLiteral(i)&&q.is(r.kind)&&a.string(r.value)}e.is=n})(P||(P={}));var v;(function(e){e.Text=1,e.Method=2,e.Function=3,e.Constructor=4,e.Field=5,e.Variable=6,e.Class=7,e.Interface=8,e.Module=9,e.Property=10,e.Unit=11,e.Value=12,e.Enum=13,e.Keyword=14,e.Snippet=15,e.Color=16,e.File=17,e.Reference=18,e.Folder=19,e.EnumMember=20,e.Constant=21,e.Struct=22,e.Event=23,e.Operator=24,e.TypeParameter=25})(v||(v={}));var Q;(function(e){e.PlainText=1,e.Snippet=2})(Q||(Q={}));var ue;(function(e){e.Deprecated=1})(ue||(ue={}));var ce;(function(e){function n(r,t,o){return{newText:r,insert:t,replace:o}}e.create=n;function i(r){const t=r;return t&&a.string(t.newText)&&h.is(t.insert)&&h.is(t.replace)}e.is=i})(ce||(ce={}));var de;(function(e){e.asIs=1,e.adjustIndentation=2})(de||(de={}));var le;(function(e){function n(i){const r=i;return r&&(a.string(r.detail)||r.detail===void 0)&&(a.string(r.description)||r.description===void 0)}e.is=n})(le||(le={}));var fe;(function(e){function n(i){return{label:i}}e.create=n})(fe||(fe={}));var ge;(function(e){function n(i,r){return{items:i||[],isIncomplete:!!r}}e.create=n})(ge||(ge={}));var y;(function(e){function n(r){return r.replace(/[\\`*_{}[\]()#+\-.!]/g,"\\$&")}e.fromPlainText=n;function i(r){const t=r;return a.string(t)||a.objectLiteral(t)&&a.string(t.language)&&a.string(t.value)}e.is=i})(y||(y={}));var he;(function(e){function n(i){let r=i;return!!r&&a.objectLiteral(r)&&(P.is(r.contents)||y.is(r.contents)||a.typedArray(r.contents,y.is))&&(i.range===void 0||h.is(i.range))}e.is=n})(he||(he={}));var ve;(function(e){function n(i,r){return r?{label:i,documentation:r}:{label:i}}e.create=n})(ve||(ve={}));var pe;(function(e){function n(i,r,...t){let o={label:i};return a.defined(r)&&(o.documentation=r),a.defined(t)?o.parameters=t:o.parameters=[],o}e.create=n})(pe||(pe={}));var R;(function(e){e.Text=1,e.Read=2,e.Write=3})(R||(R={}));var me;(function(e){function n(i,r){let t={range:i};return a.number(r)&&(t.kind=r),t}e.create=n})(me||(me={}));var p;(function(e){e.File=1,e.Module=2,e.Namespace=3,e.Package=4,e.Class=5,e.Method=6,e.Property=7,e.Field=8,e.Constructor=9,e.Enum=10,e.Interface=11,e.Function=12,e.Variable=13,e.Constant=14,e.String=15,e.Number=16,e.Boolean=17,e.Array=18,e.Object=19,e.Key=20,e.Null=21,e.EnumMember=22,e.Struct=23,e.Event=24,e.Operator=25,e.TypeParameter=26})(p||(p={}));var _e;(function(e){e.Deprecated=1})(_e||(_e={}));var we;(function(e){function n(i,r,t,o,s){let u={name:i,kind:r,location:{uri:o,range:t}};return s&&(u.containerName=s),u}e.create=n})(we||(we={}));var be;(function(e){function n(i,r,t,o){return o!==void 0?{name:i,kind:r,location:{uri:t,range:o}}:{name:i,kind:r,location:{uri:t}}}e.create=n})(be||(be={}));var ke;(function(e){function n(r,t,o,s,u,f){let d={name:r,detail:t,kind:o,range:s,selectionRange:u};return f!==void 0&&(d.children=f),d}e.create=n;function i(r){let t=r;return t&&a.string(t.name)&&a.number(t.kind)&&h.is(t.range)&&h.is(t.selectionRange)&&(t.detail===void 0||a.string(t.detail))&&(t.deprecated===void 0||a.boolean(t.deprecated))&&(t.children===void 0||Array.isArray(t.children))&&(t.tags===void 0||Array.isArray(t.tags))}e.is=i})(ke||(ke={}));var xe;(function(e){e.Empty="",e.QuickFix="quickfix",e.Refactor="refactor",e.RefactorExtract="refactor.extract",e.RefactorInline="refactor.inline",e.RefactorRewrite="refactor.rewrite",e.Source="source",e.SourceOrganizeImports="source.organizeImports",e.SourceFixAll="source.fixAll"})(xe||(xe={}));var j;(function(e){e.Invoked=1,e.Automatic=2})(j||(j={}));var Ie;(function(e){function n(r,t,o){let s={diagnostics:r};return t!=null&&(s.only=t),o!=null&&(s.triggerKind=o),s}e.create=n;function i(r){let t=r;return a.defined(t)&&a.typedArray(t.diagnostics,F.is)&&(t.only===void 0||a.typedArray(t.only,a.string))&&(t.triggerKind===void 0||t.triggerKind===j.Invoked||t.triggerKind===j.Automatic)}e.is=i})(Ie||(Ie={}));var Ee;(function(e){function n(r,t,o){let s={title:r},u=!0;return typeof t=="string"?(u=!1,s.kind=t):I.is(t)?s.command=t:s.edit=t,u&&o!==void 0&&(s.kind=o),s}e.create=n;function i(r){let t=r;return t&&a.string(t.title)&&(t.diagnostics===void 0||a.typedArray(t.diagnostics,F.is))&&(t.kind===void 0||a.string(t.kind))&&(t.edit!==void 0||t.command!==void 0)&&(t.command===void 0||I.is(t.command))&&(t.isPreferred===void 0||a.boolean(t.isPreferred))&&(t.edit===void 0||z.is(t.edit))}e.is=i})(Ee||(Ee={}));var Le;(function(e){function n(r,t){let o={range:r};return a.defined(t)&&(o.data=t),o}e.create=n;function i(r){let t=r;return a.defined(t)&&h.is(t.range)&&(a.undefined(t.command)||I.is(t.command))}e.is=i})(Le||(Le={}));var Ae;(function(e){function n(r,t){return{tabSize:r,insertSpaces:t}}e.create=n;function i(r){let t=r;return a.defined(t)&&a.uinteger(t.tabSize)&&a.boolean(t.insertSpaces)}e.is=i})(Ae||(Ae={}));var Re;(function(e){function n(r,t,o){return{range:r,target:t,data:o}}e.create=n;function i(r){let t=r;return a.defined(t)&&h.is(t.range)&&(a.undefined(t.target)||a.string(t.target))}e.is=i})(Re||(Re={}));var Pe;(function(e){function n(r,t){return{range:r,parent:t}}e.create=n;function i(r){let t=r;return a.objectLiteral(t)&&h.is(t.range)&&(t.parent===void 0||e.is(t.parent))}e.is=i})(Pe||(Pe={}));var De;(function(e){e.namespace="namespace",e.type="type",e.class="class",e.enum="enum",e.interface="interface",e.struct="struct",e.typeParameter="typeParameter",e.parameter="parameter",e.variable="variable",e.property="property",e.enumMember="enumMember",e.event="event",e.function="function",e.method="method",e.macro="macro",e.keyword="keyword",e.modifier="modifier",e.comment="comment",e.string="string",e.number="number",e.regexp="regexp",e.operator="operator",e.decorator="decorator"})(De||(De={}));var Me;(function(e){e.declaration="declaration",e.definition="definition",e.readonly="readonly",e.static="static",e.deprecated="deprecated",e.abstract="abstract",e.async="async",e.modification="modification",e.documentation="documentation",e.defaultLibrary="defaultLibrary"})(Me||(Me={}));var Ce;(function(e){function n(i){const r=i;return a.objectLiteral(r)&&(r.resultId===void 0||typeof r.resultId=="string")&&Array.isArray(r.data)&&(r.data.length===0||typeof r.data[0]=="number")}e.is=n})(Ce||(Ce={}));var Fe;(function(e){function n(r,t){return{range:r,text:t}}e.create=n;function i(r){const t=r;return t!=null&&h.is(t.range)&&a.string(t.text)}e.is=i})(Fe||(Fe={}));var ye;(function(e){function n(r,t,o){return{range:r,variableName:t,caseSensitiveLookup:o}}e.create=n;function i(r){const t=r;return t!=null&&h.is(t.range)&&a.boolean(t.caseSensitiveLookup)&&(a.string(t.variableName)||t.variableName===void 0)}e.is=i})(ye||(ye={}));var je;(function(e){function n(r,t){return{range:r,expression:t}}e.create=n;function i(r){const t=r;return t!=null&&h.is(t.range)&&(a.string(t.expression)||t.expression===void 0)}e.is=i})(je||(je={}));var Ne;(function(e){function n(r,t){return{frameId:r,stoppedLocation:t}}e.create=n;function i(r){const t=r;return a.defined(t)&&h.is(r.stoppedLocation)}e.is=i})(Ne||(Ne={}));var T;(function(e){e.Type=1,e.Parameter=2;function n(i){return i===1||i===2}e.is=n})(T||(T={}));var G;(function(e){function n(r){return{value:r}}e.create=n;function i(r){const t=r;return a.objectLiteral(t)&&(t.tooltip===void 0||a.string(t.tooltip)||P.is(t.tooltip))&&(t.location===void 0||C.is(t.location))&&(t.command===void 0||I.is(t.command))}e.is=i})(G||(G={}));var Se;(function(e){function n(r,t,o){const s={position:r,label:t};return o!==void 0&&(s.kind=o),s}e.create=n;function i(r){const t=r;return a.objectLiteral(t)&&b.is(t.position)&&(a.string(t.label)||a.typedArray(t.label,G.is))&&(t.kind===void 0||T.is(t.kind))&&t.textEdits===void 0||a.typedArray(t.textEdits,E.is)&&(t.tooltip===void 0||a.string(t.tooltip)||P.is(t.tooltip))&&(t.paddingLeft===void 0||a.boolean(t.paddingLeft))&&(t.paddingRight===void 0||a.boolean(t.paddingRight))}e.is=i})(Se||(Se={}));var Oe;(function(e){function n(i){return{kind:"snippet",value:i}}e.createSnippet=n})(Oe||(Oe={}));var Ue;(function(e){function n(i,r,t,o){return{insertText:i,filterText:r,range:t,command:o}}e.create=n})(Ue||(Ue={}));var Ve;(function(e){function n(i){return{items:i}}e.create=n})(Ve||(Ve={}));var We;(function(e){e.Invoked=0,e.Automatic=1})(We||(We={}));var He;(function(e){function n(i,r){return{range:i,text:r}}e.create=n})(He||(He={}));var Xe;(function(e){function n(i,r){return{triggerKind:i,selectedCompletionInfo:r}}e.create=n})(Xe||(Xe={}));var $e;(function(e){function n(i){const r=i;return a.objectLiteral(r)&&S.is(r.uri)&&a.string(r.name)}e.is=n})($e||($e={}));var ze;(function(e){function n(o,s,u,f){return new wt(o,s,u,f)}e.create=n;function i(o){let s=o;return!!(a.defined(s)&&a.string(s.uri)&&(a.undefined(s.languageId)||a.string(s.languageId))&&a.uinteger(s.lineCount)&&a.func(s.getText)&&a.func(s.positionAt)&&a.func(s.offsetAt))}e.is=i;function r(o,s){let u=o.getText(),f=t(s,(g,_)=>{let w=g.range.start.line-_.range.start.line;return w===0?g.range.start.character-_.range.start.character:w}),d=u.length;for(let g=f.length-1;g>=0;g--){let _=f[g],w=o.offsetAt(_.range.start),l=o.offsetAt(_.range.end);if(l<=d)u=u.substring(0,w)+_.newText+u.substring(l,u.length);else throw new Error("Overlapping edit");d=w}return u}e.applyEdits=r;function t(o,s){if(o.length<=1)return o;const u=o.length/2|0,f=o.slice(0,u),d=o.slice(u);t(f,s),t(d,s);let g=0,_=0,w=0;for(;g<f.length&&_<d.length;)s(f[g],d[_])<=0?o[w++]=f[g++]:o[w++]=d[_++];for(;g<f.length;)o[w++]=f[g++];for(;_<d.length;)o[w++]=d[_++];return o}})(ze||(ze={}));var wt=class{constructor(e,n,i,r){this._uri=e,this._languageId=n,this._version=i,this._content=r,this._lineOffsets=void 0}get uri(){return this._uri}get languageId(){return this._languageId}get version(){return this._version}getText(e){if(e){let n=this.offsetAt(e.start),i=this.offsetAt(e.end);return this._content.substring(n,i)}return this._content}update(e,n){this._content=e.text,this._version=n,this._lineOffsets=void 0}getLineOffsets(){if(this._lineOffsets===void 0){let e=[],n=this._content,i=!0;for(let r=0;r<n.length;r++){i&&(e.push(r),i=!1);let t=n.charAt(r);i=t==="\r"||t===`
`,t==="\r"&&r+1<n.length&&n.charAt(r+1)===`
`&&r++}i&&n.length>0&&e.push(n.length),this._lineOffsets=e}return this._lineOffsets}positionAt(e){e=Math.max(Math.min(e,this._content.length),0);let n=this.getLineOffsets(),i=0,r=n.length;if(r===0)return b.create(0,e);for(;i<r;){let o=Math.floor((i+r)/2);n[o]>e?r=o:i=o+1}let t=i-1;return b.create(t,e-n[t])}offsetAt(e){let n=this.getLineOffsets();if(e.line>=n.length)return this._content.length;if(e.line<0)return 0;let i=n[e.line],r=e.line+1<n.length?n[e.line+1]:this._content.length;return Math.max(Math.min(i+e.character,r),i)}get lineCount(){return this.getLineOffsets().length}},a;(function(e){const n=Object.prototype.toString;function i(l){return typeof l<"u"}e.defined=i;function r(l){return typeof l>"u"}e.undefined=r;function t(l){return l===!0||l===!1}e.boolean=t;function o(l){return n.call(l)==="[object String]"}e.string=o;function s(l){return n.call(l)==="[object Number]"}e.number=s;function u(l,N,dt){return n.call(l)==="[object Number]"&&N<=l&&l<=dt}e.numberRange=u;function f(l){return n.call(l)==="[object Number]"&&-2147483648<=l&&l<=2147483647}e.integer=f;function d(l){return n.call(l)==="[object Number]"&&0<=l&&l<=2147483647}e.uinteger=d;function g(l){return n.call(l)==="[object Function]"}e.func=g;function _(l){return l!==null&&typeof l=="object"}e.objectLiteral=_;function w(l,N){return Array.isArray(l)&&l.every(N)}e.typedArray=w})(a||(a={}));var yt=class{constructor(e,n,i){this._languageId=e,this._worker=n,this._disposables=[],this._listener=Object.create(null);const r=o=>{let s=o.getLanguageId();if(s!==this._languageId)return;let u;this._listener[o.uri.toString()]=o.onDidChangeContent(()=>{window.clearTimeout(u),u=window.setTimeout(()=>this._doValidate(o.uri,s),500)}),this._doValidate(o.uri,s)},t=o=>{c.editor.setModelMarkers(o,this._languageId,[]);let s=o.uri.toString(),u=this._listener[s];u&&(u.dispose(),delete this._listener[s])};this._disposables.push(c.editor.onDidCreateModel(r)),this._disposables.push(c.editor.onWillDisposeModel(t)),this._disposables.push(c.editor.onDidChangeModelLanguage(o=>{t(o.model),r(o.model)})),this._disposables.push(i(o=>{c.editor.getModels().forEach(s=>{s.getLanguageId()===this._languageId&&(t(s),r(s))})})),this._disposables.push({dispose:()=>{c.editor.getModels().forEach(t);for(let o in this._listener)this._listener[o].dispose()}}),c.editor.getModels().forEach(r)}dispose(){this._disposables.forEach(e=>e&&e.dispose()),this._disposables.length=0}_doValidate(e,n){this._worker(e).then(i=>i.doValidation(e.toString())).then(i=>{const r=i.map(o=>kt(e,o));let t=c.editor.getModel(e);t&&t.getLanguageId()===n&&c.editor.setModelMarkers(t,n,r)}).then(void 0,i=>{console.error(i)})}};function bt(e){switch(e){case x.Error:return c.MarkerSeverity.Error;case x.Warning:return c.MarkerSeverity.Warning;case x.Information:return c.MarkerSeverity.Info;case x.Hint:return c.MarkerSeverity.Hint;default:return c.MarkerSeverity.Info}}function kt(e,n){let i=typeof n.code=="number"?String(n.code):n.code;return{severity:bt(n.severity),startLineNumber:n.range.start.line+1,startColumn:n.range.start.character+1,endLineNumber:n.range.end.line+1,endColumn:n.range.end.character+1,message:n.message,code:i,source:n.source}}var xt=class{constructor(e,n){this._worker=e,this._triggerCharacters=n}get triggerCharacters(){return this._triggerCharacters}provideCompletionItems(e,n,i,r){const t=e.uri;return this._worker(t).then(o=>o.doComplete(t.toString(),k(n))).then(o=>{if(!o)return;const s=e.getWordUntilPosition(n),u=new c.Range(n.lineNumber,s.startColumn,n.lineNumber,s.endColumn),f=o.items.map(d=>{const g={label:d.label,insertText:d.insertText||d.label,sortText:d.sortText,filterText:d.filterText,documentation:d.documentation,detail:d.detail,command:Lt(d.command),range:u,kind:Et(d.kind)};return d.textEdit&&(It(d.textEdit)?g.range={insert:m(d.textEdit.insert),replace:m(d.textEdit.replace)}:g.range=m(d.textEdit.range),g.insertText=d.textEdit.newText),d.additionalTextEdits&&(g.additionalTextEdits=d.additionalTextEdits.map(D)),d.insertTextFormat===Q.Snippet&&(g.insertTextRules=c.languages.CompletionItemInsertTextRule.InsertAsSnippet),g});return{isIncomplete:o.isIncomplete,suggestions:f}})}};function k(e){if(e)return{character:e.column-1,line:e.lineNumber-1}}function Te(e){if(e)return{start:{line:e.startLineNumber-1,character:e.startColumn-1},end:{line:e.endLineNumber-1,character:e.endColumn-1}}}function m(e){if(e)return new c.Range(e.start.line+1,e.start.character+1,e.end.line+1,e.end.character+1)}function It(e){return typeof e.insert<"u"&&typeof e.replace<"u"}function Et(e){const n=c.languages.CompletionItemKind;switch(e){case v.Text:return n.Text;case v.Method:return n.Method;case v.Function:return n.Function;case v.Constructor:return n.Constructor;case v.Field:return n.Field;case v.Variable:return n.Variable;case v.Class:return n.Class;case v.Interface:return n.Interface;case v.Module:return n.Module;case v.Property:return n.Property;case v.Unit:return n.Unit;case v.Value:return n.Value;case v.Enum:return n.Enum;case v.Keyword:return n.Keyword;case v.Snippet:return n.Snippet;case v.Color:return n.Color;case v.File:return n.File;case v.Reference:return n.Reference}return n.Property}function D(e){if(e)return{range:m(e.range),text:e.newText}}function Lt(e){return e&&e.command==="editor.action.triggerSuggest"?{id:e.command,title:e.title,arguments:e.arguments}:void 0}var Ge=class{constructor(e){this._worker=e}provideHover(e,n,i){let r=e.uri;return this._worker(r).then(t=>t.doHover(r.toString(),k(n))).then(t=>{if(t)return{range:m(t.range),contents:Rt(t.contents)}})}};function At(e){return e&&typeof e=="object"&&typeof e.kind=="string"}function Be(e){return typeof e=="string"?{value:e}:At(e)?e.kind==="plaintext"?{value:e.value.replace(/[\\`*_{}[\]()#+\-.!]/g,"\\$&")}:{value:e.value}:{value:"```"+e.language+`
`+e.value+"\n```\n"}}function Rt(e){if(e)return Array.isArray(e)?e.map(Be):[Be(e)]}var Je=class{constructor(e){this._worker=e}provideDocumentHighlights(e,n,i){const r=e.uri;return this._worker(r).then(t=>t.findDocumentHighlights(r.toString(),k(n))).then(t=>{if(t)return t.map(o=>({range:m(o.range),kind:Pt(o.kind)}))})}};function Pt(e){switch(e){case R.Read:return c.languages.DocumentHighlightKind.Read;case R.Write:return c.languages.DocumentHighlightKind.Write;case R.Text:return c.languages.DocumentHighlightKind.Text}return c.languages.DocumentHighlightKind.Text}var jt=class{constructor(e){this._worker=e}provideDefinition(e,n,i){const r=e.uri;return this._worker(r).then(t=>t.findDefinition(r.toString(),k(n))).then(t=>{if(t)return[Ye(t)]})}};function Ye(e){return{uri:c.Uri.parse(e.uri),range:m(e.range)}}var Nt=class{constructor(e){this._worker=e}provideReferences(e,n,i,r){const t=e.uri;return this._worker(t).then(o=>o.findReferences(t.toString(),k(n))).then(o=>{if(o)return o.map(Ye)})}},Ze=class{constructor(e){this._worker=e}provideRenameEdits(e,n,i,r){const t=e.uri;return this._worker(t).then(o=>o.doRename(t.toString(),k(n),i)).then(o=>Dt(o))}};function Dt(e){if(!e||!e.changes)return;let n=[];for(let i in e.changes){const r=c.Uri.parse(i);for(let t of e.changes[i])n.push({resource:r,versionId:void 0,textEdit:{range:m(t.range),text:t.newText}})}return{edits:n}}var Ke=class{constructor(e){this._worker=e}provideDocumentSymbols(e,n){const i=e.uri;return this._worker(i).then(r=>r.findDocumentSymbols(i.toString())).then(r=>{if(r)return r.map(t=>Mt(t)?et(t):{name:t.name,detail:"",containerName:t.containerName,kind:tt(t.kind),range:m(t.location.range),selectionRange:m(t.location.range),tags:[]})})}};function Mt(e){return"children"in e}function et(e){return{name:e.name,detail:e.detail??"",kind:tt(e.kind),range:m(e.range),selectionRange:m(e.selectionRange),tags:e.tags??[],children:(e.children??[]).map(n=>et(n))}}function tt(e){let n=c.languages.SymbolKind;switch(e){case p.File:return n.File;case p.Module:return n.Module;case p.Namespace:return n.Namespace;case p.Package:return n.Package;case p.Class:return n.Class;case p.Method:return n.Method;case p.Property:return n.Property;case p.Field:return n.Field;case p.Constructor:return n.Constructor;case p.Enum:return n.Enum;case p.Interface:return n.Interface;case p.Function:return n.Function;case p.Variable:return n.Variable;case p.Constant:return n.Constant;case p.String:return n.String;case p.Number:return n.Number;case p.Boolean:return n.Boolean;case p.Array:return n.Array}return n.Function}var rt=class{constructor(e){this._worker=e}provideLinks(e,n){const i=e.uri;return this._worker(i).then(r=>r.findDocumentLinks(i.toString())).then(r=>{if(r)return{links:r.map(t=>({range:m(t.range),url:t.target}))}})}},nt=class{constructor(e){this._worker=e}provideDocumentFormattingEdits(e,n,i){const r=e.uri;return this._worker(r).then(t=>t.format(r.toString(),null,ot(n)).then(o=>{if(!(!o||o.length===0))return o.map(D)}))}},it=class{constructor(e){this._worker=e,this.canFormatMultipleRanges=!1}provideDocumentRangeFormattingEdits(e,n,i,r){const t=e.uri;return this._worker(t).then(o=>o.format(t.toString(),Te(n),ot(i)).then(s=>{if(!(!s||s.length===0))return s.map(D)}))}};function ot(e){return{tabSize:e.tabSize,insertSpaces:e.insertSpaces}}var St=class{constructor(e){this._worker=e}provideDocumentColors(e,n){const i=e.uri;return this._worker(i).then(r=>r.findDocumentColors(i.toString())).then(r=>{if(r)return r.map(t=>({color:t.color,range:m(t.range)}))})}provideColorPresentations(e,n,i){const r=e.uri;return this._worker(r).then(t=>t.getColorPresentations(r.toString(),n.color,Te(n.range))).then(t=>{if(t)return t.map(o=>{let s={label:o.label};return o.textEdit&&(s.textEdit=D(o.textEdit)),o.additionalTextEdits&&(s.additionalTextEdits=o.additionalTextEdits.map(D)),s})})}},at=class{constructor(e){this._worker=e}provideFoldingRanges(e,n,i){const r=e.uri;return this._worker(r).then(t=>t.getFoldingRanges(r.toString(),n)).then(t=>{if(t)return t.map(o=>{const s={start:o.startLine+1,end:o.endLine+1};return typeof o.kind<"u"&&(s.kind=Ct(o.kind)),s})})}};function Ct(e){switch(e){case A.Comment:return c.languages.FoldingRangeKind.Comment;case A.Imports:return c.languages.FoldingRangeKind.Imports;case A.Region:return c.languages.FoldingRangeKind.Region}}var st=class{constructor(e){this._worker=e}provideSelectionRanges(e,n,i){const r=e.uri;return this._worker(r).then(t=>t.getSelectionRanges(r.toString(),n.map(k))).then(t=>{if(t)return t.map(o=>{const s=[];for(;o;)s.push({range:m(o.range)}),o=o.parent;return s})})}},ut=class extends xt{constructor(e){super(e,[".",":","<",'"',"=","/"])}};function Ot(e){const n=new Qe(e),i=(...t)=>n.getLanguageServiceWorker(...t);let r=e.languageId;c.languages.registerCompletionItemProvider(r,new ut(i)),c.languages.registerHoverProvider(r,new Ge(i)),c.languages.registerDocumentHighlightProvider(r,new Je(i)),c.languages.registerLinkProvider(r,new rt(i)),c.languages.registerFoldingRangeProvider(r,new at(i)),c.languages.registerDocumentSymbolProvider(r,new Ke(i)),c.languages.registerSelectionRangeProvider(r,new st(i)),c.languages.registerRenameProvider(r,new Ze(i)),r==="html"&&(c.languages.registerDocumentFormattingEditProvider(r,new nt(i)),c.languages.registerDocumentRangeFormattingEditProvider(r,new it(i)))}function Ut(e){const n=[],i=[],r=new Qe(e);n.push(r);const t=(...s)=>r.getLanguageServiceWorker(...s);function o(){const{languageId:s,modeConfiguration:u}=e;ct(i),u.completionItems&&i.push(c.languages.registerCompletionItemProvider(s,new ut(t))),u.hovers&&i.push(c.languages.registerHoverProvider(s,new Ge(t))),u.documentHighlights&&i.push(c.languages.registerDocumentHighlightProvider(s,new Je(t))),u.links&&i.push(c.languages.registerLinkProvider(s,new rt(t))),u.documentSymbols&&i.push(c.languages.registerDocumentSymbolProvider(s,new Ke(t))),u.rename&&i.push(c.languages.registerRenameProvider(s,new Ze(t))),u.foldingRanges&&i.push(c.languages.registerFoldingRangeProvider(s,new at(t))),u.selectionRanges&&i.push(c.languages.registerSelectionRangeProvider(s,new st(t))),u.documentFormattingEdits&&i.push(c.languages.registerDocumentFormattingEditProvider(s,new nt(t))),u.documentRangeFormattingEdits&&i.push(c.languages.registerDocumentRangeFormattingEditProvider(s,new it(t)))}return o(),n.push(qe(i)),qe(n)}function qe(e){return{dispose:()=>ct(e)}}function ct(e){for(;e.length;)e.pop().dispose()}export{xt as CompletionAdapter,jt as DefinitionAdapter,yt as DiagnosticsAdapter,St as DocumentColorAdapter,nt as DocumentFormattingEditProvider,Je as DocumentHighlightAdapter,rt as DocumentLinkAdapter,it as DocumentRangeFormattingEditProvider,Ke as DocumentSymbolAdapter,at as FoldingRangeAdapter,Ge as HoverAdapter,Nt as ReferenceAdapter,Ze as RenameAdapter,st as SelectionRangeAdapter,Qe as WorkerManager,k as fromPosition,Te as fromRange,Ut as setupMode,Ot as setupMode1,m as toRange,D as toTextEdit};
