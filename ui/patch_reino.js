const fs = require('fs');
let html = fs.readFileSync('reino_quantico_amazonia.html', 'utf8');

// 1. Fix Camera Far Clipping (to fix "escuridão total")
html = html.replace(/const camera = new THREE\.PerspectiveCamera\(55, innerWidth\/innerHeight, 0\.1, \d+\);/, 
    'const camera = new THREE.PerspectiveCamera(55, innerWidth/innerHeight, 0.1, 10000);');

// 2. Add Orbit Zoom and NASA Effect Logic (camRadius up to 1500)
if (!html.includes('let drag=false, px=0, py=0, baseRotY=0, baseRotX=0.2, camRadius=35;')) {
    html = html.replace(/let drag=false, px=0, py=0, baseRotY=0, baseRotX=0.2;/, 
        'let drag=false, px=0, py=0, baseRotY=0, baseRotX=0.2, camRadius=35;');
    
    html = html.replace(/renderer\.domElement\.addEventListener\('wheel',e=>\{if\(!tourActive\) camera\.position\.z=Math\.max\(8,Math\.min\(60,camera\.position\.z\+e\.deltaY\*0\.04\)\);\}\);/,
        'renderer.domElement.addEventListener(\'wheel\',e=>{if(!tourActive) camRadius=Math.max(8,Math.min(1500,camRadius+e.deltaY*0.1));});');
        
    html = html.replace(/camera\.position\.x=Math\.sin\(baseRotY\)\*35;[\s\S]*?camera\.lookAt\(0,3,0\);/,
        `camera.position.x=Math.sin(baseRotY)*camRadius;
    camera.position.z=Math.cos(baseRotY)*camRadius;
    camera.position.y=14 + (camRadius-35)*0.5 + Math.sin(baseRotX)*camRadius*0.2;
    camera.lookAt(0,3,0);`);
}

// 3. Add Layers UI
if (!html.includes('id="filtro-camada"')) {
    const layersUI = `
  <div style="margin-top: 15px; padding-top: 15px; border-top: 1px solid #00f2ff22;">
    <div class="tp-header" style="font-size: 10px; margin-bottom: 15px;">FILTROS QUÂNTICOS & CAMADAS</div>
    <div class="tp-row">
      <span class="tp-label">CAMADAS 3D SOBERANAS:</span>
      <select id="filtro-camada" style="width: 100%; background: #001105; color: #ff00ff; border: 1px solid #ff00ff44; padding: 8px; font-family: monospace; font-size: 10px; outline: none; margin-bottom: 10px; text-transform: uppercase;" onchange="toggleCamada(this.value)">
        <option value="none">NENHUMA CAMADA ATIVA</option>
        <option value="verra">PROJETOS VERRA (CARBONO)</option>
        <option value="ti">TERRAS INDÍGENAS (FUNAI)</option>
        <option value="uc">UNIDADES DE CONSERVAÇÃO</option>
        <option value="car">MAPA CAR</option>
        <option value="deter">ALERTAS DETER</option>
      </select>
    </div>
    `;
    html = html.replace(/<div style="margin-top: 15px; padding-top: 15px; border-top: 1px solid #00f2ff22;">\s*<div class="tp-header".*?>FILTROS QUÂNTICOS<\/div>/, layersUI);
}

