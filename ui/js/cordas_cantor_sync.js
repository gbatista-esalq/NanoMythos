// MOTOR DE NEURO-SINCRONIA E CORDAS DE CANTOR (Three.js)

document.addEventListener("DOMContentLoaded", () => {
    // 1. Aplica classe master no body
    document.body.classList.add('ultradopamina-active');

    // 2. Injeta Canvas para o fundo 3D se não existir
    if (!document.getElementById('cantor-canvas-bg')) {
        const canvasDiv = document.createElement('div');
        canvasDiv.id = 'cantor-canvas-bg';
        document.body.prepend(canvasDiv);
    }

    // 3. Verifica se Three.js está carregado, se não, injeta
    if (typeof THREE === 'undefined') {
        const script = document.createElement('script');
        script.src = "https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js";
        script.onload = initCantorCords;
        document.head.appendChild(script);
    } else {
        initCantorCords();
    }
});

function initCantorCords() {
    // Detecta Contexto da Página para aplicar a Frequência Correta
    const pageUrl = window.location.href.toLowerCase();
    const pageTitle = document.title.toLowerCase();
    
    let profile = "DEFAULT";
    let cordaHz = 0;
    let corPrincipal = 0x00ffff; // Cyan
    let corSecundaria = 0xff00ff; // Magenta

    if (pageUrl.includes("felipe") || pageTitle.includes("felipe")) {
        profile = "FELIPE"; cordaHz = 11.11; corPrincipal = 0xffffff; corSecundaria = 0x00ffaa;
    } else if (pageUrl.includes("goliath") || pageTitle.includes("goliath")) {
        profile = "GOLIATH"; cordaHz = 432.0; corPrincipal = 0xff0000; corSecundaria = 0xff5500;
    } else if (pageUrl.includes("moondo") || pageTitle.includes("moondo") || pageTitle.includes("aline")) {
        profile = "MOONDO"; cordaHz = 528.0; corPrincipal = 0x00ff66; corSecundaria = 0x00aaff;
    } else if (pageUrl.includes("discord") || pageTitle.includes("discord")) {
        profile = "DISCORD"; cordaHz = 445.0; corPrincipal = 0x5865f2; corSecundaria = 0x00ffff;
    } else {
        // Redoma V6 Global (Verde Amarelo)
        profile = "BRASIL_V6"; cordaHz = 528.0; corPrincipal = 0x00ff66; corSecundaria = 0xffcc00;
    }

    console.log(`[ CORDAS DE CANTOR ] Sincronizando Perfil: ${profile} | Frequência: ${cordaHz}Hz`);

    // Renderizador Three.js
    const container = document.getElementById('cantor-canvas-bg');
    const scene = new THREE.Scene();
    scene.fog = new THREE.FogExp2(0x050508, 0.002);

    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.z = 50;

    const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    container.appendChild(renderer.domElement);

    // Sistema de Partículas (A Corda de Cantor em si)
    const particleCount = 5000;
    const geometry = new THREE.BufferGeometry();
    const positions = new Float32Array(particleCount * 3);
    const colors = new Float32Array(particleCount * 3);

    const color1 = new THREE.Color(corPrincipal);
    const color2 = new THREE.Color(corSecundaria);

    for (let i = 0; i < particleCount * 3; i += 3) {
        positions[i] = (Math.random() - 0.5) * 200;
        positions[i+1] = (Math.random() - 0.5) * 200;
        positions[i+2] = (Math.random() - 0.5) * 100;

        const mixedColor = color1.clone().lerp(color2, Math.random());
        colors[i] = mixedColor.r;
        colors[i+1] = mixedColor.g;
        colors[i+2] = mixedColor.b;
    }

    geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));

    const material = new THREE.PointsMaterial({
        size: 0.5,
        vertexColors: true,
        transparent: true,
        opacity: 0.6,
        blending: THREE.AdditiveBlending
    });

    const cordaSystem = new THREE.Points(geometry, material);
    scene.add(cordaSystem);

    let time = 0;
    function animate() {
        requestAnimationFrame(animate);
        time += 0.005 * (cordaHz / 100); // Velocidade baseada na frequência
        
        // Movimento Senoidal (Corda)
        cordaSystem.rotation.y = time;
        cordaSystem.rotation.z = Math.sin(time * 2) * 0.1;
        
        renderer.render(scene, camera);
    }
    animate();

    window.addEventListener('resize', () => {
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
    });

    // Envelopamento Automático: Aplica Ultradopamina Panel em Divs Maiores
    document.querySelectorAll('div').forEach(div => {
        // Regra simples: se tiver padding ou for um container maior, aplica o painel
        const style = window.getComputedStyle(div);
        if (parseInt(style.width) > 300 && parseInt(style.height) > 100 && !div.id.includes("canvas")) {
            div.classList.add('ultradopamina-panel');
        }
    });
}
