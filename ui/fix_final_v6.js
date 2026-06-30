const fs = require('fs');
let html = fs.readFileSync('reino_quantico_amazonia.html', 'utf8');

// Remove blue background test
html = html.replace('scene.background = new THREE.Color(0x0000ff);', '');

// Restore tone mapping for "Diamond" quality
if (!html.includes('renderer.toneMapping = THREE.ReinhardToneMapping;')) {
    html = html.replace('const renderer = new THREE.WebGLRenderer({ antialias:true, preserveDrawingBuffer:true });', 
        'const renderer = new THREE.WebGLRenderer({ antialias:true, preserveDrawingBuffer:true });\nrenderer.toneMapping = THREE.ReinhardToneMapping;\nrenderer.toneMappingExposure = 1.8;');
}

fs.writeFileSync('reino_quantico_amazonia.html', html);
console.log("Back to Diamond Sovereignty!");
