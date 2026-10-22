// Progressive enhancement only: page content and navigation exist without JavaScript.
(() => {
  const panel = document.querySelector('[data-explore]');
  if (!panel) return;
  const cards = Array.from(panel.querySelectorAll('[data-card]'));
  const buttons = Array.from(panel.querySelectorAll('[data-filter]'));
  const input = panel.querySelector('input[name="q"]');
  const empty = panel.querySelector('[data-empty]');
  const resultSummary = panel.querySelector('#directory-results');
  const params = new URLSearchParams(location.search);
  const aliases = {food:'eat',shopping:'shop',learning:'learn',activity:'experience'};
  let activity = aliases[params.get('activity')] || params.get('activity') || 'all';
  if (!['all','eat','shop','learn','experience'].includes(activity)) activity = 'all';
  const query = (params.get('q') || '').trim();
  if (input) input.value = query;
  const normalize = v => String(v||'').normalize('NFKC').toLocaleLowerCase('ja');
  const refresh = () => {
    let shown = 0;
    const term = normalize(input?.value || '');
    for (const card of cards) {
      const types = (card.getAttribute('data-activity') || '').split(' ');
      const text = normalize(card.getAttribute('data-keywords') || '') + normalize(card.textContent || '');
      const match = (activity==='all'||types.includes(activity)) && (!term||text.includes(term));
      card.hidden = !match;
      if (match) shown++;
    }
    for (const button of buttons) button.setAttribute('aria-pressed',String(button.dataset.filter===activity));
    if (empty) empty.hidden = shown!==0;
    if (resultSummary) resultSummary.textContent = `${shown}件の記録を表示`;
  };
  for (const button of buttons) button.addEventListener('click',() => {activity=button.dataset.filter;refresh()});
  input?.addEventListener('input',refresh);
  refresh();
})();