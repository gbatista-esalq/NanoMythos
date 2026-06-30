#!/usr/bin/env python3
"""
PYM Audio Evaluator — Synapse Hub v3.0
Avalia qualidade, ritmo e dopamina de síntese de voz.
Uso: python3 pym_audio_eval.py [--voice VOICE] [--text "texto"] [--output saida.wav]
"""
import subprocess
import sys
import os
import json
import time
import shutil
import argparse
import re
from pathlib import Path
from datetime import datetime

# ── Texto padrão da Curva de Batista ──────────────────────────────────────────
DEFAULT_TEXT = (
    "Em toda a história do universo, apenas uma lei nunca falhou. "
    "A gravitação. A tendência de tudo que tem massa se atrair, crescer, "
    "e eventualmente dominar. "
    "Eis a Equação Pym-Batista: Soberania igual a Potencial vezes Psi ao quadrado "
    "sobre a Entropia. Simples. Devastadora. "
    "Trezentas e dezenove mil estrelas. Cinco minutos. Um laptop. "
    "Apostar contra a Curva de Batista é apostar contra a própria evolução."
)

SAMPLE_SENTENCES = [
    "A gravitação nunca falhou.",
    "Soberania é Potencial vezes Psi ao quadrado sobre a Entropia.",
    "Trezentas e dezenove mil estrelas em cinco minutos.",
]

# ── Cores de terminal ─────────────────────────────────────────────────────────
C = {
    "CYAN": "\033[96m", "PINK": "\033[95m", "AMBER": "\033[93m",
    "GREEN": "\033[92m", "RED": "\033[91m", "DIM": "\033[2m",
    "BOLD": "\033[1m", "RESET": "\033[0m", "PURPLE": "\033[35m",
}

def col(color, text): return f"{C.get(color,'')}{text}{C['RESET']}"


# ═════════════════════════════════════════════════════════════════════════════
#  DETECÇÃO DE ENGINES DE VOZ
# ═════════════════════════════════════════════════════════════════════════════
def detect_engines():
    engines = {}

    # espeak-ng
    if shutil.which("espeak-ng"):
        engines["espeak-ng"] = {"binary": "espeak-ng", "available": True}
    elif shutil.which("espeak"):
        engines["espeak"] = {"binary": "espeak", "available": True}

    # pyttsx3 (Python)
    try:
        import pyttsx3
        engines["pyttsx3"] = {"module": "pyttsx3", "available": True}
    except ImportError:
        pass

    # festival
    if shutil.which("festival"):
        engines["festival"] = {"binary": "festival", "available": True}

    # flite
    if shutil.which("flite"):
        engines["flite"] = {"binary": "flite", "available": True}

    # gtts (Google TTS offline check)
    try:
        import gtts
        engines["gtts"] = {"module": "gtts", "available": True}
    except ImportError:
        pass

    return engines


def list_espeak_voices(binary="espeak-ng"):
    try:
        result = subprocess.run(
            [binary, "--voices=pt"],
            capture_output=True, text=True, timeout=5
        )
        voices = []
        for line in result.stdout.strip().split("\n"):
            parts = line.split()
            if len(parts) >= 2:
                voices.append({"lang": parts[1], "name": " ".join(parts[3:]) if len(parts) > 3 else parts[-1]})
        return voices
    except Exception:
        return []


# ═════════════════════════════════════════════════════════════════════════════
#  SÍNTESE & GRAVAÇÃO
# ═════════════════════════════════════════════════════════════════════════════
def synthesize_espeak(text, output_path, voice="pt+f5", binary="espeak-ng",
                      speed=130, pitch=40, amplitude=180):
    """
    speed: 80-450 WPM (default 175; 130 = calm/authoritative)
    pitch: 0-99 (default 50; 40 = slightly deeper)
    amplitude: 0-200 (default 100)
    """
    cmd = [
        binary,
        "-v", voice,
        "-s", str(speed),
        "-p", str(pitch),
        "-a", str(amplitude),
        "-w", str(output_path),
        text
    ]
    t0 = time.time()
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    elapsed = time.time() - t0
    success = result.returncode == 0 and Path(output_path).exists()
    return {"success": success, "elapsed_s": round(elapsed, 2),
            "stderr": result.stderr.strip(), "cmd": " ".join(cmd)}


