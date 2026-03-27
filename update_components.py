import sys

with open("index.html", "r", encoding="utf-8") as f:
    text = f.read()

new_styles = """
    /* --- QUANTIX COMPONENT OVERRIDES --- */
    .score-wrap {
      background: linear-gradient(145deg, var(--surface) 0%, rgba(21, 24, 33, 0.4) 100%);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      box-shadow: 0 4px 24px rgba(0, 0, 0, 0.2);
      backdrop-filter: blur(10px);
      position: relative;
    }
    .score-wrap::before {
      content: '';
      position: absolute;
      top: 0; left: 0; right: 0; height: 1px;
      background: linear-gradient(90deg, transparent, rgba(255,255,255,0.15), transparent);
    }
    .al {
      background: rgba(255, 255, 255, 0.02);
      border: 1px solid rgba(255,255,255,0.05);
      backdrop-filter: blur(5px);
    }
    .al-g { border-left: 2px solid var(--success); box-shadow: inset 20px 0 30px -20px rgba(0, 208, 132, 0.15); }
    .al-w { border-left: 2px solid var(--warn); box-shadow: inset 20px 0 30px -20px rgba(255, 176, 32, 0.15); }
    .al-r { border-left: 2px solid var(--danger); box-shadow: inset 20px 0 30px -20px rgba(255, 77, 77, 0.15); }
    
    .op {
      background: linear-gradient(145deg, var(--surface) 0%, rgba(21, 24, 33, 0.4) 100%);
      border: 1px solid var(--border);
      backdrop-filter: blur(10px);
    }
    .op-a { border-left: 2px solid var(--success); box-shadow: inset 20px 0 40px -20px rgba(0, 208, 132, 0.1); }
    .op-m { border-left: 2px solid var(--warn); box-shadow: inset 20px 0 40px -20px rgba(255, 176, 32, 0.1); }
    .op-b { border-left: 2px solid var(--danger); box-shadow: inset 20px 0 40px -20px rgba(255, 77, 77, 0.1); }
    
    .map-outer {
      background: linear-gradient(145deg, var(--surface) 0%, rgba(21, 24, 33, 0.4) 100%);
      border: 1px solid var(--border);
      box-shadow: 0 4px 24px rgba(0, 0, 0, 0.2);
    }
    
    /* Neon Text for Score/Values */
    .mc-v, .score-num {
      text-shadow: 0 0 20px currentColor;
    }
</style>
"""

text = text.replace("</style>", new_styles)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(text)

print("Quantix overrides injected!")
