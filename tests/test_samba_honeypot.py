import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "core"))
import samba_honeypot as sh


def _temp_vault(tmp_path):
    vault = str(tmp_path / "quantum_world")
    os.makedirs(vault, exist_ok=True)
    sh.VAULT_DIR     = vault
    sh.CONVERTS_PATH = os.path.join(vault, "samba_converts.jsonl")
    sh.CONVITES_PATH = os.path.join(vault, "convites_enviados.jsonl")


class TestConviteFields:
    def test_returns_required_fields(self, tmp_path):
        _temp_vault(tmp_path)
        c = sh.generate_convite("1.2.3.4", 1)
        for f in ["convite_id", "ts", "source_ip", "attempt_number",
                  "mensagem_pt", "message_en", "mensaje_es",
                  "caipirinha", "praia", "ritmo", "projeto_aberto",
                  "encerramento", "status", "energia_doada"]:
            assert f in c, f"Campo ausente: {f}"

    def test_status_is_convidado(self, tmp_path):
        _temp_vault(tmp_path)
        c = sh.generate_convite("5.5.5.5", 2)
        assert c["status"] == "CONVIDADO"

    def test_energia_doada_true(self, tmp_path):
        _temp_vault(tmp_path)
        c = sh.generate_convite("9.9.9.9", 1)
        assert c["energia_doada"] is True

    def test_ip_stored(self, tmp_path):
        _temp_vault(tmp_path)
        c = sh.generate_convite("10.0.0.1", 3)
        assert c["source_ip"] == "10.0.0.1"

    def test_attempt_stored(self, tmp_path):
        _temp_vault(tmp_path)
        c = sh.generate_convite("1.1.1.1", 7)
        assert c["attempt_number"] == 7

    def test_convite_id_is_10_chars(self, tmp_path):
        _temp_vault(tmp_path)
        c = sh.generate_convite("2.2.2.2", 1)
        assert len(c["convite_id"]) == 10

    def test_caipirinha_from_list(self, tmp_path):
        _temp_vault(tmp_path)
        c = sh.generate_convite("3.3.3.3", 1)
        assert c["caipirinha"] in sh.CAIPIRINHAS

    def test_praia_from_list(self, tmp_path):
        _temp_vault(tmp_path)
        c = sh.generate_convite("4.4.4.4", 1)
        assert c["praia"] in sh.PRAIAS

    def test_ritmo_from_list(self, tmp_path):
        _temp_vault(tmp_path)
        c = sh.generate_convite("5.5.5.5", 1)
        assert c["ritmo"] in sh.RITMOS

    def test_projeto_from_list(self, tmp_path):
        _temp_vault(tmp_path)
        c = sh.generate_convite("6.6.6.6", 1)
        assert c["projeto_aberto"] in sh.PROJETOS_ABERTOS


class TestLogPersistence:
    def test_writes_convite_to_jsonl(self, tmp_path):
        _temp_vault(tmp_path)
        sh.generate_convite("1.2.3.4", 1)
        assert os.path.exists(sh.CONVITES_PATH)

    def test_multiple_convites_appended(self, tmp_path):
        _temp_vault(tmp_path)
        sh.generate_convite("1.1.1.1", 1)
        sh.generate_convite("2.2.2.2", 1)
        sh.generate_convite("3.3.3.3", 1)
        with open(sh.CONVITES_PATH) as f:
            lines = [l for l in f if l.strip()]
        assert len(lines) == 3

    def test_jsonl_is_valid(self, tmp_path):
        _temp_vault(tmp_path)
        sh.generate_convite("7.7.7.7", 2, "FERRÃO")
        with open(sh.CONVITES_PATH) as f:
            entry = json.loads(f.readline())
        assert entry["attack_pattern"] == "FERRÃO"


class TestJsonResponse:
    def test_returns_bytes(self, tmp_path):
        _temp_vault(tmp_path)
        body = sh.generate_json_response("1.2.3.4", 1)
        assert isinstance(body, bytes)

    def test_valid_json(self, tmp_path):
        _temp_vault(tmp_path)
        body = sh.generate_json_response("1.2.3.4", 1)
        data = json.loads(body)
        assert data["status"] == "CONVITE_SOBERANO"

    def test_has_convite_block(self, tmp_path):
        _temp_vault(tmp_path)
        body = sh.generate_json_response("2.2.2.2", 2)
        data = json.loads(body)
        assert "convite" in data
        for f in ["praia", "caipirinha", "ritmo", "projeto"]:
            assert f in data["convite"], f"Campo convite ausente: {f}"

    def test_has_contact_email(self, tmp_path):
        _temp_vault(tmp_path)
        body = sh.generate_json_response("3.3.3.3", 1)
        data = json.loads(body)
        assert "gabrielbatista" in data.get("contato", "")


