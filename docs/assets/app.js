/*
 * Hop to Heal — tiny page runtime (no build step, no dependencies).
 *
 * Every page has:
 *   <template id="view"> … HTML with {{holes}} … </template>
 *   <script> class Component extends DCLogic { renderVals() { return {...} } }  HopApp.mount(Component, props) </script>
 *
 * Template rules:
 *   {{name}} / {{item.name}}                 text or attribute value from renderVals()
 *   <sc-if value="{{flag}}"> … </sc-if>      show the inside only when flag is true
 *   <sc-for list="{{items}}" as="item"> …    repeat the inside for each item
 *   onClick="{{fn}}" onInput onChange        event handlers
 *   ref="{{fn}}"                             fn(element) is called once when the element is created
 * Call this.setState({...}) in the page class to change data; the page redraws itself.
 */
(function () {
  'use strict';
  var HOLE = /\{\{\s*([^}]+?)\s*\}\}/g;
  var ONE = /^\{\{\s*([^}]+?)\s*\}\}$/;
  var BOOL = { disabled: 1, checked: 1, selected: 1, hidden: 1, required: 1, readonly: 1, open: 1 };
  var SVG = 'http://www.w3.org/2000/svg';
  function truthy(v) { return !(v === false || v == null || v === '' || v === 'false' || v === 0); }
  function look(scope, path) {
    if (path === 'true') return true;
    if (path === 'false') return false;
    var parts = path.split('.'), v = scope;
    for (var i = 0; i < parts.length; i++) { if (v == null) return undefined; v = v[parts[i]]; }
    return v;
  }
  function parts(text) {
    var out = [], last = 0, m; HOLE.lastIndex = 0;
    while ((m = HOLE.exec(text))) { if (m.index > last) out.push(text.slice(last, m.index)); out.push({ p: m[1] }); last = m.index + m[0].length; }
    if (last < text.length) out.push(text.slice(last));
    return out;
  }
  function fill(ps, scope) { var s = ''; for (var i = 0; i < ps.length; i++) { var x = ps[i]; if (typeof x === 'string') s += x; else { var v = look(scope, x.p); s += v == null ? '' : v; } } return s; }

  // ---- template -> small tree, done once per page ----
  function compile(node) {
    var kids = [];
    node.childNodes.forEach(function (c) {
      if (c.nodeType === 3) { if (c.nodeValue) kids.push({ t: 'text', ps: parts(c.nodeValue) }); return; }
      if (c.nodeType !== 1) return;
      var tag = c.localName, m;
      if (tag === 'sc-if') { m = ONE.exec(c.getAttribute('value') || ''); kids.push({ t: 'if', p: m ? m[1] : 'false', kids: compile(c) }); return; }
      if (tag === 'sc-for') { m = ONE.exec(c.getAttribute('list') || ''); kids.push({ t: 'for', p: m ? m[1] : '', as: c.getAttribute('as') || 'item', kids: compile(c) }); return; }
      var attrs = [];
      for (var i = 0; i < c.attributes.length; i++) {
        var a = c.attributes[i], name = a.name, val = a.value;
        if (name.indexOf('hint-') === 0) continue;
        m = ONE.exec(val);
        if (m && /^on[a-z]+$/.test(name)) attrs.push({ k: 'on', name: name.slice(2), p: m[1] });
        else if (m && name === 'ref') attrs.push({ k: 'ref', p: m[1] });
        else if (m) attrs.push({ k: 'expr', name: name, p: m[1] });
        else if (val.indexOf('{{') >= 0) attrs.push({ k: 'mix', name: name, ps: parts(val) });
        else attrs.push({ k: 'static', name: name, v: val });
      }
      kids.push({ t: 'el', tag: tag, svg: c.namespaceURI === SVG, attrs: attrs, kids: compile(c.localName === 'template' ? c.content : c) });
    });
    return kids;
  }

  // ---- tree + data -> virtual nodes ----
  function render(tree, scope, out) {
    for (var i = 0; i < tree.length; i++) {
      var n = tree[i];
      if (n.t === 'text') { out.push(fill(n.ps, scope)); continue; }
      if (n.t === 'if') { if (truthy(look(scope, n.p))) render(n.kids, scope, out); continue; }
      if (n.t === 'for') {
        var list = look(scope, n.p) || [];
        for (var j = 0; j < list.length; j++) { var s = Object.create(scope); s[n.as] = list[j]; s.index = j; render(n.kids, s, out); }
        continue;
      }
      var v = { tag: n.tag, svg: n.svg, a: {}, p: {}, on: {}, ref: null, k: [] }, type = '';
      for (var q = 0; q < n.attrs.length; q++) {
        var a = n.attrs[q], val;
        if (a.k === 'static') { v.a[a.name] = a.v; if (a.name === 'type') type = a.v; continue; }
        if (a.k === 'mix') { v.a[a.name] = fill(a.ps, scope); continue; }
        val = look(scope, a.p);
        if (a.k === 'on') { if (typeof val === 'function') v.on[a.name] = val; continue; }
        if (a.k === 'ref') { v.ref = val; continue; }
        if (a.name === 'value' && (n.tag === 'input' || n.tag === 'textarea' || n.tag === 'select')) { v.p.value = val == null ? '' : String(val); continue; }
        if (a.name === 'checked') { v.p.checked = truthy(val); continue; }
        if (BOOL[a.name]) { if (truthy(val)) v.a[a.name] = ''; continue; }
        if (val === false || val == null) { if (/^(aria-|data-)/.test(a.name) && val === false) v.a[a.name] = 'false'; continue; }
        v.a[a.name] = String(val);
      }
      // React-style onChange: fires while typing in text fields
      if (v.on.change && (n.tag === 'textarea' || (n.tag === 'input' && !/^(checkbox|radio|file|range|color)$/.test(type)))) { v.on.input = v.on.input || v.on.change; delete v.on.change; }
      render(n.kids, scope, v.k);
      out.push(v);
    }
    return out;
  }

  // ---- virtual nodes -> real page (only changes what changed) ----
  function dispatch(e) { var h = this.__on && this.__on[e.type]; if (h) return h.call(this, e); }
  function listen(el, on) { el.__ev = el.__ev || {}; for (var t in on) if (!el.__ev[t]) { el.__ev[t] = 1; el.addEventListener(t, dispatch); } el.__on = on; }
  function props(el, p) {
    if ('value' in p && el.value !== p.value) el.value = p.value;
    if ('checked' in p && el.checked !== p.checked) el.checked = p.checked;
  }
  function create(v) {
    if (typeof v === 'string') return document.createTextNode(v);
    var el = v.svg ? document.createElementNS(SVG, v.tag) : document.createElement(v.tag);
    for (var name in v.a) el.setAttribute(name, v.a[name]);
    for (var i = 0; i < v.k.length; i++) el.appendChild(create(v.k[i]));
    props(el, v.p); listen(el, v.on);
    if (typeof v.ref === 'function') v.ref(el);
    return el;
  }
  function patch(parent, olds, news) {
    for (var i = 0; i < news.length; i++) {
      var o = olds[i], n = news[i], dom = parent.childNodes[i];
      if (o === undefined || !dom) { parent.appendChild(create(n)); continue; }
      if (typeof n === 'string') {
        if (typeof o === 'string') { if (o !== n) dom.nodeValue = n; } else parent.replaceChild(create(n), dom);
        continue;
      }
      if (typeof o === 'string' || o.tag !== n.tag || o.svg !== n.svg) { parent.replaceChild(create(n), dom); continue; }
      var name;
      for (name in n.a) if (o.a[name] !== n.a[name]) dom.setAttribute(name, n.a[name]);
      for (name in o.a) if (!(name in n.a)) dom.removeAttribute(name);
      patch(dom, o.k, n.k);
      props(dom, n.p); listen(dom, n.on);
    }
    for (var j = olds.length - 1; j >= news.length; j--) { var extra = parent.childNodes[j]; if (extra) parent.removeChild(extra); }
  }

  // ---- page class base ----
  function DCLogic(p) { this.props = p || {}; this.state = {}; }
  DCLogic.prototype.setState = function (patchObj) {
    var add = typeof patchObj === 'function' ? patchObj(this.state) : patchObj;
    this.state = Object.assign({}, this.state, add);
    var self = this;
    if (!this.__queued && this.__draw) { this.__queued = true; Promise.resolve().then(function () { self.__queued = false; self.__draw(); }); }
  };
  DCLogic.prototype.renderVals = function () { return {}; };

  function mount(Component, defaults) {
    var p = Object.assign({}, defaults || {});
    try {
      new URLSearchParams(location.search).forEach(function (val, key) {
        if (!(key in p)) return;
        p[key] = val === 'true' ? true : val === 'false' ? false : (val !== '' && !isNaN(val) && typeof p[key] === 'number') ? Number(val) : val;
      });
    } catch (e) {}
    var root = document.getElementById('app'), tpl = document.getElementById('view');
    var tree = compile(tpl.content), inst = new Component(p), old = [];
    inst.__draw = function () {
      var vals;
      try { vals = inst.renderVals() || {}; } catch (e) { console.error('renderVals failed', e); return; }
      var next = render(tree, vals, []);
      patch(root, old, next); old = next;
    };
    inst.__draw();
    if (typeof inst.componentDidMount === 'function') { try { inst.componentDidMount(); } catch (e) { console.error(e); } }
    window.addEventListener('pagehide', function () { if (typeof inst.componentWillUnmount === 'function') { try { inst.componentWillUnmount(); } catch (e) {} } });
    return inst;
  }

  window.DCLogic = DCLogic;
  window.HopApp = { mount: mount, Logic: DCLogic };
})();