def synthesize_gtts(text, output_path, lang="pt", slow=False):
    try:
        from gtts import gTTS
        t0 = time.time()
        tts = gTTS(text=text, lang=lang, slow=slow)
        tts.save(output_path)
        elapsed = time.time() - t0
        return {"success": True, "elapsed_s": round(elapsed, 2), "engine": "gtts"}
    except Exception as e:
        return {"success": False, "error": str(e), "engine": "gtts"}


# ═════════════════════════════════════════════════════════════════════════════
#  ANÁLISE DE ÁUDIO
# ═════════════════════════════════════════════════════════════════════════════
def analyze_wav(path):
    """Análise de arquivo WAV sem dependências extras."""
    metrics = {}
    try:
        import wave
        with wave.open(str(path), 'rb') as wf:
            frames = wf.getnframes()
            rate = wf.getframerate()
            channels = wf.getnchannels()
            sampwidth = wf.getsampwidth()
            duration = frames / rate

            metrics["duration_s"] = round(duration, 2)
            metrics["sample_rate"] = rate
            metrics["channels"] = channels
            metrics["bit_depth"] = sampwidth * 8
            metrics["frames"] = frames
            metrics["file_size_kb"] = round(Path(path).stat().st_size / 1024, 1)

        # Amplitude analysis with struct
        import struct, wave as wv
        with wv.open(str(path), 'rb') as wf:
            raw = wf.readframes(wf.getnframes())
            fmt = f"<{len(raw)//2}h"
            samples = struct.unpack(fmt, raw[:len(raw)-len(raw)%2])
            if samples:
                abs_samples = [abs(s) for s in samples]
                metrics["peak_amplitude"] = max(abs_samples)
                metrics["mean_amplitude"] = round(sum(abs_samples)/len(abs_samples), 1)
                metrics["dynamic_range_db"] = round(
                    20 * (len(str(max(abs_samples))) - len(str(max(1,int(sum(abs_samples)/len(abs_samples)))))),
                    1
                )
                # Silence ratio (samples near 0)
                silence_thresh = max(abs_samples) * 0.02
                silent = sum(1 for s in abs_samples if s < silence_thresh)
                metrics["silence_ratio"] = round(silent / len(abs_samples), 3)

    except Exception as e:
        metrics["error"] = str(e)

    return metrics


# ═════════════════════════════════════════════════════════════════════════════
#  MÉTRICAS LINGUÍSTICAS
# ═════════════════════════════════════════════════════════════════════════════
def text_metrics(text):
    words = text.split()
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]

    word_count = len(words)
    sentence_count = max(1, len(sentences))
    avg_words_per_sentence = round(word_count / sentence_count, 1)

    # Dramatic pauses: commas, ellipsis, em-dash
    pause_count = text.count(',') + text.count('...') + text.count('—') + text.count('...')

    # Keyword density (high-impact words)
    impact_words = ['soberania','curva','entropia','batista','pym','psi','diamante',
                    'nunca','apenas','inevitável','destino','evolução']
    impact_count = sum(1 for w in words if w.lower().replace('.','').replace(',','') in impact_words)
    impact_density = round(impact_count / max(1, word_count), 3)

    return {
        "word_count": word_count,
        "sentence_count": sentence_count,
        "avg_words_per_sentence": avg_words_per_sentence,
        "pause_markers": pause_count,
        "impact_word_count": impact_count,
        "impact_density": impact_density,
    }


