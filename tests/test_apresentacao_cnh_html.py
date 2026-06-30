"""
TDD Red: Apresentacao_CNH_Agro_Soberana.html
Verifica estrutura, integridade técnica, dados auditáveis e design premium.
"""
import os
import re
import math

HTML_PATH = os.path.join(
    os.path.dirname(__file__), "..",
    "Apresentacao_CNH_Agro_Soberana.html"
)


def read_html():
    with open(HTML_PATH, encoding="utf-8") as f:
        return f.read()


# --- Estrutura base ---

def test_file_exists():
    assert os.path.exists(HTML_PATH), "HTML não existe"


def test_valid_html_doctype():
    html = read_html()
    assert "<!DOCTYPE html>" in html.lower() or "<!doctype html>" in html.lower()


def test_has_10_slides():
    html = read_html()
    # id="slide-N" é mais robusto que class (active pode estar junto)
    count = len(re.findall(r'id="slide-\d+"', html))
    assert count >= 10, f"Esperado >= 10 slides, encontrado {count}"


def test_slide_navigation_controls():
    html = read_html()
    assert "btn-nav" in html or "nav-btn" in html or "nav-dot" in html or "nav-arrow" in html, \
        "Sem controles de navegação"


def test_has_presenter_notes():
    html = read_html()
    assert "presenter" in html.lower() or "notes" in html.lower() or "roteiro" in html.lower(), \
        "Sem notas de apresentador"


# --- Integridade técnica / dados auditáveis ---

def test_latency_math_cloud_displacement():
    html = read_html()
    # 16.67m ou 16,67m deve aparecer
    assert re.search(r"16[.,]6[67]", html), "Deslocamento nuvem (16.67m) ausente"


def test_latency_edge_value():
    html = read_html()
    # 0.2ms ou 1.1mm deve aparecer
    assert "0.2ms" in html or "0,2ms" in html or "1.1mm" in html or "1,1mm" in html, \
        "Latência borda (<0.2ms) ausente"


def test_math_constants_correct():
    """Verifica que a matemática interna está correta."""
    v = 20 / 3.6  # m/s
    t_cloud = 3.0
    t_edge = 0.0002
    d_cloud = v * t_cloud
    d_edge = v * t_edge
    assert abs(d_cloud - 16.667) < 0.01
    assert abs(d_edge - 0.00111) < 0.00001
    ratio = d_cloud / d_edge
    assert ratio > 14000, f"Ratio deveria ser >14000x, foi {ratio:.0f}"


def test_speed_reference_present():
    html = read_html()
    assert "20 km/h" in html or "20km/h" in html, "Velocidade referência ausente"


# --- Conteúdo estratégico CNH ---

def test_cnh_industrial_reference():
    html = read_html()
    assert "CNH" in html, "CNH Industrial não referenciado"


def test_avm_rural_reference():
    html = read_html()
    assert "AVM" in html, "AVM Rural não referenciado"


def test_lora_mesh_reference():
    html = read_html()
    assert "LoRa" in html or "LORA" in html or "lora" in html, \
        "LoRa Mesh não mencionado"


def test_can_bus_reference():
    html = read_html()
    assert "CAN" in html, "CAN bus não mencionado"


def test_kyber_or_postquantum_reference():
    html = read_html()
    assert "Kyber" in html or "pós-quântic" in html or "post-quantum" in html.lower(), \
        "Segurança pós-quântica não mencionada"


# --- Design premium glassmorphism ---

def test_glassmorphism_css():
    html = read_html()
    assert "backdrop-filter" in html, "backdrop-filter ausente (glassmorphism)"


def test_dark_background_theme():
    html = read_html()
    assert "#0" in html or "rgb(0" in html or "hsl(" in html, \
        "Fundo escuro não configurado"


def test_inter_font():
    html = read_html()
    assert "Inter" in html, "Fonte Inter não carregada"


# --- Simulador interativo ---

def test_interactive_simulator_canvas():
    html = read_html()
    assert "<canvas" in html, "Canvas do simulador ausente"


def test_simulator_mode_toggle():
    html = read_html()
    html_lower = html.lower()
    assert "nuvem" in html_lower and "borda" in html_lower, \
        "Sem toggle NUVEM/BORDA no simulador"


def test_simulator_speed_control():
    html = read_html()
    assert "km/h" in html, "Controle de velocidade ausente no simulador"


