// Optional public links only. Never store secrets in site-config.json.
document.addEventListener('DOMContentLoaded', async () => {
  // Quarto inserts before-body includes after its navbar. Put the skip link first
  // in keyboard order while retaining a useful fallback when JavaScript is off.
  const skip = document.querySelector('.skip-link');
  if (skip) document.body.prepend(skip);
  document.getElementById('quarto-content')?.setAttribute('tabindex', '-1');
  // Preserve the native button role; Quarto 1.8 assigns role="menu" here.
  document.querySelector('.navbar-toggler')?.removeAttribute('role');
  for (const category of document.querySelectorAll('.quarto-listing-category .category')) {
    category.setAttribute('role', 'button');
    category.tabIndex = 0;
    const update = () => category.setAttribute('aria-pressed', String(category.classList.contains('active')));
    update();
    new MutationObserver(update).observe(category, {attributes: true, attributeFilter: ['class']});
    category.addEventListener('keydown', event => {
      if (event.key === 'Enter' || event.key === ' ') {
        event.preventDefault();
        category.click();
      }
    });
  }
  for (const filter of document.querySelectorAll('.quarto-listing input.search')) {
    filter.setAttribute('aria-label', 'Filter this archive');
    // List.js listens to keyup; also support paste, dictation, and other input.
    filter.addEventListener('input', () => {
      const id = filter.closest('.quarto-listing')?.id;
      window['quarto-listings']?.[id]?.search(filter.value);
    });
  }
  const target = document.querySelector('[data-social-links]');
  if (!target) return;
  try {
    const script = [...document.scripts].find(s => s.src.endsWith('/assets/site.js'));
    const response = await fetch(new URL('site-config.json', script.src));
    if (!response.ok) throw new Error('Configuration unavailable');
    const config = await response.json();
    for (const [name, url] of Object.entries(config.socialLinks || {})) {
      if (typeof url !== 'string') continue;
      const parsed = new URL(url);
      if (parsed.protocol !== 'https:') continue;
      const link = document.createElement('a');
      link.href = parsed.href;
      link.textContent = name;
      link.className = 'social-link';
      target.append(link);
    }
    if (target.childElementCount) {
      document.querySelector('[data-social-unconfigured]')?.setAttribute('hidden', '');
    }
  } catch (_) {
    // Keep the explicit, accessible unconfigured message visible.
  }
});