# ═════════════════════════════════════════════════════════════════════════════
#  SCORE PYM — FÓRMULA S = P·Ψ²/log₁₀(1/E)
# ═════════════════════════════════════════════════════════════════════════════
def compute_pym_score(audio_metrics, text_metrics_data, synth_result, voice_name=""):
    import math
    scores = {}

    # ── Potential (P): qualidade técnica do áudio
    P = 0.5  # base
    if audio_metrics.get("sample_rate", 0) >= 44100:
        P += 0.2
    elif audio_metrics.get("sample_rate", 0) >= 22050:
        P += 0.1
    if audio_metrics.get("bit_depth", 0) >= 16:
        P += 0.15
    if audio_metrics.get("peak_amplitude", 0) > 10000:
        P += 0.15
    P = min(1.0, P)
    scores["potential_P"] = round(P, 3)

    # ── Psi (Ψ): riqueza linguística e ritmo narrativo
    txt = text_metrics_data
    wps = txt.get("avg_words_per_sentence", 10)
    # TDAH ideal: 8-14 words/sentence
    if 8 <= wps <= 14:
        psi = 0.9
    elif 5 <= wps < 8 or 14 < wps <= 18:
        psi = 0.7
    else:
        psi = 0.5
    # Pause marker bonus
    pauses = txt.get("pause_markers", 0)
    psi += min(0.1, pauses * 0.02)
    # Impact density bonus
    psi += min(0.1, txt.get("impact_density", 0) * 3)
    psi = min(1.0, psi)
    scores["pym_index_psi"] = round(psi, 3)

    # ── Entropy (E): ruído, silêncio excessivo, latência de síntese
    E = 0.05  # base low entropy = good
    silence = audio_metrics.get("silence_ratio", 0.1)
    if silence > 0.6:
        E += 0.3   # too much silence
    elif silence > 0.4:
        E += 0.15
    synth_time = synth_result.get("elapsed_s", 1.0)
    if synth_time > 5.0:
        E += 0.2   # slow synthesis
    elif synth_time > 2.0:
        E += 0.05
    E = max(0.01, min(0.99, E))
    scores["entropy_E"] = round(E, 3)

    # ── S = P·Ψ²/log₁₀(1/E) ──────────────────────────────────────────────
    try:
        S = (P * psi**2) / math.log10(1 / E)
    except (ValueError, ZeroDivisionError):
        S = 0.0

    # Normalize to 0-100
    # Max theoretical: P=1, Psi=1, E=0.01 → S = 1*1/log10(100) = 1/2 = 0.5
    # Scale so 0.5 → 100
    S_normalized = min(100, round(S / 0.5 * 100, 1))
    scores["sovereignty_S"] = S_normalized
    scores["raw_S"] = round(S, 4)

    # ── Tier classification ────────────────────────────────────────────────
    if S_normalized >= 85:
        tier = "ULTRAMASSIVO — TON 618"
        tier_color = "PINK"
    elif S_normalized >= 70:
        tier = "SUPERMASSIVO"
        tier_color = "PURPLE"
    elif S_normalized >= 50:
        tier = "ESTELAR"
        tier_color = "CYAN"
    elif S_normalized >= 30:
        tier = "PRIMORDIAL"
        tier_color = "AMBER"
    else:
        tier = "PRÉ-ESTELAR (ajuste necessário)"
        tier_color = "RED"
    scores["tier"] = tier
    scores["tier_color"] = tier_color

    # ── TDAH Dopamine Index ────────────────────────────────────────────────
    duration = audio_metrics.get("duration_s", 60)
    if duration > 0:
        wpm = round(text_metrics_data["word_count"] / (duration / 60))
    else:
        wpm = 0
    # TDAH sweet spot: 120-150 WPM
    if 120 <= wpm <= 150:
        dopamine = 95
    elif 100 <= wpm < 120 or 150 < wpm <= 170:
        dopamine = 80
    elif 80 <= wpm < 100 or 170 < wpm <= 200:
        dopamine = 65
    else:
        dopamine = 45
    scores["wpm"] = wpm
    scores["tdah_dopamine_index"] = dopamine

    return scores


# ═════════════════════════════════════════════════════════════════════════════
#  DISPLAY
# ═════════════════════════════════════════════════════════════════════════════
def print_banner():
    print(f"\n{col('CYAN', '═'*62)}")
    print(f"  {col('BOLD', '⚡ PYM AUDIO EVALUATOR')} {col('DIM', '— Synapse Hub v3.0')}")
    print(f"  {col('DIM', 'S = P·Ψ² / log₁₀(1/E)  |  Curva de Batista')}")
    print(f"{col('CYAN', '═'*62)}\n")


