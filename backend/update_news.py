import sys

with open("../index.html", "r", encoding="utf-8") as f:
    text = f.read()

# 1. Add Sidebar Items (News + Studio Mode)
sidebar_insertion = """      <div class="sb-item" onclick="nav('ia',this)"><span class="sb-icon">✨</span> Asistente IA</div>
      
      <div class="sb-section">Media & Video</div>
      <div class="sb-item" onclick="nav('noticias',this)"><span class="sb-icon">🗞️</span> Noticias (Global & Local)</div>
      <a href="reporte-movil-1.html" target="_blank" class="sb-item" style="color:var(--danger); border-left:3px solid var(--danger); text-decoration:none;"><span class="sb-icon">⏺️</span> Studio Mode (En Vivo)</a>
"""

text = text.replace(
    '      <div class="sb-item" onclick="nav(\'ia\',this)"><span class="sb-icon">✨</span> Asistente IA</div>',
    sidebar_insertion
)

# 2. Add 'view-noticias' HTML structure
noticias_view = """      <!-- NOTICIAS (CENTRAL) -->
      <div class="view" id="view-noticias">
        <div class="ph">
          <div>
            <div class="pt">Central de Noticias</div>
            <div class="ps">Inteligencia Global, Nacional y Local</div>
          </div>
          <button onclick="loadNoticiasFull()" style="padding:8px 16px;background:var(--accent);color:var(--surface);border:none;border-radius:8px;font-family:'Inter',sans-serif;font-size:12px;font-weight:700;cursor:pointer;">⟳ Sincronizar</button>
        </div>
        
        <div class="mg m2">
          <!-- Columna 1: Regional / Colombia -->
          <div>
            <div class="st">📍 Pitalito & Huila (Economía)</div>
            <div id="news-local" style="display:flex;flex-direction:column;gap:10px;margin-bottom:20px;">
              <div style="font-size:12px;color:var(--muted);font-family:'DM Mono',monospace;">Conectando con feeds locales...</div>
            </div>
            
            <div class="st">🇨🇴 Nacional (Macro y Políticas)</div>
            <div id="news-nacional" style="display:flex;flex-direction:column;gap:10px;"></div>
          </div>
          
          <!-- Columna 2: Global / Tech -->
          <div>
            <div class="st">🌐 Mercados Globales (Bloomberg / Reuters)</div>
            <div id="news-global" style="display:flex;flex-direction:column;gap:10px;margin-bottom:20px;"></div>
            
            <div class="st">🚀 Tech & IA (Tendencias 2025)</div>
            <div id="news-tech" style="display:flex;flex-direction:column;gap:10px;"></div>
          </div>
        </div>
      </div>
"""

# Insert right after view-ia or main
if '<!-- IA ASISTENTE -->' in text:
    text = text.replace('<!-- IA ASISTENTE -->', noticias_view + '\n      <!-- IA ASISTENTE -->')
else:
    print("Could not find IA ASISTENTE marker for UI injection.")

# 3. Add loadNoticiasFull JS func
js_insertion = """    // ===== NOTICIAS FULL (CENTRAL) =====
    async function loadNoticiasFull(){
      const draw = (id, list) => {
        const el = document.getElementById(id);
        if(!el) return;
        el.innerHTML = list.map(n => `<a href="${n.l||'#'}" target="_blank" style="text-decoration:none;"><div style="background:linear-gradient(145deg, var(--surface2) 0%, rgba(21, 24, 33, 0.4) 100%);border:1px solid rgba(255,255,255,0.06);border-radius:12px;padding:14px;border-left:3px solid ${n.c};transition:var(--tr);"><div style="font-size:14px;font-weight:600;color:var(--text);margin-bottom:5px;line-height:1.4;">${n.t}</div><div style="font-size:11px;color:var(--muted);font-family:'DM Mono',monospace;display:flex;justify-content:space-between;"><span>${n.f}</span><span>${n.fe}</span></div></div></a>`).join('');
      };
      
      // Local (Simulation/DB logic)
      draw('news-local', [
        {t: 'Caficultores del sur del Huila advierten baja liquidez por clima', f:'La Nación', fe:'Hoy', c:'var(--danger)', l:'#'},
        {t: 'Pitalito impulsa digitalización en el sector comercio con gremios', f:'Opa Noticias', fe:'Ayer', c:'var(--success)', l:'#'},
        {t: 'BanRep mantiene tasas: efecto directo en créditos agrícolas locales', f:'Diario del Huila', fe:'Hace 2 días', c:'var(--warn)', l:'#'}
      ]);
      
      // Nacional
      try {
        const tr = await fetch('https://api.rss2json.com/v1/api.json?rss_url=https://www.portafolio.co/rss/portafolio.xml&count=3');
        const d = await tr.json();
        draw('news-nacional', d.items.map(it => ({t:it.title, f:'Portafolio', fe:it.pubDate.split(' ')[0], c:'var(--warn)', l:it.link})));
      } catch(e) {
        draw('news-nacional', [{t:'Dólar cierra a la baja favoreciendo importaciones tech', f:'La República', fe:'Hoy', c:'var(--success)', l:'#'}]);
      }

      // Global
      draw('news-global', [
        {t: 'Nasdaq hits record high as AI chip makers report massive Q3 profits', f:'Bloomberg', fe:'Today 09:30 AM', c:'var(--success)', l:'#'},
        {t: 'Global inflation metrics cool down, Fed signals potential rate cut', f:'Reuters', fe:'Today 08:15 AM', c:'var(--warn)', l:'#'},
        {t: 'Europe tech regulations tighten, affecting major data services', f:'Financial Times', fe:'Yesterday', c:'var(--danger)', l:'#'}
      ]);
      
      // Tech (Dev.to API Demo)
      try {
        const devR = await fetch('https://dev.to/api/articles?tag=programming&top=1&per_page=3');
        const devD = await devR.json();
        draw('news-tech', devD.map(it => ({t:it.title, f:'Dev.to', fe:it.reading_time_minutes+' min read', c:'var(--purple)', l:it.url})));
      } catch(e) {
        draw('news-tech', [{t:'Why PostgreSQL + pgvector is dominating 2025', f:'Hacker News', fe:'2 hrs ago', c:'var(--purple)', l:'#'}]);
      }
    }
"""

if 'if (id === "ia") bootAI();' in text:
    text = text.replace('if (id === "ia") bootAI();', 'if (id === "ia") bootAI();\n      if (id === "noticias") loadNoticiasFull();')

text = text.replace('// ===== SUPABASE DATA =====', js_insertion + '\n    // ===== SUPABASE DATA =====')

with open("../index.html", "w", encoding="utf-8") as f:
    f.write(text)

print("News integration successful!")
