// German Morning — stale-page refresh, theme toggle, sticky Telegram bar on phones.
// No redirects, no cookies, no trackers. localStorage only remembers the theme.
(function () {
  var root = document.documentElement;

  // GitHub Pages lets browsers reuse HTML for 10 minutes. If the deployed build differs
  // from the one this page was built with, reload once (reload revalidates the HTML).
  var build = root.getAttribute('data-build');
  var css = document.querySelector('link[rel="stylesheet"]');
  if (build && css && window.fetch) {
    var versionUrl = css.href.replace(/assets\/css\/styles\.css.*$/, 'version.json');
    fetch(versionUrl + '?t=' + Date.now(), { cache: 'no-store' })
      .then(function (r) { return r.ok ? r.json() : null; })
      .then(function (v) {
        if (!v || !v.build || v.build === build) return;
        var key = 'gm-reloaded:' + v.build;
        try {
          if (sessionStorage.getItem(key)) return; // already tried for this build: no loop
          sessionStorage.setItem(key, '1');
        } catch (e) { return; } // no storage: cannot guard against loops, skip
        location.reload();
      })
      .catch(function () { /* offline or blocked: keep the page as is */ });
  }
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
})();