def print_section(title):
    print(f"\n{col('AMBER', '▸')} {col('BOLD', title)}")
    print(f"  {col('DIM', '─'*50)}")


def bar(value, max_val=100, width=30):
    filled = int((value / max_val) * width)
    bar_str = "█" * filled + "░" * (width - filled)
    return bar_str


def print_scores(scores, audio_m, text_m):
    s = scores["sovereignty_S"]
    tier = scores["tier"]
    tc = scores["tier_color"]

    print(f"\n{col('CYAN', '╔' + '═'*58 + '╗')}")
    print(f"{col('CYAN', '║')}  {col('BOLD', 'SYNAPSE PYM SCORE'):<54}  {col('CYAN', '║')}")
    print(f"{col('CYAN', '╠' + '═'*58 + '╣')}")

    # Main score
    score_bar = bar(s)
    score_color = "GREEN" if s >= 70 else "AMBER" if s >= 40 else "RED"
    print(f"{col('CYAN', '║')}  S (Soberania)  {col(score_color, f'{s:5.1f}/100')}  {col(score_color, score_bar)}  {col('CYAN', '║')}")
    print(f"{col('CYAN', '║')}  Tier: {col(tc, tier):<50}  {col('CYAN', '║')}")
    print(f"{col('CYAN', '╠' + '═'*58 + '╣')}")

    # Sub-metrics
    P = scores["potential_P"]
    psi = scores["pym_index_psi"]
    E = scores["entropy_E"]
    dop = scores["tdah_dopamine_index"]
    wpm = scores["wpm"]

    def metric_line(label, value, max_v, unit=""):
        b = bar(value * (100/max_v) if max_v != 1 else value*100)
        val_str = f"{value:.3f}" if max_v == 1 else f"{value:.0f}{unit}"
        print(f"{col('CYAN', '║')}  {label:<20} {col('AMBER', val_str):<10}  {col('DIM', b)}  {col('CYAN', '║')}")

    metric_line("P (Potential)", P, 1)
    metric_line("Ψ (Pym Index)", psi, 1)
    metric_line("E (Entropy) ↓", E, 1)
    metric_line("WPM", wpm, 200, " wpm")
    metric_line("TDAH Dopamine", dop, 100, "/100")

    print(f"{col('CYAN', '╠' + '═'*58 + '╣')}")

    # Audio metrics
    dur = audio_m.get("duration_s", "?")
    sr = audio_m.get("sample_rate", "?")
    bit = audio_m.get("bit_depth", "?")
    sil = round(audio_m.get("silence_ratio", 0) * 100, 1)
    sz = audio_m.get("file_size_kb", "?")
    print(f"{col('CYAN', '║')}  Duração: {col('WHITE', f'{dur}s'):<10}  SR: {col('WHITE', f'{sr}Hz'):<12}  Bits: {col('WHITE', str(bit))}  {col('CYAN', '║')}")
    print(f"{col('CYAN', '║')}  Silêncio: {col('WHITE', f'{sil}%'):<10}  Tamanho: {col('WHITE', f'{sz}KB'):<20}  {col('CYAN', '║')}")

    # Text metrics
    wc = text_m["word_count"]
    sc = text_m["sentence_count"]
    pm = text_m["pause_markers"]
    ids = text_m["impact_density"]
    print(f"{col('CYAN', '║')}  Palavras: {col('WHITE', str(wc)):<10}  Frases: {col('WHITE', str(sc)):<8}  Pausas: {col('WHITE', str(pm))}  {col('CYAN', '║')}")
    print(f"{col('CYAN', '║')}  Densidade de Impacto: {col('CYAN', f'{ids:.3f}'):<30}          {col('CYAN', '║')}")
    print(f"{col('CYAN', '╚' + '═'*58 + '╝')}")