# --- Auditoria 360°: consistência física Slide 3 ---

def test_no_markdown_bold_in_html():
    html = read_html()
    assert "**" not in html, "Markdown bold (**) encontrado em HTML — usar <strong>"


def test_slide3_text_consistent_with_diagram():
    html = read_html()
    assert "16,5 metros" not in html and "16.5 metros" not in html, \
        "Valor inconsistente 16.5m ainda presente no texto do Slide 3"


# --- ROI e Métricas Econômicas (CEPEA/ESALQ) ---

def test_cepea_source_cited():
    html = read_html()
    assert "CEPEA" in html, "Fonte CEPEA/ESALQ não citada — credibilidade financeira comprometida"


def test_roi_ha_savings_value():
    html = read_html()
    assert "172" in html, "Valor de economia R$ 172/ha (calculado CEPEA) ausente"


def test_payback_months_stated():
    html = read_html()
    assert "2,1" in html or "Payback" in html or "payback" in html.lower(), \
        "Período de payback em meses não declarado no slide de ROI"


def test_token_or_precision_pricing():
    html = read_html()
    html_lower = html.lower()
    assert "token" in html_lower or "acionamento" in html_lower or "R$ 0,25" in html, \
        "Modelo de cobrança por acionamento de precisão ausente"


# --- Arquitetura de acoplamento (Slide 5) ---

def test_afs_connect_not_replacing():
    html = read_html()
    assert "INALTERADO" in html or "Inalterado" in html, \
        "Slide 5 deve deixar explícito que AFS Connect é 'Inalterado' — não substituto do sistema do trator"


def test_isobus_iso11783_named():
    html = read_html()
    assert "ISOBUS" in html or "ISO 11783" in html, \
        "Protocolo ISOBUS / ISO 11783 não explicitamente nomeado no slide de integração"


# --- Salto Pym Temporal (Slide 6) ---

def test_temporal_pym_spray_waste():
    html = read_html()
    assert "3.333" in html or "3333" in html, \
        "Volume de desperdício por evento (3.333 mL nuvem vs 0,22 mL borda) não presente no visual temporal"


def test_salto_pym_named():
    html = read_html()
    assert "Salto Pym" in html, \
        "Conceito 'Salto Pym' não nomeado explicitamente — relógio temporal ausente"


# --- Evento Cubo Itaú / Piloto concreto (Slide 10) ---

def test_agrointeligente_or_cubo_itau():
    html = read_html()
    assert "Agrointeligente" in html or "Cubo Itaú" in html or "Cubo Itau" in html, \
        "Referência ao evento Agrointeligente / Cubo Itaú ausente — perde o fio vermelho da proposta"


def test_pilot_duration_or_terms():
    html = read_html()
    assert "90 dias" in html or "Q3/2026" in html or "Q3 2026" in html, \
        "Período do piloto não especificado (90 dias / Q3 2026)"


# --- HUD do simulador ---

def test_hud_initial_error_display():
    html = read_html()
    assert ">0.001m<" not in html, \
        "HUD telemetry-error exibe '0.001m' estático — deve ser '1.1mm' como valor inicial de borda"


# --- Slide 11: Mapa Estratégico / Manifestação de Mercado ---

def test_has_at_least_11_slides():
    html = read_html()
    count = len(re.findall(r'id="slide-\d+"', html))
    assert count >= 11, f"Esperado >= 11 slides (inclui manifesto estratégico), encontrado {count}"


def test_tam_latam_market_quantified():
    html = read_html()
    # TAM auditável: 375M ou 46,9M (royalty CNH) ou 3M ha
    assert re.search(r"375M|46[,.]9M|3M ha|3\.000\.000", html), \
        "TAM LatAm não quantificado — slide estratégico deve citar oportunidade de mercado em R$"


def test_cnh_royalty_revenue_explicit():
    html = read_html()
    # Royalty CNH: 31,25 por ha ou 46,9M/ano ou 46.875 por trator
    assert re.search(r"31[,.]25|46[,.]9M|46\.875|royalty", html, re.IGNORECASE), \
        "Receita CNH por royalty não explicitada — modelo de negócio do parceiro ausente"


def test_competitive_window_or_pioneer_context():
    html = read_html()
    html_lower = html.lower()
    assert "pioneirismo" in html_lower or "janela" in html_lower or "oem" in html_lower \
        or "2027" in html or "2028" in html, \
        "Contexto de janela competitiva ou roadmap 2027-2028 ausente no slide estratégico"


