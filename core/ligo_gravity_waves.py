from gwpy.timeseries import TimeSeries
from gwosc.datasets import event_gps
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# GW150914: primeira onda gravitacional detectada na história humana
# Dois buracos negros: 36 M☉ + 29 M☉ → fusão em 62 M☉
# Distância: 1.3 bilhões de anos-luz
# Data: 14 setembro 2015, 09:50:45 UTC

EVENT = "GW150914"
DETECTOR = "H1"  # LIGO Hanford, Washington

def fetch_gravitational_wave():
    print(f"🌌 [LIGO] Baixando dados reais do evento {EVENT}...")
    print(f"   → Detector: {DETECTOR} (LIGO Hanford)")
    print(f"   → Dois buracos negros colidiram a 1,3 bilhão de anos-luz")

    gps = event_gps(EVENT)
    print(f"   → GPS Time: {gps} s (tempo absoluto do evento)")

    # Baixa 8 segundos ao redor do evento
    start = gps - 4
    end = gps + 4
    data = TimeSeries.fetch_open_data(DETECTOR, start, end, verbose=False)
    print(f"   → {len(data)} amostras baixadas a {data.sample_rate}")
    return data, gps

def process_and_plot(data, gps):
    print("\n📊 [PROCESSAMENTO] Aplicando filtro de banda gravitacional...")

    # Filtra o ruído (banda 30-400 Hz é onde LIGO detecta fusões de BH)
    filtered = data.bandpass(30, 400)

    # Whitening remove o ruído colorido do detector
    whitened = filtered.whiten(4, 2)

    # Janela ao redor do chirp (sinal de fusão)
    start_plot = gps - 0.4
    end_plot = gps + 0.3
    cropped = whitened.crop(start_plot, end_plot)

    # Plot
    fig, axes = plt.subplots(2, 1, figsize=(12, 8))
    fig.suptitle(
        "GW150914 — Primeira Onda Gravitacional da História\n"
        "Fusão de Dois Buracos Negros (36 M☉ + 29 M☉) | LIGO Hanford",
        fontsize=13, fontweight='bold'
    )

    # Sinal no tempo
    axes[0].plot(cropped.times.value - gps, cropped.value, color='#00CFFF', linewidth=1.2)
    axes[0].set_xlabel("Tempo relativo ao evento (s)")
    axes[0].set_ylabel("Strain (deformação do espaço-tempo)")
    axes[0].set_title("Deformação do Espaço-Tempo — o chirp gravitacional")
    axes[0].axvline(0, color='yellow', linestyle='--', alpha=0.7, label='Momento da fusão')
    axes[0].legend()
    axes[0].set_facecolor('#0a0a1a')
    axes[0].grid(True, alpha=0.3)

    # Espectrograma (frequência ao longo do tempo)
    specgram = whitened.spectrogram2(fftlength=0.1, overlap=0.095) ** (1/2)
    specgram_crop = specgram.crop(start_plot, end_plot)
    specgram_crop = specgram_crop.crop_frequencies(30, 400)

    times_rel = specgram_crop.times.value - gps
    freqs = specgram_crop.frequencies.value

    vals = specgram_crop.value
    axes[1].pcolormesh(
        times_rel,
        freqs,
        vals.T,
        cmap='magma',
        vmin=vals.min(),
        vmax=np.percentile(vals, 99),
        shading='auto'
    )
    axes[1].set_ylim(30, 400)
    axes[1].set_xlabel("Tempo relativo ao evento (s)")
    axes[1].set_ylabel("Frequência (Hz)")
    axes[1].set_title("Espectrograma — o chirp: frequência sobe de 35→150 Hz durante a fusão")
    axes[1].set_facecolor('#0a0a1a')

    fig.patch.set_facecolor('#0d0d1f')
    plt.tight_layout()

    output = "/home/synapseagtech/Área de Trabalho/SYNAPSE AGTECH/gw150914_gravity_wave.png"
    plt.savefig(output, dpi=150, bbox_inches='tight', facecolor='#0d0d1f')
    print(f"\n✅ Gráfico salvo: {output}")
    return cropped

def report_physics(data):
    peak_strain = np.max(np.abs(data.value))
    print(f"\n⚛️  FÍSICA REAL DO EVENTO GW150914:")
    print(f"   → Strain máximo detectado: {peak_strain:.4f} (adimensional)")
    print(f"   → Isso significa: o LIGO detectou uma deformação de ~10⁻²¹ m/m")
    print(f"   → Equivalente a medir 1/1000 do diâmetro de um próton")
    print(f"   → ao longo de 4 km de braço do detector")
    print(f"   → Energia liberada na fusão: ~3 M☉ × c² = 5.4 × 10⁴⁷ J")
    print(f"   → Por 0.2 segundos, mais potência que todas as estrelas do universo observável")

if __name__ == "__main__":
    data, gps = fetch_gravitational_wave()
    cropped = process_and_plot(data, gps)
    report_physics(cropped)