class TestHtmlResponse:
    def test_returns_bytes(self, tmp_path):
        _temp_vault(tmp_path)
        body = sh.generate_html_response("1.2.3.4", 1)
        assert isinstance(body, bytes)

    def test_valid_html_structure(self, tmp_path):
        _temp_vault(tmp_path)
        body = sh.generate_html_response("1.2.3.4", 1).decode()
        assert "<!DOCTYPE html>" in body
        assert "<title>" in body

    def test_contains_sul_global(self, tmp_path):
        _temp_vault(tmp_path)
        body = sh.generate_html_response("5.5.5.5", 1).decode()
        assert "Sul Global" in body

    def test_contains_praia(self, tmp_path):
        _temp_vault(tmp_path)
        body = sh.generate_html_response("6.6.6.6", 1).decode()
        # Alguma praia deve aparecer no HTML
        assert any(p.split("/")[0].strip() in body for p in sh.PRAIAS)

    def test_contains_contact(self, tmp_path):
        _temp_vault(tmp_path)
        body = sh.generate_html_response("7.7.7.7", 1).decode()
        assert "gabrielbatista" in body


class TestMelAmaroPage:
    def test_returns_bytes(self, tmp_path):
        _temp_vault(tmp_path)
        body = sh.generate_mel_amargo_page("1.2.3.4", 10)
        assert isinstance(body, bytes)

    def test_contains_ton618(self, tmp_path):
        _temp_vault(tmp_path)
        body = sh.generate_mel_amargo_page("8.8.8.8", 10).decode()
        assert "TON 618" in body

    def test_contains_ip(self, tmp_path):
        _temp_vault(tmp_path)
        body = sh.generate_mel_amargo_page("9.9.9.9", 5).decode()
        assert "9.9.9.9" in body

    def test_contains_invite_despite_block(self, tmp_path):
        _temp_vault(tmp_path)
        body = sh.generate_mel_amargo_page("1.1.1.1", 99).decode()
        assert any(c.split(" ")[0] in body for c in sh.CAIPIRINHAS)


class TestStats:
    def test_empty_stats_on_no_file(self, tmp_path):
        _temp_vault(tmp_path)
        stats = sh.load_convites_stats()
        assert stats["total"] == 0
        assert stats["ips_unicos"] == 0

    def test_counts_correctly(self, tmp_path):
        _temp_vault(tmp_path)
        sh.generate_convite("1.1.1.1", 1, "negado")
        sh.generate_convite("2.2.2.2", 1, "FERRÃO")
        sh.generate_convite("1.1.1.1", 2, "negado")
        stats = sh.load_convites_stats()
        assert stats["total"] == 3
        assert stats["ips_unicos"] == 2
        assert stats["por_padrao"]["negado"] == 2


class TestConstants:
    def test_has_caipirinhas(self):
        assert len(sh.CAIPIRINHAS) >= 5

    def test_has_praias(self):
        assert len(sh.PRAIAS) >= 5

    def test_has_ritmos(self):
        assert len(sh.RITMOS) >= 4

    def test_has_projetos(self):
        assert len(sh.PROJETOS_ABERTOS) >= 4

    def test_convites_pt_in_portuguese(self):
        keywords = ["soberania", "energia", "praia", "caipirinha", "redoma",
                    "buraco", "pym", "construi", "colabor", "convidado", "convite",
                    "transmut", "captur", "invasor", "tentativa", "escudo",
                    "sambar", "visita", "proposta"]
        for msg in sh.CONVITES_PT:
            assert any(w in msg.lower() for w in keywords), f"Mensagem sem palavra-chave: {msg}"

    def test_all_messages_nonempty(self):
        for lst in [sh.CONVITES_PT, sh.CONVITES_EN, sh.CONVITES_ES, sh.FRASES_ENCERRAMENTO, sh.CAIPIRINHAS]:
            for item in lst:
                assert len(item) > 10, f"Item muito curto: {item!r}"
        for praia in sh.PRAIAS:
            assert len(praia) >= 8, f"Praia muito curta: {praia!r}"
