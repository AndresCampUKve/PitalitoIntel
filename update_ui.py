import re

with open("index.html", "r", encoding="utf-8") as f:
    text = f.read()

# 1. Update font imports
text = text.replace(
    '<link href="https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Syne:wght@400;700;800&display=swap"',
    '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Outfit:wght@400;500;600;700;800&family=DM+Mono:wght@400;500&display=swap"'
)

# 2. Syne -> Inter globally
text = text.replace("'Syne', sans-serif", "'Inter', sans-serif")

# 3. Replace Themes with Quantix Dark Mode
new_css = """    /* ===== THEME (QUANTIX INSPIRED) ===== */
    :root {
      --bg: #0b0e14;
      --surface: #151821;
      --surface2: #1e222d;
      --border: rgba(255, 255, 255, 0.08);
      --text: #ffffff;
      --muted: #8b92a5;
      --accent: #ffffff;
      --accent2: #8b92a5;
      --accent3: #ffffff;
      --danger: #ff4d4d;
      --success: #00d084;
      --warn: #ffb020;
      --purple: #8b5cf6;
      --sb-bg: #0b0e14;
      --sb-text: #ffffff;
      --sb-muted: #6b7280;
      --sb-active: #ffffff;
      --shadow: 0 8px 32px rgba(0, 0, 0, 0.6);
      --radius: 16px;
      --tr: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }

    /* Scrollbar Quantix */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: var(--bg); }
    ::-webkit-scrollbar-thumb { background: var(--surface2); border-radius: 6px; }

    * {"""

text = re.sub(r'/\* ===== THEMES ===== \*/.*?\[data-theme="neon"\] \{.*?\}\s*\*\s*\{', new_css, text, flags=re.DOTALL)

# 4. Remove theme selectors from HTML
text = re.sub(r'<div class="themes">.*?</div>\s*<div class="sb-clock">', '<div class="sb-clock">', text, flags=re.DOTALL)
text = re.sub(r'<div class="l-themes">.*?</div>', '', text, flags=re.DOTALL)
text = text.replace('<body data-theme="minimal">', '<body>')

# 5. Enhance Sidebar styles to match Quantix
new_sb_item = """.sb-item {
      display: flex;
      align-items: center;
      gap: 12px;
      padding: 12px 14px;
      border-radius: 12px;
      cursor: pointer;
      font-size: 13px;
      font-weight: 500;
      color: var(--sb-muted);
      transition: var(--tr);
      border: 1px solid transparent;
      user-select: none;
    }

    .sb-item:hover {
      background: rgba(255, 255, 255, 0.03);
      color: var(--sb-text);
    }

    .sb-item.on {
      background: linear-gradient(90deg, rgba(255,255,255,0.08) 0%, transparent 100%);
      color: var(--sb-active);
      border-color: transparent;
      border-left: 3px solid var(--accent);
      border-radius: 4px 12px 12px 4px;
    }"""
text = re.sub(r'\.sb-item \{.*?\.sb-item\.on \{.*?\}', new_sb_item, text, flags=re.DOTALL)

# Update logo name
text = text.replace(
    ".sb-logo-name {\n      font-size: 17px;\n      font-weight: 800;\n      color: var(--sb-active);\n      margin-top: 2px;\n      letter-spacing: -0.5px;\n    }",
    ".sb-logo-name {\n      font-size: 22px;\n      font-weight: 800;\n      font-family: 'Outfit', sans-serif;\n      color: var(--sb-active);\n      margin-top: 2px;\n      letter-spacing: -0.5px;\n    }"
)

# 6. Enhance Cards (Glassmorphism glow)
new_mc = """.mc {
      background: linear-gradient(145deg, var(--surface) 0%, rgba(21, 24, 33, 0.4) 100%);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 20px 22px;
      box-shadow: 0 4px 24px rgba(0, 0, 0, 0.2);
      transition: var(--tr);
      backdrop-filter: blur(10px);
      position: relative;
      overflow: hidden;
    }
    
    .mc::before {
      content: '';
      position: absolute;
      top: 0; left: 0; right: 0; height: 1px;
      background: linear-gradient(90deg, transparent, rgba(255,255,255,0.15), transparent);
    }

    .mc:hover {
      transform: translateY(-2px);
      box-shadow: 0 8px 32px rgba(255, 255, 255, 0.03), 0 4px 24px rgba(0,0,0,0.4);
      border-color: rgba(255, 255, 255, 0.15);
    }"""
text = re.sub(r'\.mc \{.*?\.mc:hover \{.*?\}', new_mc, text, flags=re.DOTALL)

# 7. Update Page Header structure to look like "Welcome Back"
# e.g., "Clima financiero" -> "Overview / Clima financiero"
# We just add CSS for .ph and .pt to match "Overview / Dashboard"
new_pt = """.pt {
      font-size: 28px;
      font-weight: 600;
      letter-spacing: -0.5px;
      font-family: 'Outfit', sans-serif;
    }
    
    .pt::before {
      content: 'Overview / ';
      font-size: 14px;
      font-weight: 500;
      color: var(--muted);
      font-family: 'Inter', sans-serif;
      display: block;
      margin-bottom: 4px;
      letter-spacing: 0;
    }"""
text = re.sub(r'\.pt \{\s*font-size: 26px;\s*font-weight: 800;\s*letter-spacing: -0\.5px;\s*\}', new_pt, text)

# 8. Remove JS dynamic theme logic
js_to_remove = """      if (!localStorage.getItem('lab_theme')) {
        if (h >= 6 && h < 9) setTheme('minimal', null);
        else if (h >= 9 && h < 12) setTheme('forest', null);
        else if (h >= 12 && h < 18) setTheme('gold', null);
        else if (h >= 18 && h < 21) setTheme('dark', null);
        else setTheme('neon', null);
      }"""
text = text.replace(js_to_remove, "")

# 9. Clean up setTheme references (make it dummy)
text = text.replace("function setTheme(name, el) {", "function setTheme(name, el) { return;\n")

# 10. Map styling to dark mode
new_map_styles = "styles: [{ featureType: 'all', elementType: 'geometry.fill', stylers: [{ color: '#0b0e14' }] }, { featureType: 'water', elementType: 'geometry', stylers: [{ color: '#151821' }] }, { featureType: 'road.highway', elementType: 'geometry', stylers: [{ color: '#1e222d' }] }, { featureType: 'road', elementType: 'labels.text.fill', stylers: [{ color: '#8b92a5' }] }, { featureType: 'road', elementType: 'labels.text.stroke', stylers: [{ color: '#0b0e14' }] }, { featureType: 'landscape', elementType: 'geometry', stylers: [{ color: '#0b0e14' }] }, { featureType: 'poi', elementType: 'geometry', stylers: [{ color: '#151821' }] }, { featureType: 'poi', elementType: 'labels', stylers: [{ visibility: 'off' }] }, { featureType: 'administrative', elementType: 'labels.text.fill', stylers: [{ color: '#ffffff' }] }, { featureType: 'administrative', elementType: 'labels.text.stroke', stylers: [{ color: '#0b0e14' }] }]"
text = re.sub(r"styles: \[\{ featureType: 'all'.*?\]\}\]", new_map_styles, text, flags=re.DOTALL)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(text)

print("UI update complete.")
