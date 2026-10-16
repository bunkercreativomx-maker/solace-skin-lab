/* Bunker client photo uploads — per-day photo drop for approval portals.
   Backend: PocketBase collection `client_photos` at aprovaciones.bunkeragent.cloud
   Usage:
     ClientPhotos.init({pb, client, campaign, reviewer, onChange})
     template: ClientPhotos.slot(day)   -> HTML for a card
     after each render(): ClientPhotos.hydrate()
     ClientPhotos.urls(day) -> [full URLs] (for including in the review payload)
*/
(function () {
  const C = { pb: '', client: '', campaign: '', reviewer: '', onChange: null };
  const byDay = {};
  const busy = {};
  const MAX = 25 * 1024 * 1024;
  const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const fileUrl = (r, thumb) => `${C.pb}/api/files/${r.collectionId}/${r.id}/${encodeURIComponent(r.photo)}${thumb ? '?thumb=' + thumb : ''}`;
  const q = s => "'" + String(s).replace(/\\/g, '\\\\').replace(/'/g, "\\'") + "'";

  const css = `.cp-wrap{padding:0 18px 18px}.cp-btn{display:flex;align-items:center;justify-content:center;gap:8px;width:100%;border:1.5px dashed #c9a99a;border-radius:12px;padding:12px;background:#fdf8f4;color:#9a5f52;font:700 12px Inter,system-ui,sans-serif;cursor:pointer;transition:.2s;text-align:center}.cp-btn:hover,.cp-wrap.drag .cp-btn{background:#f6ebe4;border-color:#9a5f52}.cp-btn input{display:none}.cp-btn small{display:block;font-weight:500;opacity:.75;margin-top:2px}.cp-list{display:grid;grid-template-columns:repeat(auto-fill,minmax(76px,1fr));gap:8px;margin-top:10px}.cp-list:empty{display:none}.cp-item{position:relative;border-radius:10px;overflow:hidden;background:#eee7df;aspect-ratio:1;border:1px solid #e3d6cc}.cp-item img{width:100%;height:100%;object-fit:cover;display:block;cursor:zoom-in}.cp-item .cp-x{position:absolute;top:4px;right:4px;width:22px;height:22px;border-radius:50%;border:0;background:rgba(35,28,24,.75);color:#fff;font:700 12px/22px Inter;cursor:pointer;padding:0}.cp-item .cp-name{display:grid;place-items:center;height:100%;font:600 9px Inter;padding:6px;text-align:center;word-break:break-all;color:#6d5c52}.cp-item.loading{display:grid;place-items:center;font:600 10px Inter;color:#9a5f52}.cp-ok{margin-top:8px;font:600 11px Inter;color:#4f8569}`;

  function init(cfg) {
    Object.assign(C, cfg);
    if (!document.getElementById('cp-style')) {
      const st = document.createElement('style'); st.id = 'cp-style'; st.textContent = css; document.head.appendChild(st);
    }
    return load();
  }

  function load() {
    const f = encodeURIComponent(`(client=${q(C.client)}&&campaign=${q(C.campaign)})`);
    return fetch(`${C.pb}/api/collections/client_photos/records?filter=${f}&perPage=500&sort=created`)
      .then(r => r.ok ? r.json() : { items: [] })
      .then(d => {
        Object.keys(byDay).forEach(k => delete byDay[k]);
        (d.items || []).forEach(r => (byDay[r.day] ??= []).push(r));
        hydrate();
      }).catch(() => {});
  }

  function slot(day) {
    return `<div class="cp-wrap" data-cp="${day}"><label class="cp-btn">📷 <span>Have a specific photo for this post? Upload it here<small>Tap to choose from your phone or computer · several allowed</small></span><input type="file" accept="image/*" multiple data-cp-input="${day}"></label><div class="cp-list" data-cp-list="${day}"></div></div>`;
  }

  function listHtml(day) {
    const items = (byDay[day] || []).map(r => {
      const isHeic = /\.(heic|heif)$/i.test(r.photo);
      const inner = isHeic ? `<a class="cp-name" href="${fileUrl(r)}" target="_blank" rel="noopener">${esc(r.photo)}</a>`
        : `<img loading="lazy" src="${fileUrl(r, '400x400')}" data-cp-full="${fileUrl(r)}" alt="Uploaded photo">`;
      return `<div class="cp-item">${inner}<button class="cp-x" title="Remove" data-cp-del="${r.id}" data-cp-day="${day}">✕</button></div>`;
    });
    const n = busy[day] || 0;
    for (let i = 0; i < n; i++) items.push('<div class="cp-item loading">Uploading…</div>');
    return items.join('');
  }

  function hydrate() {
    document.querySelectorAll('[data-cp]').forEach(w => {
      const day = +w.dataset.cp;
      const list = w.querySelector('[data-cp-list]');
      list.innerHTML = listHtml(day);
      let ok = w.querySelector('.cp-ok');
      const count = (byDay[day] || []).length;
      if (count) { if (!ok) { ok = document.createElement('div'); ok.className = 'cp-ok'; w.appendChild(ok) } ok.textContent = `✓ ${count} photo${count > 1 ? 's' : ''} received by Bunker for this post`; }
      else if (ok) ok.remove();
      if (w.dataset.bound) return; w.dataset.bound = 1;
      const input = w.querySelector('[data-cp-input]');
      input.onchange = () => { upload(day, [...input.files]); input.value = ''; };
      w.addEventListener('dragover', e => { e.preventDefault(); w.classList.add('drag') });
      w.addEventListener('dragleave', () => w.classList.remove('drag'));
      w.addEventListener('drop', e => { e.preventDefault(); w.classList.remove('drag'); upload(day, [...e.dataTransfer.files].filter(f => f.type.startsWith('image/') || /\.(heic|heif)$/i.test(f.name))) });
      w.addEventListener('click', e => {
        const del = e.target.closest('[data-cp-del]');
        if (del) { e.preventDefault(); remove(del.dataset.cpDel, +del.dataset.cpDay); return; }
        const img = e.target.closest('[data-cp-full]');
        if (img) { const m = document.getElementById('modal'); if (m) { m.querySelector('img').src = img.dataset.cpFull; m.classList.add('open') } else window.open(img.dataset.cpFull, '_blank') }
      });
    });
  }

  function upload(day, files) {
    files = files.filter(f => { if (f.size > MAX) { alert(`"${f.name}" is larger than 25 MB. Please send a smaller version.`); return false } return true });
    if (!files.length) return;
    busy[day] = (busy[day] || 0) + files.length; hydrate();
    Promise.all(files.map(f => {
      const fd = new FormData();
      fd.append('client', C.client); fd.append('campaign', C.campaign); fd.append('day', day);
      fd.append('client_name', C.reviewer || ''); fd.append('photo', f, f.name);
      return fetch(`${C.pb}/api/collections/client_photos/records`, { method: 'POST', body: fd })
        .then(r => r.ok ? r.json() : r.text().then(t => { throw Error(t) }))
        .then(rec => { (byDay[day] ??= []).push(rec); return true })
        .catch(() => { alert(`Could not upload "${f.name}". Please check your connection and try again.`); return false })
        .finally(() => { busy[day]--; hydrate() });
    })).then(() => { C.onChange && C.onChange() });
  }

  function remove(id, day) {
    if (!confirm('Remove this photo?')) return;
    fetch(`${C.pb}/api/collections/client_photos/records/${id}`, { method: 'DELETE' }).then(r => {
      if (!r.ok) { alert('This photo can no longer be removed from here. Just leave a note and Bunker will ignore it.'); return }
      byDay[day] = (byDay[day] || []).filter(x => x.id !== id); hydrate(); C.onChange && C.onChange();
    });
  }

  window.ClientPhotos = { init, slot, hydrate, reload: load, urls: day => (byDay[day] || []).map(r => fileUrl(r)) };
})();
