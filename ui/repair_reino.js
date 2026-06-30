const fs = require('fs');
let html = fs.readFileSync('reino_quantico_amazonia.html', 'utf8');

// 1. Z-Index Sovereignty (HUD visibility fix)
html = html.replace(/z-index:\d+/g, 'z-index:9999');
html = html.replace(/#ctrl\{position:fixed;top:84px;left:50%;transform:translateX\(-50%\);display:flex;gap:8px;z-index:9999;/, 
    '#ctrl{position:fixed;top:84px;left:50%;transform:translateX(-50%);display:flex;gap:8px;z-index:9999;pointer-events:all !important;');

// 2. Camera & Exposure (NASA Effect & Brightness fix)
html = html.replace(/const camera = new THREE\.PerspectiveCamera\(55, innerWidth\/innerHeight, 0\.1, \d+\);/, 
    'const camera = new THREE.PerspectiveCamera(55, innerWidth/innerHeight, 0.1, 10000);');

if (!html.includes('toneMappingExposure')) {
    html = html.replace(/const renderer = new THREE\.WebGLRenderer\(\{ antialias:true, preserveDrawingBuffer:true \}\);/,
        'const renderer = new THREE.WebGLRenderer({ antialias:true, preserveDrawingBuffer:true });\nrenderer.toneMapping = THREE.ReinhardToneMapping;\nrenderer.toneMappingExposure = 1.8;');
}

// 3. Dossel Mode & Buttons
if (!html.includes("setMode('dossel')")) {
    html = html.replace(/<button class="btn bi" onclick="setMode\('bio'\)">BIODIVERSIDADE<\/button>/,
        '<button class="btn bi" onclick="setMode(\'bio\')">BIODIVERSIDADE</button>\n  <button class="btn do" onclick="setMode(\'dossel\')" style="border-color:#00ff88; color:#00ff88;">DOSSEL</button>');
}

// 4. Dossel logic injection
if (!html.includes('let isDosselMode = false;')) {
    html = html.replace(/let REAL_BIO = \[\];/, 'let REAL_BIO = [];\nlet isDosselMode = false;');
    html = html.replace(/window\.setMode = function\(m\) \{/, 'window.setMode = function(m) {\n  isDosselMode = (m === "dossel");');
    
    // Fix tree colors for Dossel Mode
    html = html.replace(/if\(c\.geometry\.type === 'ConeGeometry'\) \{/g, 
        `if(c.geometry.type === 'ConeGeometry') {
          const origCol = tree.userData.color || 0x0d4a10;
          if (isDosselMode) {
              c.material.emissive.setHex(0x00ff88);
              c.material.emissiveIntensity = 3;
          } else {
              c.material.emissive.set(new THREE.Color(origCol).multiplyScalar(0.3));
              c.material.emissiveIntensity = 1;
          }`);
}

// 5. NASA Zoom & Orbital Points
if (!html.includes('camRadius')) {
    html = html.replace(/let drag=false, px=0, py=0, baseRotY=0, baseRotX=0\.2;/, 
        'let drag=false, px=0, py=0, baseRotY=0, baseRotX=0.2, camRadius=35;');
    
    html = html.replace(/renderer\.domElement\.addEventListener\('wheel',e=>\{if\(!tourActive\) camera\.position\.z=Math\.max\(8,Math\.min\(60,camera\.position\.z\+e\.deltaY\*0\.04\)\);\}\);/,
        'renderer.domElement.addEventListener(\'wheel\',e=>{if(!tourActive) camRadius=Math.max(8,Math.min(1500,camRadius+e.deltaY*0.1));});');
        
    html = html.replace(/camera\.position\.x=Math\.sin\(baseRotY\)\*35;\s*camera\.position\.z=Math\.cos\(baseRotY\)\*35;\s*camera\.position\.y=14\+Math\.sin\(baseRotX\)\*8;\s*camera\.lookAt\(0,3,0\);/,
        `camera.position.x=Math.sin(baseRotY)*camRadius;
    camera.position.z=Math.cos(baseRotY)*camRadius;
    camera.position.y=14 + (camRadius-35)*0.5 + Math.sin(baseRotX)*camRadius*0.2;
    camera.lookAt(0,3,0);`);
}

// 6. NASA Points in initFires
if (!html.includes('EFEITO NASA')) {
    const nasaEffect = `
    // ═══ EFEITO NASA: Visão Orbital Ininterrupta ═══
    if(REAL_FIRES && REAL_FIRES.length > 0) {
        const orbGeo = new THREE.BufferGeometry();
        const pts = [], cols = [];
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
console.log("Diamond Sovereignty Restored!");