def test_roadmap_milestones_2027_2028():
    html = read_html()
    assert "2027" in html and "2028" in html, \
        "Roadmap de execução deve cobrir 2027 e 2028 — não só o piloto de Q3/2026"


def test_strategy_timeline_css_present():
    html = read_html()
    assert "strategy-timeline" in html or "timeline-milestone" in html, \
        "CSS/HTML de timeline estratégico ausente — layout do slide 11 não implementado"


# --- Quantum Lock Screen ---

def test_quantum_lock_screen_exists():
    html = read_html()
    assert "quantum-lock-screen" in html, \
        "Tela de desbloqueio quântico ausente — id=quantum-lock-screen não encontrado"


def test_quantum_lock_screen_has_unlock_function():
    html = read_html()
    assert "unlockPresentation" in html, \
        "Função unlockPresentation() ausente — botão de desbloqueio não tem ação"


def test_quantum_lock_screen_cnh_logo():
    html = read_html()
    assert "data:image/png;base64" in html, \
        "Logo CNH não embutida como base64 — apresentação não funciona offline"


def test_quantum_lock_screen_avm_logo():
    html = read_html()
    # Wordmark real: barra verde #00E676 + texto "RURAL" no SVG do lock screen
    lock_start = html.find('id="quantum-lock-screen"')
    lock_chunk = html[lock_start:lock_start + 4000]
    assert "#00E676" in lock_chunk or "RURAL" in lock_chunk, \
        "Wordmark AVM Rural ausente no lock screen — #00E676 ou texto RURAL não encontrado"


def test_quantum_lock_screen_desbloquear_button():
    html = read_html()
    html_lower = html.lower()
    assert "desbloquear" in html_lower or "unlock" in html_lower, \
        "Botão de desbloqueio sem texto DESBLOQUEAR"


# --- Logos nos Slides 1 e 11 ---

def test_logo_bar_on_slide_1():
    html = read_html()
    slide1_start = html.find('id="slide-1"')
    slide2_start = html.find('id="slide-2"')
    slide1_chunk = html[slide1_start:slide2_start]
    assert "logo-bar" in slide1_chunk or "slide-logo" in slide1_chunk, \
        "Barra de logos ausente no slide 1 (capa de abertura)"


def test_logo_bar_on_slide_11():
    html = read_html()
    slide11_start = html.find('id="slide-11"')
    # Slide 11 has ~6KB content (timeline + logo bar); use generous window
    slide11_chunk = html[slide11_start:slide11_start + 8000]
    assert "logo-bar" in slide11_chunk or "slide-logo" in slide11_chunk, \
        "Barra de logos ausente no slide 11 (capa final)"


# --- Slide 12: Agradecimento + Soberania ---

def test_slide_12_exists():
    html = read_html()
    assert 'id="slide-12"' in html, \
        "Slide 12 (agradecimento) ausente"


def test_slide_12_has_logos():
    html = read_html()
    s12_start = html.find('id="slide-12"')
    s12_chunk = html[s12_start:s12_start + 6000]
    assert "logo-bar" in s12_chunk or "slide-logo" in s12_chunk or \
           ("avm" in s12_chunk.lower() and "cnh" in s12_chunk.lower()), \
        "Slide 12 sem logos AVM Rural e CNH"


def test_slide_12_sovereignty_phrase():
    html = read_html()
    s12_start = html.find('id="slide-12"')
    # Skip base64 blob (~37KB); text content starts after the img tag
    # Search the full slide chunk but skip base64 by looking for visible text
    s12_chunk = html[s12_start:s12_start + 80000].lower()
    # Remove base64 sequences before searching
    clean = re.sub(r'data:image/[^"]+', '', s12_chunk)
    assert "sul global" in clean or "soberania" in clean or "soberan" in clean, \
        "Frase de soberania do Sul Global ausente no slide 12"


def test_slide_12_contact_info():
    html = read_html()
    s12_start = html.find('id="slide-12"')
    s12_chunk = html[s12_start:s12_start + 6000]
    assert "gabrielbatista" in s12_chunk or "gabriel" in s12_chunk.lower() or \
           "contato" in s12_chunk.lower() or "avm" in s12_chunk.lower(), \
        "Slide 12 sem informação de contato"


