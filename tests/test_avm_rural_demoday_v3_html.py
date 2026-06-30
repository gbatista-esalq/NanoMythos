import pytest
import os
import re

HTML_PATH = os.path.join(
    os.path.dirname(__file__), '..',
    'AVM_Rural_EntregaFinal_Demoday_v3.html'
)

@pytest.fixture
def html():
    if not os.path.exists(HTML_PATH):
        return ''
    with open(HTML_PATH, 'r', encoding='utf-8') as f:
        return f.read()

# --- estrutura basica ---
def test_file_exists():
    assert os.path.exists(HTML_PATH), 'v3 nao encontrado'

def test_valid_doctype(html):
    assert html.strip().startswith('<!DOCTYPE html>')

def test_has_6_slides(html):
    ids = re.findall(r'id=["\']slide-\d+["\']', html)
    assert len(ids) >= 6, f'Esperado >= 6 slides, encontrado {len(ids)}'

def test_has_slide_1(html):
    assert 'id="slide-1"' in html

def test_has_slide_6(html):
    assert 'id="slide-6"' in html

def test_has_sidebar(html):
    assert 'sidebar' in html

# --- Three.js 3D obrigatorio ---
def test_has_threejs_load(html):
    assert 'loadThree' in html or 'three.min.js' in html, 'loadThree ausente'

def test_has_threejs_cdn(html):
    assert 'cdnjs.cloudflare.com' in html or 'unpkg.com/three' in html, 'CDN Three.js ausente'

def test_has_bg3d_canvas(html):
    assert 'bg3d' in html or 'bg-3d' in html or ('canvas' in html and 'Three' in html.replace('three','Three') or 'canvas' in html), 'canvas 3D ausente'

def test_has_activate_scene(html):
    assert 'activateScene' in html or 'activeScene' in html or 'setScene' in html.lower(), 'activateScene ausente'

def test_has_animate_fn(html):
    assert 'function animate' in html or 'animate = function' in html or 'const animate' in html, 'animate fn ausente'

def test_has_scene_field(html):
    assert 'field' in html.lower() or 'campo' in html.lower(), 'cena field/campo ausente'

def test_has_scene_chaos(html):
    assert 'chaos' in html.lower() or 'caos' in html.lower(), 'cena chaos/caos ausente'

def test_has_scene_net(html):
    assert 'network' in html.lower() or 'net' in html.lower() or 'neural' in html.lower(), 'cena network ausente'

def test_has_scene_orbit(html):
    assert 'orbit' in html.lower(), 'cena orbit ausente'

def test_has_scene_dna(html):
    assert 'dna' in html.lower() or 'DNA' in html, 'cena DNA ausente'

def test_has_mesh_material(html):
    assert 'MeshStandardMaterial' in html or 'MeshPhongMaterial' in html, 'MeshMaterial ausente'

def test_has_ambient_light(html):
    assert 'AmbientLight' in html, 'AmbientLight ausente'

def test_has_tone_mapping(html):
    assert 'toneMapping' in html or 'toneMappingExposure' in html, 'toneMapping ausente'

def test_has_camera_setup(html):
    assert 'PerspectiveCamera' in html, 'PerspectiveCamera ausente'

def test_has_webgl_renderer(html):
    assert 'WebGLRenderer' in html, 'WebGLRenderer ausente'

# --- conteudo obrigatorio ---
def test_has_sebrae(html):
    assert 'SEBRAE' in html or 'Sebrae' in html

def test_has_demoday(html):
    assert 'Demoday' in html or 'demoday' in html

def test_has_jarvis(html):
    assert 'J.A.R.V.I.S' in html or 'JARVIS' in html

def test_has_pipe_fapesp(html):
    assert 'PIPE' in html and 'FAPESP' in html

def test_has_bolsa_equipe(html):
    assert 'bolsa' in html.lower() or 'TT-5A' in html

def test_has_esalq_usp(html):
    assert 'ESALQ' in html and 'USP' in html

def test_has_cac_ltv(html):
    assert '1.200' in html and '14.000' in html

def test_has_ltv_ratio(html):
    assert '11.7' in html

def test_has_seed(html):
    assert '500K' in html or '500.000' in html

def test_has_okrs(html):
    assert 'OKR' in html

def test_has_precificacao(html):
    assert '490' in html and '990' in html and '2.500' in html

def test_has_tam_sam_som(html):
    assert 'TAM' in html and 'SAM' in html and 'SOM' in html

def test_has_founder(html):
    assert 'Gabriel Batista' in html

def test_has_email(html):
    assert 'negocios.gabrielbatista@gmail.com' in html

def test_has_nps(html):
    assert 'NPS' in html

def test_sem_em_dash(html):
    assert '—' not in html

def test_no_relative_img(html):
    bad = re.findall(r'<img[^>]+src=["\'](?!data:|http|https|//)[^"\']+["\']', html)
    assert len(bad) == 0, f'img relativo: {bad}'
