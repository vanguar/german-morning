// German Morning — theme toggle + gentle language suggestion on the root page.
// No redirects, no cookies, no trackers. localStorage only remembers the theme.
(function () {
  var root = document.documentElement;
  var media = window.matchMedia ? window.matchMedia('(prefers-color-scheme: dark)') : null;

  function isDark() {
    var t = root.getAttribute('data-theme');
    if (t === 'dark') return true;
    if (t === 'light') return false;
    return !!(media && media.matches);
  }

  var toggles = document.querySelectorAll('.theme-toggle');
  function sync() {
    for (var i = 0; i < toggles.length; i++) {
      toggles[i].setAttribute('aria-pressed', isDark() ? 'true' : 'false');
    }
  }
  for (var i = 0; i < toggles.length; i++) {
    toggles[i].addEventListener('click', function () {
      var next = isDark() ? 'light' : 'dark';
      root.setAttribute('data-theme', next);
      try { localStorage.setItem('gm-theme', next); } catch (e) { /* storage blocked */ }
      sync();
    });
  }
  if (media) {
    var onChange = function () { sync(); };
    if (media.addEventListener) media.addEventListener('change', onChange);
    else if (media.addListener) media.addListener(onChange);
  }
  sync();

  // Phones: the sticky Telegram bar hides while the hero or final CTA is on screen.
  var bar = document.getElementById('sticky-cta');
  if (bar && 'IntersectionObserver' in window) {
    var seen = {};
    var io = new IntersectionObserver(function (entries) {
      for (var k = 0; k < entries.length; k++) seen[entries[k].target.id] = entries[k].isIntersecting;
      var any = false;
      for (var key in seen) if (seen[key]) any = true;
      bar.classList.toggle('is-hidden', any);
    });
    var targets = ['hero-cta', 'final-cta'];
    for (var m = 0; m < targets.length; m++) {
      var el = document.getElementById(targets[m]);
      if (el) io.observe(el);
    }
  }

  // Root page: highlight the version matching the browser language (Ukrainian by default).
  var box = document.getElementById('suggest');
  if (!box) return;
  var langs = navigator.languages || [navigator.language || ''];
  // The course is taught in Ukrainian or Russian, so those win over German anywhere in the list.
  var codes = [];
  for (var j = 0; j < langs.length; j++) codes.push(String(langs[j] || '').toLowerCase().slice(0, 2));
  var pick = null;
  for (var n = 0; n < codes.length && !pick; n++) if (codes[n] === 'uk' || codes[n] === 'ru') pick = codes[n];
  if (!pick && codes.indexOf('de') !== -1) pick = 'de';
  if (!pick || pick === 'uk') return; // Ukrainian is already the highlighted default
  var def = document.querySelector('[data-lang="uk"]');
  var btn = document.querySelector('[data-lang="' + pick + '"]');
  if (!btn || !def) return;
  def.classList.remove('btn-primary', 'is-suggested');
  def.classList.add('btn-ghost');
  btn.classList.remove('btn-ghost');
  btn.classList.add('btn-primary', 'is-suggested');
  box.lang = pick;
  box.textContent = pick === 'ru'
    ? 'Похоже, вам подойдёт русская версия.'
    : 'Die deutsche Version passt vielleicht besser zu Ihnen.';
})();