def test_no_relative_img_src():
    """Toda <img> deve ser base64 inline — zero paths relativos (deck é arquivo único)."""
    html = read_html()
    bad = re.findall(r'<img[^>]+src="(?!data:)[^"]*"', html)
    assert not bad, f"<img> com src relativo encontrado (quebra em arquivo único): {bad}"

def test_total_slides_at_least_12():
    html = read_html()
    count = len(re.findall(r'id="slide-\d+"', html))
    assert count >= 12, f"Esperado >= 12 slides, encontrado {count}"

def test_connectivity_three_channels_present():
    html = read_html()
    assert "conn-tier" in html, "Estrutura de 3 camadas de conectividade ausente"

def test_connectivity_radio_lora_explained():
    html = read_html()
    assert "LoRa" in html or "LoRaWAN" in html, "Canal rádio/LoRa não explicado"
    assert "915" in html or "mesh" in html.lower(), "Protocolo LoRa sem detalhe técnico"

def test_connectivity_satellite_explained():
    html = read_html()
    assert "Starlink" in html or "Inmarsat" in html or "atélite" in html, \
        "Canal satélite não explicado"

def test_connectivity_cloud_afs_coupling():
    html = read_html()
    assert "AFS Connect" in html, "Acoplamento AFS Connect não mencionado"
    assert "Wi-Fi" in html or "galpão" in html, "Sync no galpão não explicado"

def test_connectivity_decision_never_needs_network():
    html = read_html()
    assert "Decisão" in html or "decisão" in html, "Mensagem chave sobre borda autônoma ausente"
    assert "conn-ceb" in html or "BORDO" in html or "bordo" in html.lower(), \
        "Nó central C.E.B. bordo ausente no diagrama"


# --- Apêndice Técnico: 4 slides (13=transição 3D, 14=hardware, 15=ML, 16=decisão) ---

def test_appendix_slides_exist():
    html = read_html()
    assert 'id="slide-13"' in html, "Slide 13 (transição 3D) ausente"
    assert 'id="slide-14"' in html, "Slide 14 (hardware) ausente"
    assert 'id="slide-15"' in html, "Slide 15 (pipeline ML) ausente"
    assert 'id="slide-16"' in html, "Slide 16 (fluxo decisão) ausente"

def test_total_slides_at_least_16():
    html = read_html()
    count = len(re.findall(r'id="slide-\d+"', html))
    assert count >= 16, f"Esperado >= 16 slides (12 principais + 4 apêndice), encontrado {count}"

def test_transition_slide_3d_exists():
    """Slide 13 deve ter canvas Three.js e overlay de texto da cena 3D C.E.B."""
    html = read_html()
    s13_start = html.find('id="slide-13"')
    assert s13_start >= 0, "Slide 13 ausente"
    s13_chunk = html[s13_start:s13_start + 4000]
    assert "ceb3d-canvas" in s13_chunk, "Canvas 3D CEB ausente no slide 13"
    assert "ceb3d-overlay" in s13_chunk or "ceb3d" in s13_chunk, "Overlay 3D ausente no slide 13"

def test_transition_slide_3d_js_loader():
    """JS deve conter lazy loader para Three.js CDN."""
    html = read_html()
    assert "CDN_SCRIPTS" in html or "three.min.js" in html or "three@0.128" in html, \
        "Lazy loader Three.js CDN ausente"
    assert "loadScripts" in html or "createElement" in html, \
        "Injetor dinâmico de scripts Three.js ausente"

def test_transition_slide_numbering():
    """Slide 13 deve mostrar Apêndice · 1 / 4."""
    html = read_html()
    s13_start = html.find('id="slide-13"')
    s13_chunk = html[s13_start:s13_start + 1000]
    assert "1 / 4" in s13_chunk or "1/4" in s13_chunk, "Numeração 1/4 ausente no slide 13"

def test_appendix_hardware_components_labeled():
    html = read_html()
    s14_start = html.find('id="slide-14"')
    s14_chunk = html[s14_start:s14_start + 8000]
    assert "C.E.B" in s14_chunk or "ceb" in s14_chunk.lower(), "Módulo C.E.B. não identificado no slide 14"
    assert "ISOBUS" in s14_chunk or "CAN" in s14_chunk, "Barramento CAN/ISOBUS ausente no slide 14"
    assert "plug" in s14_chunk.lower() or "conector" in s14_chunk.lower(), "Conector plug não mencionado no slide 14"