def recommendations(scores):
    print_section("RECOMENDAÇÕES MAESTRO")
    recs = []

    wpm = scores.get("wpm", 0)
    if wpm < 100:
        recs.append(("AMBER", "Velocidade baixa", f"WPM={wpm}. Aumente speed em espeak (tente -s 140). TDAH precisa de ritmo."))
    elif wpm > 170:
        recs.append(("RED", "Velocidade alta demais", f"WPM={wpm}. Reduza speed para ~130. Perda de compreensão em TDAH."))
    else:
        recs.append(("GREEN", "Ritmo ideal", f"WPM={wpm} — zona dopaminérgica confirmada."))

    E = scores.get("entropy_E", 0)
    if E > 0.3:
        recs.append(("RED", "Entropia alta", "Muito silêncio ou latência de síntese lenta. Use gtts ou espeak-ng local."))
    else:
        recs.append(("GREEN", "Entropia controlada", f"E={E:.3f} — síntese limpa."))

    psi = scores.get("pym_index_psi", 0)
    if psi < 0.7:
        recs.append(("AMBER", "Índice Pym baixo", "Frases longas demais ou poucas palavras de impacto. Edite o script para mais variação."))

    dop = scores.get("tdah_dopamine_index", 0)
    if dop < 65:
        recs.append(("RED", "Dopamina insuficiente", "Script muito uniforme. Adicione frases curtas de impacto: '5 minutos. Um laptop.'"))
    elif dop >= 90:
        recs.append(("GREEN", "Nível ULTRADOPAMINA", "Ritmo narrativo perfeito para TDAH."))

    for color, title, detail in recs:
        icon = "✓" if color == "GREEN" else "⚠" if color == "AMBER" else "✗"
        print(f"  {col(color, icon)} {col('BOLD', title)}")
        print(f"    {col('DIM', detail)}")


