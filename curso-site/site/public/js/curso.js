// Curso Sentinel — progresso local (localStorage), quizzes, testes, bloqueio por nota e corretor de CSV.
(() => {
  const BASE = window.CS_BASE || '/';
  const KEY = 'curso-sentinel-v1';
  const ORDEM = ['m0', 'm2', 'm4'];
  const st = () => JSON.parse(localStorage.getItem(KEY) || '{"aulas":{},"quiz":{},"teste":{},"pratico":{}}');
  const save = (s) => localStorage.setItem(KEY, JSON.stringify(s));
  let DATA = null;
  const el = (t, a = {}, ...kids) => { const e = document.createElement(t); for (const [k, v] of Object.entries(a)) { if (k === 'class') e.className = v; else if (k.startsWith('on')) e.addEventListener(k.slice(2), v); else e.setAttribute(k, v); } kids.flat().forEach(k => e.append(k)); return e; };
  const md = (s) => { const span = document.createElement('span'); span.innerHTML = s.replace(/[&<>]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;' }[c])).replace(/`([^`]+)`/g, '<code>$1</code>'); return span; };

  const moduloAprovado = (s, m) => { const mod = DATA.modulos.find(x => x.id === m); const t = s.teste[m]; const p = s.pratico[m]; return !!(t && t.pct >= mod.minimo && p && p.ok); };
  const moduloLiberado = (s, m) => { const i = ORDEM.indexOf(m); return i <= 0 || moduloAprovado(s, ORDEM[i - 1]); };

  function guard() {
    const g = document.querySelector('[data-modulo]'); if (!g) return;
    const m = g.dataset.modulo, s = st();
    if (moduloLiberado(s, m)) return;
    const prev = ORDEM[ORDEM.indexOf(m) - 1]; const pm = DATA.modulos.find(x => x.id === prev);
    const ov = el('div', { class: 'cs-lock' }, el('div', { class: 'cs-lock-box' },
      el('h2', {}, '🔒 Módulo bloqueado'),
      el('p', {}, `Para liberar, faça o teste do ${pm.titulo.split(' — ')[0]} com pelo menos ${pm.minimo}% e conclua o desafio prático.`),
      el('p', {}, el('a', { href: `${BASE}${prev}/teste/`, class: 'cs-btn' }, 'Ir para o teste'), ' ', el('button', { class: 'cs-btn cs-ghost', onclick: () => ov.remove() }, 'Só dar uma olhada')),
    ));
    document.body.append(ov);
  }

  function quiz(box, perguntas, onDone, chave, revelar = true) {
    const respostas = new Array(perguntas.length).fill(null);
    const lista = el('ol', { class: 'cs-quiz' });
    perguntas.forEach((p, qi) => {
      const fb = el('div', { class: 'cs-fb', hidden: '' });
      const opts = p.opts.map((o, oi) => el('label', { class: 'cs-opt' }, el('input', { type: 'radio', name: `${chave}-${qi}`, onchange: () => { respostas[qi] = oi; } }), md(o)));
      lista.append(el('li', {}, el('p', { class: 'cs-q' }, md(p.q)), ...opts, fb));
    });
    const res = el('div', { class: 'cs-res', 'aria-live': 'polite' });
    const btn = el('button', { class: 'cs-btn', onclick: () => {
      let ok = 0;
      lista.querySelectorAll(':scope > li').forEach((li, qi) => {
        const p = perguntas[qi], fb = li.querySelector('.cs-fb'), certo = respostas[qi] === p.a; if (certo) ok++;
        li.classList.toggle('cs-certo', certo); li.classList.toggle('cs-errado', !certo);
        fb.hidden = false; if (revelar || certo) fb.replaceChildren(el('strong', {}, certo ? '✓ Certo. ' : `✗ Resposta: ${p.opts[p.a]}. `), md(p.exp)); else fb.replaceChildren(el('strong', {}, '✗ Errada. '), 'Revise a aula correspondente e tente de novo.');
      });
      const pct = Math.round(100 * ok / perguntas.length);
      res.textContent = `${ok}/${perguntas.length} (${pct}%)`;
      onDone(ok, pct, res);
    } }, 'Corrigir');
    box.replaceChildren(lista, btn, res);
  }

  function initQuiz() {
    document.querySelectorAll('[data-quiz]').forEach(box => {
      const id = box.dataset.quiz; const aula = DATA.aulas[id];
      quiz(box, aula.quiz, (ok, pct, res) => { const s = st(); s.quiz[id] = { ok, pct, em: Date.now() }; save(s); }, 'q' + id);
      const prev = st().quiz[id]; if (prev) box.prepend(el('p', { class: 'cs-prev' }, `Sua última nota neste quiz: ${prev.ok}/${aula.quiz.length}.`));
    });
    document.querySelectorAll('[data-concluir]').forEach(b => {
      const id = b.dataset.concluir; const marcar = () => { b.textContent = '✓ Aula concluída'; b.classList.add('cs-ok'); };
      if (st().aulas[id]) marcar();
      b.addEventListener('click', () => { const s = st(); s.aulas[id] = Date.now(); save(s); marcar(); progresso(); });
    });
  }

  function initTeste() {
    document.querySelectorAll('[data-teste]').forEach(box => {
      const m = box.dataset.teste; const mod = DATA.modulos.find(x => x.id === m);
      quiz(box, mod.teste, (ok, pct, res) => {
        const s = st(); const best = Math.max(pct, (s.teste[m] || {}).pct || 0); s.teste[m] = { ok, pct: best, em: Date.now() }; save(s);
        res.append(el('div', { class: pct >= mod.minimo ? 'cs-pass' : 'cs-fail' }, pct >= mod.minimo ? ` Aprovado na parte teórica (mínimo ${mod.minimo}%).` : ` Ainda não: o mínimo é ${mod.minimo}%. Revise as explicações e tente de novo.`));
        estado(m); progresso();
      }, 't' + m, false);
    });
  }

  // ---------- corretor de CSV (mesma normalização do grader/corrigir.py) ----------
  function parseCSV(txt) {
    const rows = []; let row = [], cur = '', q = false;
    txt = txt.replace(/\r/g, '');
    for (let i = 0; i < txt.length; i++) {
      const c = txt[i];
      if (q) { if (c === '"') { if (txt[i + 1] === '"') { cur += '"'; i++; } else q = false; } else cur += c; }
      else if (c === '"') q = true; else if (c === ',') { row.push(cur); cur = ''; }
      else if (c === '\n') { row.push(cur); rows.push(row); row = []; cur = ''; } else cur += c;
    }
    if (cur !== '' || row.length) { row.push(cur); rows.push(row); }
    return rows.filter(r => r.some(c => c.trim() !== ''));
  }
  const norm = (v) => { v = String(v ?? '').trim(); if (v !== '' && !isNaN(Number(v))) return Number(v).toFixed(2);
    if (/^\d{4}-\d{2}-\d{2}/.test(v)) { v = v.replace(' ', 'T').replace('+00:00', 'Z').replace(/\.0+Z$/, 'Z'); if (!/Z$/.test(v) && /T\d\d:\d\d:\d\d$/.test(v)) v += 'Z'; } return v; };
  function comparar(colado, esperado) {
    const g = parseCSV(colado), w = parseCSV(esperado);
    if (g.length < 1) return [false, 'Cole o CSV completo, com a linha de cabeçalho.'];
    const gr = g.slice(1).map(r => r.map(norm).join('\u0001')).sort(), wr = w.slice(1).map(r => r.map(norm).join('\u0001')).sort();
    if (g[0].length !== w[0].length) return [false, `O resultado tem ${g[0].length} colunas; o esperado tem ${w[0].length} (${w[0].join(', ')}).`];
    if (gr.length !== wr.length) return [false, `Devolveu ${gr.length} linhas; o esperado são ${wr.length}.`];
    const ok = gr.every((x, i) => x === wr[i]);
    return ok ? [true, 'Bate com o resultado do Kusto real.'] : [false, 'Número de linhas certo, mas os valores não batem.'];
  }

  function initPratico() {
    document.querySelectorAll('[data-pratico]').forEach(box => {
      const m = box.dataset.pratico; const P = DATA.praticos[m]; const resumo = el('div', { class: 'cs-res' });
      const s0 = st(); const notas = (s0.pratico[m] && s0.pratico[m].itens) || {};
      const registrar = () => { const s = st(); const ok = Object.values(notas).filter(Boolean).length; const passou = ok >= P.minimo; s.pratico[m] = { ok: passou, nota: ok, itens: notas }; save(s); resumo.replaceChildren(el('div', { class: passou ? 'cs-pass' : 'cs-fail' }, `Prático: ${ok}/${P.itens.length} — ${passou ? 'aprovado' : `mínimo ${P.minimo}`}`)); estado(m); progresso(); };
      const lista = el('ol', { class: 'cs-quiz' });
      P.itens.forEach(it => {
        const ta = el('textarea', { rows: '5', placeholder: it.tipo === 'saida' ? 'Cole aqui a saída do testar_regra.py' : 'Cole aqui o CSV (kql.py --csv saida.csv)', spellcheck: 'false' });
        const fb = el('div', { class: 'cs-fb' }); if (notas[it.id]) fb.replaceChildren(el('strong', {}, '✓ Já validado anteriormente.'));
        const btn = el('button', { class: 'cs-btn', onclick: () => {
          let ok, msg;
          if (it.tipo === 'saida') { ok = /✓ APROVADO/.test(ta.value) && /203\.0\.113\.\d+/.test(ta.value); msg = ok ? 'Saída aprovada pelo testar_regra.py.' : 'Não encontrei "✓ APROVADO" com um IP 203.0.113.x na saída.'; }
          else [ok, msg] = comparar(ta.value, it.esperado);
          notas[it.id] = ok; fb.replaceChildren(el('strong', {}, ok ? '✓ ' : '✗ '), msg); registrar();
        } }, 'Validar');
        lista.append(el('li', {}, el('p', { class: 'cs-q' }, md(it.enunciado)), ta, btn, fb));
      });
      box.replaceChildren(lista, resumo); if (s0.pratico[m]) registrar();
    });
  }

  function estado(m) {
    const box = document.querySelector(`[data-estado="${m}"]`); if (!box) return;
    const s = st(); const mod = DATA.modulos.find(x => x.id === m); const t = s.teste[m], p = s.pratico[m];
    const prox = ORDEM[ORDEM.indexOf(m) + 1];
    box.replaceChildren(el('p', {}, `Teórico: ${t ? t.pct + '%' : '—'} (mínimo ${mod.minimo}%) · Prático: ${p ? (p.ok ? 'aprovado' : 'pendente') : '—'}`),
      moduloAprovado(s, m) ? el('p', { class: 'cs-pass' }, prox ? `🎉 Módulo concluído! O próximo módulo está liberado.` : '🎉 Módulo concluído!') : el('p', {}, 'Complete as duas partes para liberar o próximo módulo.'));
  }

  function progresso() {
    const box = document.querySelector('[data-progresso]'); if (!box) return; const s = st();
    box.replaceChildren(...DATA.modulos.map(mod => {
      const aulas = mod.aulas.filter(a => s.aulas[a]).length;
      return el('div', { class: 'cs-mod' }, el('strong', {}, mod.titulo), el('progress', { max: mod.aulas.length, value: aulas }),
        el('span', {}, `${aulas}/${mod.aulas.length} aulas · ${moduloAprovado(s, mod.id) ? '✓ aprovado' : moduloLiberado(s, mod.id) ? 'liberado' : '🔒 bloqueado'}`));
    }), el('button', { class: 'cs-btn cs-ghost', onclick: () => { if (confirm('Apagar todo o seu progresso neste navegador?')) { localStorage.removeItem(KEY); location.reload(); } } }, 'Zerar progresso'));
  }

  function glossario() {
    const box = document.querySelector('[data-glossario]'); if (!box) return;
    const inp = el('input', { type: 'search', placeholder: 'Buscar termo… (ex.: join, entidade, NRT)', class: 'cs-busca' });
    const lista = el('dl', { class: 'cs-gloss' });
    const render = () => { const q = inp.value.toLowerCase().normalize('NFD').replace(/\p{M}/gu, '');
      lista.replaceChildren(...DATA.glossario.filter(([t, d]) => (t + ' ' + d).toLowerCase().normalize('NFD').replace(/\p{M}/gu, '').includes(q)).flatMap(([t, d, a]) => [el('dt', {}, t), el('dd', {}, d, ' ', el('a', { href: `${BASE}${a.url}` }, `(Aula ${a.id})`))])); };
    inp.addEventListener('input', render); box.replaceChildren(inp, lista); render();
  }

  async function grafico() {
    const c = document.querySelector('canvas[data-grafico]'); if (!c || !window.Chart) return;
    const rows = parseCSV(await (await fetch(`${BASE}data/render_26.csv`)).text()).slice(1);
    const series = {}; rows.forEach(([t, s, n]) => { (series[s] ||= {})[t] = +n; });
    const xs = [...new Set(rows.map(r => r[0]))].sort();
    const cores = { '200': '#2f9e44', '401': '#e03131', '500': '#f08c00', '503': '#7048e8', '404': '#868e96' };
    new Chart(c, { type: 'line', data: { labels: xs.map(x => x.slice(5, 16).replace('T', ' ')), datasets: Object.keys(series).sort().map(s => ({ label: s, data: xs.map(x => series[s][x] || 0), borderColor: cores[s] || '#1e66f5', tension: .2, pointRadius: 0 })) }, options: { plugins: { title: { display: true, text: 'LojaApi_CL · pedidos por status a cada 30 min (dados reais do Kusto)' } } } });
  }

  fetch(`${BASE}data/curso.json`).then(r => r.json()).then(d => { DATA = d; guard(); initQuiz(); initTeste(); initPratico(); DATA.modulos.forEach(m => estado(m.id)); progresso(); glossario(); grafico(); });
})();