def test_appendix_ml_pipeline_components():
    html = read_html()
    s15_start = html.find('id="slide-15"')
    s15_chunk = html[s15_start:s15_start + 8000]
    assert "canvas" in s15_chunk.lower() or "grid" in s15_chunk.lower(), "Grid/canvas de campo ausente no slide 15"
    assert "inferência" in s15_chunk.lower() or "modelo" in s15_chunk.lower() or "ml" in s15_chunk.lower(), \
        "Referência ao modelo ML ausente no slide 15"

def test_appendix_decision_flow_timing():
    html = read_html()
    s16_start = html.find('id="slide-16"')
    s16_chunk = html[s16_start:s16_start + 8000]
    assert "0,2" in s16_chunk or "0.2" in s16_chunk, "Latência 0,2ms ausente no slide 16"
    assert "aprendizado" in s16_chunk.lower() or "contínuo" in s16_chunk.lower() or "modelo" in s16_chunk.lower(), \
        "Aprendizado contínuo não mencionado no slide 16"

def test_appendix_navigation_updated():
    html = read_html()
    assert "totalSlides = 16" in html or "totalSlides=16" in html, \
        "totalSlides não atualizado para 16 — navegação quebrada"

def test_appendix_presenter_scripts_exist():
    html = read_html()
    assert "13:" in html or '"13"' in html, "presenterScripts não tem entrada para slide 13"
    assert "14:" in html or '"14"' in html, "presenterScripts não tem entrada para slide 14"
    assert "15:" in html or '"15"' in html, "presenterScripts não tem entrada para slide 15"
    assert "16:" in html or '"16"' in html, "presenterScripts não tem entrada para slide 16"

def test_appendix_tag_labeled_as_appendix():
    html = read_html()
    s13_start = html.find('id="slide-13"')
    s13_chunk = html[s13_start:s13_start + 1000]
    assert "pêndice" in s13_chunk or "Anexo" in s13_chunk or "Técnico" in s13_chunk or "3D" in s13_chunk, \
        "Slide 13 não identificado como apêndice/3D no slide-tag"

def test_appendix_alignment_fixed():
    """Slides 14-16 não devem usar justify-content:flex-start (causa descentralização)."""
    html = read_html()
    for sid in [14, 15, 16]:
        sstart = html.find(f'id="slide-{sid}"')
        if sstart < 0:
            continue
        chunk = html[sstart:sstart + 3000]
        assert "justify-content:flex-start" not in chunk and "justify-content: flex-start" not in chunk, \
            f"Slide {sid} ainda usa justify-content:flex-start — descentralizado"


# --- Slide 13: IDs dos botões interativos, destroyScene, MutationObserver (v2 premium) ---

def test_slide13_btn_cloud_id():
    """Botão 'vs Nuvem' deve ter id='btn-cloud' para o JS ligar o modo cloud."""
    html = read_html()
    s13 = html[html.find('id="slide-13"'):html.find('id="slide-14"')]
    assert 'id="btn-cloud"' in s13, "id='btn-cloud' ausente no slide 13"


def test_slide13_btn_offline_id():
    """Botão 'Offline Total' deve ter id='btn-offline'."""
    html = read_html()
    s13 = html[html.find('id="slide-13"'):html.find('id="slide-14"')]
    assert 'id="btn-offline"' in s13, "id='btn-offline' ausente no slide 13"


def test_slide13_btn_infestation_id():
    """Botão 'Infestação Alta' deve ter id='btn-infestation'."""
    html = read_html()
    s13 = html[html.find('id="slide-13"'):html.find('id="slide-14"')]
    assert 'id="btn-infestation"' in s13, "id='btn-infestation' ausente no slide 13"


def test_slide13_destroyscene_function():
    """destroyScene() deve existir para limpar memória Three.js ao sair do slide 13."""
    html = read_html()
    assert "destroyScene" in html, "destroyScene() ausente — leak de memória Three.js ao navegar"


def test_slide13_mutation_observer():
    """MutationObserver deve observar slide 13 para ativar/destruir cena Three.js automaticamente."""
    html = read_html()
    assert "MutationObserver" in html, "MutationObserver ausente — cena Three.js não ativa/desativa com navegação"


# --- Slide 13 v2 Premium: recursos novos ----------------------------------------

