document.addEventListener("DOMContentLoaded", () => {
  fetchGamesAndCache();
});

async function fetchGamesAndCache() {
  try {
    const res = await fetch("/api/juegos");
    if (!res.ok) throw new Error("HTTP " + res.status);
    const juegos = await res.json();
    window.__GV_JUEGOS = juegos;
    renderExplorarIfVisible();
  } catch (err) {
    console.warn("Error cargando /api/juegos:", err);
    // no romper la app si falla; usar fallback mínimo
    window.__GV_JUEGOS = window.__GV_JUEGOS || [
      { id:381210, titulo:"Dead by Daylight", descripcion:"Horror multijugador 4v1.", imagen:"https://cdn.cloudflare.steamstatic.com/steam/apps/381210/header.jpg" }
    ];
    renderExplorarIfVisible();
  }
}

function renderExplorarIfVisible() {
  const lista = document.getElementById("lista-juegos");
  if (!lista) return;
  const juegos = window.__GV_JUEGOS || [];
  lista.innerHTML = "";
  juegos.forEach(j => {
    const card = document.createElement("div");
    card.className = "project-card";
    const img = j.imagen ? `<img src="${j.imagen}" alt="${escapeHtml(j.titulo)}" style="width:100%;height:140px;object-fit:cover;border-radius:8px;">` : "";
    card.innerHTML = `
      ${img}
      <h4>${escapeHtml(j.titulo || "Sin título")}</h4>
      <p>${escapeHtml((j.descripcion||"").slice(0,140))}</p>
      <div style="margin-top:10px;">
        <a href="https://store.steampowered.com/app/${j.id}" target="_blank" class="btn-small">Ver en Steam</a>
      </div>
    `;
    lista.appendChild(card);
  });
}

function escapeHtml(s){ return String(s||"").replace(/[&<>"']/g, c=>({ '&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;' }[c])); }
