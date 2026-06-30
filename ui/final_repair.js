const fs = require('fs');
let html = fs.readFileSync('reino_quantico_amazonia.html', 'utf8');

// 1. Full HUD reconstruction (Soberania V6)
const HUD_HTML = `
  <button class="btn fl active" onclick="setMode('floresta')">FLORESTA</button>
  <button class="btn fi" onclick="setMode('fogo')">INCÊNDIO</button>
  <button class="btn re" onclick="setMode('restauro')">RESTAURO</button>
  <button class="btn ni" onclick="setMode('noite')">NOITE</button>
  <button class="btn bi" onclick="setMode('bio')">BIODIVERSIDADE</button>
  <button class="btn do" onclick="setMode('dossel')" style="border-color:#00ff88; color:#00ff88;">DOSSEL</button>
  <div style="width:2px; height:20px; background:rgba(255,255,255,0.1); margin:0 5px;"></div>
  <button class="btn tr" onclick="toggleTactical()" id="btn-filtros">🔍 FILTROS</button>
  <button class="btn" style="border:1px solid #ff00ff; color:#ff00ff;" onclick="toggleGenerativePanel()" id="btn-gen">🧠 IA GENERATIVA</button>
  <button class="btn" style="border:1px solid #ffd700; color:#ffd700;" onclick="toggleTour()">◉ TOUR FOCOS</button>
  <button class="btn rec" onclick="toggleRecord()" id="rec-btn">⏺ GRAVAR</button>
`;
html = html.replace(/<div id="ctrl"[\s\S]*?<\/div>/, `<div id="ctrl">${HUD_HTML}</div>`);

// 2. Generative Panel HTML
if (!html.includes('id="generative-panel"')) {
    const GEN_PANEL = `
<div id="generative-panel" style="position:fixed; bottom:100px; left:50%; transform:translateX(-50%); width:400px; background:rgba(0,10,5,0.95); border:1px solid #ff00ff44; padding:20px; z-index:9999; display:none; backdrop-filter:blur(10px); border-radius:8px;">
  <div style="font-size:12px; color:#ff00ff; letter-spacing:4px; margin-bottom:15px; border-bottom:1px solid #ff00ff22; padding-bottom:8px;">NÚCLEO DE SÍNTESE GENERATIVA V6</div>
  <div style="font-size:10px; color:#fff; line-height:1.6; margin-bottom:15px; opacity:0.8;">
    Ativando o motor de processamento quântico para super-resolução de biomassa e detecção preditiva de ignição. 
    A Redoma V6 utiliza embeddings de GeoLLM para fundir telemetria de radar com sensores de solo.
  </div>
  <button class="gp-action-btn" onclick="activateGenerativeCore()" style="width:100%; padding:12px; background:rgba(255,0,255,0.1); border:1px solid #ff00ff; color:#ff00ff; font-family:monospace; cursor:pointer; letter-spacing:2px; font-size:11px;">INICIAR SÍNTESE DE SINGULARIDADE</button>
</div>
    `;
    html = html.replace('</body>', GEN_PANEL + '\n</body>');
}

// 3. JS Functions (toggleGenerativePanel, activateGenerativeCore, toggleCamada)
const EXTRA_JS = `
window.toggleGenerativePanel = function() {
  const p = document.getElementById('generative-panel');
  p.style.display = p.style.display === 'none' ? 'block' : 'none';
};

window.activateGenerativeCore = function() {
  const btn = document.querySelector('.gp-action-btn');
  btn.textContent = "SINTETIZANDO...";
  btn.style.background = "rgba(255, 0, 255, 0.3)";
  
  treeGroup.children.forEach(tree => {
    tree.children.forEach(c => {
      if(c.geometry.type === 'ConeGeometry') {
        c.material.emissive.setHex(0xff00ff);
        c.material.emissiveIntensity = 2;
      }
    });
  });
  
  setTimeout(() => {
    btn.textContent = "NÚCLEO SINTÉTICO ATIVO";
    btn.style.background = "rgba(0, 255, 136, 0.2)";
    btn.style.borderColor = "#00ff88";
    btn.style.color = "#00ff88";
    
    setTimeout(() => {
       treeGroup.children.forEach(tree => {
         tree.children.forEach(c => {
           if(c.geometry.type === 'ConeGeometry') {
             const origCol = tree.userData.color || 0x0d4a10;
             c.material.emissive.set(new THREE.Color(origCol).multiplyScalar(0.3));
             c.material.emissiveIntensity = 1;
           }
         });
       });
    }, 2000);
  }, 1500);
};

function toggleTactical() {
  const p = document.getElementById('tactical-panel');
  p.classList.toggle('active');
}
`;
html = html.replace('</script>', EXTRA_JS + '\n</script>');

// 4. Layers UI inside Tactical Panel
const LAYERS_UI = `
  <div style="margin-top: 15px; padding-top: 15px; border-top: 1px solid #00f2ff22;">
    <div class="tp-header" style="font-size: 10px; margin-bottom: 15px;">CAMADAS SOBERANAS V6</div>
    <select id="filtro-camada" style="width: 100%; background: #001105; color: #ff00ff; border: 1px solid #ff00ff44; padding: 8px; font-family: monospace; font-size: 10px; outline: none;" onchange="toggleCamada(this.value)">
      <option value="none">NENHUMA CAMADA ATIVA</option>
      <option value="verra">PROJETOS VERRA (CARBONO)</option>
      <option value="ti">TERRAS INDÍGENAS (FUNAI)</option>
      <option value="uc">UNIDADES DE CONSERVAÇÃO</option>
    </select>
  </div>
`;
html = html.replace('<button class="tp-audit-btn"', LAYERS_UI + '\n  <button class="tp-audit-btn"');

fs.writeFileSync('reino_quantico_amazonia.html', html);
console.log("Final V6 UI Restored!");