def test_slide13_cdn_fallback():
    """CDN de Three.js deve ter fallback (unpkg) para redes corporativas."""
    html = read_html()
    assert "unpkg.com/three" in html or "unpkg.com" in html, \
        "Fallback CDN Three.js (unpkg) ausente — risco de tela preta em rede CNH"


def test_slide13_data_beams_system():
    """Sistema de data beams (trilha de partículas sensor→chip→bico) deve existir."""
    html = read_html()
    assert "dataBeams" in html, "dataBeams ausente — visualização de fluxo de dados C.E.B. não implementada"
    assert "launchBeam" in html, "launchBeam() ausente — beams de sinal não são disparados"


def test_slide13_mouse_orbit():
    """Canvas deve ter suporte a arrastar para girar a câmera (orbit)."""
    html = read_html()
    assert "orb.dragging" in html or "isDragging" in html, \
        "Mouse orbit ausente — canvas não é interativo para rotação"


def test_slide13_explanation_font_size():
    """Texto de explicação dos modos deve ser >= 0.75rem para legibilidade em projetor."""
    html = read_html()
    match = re.search(r'\.ceb-explanation\s*\{[^}]*font-size:\s*([\d.]+)rem', html)
    assert match, ".ceb-explanation font-size não encontrado"
    size = float(match.group(1))
    assert size >= 0.75, f".ceb-explanation font-size {size}rem < 0.75rem — ilegível em projetor"


# ── Slides 14, 15, 16: 3D Interativo ──────────────────────────────────────────

# Slide 14: Hardware Anatomy 3D Exploded View
def test_slide14_hw3d_canvas_exists():
    """Slide 14 deve ter canvas Three.js id=hw3d-canvas para anatomia 3D explodida."""
    html = read_html()
    s14 = html[html.find('id="slide-14"'):html.find('id="slide-15"')]
    assert 'id="hw3d-canvas"' in s14, "hw3d-canvas ausente no slide 14"


def test_slide14_explode_button():
    """Botão EXPLODIR deve existir no slide 14 para animação de explosão dos componentes."""
    html = read_html()
    s14 = html[html.find('id="slide-14"'):html.find('id="slide-15"')]
    assert 'EXPLODIR' in s14 or 'toggleExplode14' in s14, "Botão EXPLODIR ausente no slide 14"


def test_slide14_component_highlight_buttons():
    """Slide 14 deve ter botões de destaque por componente (①②③④⑤)."""
    html = read_html()
    s14 = html[html.find('id="slide-14"'):html.find('id="slide-15"')]
    count = s14.count('hw3d-comp-btn')
    assert count >= 4, f"Esperado >= 4 botões hw3d-comp-btn no slide 14, encontrado {count}"


def test_slide14_buildHWScene_function():
    """Função buildHWScene deve existir no JS para inicializar a cena 3D de hardware."""
    html = read_html()
    assert 'buildHWScene' in html, "buildHWScene() ausente — slide 14 sem cena 3D"


def test_slide14_explode_mode_var():
    """Variável explodeMode deve existir para animar a explosão dos componentes."""
    html = read_html()
    assert 'explodeMode' in html, "explodeMode ausente — animação de explosão não implementada"


# Slide 15: ML Pipeline 3D
def test_slide15_ml3d_canvas_exists():
    """Slide 15 deve ter canvas Three.js id=ml3d-canvas para pipeline 3D."""
    html = read_html()
    s15_start = html.find('id="slide-15"')
    s15_end = html.find('id="slide-16"')
    s15 = html[s15_start:s15_end]
    assert 'id="ml3d-canvas"' in s15, "ml3d-canvas ausente no slide 15"


def test_slide15_pipeline_3d_stations():
    """buildMLScene deve existir para as 4 estações 3D do pipeline de IA."""
    html = read_html()
    assert 'buildMLScene' in html, "buildMLScene() ausente — pipeline 3D do slide 15 não implementado"


def test_slide15_flow_particles():
    """Sistema de partículas de fluxo de dados (flowParticles ou mlBeams) deve existir."""
    html = read_html()
    assert 'flowParticles' in html or 'mlBeams' in html or 'mlParticles' in html, \
        "Partículas de fluxo ML ausentes — visualização de dados no pipeline não implementada"


def test_slide15_stage_focus_buttons():
    """Slide 15 deve ter botões para focar em cada estágio do pipeline."""
    html = read_html()
    s15_start = html.find('id="slide-15"')
    s15_end = html.find('id="slide-16"')
    s15 = html[s15_start:s15_end]
    assert 'focusMLStage' in s15 or 'ml3d-stage-btn' in s15, \
        "Botões de foco por estágio ausentes no slide 15"


