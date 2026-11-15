/* ==========================================================================
   Mascot chatbot widget: behaviour
   Read SPEC.md first.

   Usage on any page:
     <link rel="stylesheet" href="mascot.css">
     <script src="mascot.js"></script>
     <script>
       MascotChat.init({ name: "Sunny", topics: [ ... ] });
     </script>

   This file:
     1. builds the widget's HTML (mascot SVG + chat panel) and adds it to <body>
     2. runs a small state machine: closed -> open -> thinking -> open -> closed
     3. answers questions from CONFIG.topics, or from your own getReply() hook
   ========================================================================== */

(function (global) {
  "use strict";

  /* ------------------------------------------------------------------------
     DEFAULT CONFIG. Anything passed to MascotChat.init() overrides these.
     ------------------------------------------------------------------------ */
  var DEFAULTS = {
    name: "Sunny",
    subtitle: "Ask about what we offer",
    teaser: "Hi! Need a hand?",          // bubble shown beside the closed mascot
    teaserShowAfterMs: 2200,              // delay before the teaser appears
    teaserHideAfterMs: 9000,              // teaser hides itself at this time
    greeting: "Hi, I'm Sunny! Pick a topic below or type your question.",
    fallback: "I don't have that answer yet. Try one of the topics below, or leave your number and we'll call you back.",
    thinkingMs: 750,                      // how long the mascot "thinks" for built-in answers
    topics: [
      { label: "What we offer",
        keywords: ["offer", "service", "provide", "product"],
        answer: "Here is what we provide:\n• Service one\n• Service two\n• Service three" },
      { label: "Pricing",
        keywords: ["price", "pricing", "cost", "fee", "charge", "rate"],
        answer: "Our prices start at ₹___. Tell us what you need and we'll share an exact quote." },
      { label: "Timings",
        keywords: ["time", "timing", "open", "hour", "close", "when"],
        answer: "We're open Monday to Saturday, 10 am to 7 pm." },
      { label: "Contact us",
        keywords: ["contact", "call", "phone", "email", "address", "where", "book", "appointment"],
        answer: "Call or WhatsApp us on +91 _____ _____, or email hello@yoursite.com." }
    ],
    /* Optional: connect a real AI or backend.
       Signature: getReply(text, history) -> Promise<string>
       history is an array of { role: "user" | "bot", text }.
       If it is not set, or it throws, the built-in topic matching is used. */
    getReply: null
  };

  /* ------------------------------------------------------------------------
     SVG ARTWORK
     viewBox is 200 x 200. The body's bottom sits at y=182, which is why every
     motion wrapper pivots at 50% 92% (182/200 ≈ 0.91).
     ------------------------------------------------------------------------ */
  var BODY_PATH = "M100 58C132 58 149 82 149 108C149 140 128 182 100 182C72 182 51 140 51 108C51 82 68 58 100 58Z";

  var MASCOT_SVG =
    '<svg viewBox="0 0 200 200" aria-hidden="true">' +
      /* rays: outer <g> places and angles each ray, inner <rect> is what animates */
      '<g transform="translate(41 50) rotate(-52)"><rect class="mb-ray mb-ray--left" x="-6" y="-14" width="12" height="28" rx="6" fill="#F9A726"/></g>' +
      '<g transform="translate(100 24)"><rect class="mb-ray mb-ray--middle" x="-6" y="-16" width="12" height="32" rx="6" fill="#F9A726"/></g>' +
      '<g transform="translate(159 50) rotate(52)"><rect class="mb-ray mb-ray--right" x="-6" y="-14" width="12" height="28" rx="6" fill="#F9A726"/></g>' +
      /* body */
      '<path class="mb-body" d="' + BODY_PATH + '" fill="#F9A726"/>' +
      /* cheeks */
      '<ellipse class="mb-cheek" cx="72" cy="119" rx="8.5" ry="5.2" fill="#F4743B" opacity=".85"/>' +
      '<ellipse class="mb-cheek" cx="128" cy="119" rx="8.5" ry="5.2" fill="#F4743B" opacity=".85"/>' +
      /* eyes, closed (idle) */
      '<g class="mb-eyes-closed" fill="none" stroke="#3B2314" stroke-width="2.6" stroke-linecap="round">' +
        '<path d="M75 108q7 8 14 0"/><path d="M111 108q7 8 14 0"/>' +
      '</g>' +
      /* eyes, open (chatting) */
      '<g class="mb-eyes-open">' +
        '<g class="mb-eye"><ellipse cx="82" cy="108" rx="4.6" ry="5.6" fill="#3B2314"/><circle cx="83.6" cy="105.8" r="1.5" fill="#fff"/></g>' +
        '<g class="mb-eye"><ellipse cx="118" cy="108" rx="4.6" ry="5.6" fill="#3B2314"/><circle cx="119.6" cy="105.8" r="1.5" fill="#fff"/></g>' +
      '</g>' +
      /* mouth, the little "w" */
      '<path class="mb-mouth" d="M93 120q3.5 6 7 0q3.5 6 7 0" fill="none" stroke="#3B2314" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>' +
    '</svg>';

  /* Static copy of the mascot for the panel header (no animation classes) */
  var HEADER_SVG =
    '<svg viewBox="0 0 200 200" aria-hidden="true">' +
      '<path d="' + BODY_PATH + '" fill="#F9A726"/>' +
      '<rect x="94" y="8" width="12" height="32" rx="6" fill="#F9A726"/>' +
      '<rect x="-6" y="-14" width="12" height="28" rx="6" fill="#F9A726" transform="translate(41 50) rotate(-52)"/>' +
      '<rect x="-6" y="-14" width="12" height="28" rx="6" fill="#F9A726" transform="translate(159 50) rotate(52)"/>' +
      '<g fill="none" stroke="#3B2314" stroke-width="3" stroke-linecap="round">' +
        '<path d="M75 108q7 8 14 0"/><path d="M111 108q7 8 14 0"/><path d="M93 120q3.5 6 7 0q3.5 6 7 0"/>' +
      '</g>' +
    '</svg>';

  var SEND_ICON =
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>';

  /* ------------------------------------------------------------------------
     DOM TEMPLATE
     .mb-root
       ├─ .mb-panel   (dialog: header, log, chips, input form)
       └─ .mb-launcher (button: teaser + tilt > sway > bob > svg)
     ------------------------------------------------------------------------ */
  function template() {
    return (
      '<section class="mb-panel" role="dialog" aria-hidden="true">' +
        '<header class="mb-head">' + HEADER_SVG +
          '<div class="mb-head-text"><p class="mb-name"></p><p class="mb-sub"></p></div>' +
          '<button class="mb-close" type="button" aria-label="Close chat">&times;</button>' +
        '</header>' +
        '<div class="mb-log" aria-live="polite"></div>' +
        '<div class="mb-chips"></div>' +
        '<form class="mb-form" autocomplete="off">' +
          '<input class="mb-input" type="text" placeholder="Type your question" aria-label="Type your question">' +
          '<button class="mb-send" type="submit" aria-label="Send message">' + SEND_ICON + '</button>' +
        '</form>' +
      '</section>' +
      '<button class="mb-launcher" type="button" aria-label="Open chat" aria-expanded="false">' +
        '<span class="mb-teaser" aria-hidden="true"></span>' +
        '<span class="mb-tilt"><span class="mb-sway"><span class="mb-bob">' + MASCOT_SVG + '</span></span></span>' +
      '</button>'
    );
  }

  /* ------------------------------------------------------------------------
     WIDGET
     ------------------------------------------------------------------------ */
  function init(userConfig) {
    if (document.querySelector(".mb-root")) return global.MascotChat; // only one per page

    var cfg = {};
    for (var key in DEFAULTS) cfg[key] = DEFAULTS[key];
    for (key in (userConfig || {})) cfg[key] = userConfig[key];

    var root = document.createElement("div");
    root.className = "mb-root";
    root.innerHTML = template();
    document.body.appendChild(root);

    var panel = root.querySelector(".mb-panel");
    var launcher = root.querySelector(".mb-launcher");
    var closeBtn = root.querySelector(".mb-close");
    var log = root.querySelector(".mb-log");
    var chips = root.querySelector(".mb-chips");
    var form = root.querySelector(".mb-form");
    var input = root.querySelector(".mb-input");

    var panelId = "mb-panel-" + Math.random().toString(36).slice(2, 8);
    panel.id = panelId;
    panel.setAttribute("aria-label", "Chat with " + cfg.name);
    launcher.setAttribute("aria-controls", panelId);
    root.querySelector(".mb-name").textContent = cfg.name;
    root.querySelector(".mb-sub").textContent = cfg.subtitle;
    root.querySelector(".mb-teaser").textContent = cfg.teaser;

    var history = [];   // { role, text }
    var greeted = false;
    var busy = false;

    /* ---- State machine ------------------------------------------------
       data-state on .mb-root drives every visual change in mascot.css:
         "closed"   idle sway, eyes closed, panel hidden
         "open"     calmer sway, eyes open + blinking, panel shown
         "thinking" same as open, plus fast rays and quick hops
       ------------------------------------------------------------------ */
    function setState(state) {
      root.setAttribute("data-state", state);
      var isOpen = state !== "closed";
      panel.setAttribute("aria-hidden", String(!isOpen));
      launcher.setAttribute("aria-expanded", String(isOpen));
      launcher.setAttribute("aria-label", isOpen ? "Close chat" : "Open chat");
    }
    function isOpen() { return root.getAttribute("data-state") !== "closed"; }

    function open() {
      root.setAttribute("data-teaser", "off");
      setState(busy ? "thinking" : "open");
      if (!greeted) { addMsg(cfg.greeting, "bot"); greeted = true; }
      setTimeout(function () { input.focus(); }, 150);
    }
    function close() {
      setState("closed");
      launcher.focus();
    }

    /* ---- Messages ---------------------------------------------------- */
    function addMsg(text, role) {
      var m = document.createElement("div");
      m.className = "mb-msg mb-msg--" + role;
      m.textContent = text;       // textContent, never innerHTML: safe from injected HTML
      log.appendChild(m);
      log.scrollTop = log.scrollHeight;
      history.push({ role: role, text: text });
      return m;
    }

    function showTyping() {
      var t = document.createElement("div");
      t.className = "mb-msg mb-msg--bot mb-typing";
      t.innerHTML = "<i></i><i></i><i></i>";
      log.appendChild(t);
      log.scrollTop = log.scrollHeight;
      return t;
    }

    /* ---- Answering ---------------------------------------------------- */
    function matchTopic(text) {
      var q = text.toLowerCase();
      for (var i = 0; i < cfg.topics.length; i++) {
        var t = cfg.topics[i];
        if (q.indexOf(t.label.toLowerCase()) !== -1) return t;
        var words = t.keywords || [];
        for (var k = 0; k < words.length; k++) {
          if (q.indexOf(words[k].toLowerCase()) !== -1) return t;
        }
      }
      return null;
    }

    function builtInReply(text, topic) {
      var match = topic || matchTopic(text);
      return new Promise(function (resolve) {
        setTimeout(function () { resolve(match ? match.answer : cfg.fallback); }, cfg.thinkingMs);
      });
    }

    function ask(text, topic) {
      if (busy) return;
      busy = true;
      addMsg(text, "user");
      var typing = showTyping();
      setState("thinking");

      var replyPromise;
      if (typeof cfg.getReply === "function" && !topic) {
        replyPromise = Promise.resolve()
          .then(function () { return cfg.getReply(text, history.slice()); })
          .catch(function () { return builtInReply(text); });
      } else {
        replyPromise = builtInReply(text, topic);
      }

      replyPromise.then(function (reply) {
        typing.remove();
        addMsg(String(reply || cfg.fallback), "bot");
        busy = false;
        if (isOpen()) setState("open");
      });
    }

    /* ---- Topic chips ------------------------------------------------- */
    cfg.topics.forEach(function (topic) {
      var b = document.createElement("button");
      b.type = "button";
      b.className = "mb-chip";
      b.textContent = topic.label;
      b.addEventListener("click", function () { ask(topic.label, topic); });
      chips.appendChild(b);
    });

    /* ---- Events ------------------------------------------------------ */
    launcher.addEventListener("click", function () { isOpen() ? close() : open(); });
    closeBtn.addEventListener("click", close);
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && isOpen()) close();
    });
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var text = input.value.trim();
      if (!text) return;
      input.value = "";
      ask(text);
    });

    /* ---- Start ------------------------------------------------------- */
    setState("closed");
    root.setAttribute("data-teaser", "off");
    setTimeout(function () { if (!isOpen()) root.setAttribute("data-teaser", "on"); }, cfg.teaserShowAfterMs);
    setTimeout(function () { root.setAttribute("data-teaser", "off"); }, cfg.teaserHideAfterMs);

    /* Public controls, e.g. MascotChat.open() from a "Chat with us" button */
    global.MascotChat.open = open;
    global.MascotChat.close = close;
    global.MascotChat.ask = function (text) { if (!isOpen()) open(); ask(text); };
    return global.MascotChat;
  }

  global.MascotChat = { init: init };
})(window);