// 4. Inject toggleCamada function and converter
if (!html.includes('async function toggleCamada')) {
    const toggleFunc = `
let camadaVerra = null, camadaTI = null, camadaUC = null, camadaCAR = null, camadaDeter = null;
function converterGeoJsonParaThreeJS(geojson, material) {
    const group = new THREE.Group();
    if(!geojson || !geojson.features) return group;
    geojson.features.forEach(f => {
        if(!f.geometry || !f.geometry.coordinates) return;
        const coords = f.geometry.type === 'Polygon' ? f.geometry.coordinates : 
                       f.geometry.type === 'MultiPolygon' ? f.geometry.coordinates.flat(1) : [];
        coords.forEach(ring => {
            if(!Array.isArray(ring)) return;
            const pts = [];
            ring.forEach(c => {
                if(c.length >= 2) {
                    pts.push(new THREE.Vector3((c[0]+60)*8, 0.5, (c[1]+5)*-8));
                }
            });
            if(pts.length > 0) {
                const geo = new THREE.BufferGeometry().setFromPoints(pts);
                group.add(new THREE.Line(geo, material));
            }
        });
    });
    return group;
}
async function toggleCamada(tipo) {
    if(camadaVerra) camadaVerra.visible = false;
    if(camadaTI) camadaTI.visible = false;
    if(camadaUC) camadaUC.visible = false;
    if(camadaCAR) camadaCAR.visible = false;
    if(camadaDeter) camadaDeter.visible = false;

    if(tipo === 'none') {
        document.getElementById('tp-sat').textContent = "SINCROZIA DIAMANTE V6";
        document.getElementById('tp-sat').style.color = "#00f2ff";
        return;
    }
    document.getElementById('tp-sat').textContent = "CARREGANDO CAMADA QUÂNTICA...";
    document.getElementById('tp-sat').style.color = "#ffd700";

    try {
        let res, data;
        if(tipo === 'verra') {
            if(!camadaVerra) {
                res = await fetch('amazonia_legal/data/verra_confronto.json').catch(()=>null);
                if(res && res.ok) data = await res.json();
                camadaVerra = converterGeoJsonParaThreeJS(data, new THREE.LineBasicMaterial({color:0xff00ff, opacity:0.8, transparent:true}));
                scene.add(camadaVerra);
            }
            camadaVerra.visible = true;
            document.getElementById('tp-sat').textContent = "VERRA VCS: SÍNTESE 3D CONCLUÍDA";
            document.getElementById('tp-sat').style.color = "#ff00ff";
        }
        else if(tipo === 'ti') {
            if(!camadaTI) {
                res = await fetch('amazonia_legal/data/terras_indigenas.json').catch(()=>null);
                if(res && res.ok) data = await res.json();
                camadaTI = converterGeoJsonParaThreeJS(data, new THREE.LineBasicMaterial({color:0xffaa00, opacity:0.5, transparent:true}));
                scene.add(camadaTI);
            }
            camadaTI.visible = true;
            document.getElementById('tp-sat').textContent = "TERRAS INDÍGENAS: SÍNTESE 3D CONCLUÍDA";
            document.getElementById('tp-sat').style.color = "#ffaa00";
        }
        else if(tipo === 'uc') {
            if(!camadaUC) {
                res = await fetch('amazonia_legal/data/unidades_conservacao.json').catch(()=>null);
                if(res && res.ok) data = await res.json();
                camadaUC = converterGeoJsonParaThreeJS(data, new THREE.LineBasicMaterial({color:0x00ccff, opacity:0.4, transparent:true}));
                scene.add(camadaUC);
            }
            camadaUC.visible = true;
            document.getElementById('tp-sat').textContent = "UNID. CONSERVAÇÃO: SÍNTESE 3D CONCLUÍDA";
            document.getElementById('tp-sat').style.color = "#00ccff";
        }
    } catch(e) {
        console.error("Erro Camada:", e);
        document.getElementById('tp-sat').textContent = "FALHA NO LINK DE SÍNTESE";
        document.getElementById('tp-sat').style.color = "#ff0000";
    }
}
// ═══ MOTOR DE FILTROS QUÂNTICOS (Pilar 2 & 3) ═══
`;
    html = html.replace(/\/\/ ═══ MOTOR DE FILTROS QUÂNTICOS \(Pilar 2 & 3\) ═══/, toggleFunc);
}

// 5. Add NASA Effect properly (only if REAL_FIRES exist, inside loadVaultData finish)
if (!html.includes('EFEITO NASA')) {
    const nasaEffect = `
    // ═══ EFEITO NASA: Visão Orbital Ininterrupta ═══
    if(REAL_FIRES && REAL_FIRES.length > 0) {
        const orbGeo = new THREE.BufferGeometry();
        const pts = [];
        const cols = [];
        const orbC = new THREE.Color();
        REAL_FIRES.forEach(f => {
            if(!isNaN(f.x) && !isNaN(f.z)) {
                pts.push(f.x, 0.5, f.z);
                orbC.set(colorFromFrp(f.frp));
                cols.push(orbC.r, orbC.g, orbC.b);
            }
        });
        if(pts.length > 0) {
            orbGeo.setAttribute('position', new THREE.Float32BufferAttribute(pts, 3));
            orbGeo.setAttribute('color', new THREE.Float32BufferAttribute(cols, 3));
            const orbMat = new THREE.PointsMaterial({
                size: 2.5, sizeAttenuation: false, vertexColors: true,
                transparent: true, opacity: 0.95, blending: THREE.AdditiveBlending
            });
            const orbitalFires = new THREE.Points(orbGeo, orbMat);
            fireGroup.add(orbitalFires);
        }
    }
`;
    html = html.replace(/pymNeutronGroups\.push\(neutronG\);\s*\}\);/g, "pymNeutronGroups.push(neutronG);\n    });\n" + nasaEffect);
}

fs.writeFileSync('reino_quantico_amazonia.html', html);
console.log("Patched successfully!");