# Slide 16: Decision Cycle 3D
def test_slide16_flow3d_canvas_exists():
    """Slide 16 deve ter canvas Three.js id=flow3d-canvas para ciclo de decisão 3D."""
    html = read_html()
    s16_start = html.find('id="slide-16"')
    s16 = html[s16_start:s16_start + 12000]
    assert 'id="flow3d-canvas"' in s16, "flow3d-canvas ausente no slide 16"


def test_slide16_decision_ring():
    """buildFlowScene deve existir para o anel de decisão 3D com os 4 nós."""
    html = read_html()
    assert 'buildFlowScene' in html, "buildFlowScene() ausente — ciclo de decisão 3D não implementado"


def test_slide16_fleet_visual():
    """Visual de fleet learning (fleetTractors) deve existir no slide 16."""
    html = read_html()
    assert 'fleetTractors' in html or 'tractorFleet' in html, \
        "fleetTractors ausente — fleet learning 3D não implementado"


def test_slide16_spray_trigger():
    """Função triggerSpray3D deve existir para acionar ciclo de spray interativo."""
    html = read_html()
    assert 'triggerSpray3D' in html, "triggerSpray3D() ausente — sem interatividade de spray no slide 16"


def test_slide16_learn_counter_synced():
    """learnCounter deve ser incrementado pelo ciclo de spray 3D."""
    html = read_html()
    assert 'learnCounter' in html, "learnCounter ausente no slide 16"
    assert 'learnCount' in html or 'triggerSpray3D' in html, \
        "Contador de aprendizados não sincronizado com eventos 3D"


# ─── Fixes 02/06/2026 — reunião Jorey Costa ───────────────────────────────────

def test_simulator_mode_opacity_differentiation():
    """Canvas do simulador deve usar globalAlpha para destacar o modo ativo (borda vs nuvem)."""
    html = read_html()
    assert 'globalAlpha' in html, \
        "Canvas do simulador não usa globalAlpha — modo ativo não diferenciado visualmente"


def test_slide14_buttons_large_enough():
    """Slide 14 deve ter override CSS que aumenta os botões hw3d para serem clicáveis sem zoom."""
    html = read_html()
    assert '#slide-14 .ceb-mode-btn' in html, \
        "Sem override de tamanho para botões do slide 14 — Jorey reportou botões inacessíveis"


def test_token_sul_global_exempt():
    """Texto do token deve indicar que o Sul Global está isento de cobrança por token."""
    html = read_html()
    assert 'Sul Global' in html and ('ISENTO' in html or 'isento' in html or 'isenta' in html or 'gratuito' in html.lower()), \
        "Política de isenção de token para o Sul Global não aparece no slide de ROI"


def test_payback_breakdown_formula():
    """Card de payback deve ter breakdown didático com classe roi-breakdown mostrando componentes do cálculo."""
    html = read_html()
    assert 'roi-breakdown' in html, \
        "Classe roi-breakdown ausente no card de payback — Jorey pediu didatismo: hardware + savings/mês visíveis"


# ─── Fixes 02/06/2026 — pós-academia (sessão 2) ───────────────────────────────

def test_cubo_itau_date_corrected():
    """Data do evento Agrointeligente no Cubo Itaú deve ser 28/05/2026 (confirmada pelo Maestro)."""
    html = read_html()
    assert '28/05/2026' in html, \
        "Data do Cubo Itaú ainda como 01/06/2026 — deve ser 28/05/2026 (data do encontro com Jorey)"


def test_quantum_sig_has_minimize_button():
    """Overlay de assinatura gravitacional (quantum-gravity-sig) deve ter botão de minimizar."""
    html = read_html()
    assert 'sig-toggle' in html or 'grav-toggle' in html, \
        "Overlay #quantum-gravity-sig sem botão de minimizar — estava bloqueando dados em alguns slides"


def test_market_intel_methodology_note():
    """Slide 11 deve ter nota de metodologia explicando como os valores foram calculados."""
    html = read_html()
    assert ('Projeção' in html or 'projeção' in html) and ('modelo financeiro' in html.lower() or 'metodologia' in html.lower() or 'acionamento' in html), \
        "Slide de inteligência de mercado sem explicação de metodologia — Jorey pediu transparência no cálculo"