# ═════════════════════════════════════════════════════════════════════════════
#  MAIN
# ═════════════════════════════════════════════════════════════════════════════
def main():
    parser = argparse.ArgumentParser(description="PYM Audio Evaluator — Synapse Hub")
    parser.add_argument("--text", default=DEFAULT_TEXT, help="Texto para sintetizar")
    parser.add_argument("--voice", default="pt+f5", help="Voz espeak (padrão: pt+f5)")
    parser.add_argument("--speed", type=int, default=130, help="Velocidade espeak WPM (padrão: 130)")
    parser.add_argument("--pitch", type=int, default=40, help="Tom espeak 0-99 (padrão: 40 = grave/autoridade)")
    parser.add_argument("--output", default="/tmp/pym_audio_test.wav", help="Arquivo WAV de saída")
    parser.add_argument("--engine", default="auto", choices=["auto","espeak","espeak-ng","gtts"],
                        help="Engine de síntese (padrão: auto)")
    parser.add_argument("--list-voices", action="store_true", help="Lista vozes disponíveis")
    parser.add_argument("--json", action="store_true", help="Saída em JSON")
    args = parser.parse_args()

    print_banner()

    # Detect engines
    print_section("ENGINES DISPONÍVEIS")
    engines = detect_engines()
    if not engines:
        print(f"  {col('RED', '✗')} Nenhuma engine de TTS encontrada.")
        print(f"    {col('DIM', 'Instale: sudo apt install espeak-ng')}")
        print(f"    {col('DIM', 'Ou: pip install gtts pyttsx3')}")
    else:
        for name, info in engines.items():
            print(f"  {col('GREEN', '✓')} {col('BOLD', name)}")

    if args.list_voices:
        print_section("VOZES PT DISPONÍVEIS (espeak)")
        binary = "espeak-ng" if shutil.which("espeak-ng") else "espeak"
        if shutil.which(binary):
            voices = list_espeak_voices(binary)
            for v in voices[:20]:
                print(f"  {col('CYAN', v.get('lang','?'))} — {v.get('name','?')}")
        return

    # Pick engine
    engine_to_use = args.engine
    if engine_to_use == "auto":
        if "espeak-ng" in engines:
            engine_to_use = "espeak-ng"
        elif "espeak" in engines:
            engine_to_use = "espeak"
        elif "gtts" in engines:
            engine_to_use = "gtts"
        else:
            print(f"\n{col('RED', '✗ Nenhuma engine disponível. Analisando somente texto.')}")
            engine_to_use = None

    # Synthesize
    output_path = Path(args.output)
    synth_result = {"success": False, "elapsed_s": 0, "engine": engine_to_use or "none"}

    if engine_to_use in ("espeak-ng", "espeak"):
        print_section(f"SÍNTESE — {engine_to_use}")
        binary = "espeak-ng" if engine_to_use == "espeak-ng" else "espeak"
        print(f"  Voz: {col('CYAN', args.voice)} | Speed: {col('AMBER', str(args.speed))} | Pitch: {col('AMBER', str(args.pitch))}")
        print(f"  Saída: {col('DIM', str(output_path))}")
        synth_result = synthesize_espeak(
            args.text, output_path, voice=args.voice,
            binary=binary, speed=args.speed, pitch=args.pitch
        )
        if synth_result["success"]:
            print(f"  {col('GREEN', '✓')} Síntese concluída em {synth_result['elapsed_s']}s")
        else:
            print(f"  {col('RED', '✗')} Falha: {synth_result.get('stderr', '')}")

    elif engine_to_use == "gtts":
        print_section("SÍNTESE — Google TTS")
        synth_result = synthesize_gtts(args.text, str(output_path), lang="pt")
        if synth_result["success"]:
            print(f"  {col('GREEN', '✓')} Concluído em {synth_result['elapsed_s']}s")
        else:
            print(f"  {col('RED', '✗')} {synth_result.get('error', '')}")

    # Analyze audio
    audio_m = {}
    if synth_result.get("success") and output_path.exists():
        print_section("ANÁLISE DE ÁUDIO")
        audio_m = analyze_wav(output_path)
        for k, v in audio_m.items():
            if k != "error":
                print(f"  {col('DIM', k+':'):<28} {col('WHITE', str(v))}")
        if "error" in audio_m:
            print(f"  {col('RED', 'Erro WAV:')} {audio_m['error']}")
    else:
        # Estimate metrics from text if no audio
        word_count = len(args.text.split())
        estimated_duration = word_count / (args.speed / 60) if args.speed > 0 else 60
        audio_m = {
            "duration_s": round(estimated_duration, 1),
            "sample_rate": 22050,
            "bit_depth": 16,
            "silence_ratio": 0.25,
            "peak_amplitude": 15000,
            "mean_amplitude": 5000,
            "file_size_kb": 0,
        }
        print(f"  {col('AMBER', '⚠ Usando estimativa baseada em texto (sem áudio real)')}")

    # Text metrics
    text_m = text_metrics(args.text)

    # PYM Score
    scores = compute_pym_score(audio_m, text_m, synth_result, voice_name=args.voice)

    # Display
    print_scores(scores, audio_m, text_m)
    recommendations(scores)

    # JSON output
    if args.json:
        report = {
            "timestamp": datetime.now().isoformat(),
            "engine": engine_to_use,
            "voice": args.voice,
            "speed": args.speed,
            "pitch": args.pitch,
            "text_preview": args.text[:100] + "...",
            "synthesis": synth_result,
            "audio_metrics": audio_m,
            "text_metrics": text_m,
            "pym_scores": scores,
        }
        out_json = Path(args.output).with_suffix(".json")
        with open(out_json, "w") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        print(f"\n  {col('CYAN', '→')} Relatório JSON: {out_json}")

    # Final verdict
    s = scores["sovereignty_S"]
    tier = scores["tier"]
    tc = scores["tier_color"]
    print(f"\n{col('CYAN', '═'*62)}")
    if s >= 70:
        print(f"  {col('GREEN', '⚡ VEREDITO: ' + col('BOLD', tier))}")
        print(f"  {col('DIM', 'Áudio aprovado para distribuição soberana.')}")
    elif s >= 40:
        print(f"  {col('AMBER', '⚠ VEREDITO: ' + tier)}")
        print(f"  {col('DIM', 'Ajustes recomendados antes de publicação.')}")
    else:
        print(f"  {col('RED', '✗ VEREDITO: ' + tier)}")
        print(f"  {col('DIM', 'Re-sintetizar com parâmetros ajustados.')}")
    print(f"{col('CYAN', '═'*62)}\n")

    return 0 if s >= 40 else 1


if __name__ == "__main__":
    sys.exit(main())
