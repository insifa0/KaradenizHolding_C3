"""
Karadeniz Holding — Kurumsal Bilgi Asistanı
Veritabanı Modülü (database.py)

Bu modül:
  1. 'Ornek yapay veri.txt' dosyasını okur ve yapısal olarak parse eder.
  2. Her dökümanı LangChain Document nesnesine dönüştürür (metadata ile birlikte).
  3. Gemini embedding modeli ile vektörleştirir.
  4. ChromaDB yerel vektör veritabanına kaydeder / diskten yükler.
"""

import os
import re
from pathlib import Path
from typing import List, Dict, Tuple

from langchain_core.documents import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma

# ─────────────────────────────────────────────
# Sabitler
# ─────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "Ornek yapay veri.txt"
CHROMA_DIR = str(BASE_DIR / "chroma_db")
COLLECTION_NAME = "karadeniz_holding_docs"


# ─────────────────────────────────────────────
# Veri Seti Parser
# ─────────────────────────────────────────────

# Döküman tipi → bölüm başlık eşleştirmesi
SECTION_HEADERS = {
    "Prosedür": "Karadeniz Holding Kurumsal Prosedürler Veri Seti",
    "Politika": "Karadeniz Holding Kurumsal Politikalar Veri Seti",
    "Talimat": "Karadeniz Holding Kurumsal Talimatlar Veri Seti",
    "Form": "Karadeniz Holding Kurumsal Formlar Veri Seti",
}

# Departman kodu → departman adı eşleştirmesi
DEPT_MAP = {
    "İK": "İnsan Kaynakları",
    "BT": "Bilgi Teknolojileri",
    "SA": "Satın Alma",
    "FN": "Finans ve Muhasebe",
    "İSG": "İş Sağlığı ve Güvenliği",
    "OP": "Operasyon ve Denizcilik",
    "Kİ": "Kurumsal İletişim",
    "HK": "Hukuk, Etik ve Uyum",
}

# ID kalıbı: İK-PR-01, BT-TA-05 vb.
ID_PATTERN = re.compile(
    r"^\s*\d+\.\s+("
    r"[A-ZİĞÜŞÖÇa-zığüşöç]+"   # Departman kodu
    r"-"
    r"[A-ZİĞÜŞÖÇa-zığüşöç]+"   # Tip kodu (PR, PO, TA, FR)
    r"-"
    r"\d+"                        # Sıra numarası
    r"):\s+(.+)",
    re.UNICODE,
)


def _detect_department(doc_id: str) -> str:
    """Döküman ID'sindeki departman kodunu tam isme çevirir."""
    dept_code = doc_id.split("-")[0]
    return DEPT_MAP.get(dept_code, dept_code)


def _detect_doc_type(doc_id: str) -> str:
    """Döküman ID'sindeki tip kodunu okunabilir isme çevirir."""
    type_map = {"PR": "Prosedür", "PO": "Politika", "TA": "Talimat", "FR": "Form"}
    type_code = doc_id.split("-")[1]
    return type_map.get(type_code, type_code)


def _extract_related_docs(body: str) -> str:
    """İlişkili prosedür/talimat/politika referansını yakalar."""
    match = re.search(
        r"(?:İlişkili\s+(?:Prosedür|Talimat|Politika)):\s*(.+)",
        body,
        re.IGNORECASE | re.UNICODE,
    )
    return match.group(1).strip() if match else ""


def _extract_access_level(body: str, doc_type: str, doc_id: str = "") -> str:
    """Erişim yetkisini içerikten çıkarır; bulamazsa varsayılan atar."""
    # Özel durum: BT-PR-01 veya kullanıcı tarafından bildirilen kısıtlı belgeler
    if doc_id == "BT-PR-01":
        return "BT Departmanı"

    # Bazı dökümanlar kapsam bilgisinden erişim yetkisi çıkarılabilir
    body_lower = body.lower()
    if "tüm çalışan" in body_lower or "tüm grup" in body_lower:
        return "Tüm Çalışanlar"
    elif "yönetim" in body_lower and ("kurulu" in body_lower or "yönetici" in body_lower):
        return "Yönetim"
    elif "teknik" in body_lower or "mühendis" in body_lower:
        return "Teknik Ekip"
    elif "bt güvenlik" in body_lower or "bt departmanı" in body_lower:
        return "BT Departmanı"
    elif "finans" in body_lower and "hazine" in body_lower:
        return "Finans Departmanı"
    return "Tüm Çalışanlar"



def _extract_keywords(doc_name: str, body: str) -> str:
    """Döküman adı ve içeriğinden anahtar kelimeler türetir."""
    keywords = set()

    # Döküman adındaki anlamlı kelimeleri ekle
    stop_words = {"ve", "ile", "için", "bir", "bu", "da", "de", "den", "dan", "mi", "mı"}
    for word in re.findall(r"[A-Za-zİĞÜŞÖÇığüşöçâîû]+", doc_name):
        if len(word) > 2 and word.lower() not in stop_words:
            keywords.add(word.lower())

    # Yaygın eş anlamlıları ekle
    synonym_map = {
        "vpn": ["uzaktan erişim", "dış bağlantı", "remote"],
        "izin": ["tatil", "yıllık izin", "mazeret", "off"],
        "parola": ["şifre", "password", "sıfırlama"],
        "yangın": ["söndürme", "itfaiye", "alev"],
        "deprem": ["sarsıntı", "afet", "acil durum"],
        "maaş": ["ücret", "bordro", "maaş"],
        "masraf": ["harcama", "fatura", "expense"],
        "kaza": ["yaralanma", "olay", "iş kazası"],
        "eğitim": ["kurs", "seminer", "training"],
        "tedarikçi": ["supplier", "vendor", "firma"],
        "sözleşme": ["kontrat", "anlaşma", "nda"],
        "performans": ["hedef", "kpi", "değerlendirme"],
        "gemi": ["powership", "denizcilik", "filo"],
        "yakıt": ["bunker", "ikmal", "mazot", "fuel"],
        "kvkk": ["gdpr", "kişisel veri", "gizlilik"],
        "etik": ["yolsuzluk", "rüşvet", "ihbar"],
        "bütçe": ["ödenek", "mali plan", "budget"],
    }

    body_lower = body.lower()
    for key, synonyms in synonym_map.items():
        if key in body_lower or key in doc_name.lower():
            keywords.add(key)
            keywords.update(synonyms)

    return ", ".join(sorted(keywords))


def parse_data_file(file_path: Path = DATA_FILE) -> List[Document]:
    """
    Ornek yapay veri.txt dosyasını okur, her dökümanı yapısal olarak
    parse edip LangChain Document listesi olarak döndürür.

    Returns:
        List[Document]: Metadata ile zenginleştirilmiş döküman listesi.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Ana bölümlere ayır
    section_keys = list(SECTION_HEADERS.values())
    parts: List[Tuple[str, str]] = []  # (bölüm_türü, bölüm_içeriği)

    for i, header in enumerate(section_keys):
        start = content.find(header)
        if start == -1:
            continue
        # Sonraki bölümün başlangıcı
        end = len(content)
        for j in range(i + 1, len(section_keys)):
            next_start = content.find(section_keys[j])
            if next_start != -1:
                end = next_start
                break
        doc_type_name = [k for k, v in SECTION_HEADERS.items() if v == header][0]
        parts.append((doc_type_name, content[start:end]))

    documents: List[Document] = []

    for section_type, section_text in parts:
        lines = section_text.splitlines()
        current_id = None
        current_name = None
        current_body_lines: List[str] = []

        def _flush():
            """Birikmiş dökümanı Document nesnesine çevirip listeye ekler."""
            nonlocal current_id, current_name, current_body_lines
            if current_id and current_name:
                body = "\n".join(current_body_lines).strip()
                department = _detect_department(current_id)
                doc_type = _detect_doc_type(current_id)
                related = _extract_related_docs(body)
                access = _extract_access_level(body, doc_type, current_id)
                keywords = _extract_keywords(current_name, body)

                # Ana metin gövdesi — chatbot'un okuması için zengin format
                page_content = (
                    f"Doküman ID: {current_id}\n"
                    f"Doküman Adı: {current_name}\n"
                    f"Departman: {department}\n"
                    f"Doküman Tipi: {doc_type}\n"
                    f"---\n"
                    f"{body}"
                )

                doc = Document(
                    page_content=page_content,
                    metadata={
                        "Dokuman_ID": current_id,
                        "Departman": department,
                        "Dokuman_Tipi": doc_type,
                        "Dokuman_Adi": current_name,
                        "Erisim_Yetkisi": access,
                        "Anahtar_Kelimeler": keywords,
                        "Iliskili_Dokuman": related,
                    },
                )
                documents.append(doc)

            current_id = None
            current_name = None
            current_body_lines = []

        for line in lines:
            match = ID_PATTERN.match(line)
            if match:
                _flush()
                current_id = match.group(1).strip()
                current_name = match.group(2).strip()
            elif current_id:
                # Alt bölüm başlıkları (I. İnsan Kaynakları vb.) atla
                if re.match(r"^[IVXLC]+\.\s+", line.strip()):
                    continue
                current_body_lines.append(line)

        # Son dökümanı da flush et
        _flush()

    return documents


# ─────────────────────────────────────────────
# ChromaDB Yönetimi
# ─────────────────────────────────────────────

import chromadb
import time
from langchain_core.embeddings import Embeddings

class RateLimitedGeminiEmbeddings(Embeddings):
    """
    Google Gemini API'nin Ücretsiz (Free) sürümündeki 100 RPM/TPM limitlerini
    aşmamak için istekleri bölen ve rate-limit (429) durumunda
    otomatik yeniden deneme yapan sarmalayıcı sınıf.
    """
    def __init__(self, google_api_key: str, model: str = "models/gemini-embedding-2"):
        self.underlying = GoogleGenerativeAIEmbeddings(
            model=model,
            google_api_key=google_api_key,
        )

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        results = []
        chunk_size = 25  # Hata payını azaltmak için küçük gruplar halinde gönderelim
        for i in range(0, len(texts), chunk_size):
            chunk = texts[i:i + chunk_size]
            success = False
            retries = 5
            delay = 10  # 429 durumunda ilk bekleme süresi
            while not success and retries > 0:
                try:
                    chunk_embeddings = self.underlying.embed_documents(chunk)
                    results.extend(chunk_embeddings)
                    success = True
                except Exception as e:
                    err_str = str(e)
                    if "429" in err_str or "RESOURCE_EXHAUSTED" in err_str:
                        retries -= 1
                        print(f"[Embedding] Rate limit (429) reached. Retrying in {delay}s... (Retries left: {retries})")
                        time.sleep(delay)
                        delay *= 2  # Üstel artış (exponential backoff)
                    else:
                        raise e
            if not success:
                raise Exception("Failed to embed documents due to persistent rate limiting (429).")
            # İstekler arasına kısa bir bekleme ekleyelim
            if i + chunk_size < len(texts):
                time.sleep(3)
        return results

    def embed_query(self, text: str) -> List[float]:
        retries = 5
        delay = 3
        while retries > 0:
            try:
                return self.underlying.embed_query(text)
            except Exception as e:
                err_str = str(e)
                if "429" in err_str or "RESOURCE_EXHAUSTED" in err_str:
                    retries -= 1
                    time.sleep(delay)
                    delay *= 2
                else:
                    raise e
        raise Exception("Failed to embed query due to persistent rate limiting (429).")


def get_embeddings(api_key: str) -> RateLimitedGeminiEmbeddings:
    """Gemini embedding modelini oluşturur."""
    return RateLimitedGeminiEmbeddings(
        google_api_key=api_key,
        model="models/gemini-embedding-2",
    )


# Modül seviyesinde tek bir ChromaDB client tutalım (kilit sorununu önler)
_chroma_client = None


def _get_chroma_client(force_new: bool = False) -> chromadb.ClientAPI:
    """
    Tekil (singleton) ChromaDB PersistentClient döndürür.
    Windows'ta SQLite dosya kilidi sorununu önlemek için
    aynı istemci nesnesi tekrar kullanılır.
    """
    global _chroma_client
    if _chroma_client is None or force_new:
        if _chroma_client is not None:
            try:
                _chroma_client.clear_system_cache()
            except Exception:
                pass
        _chroma_client = chromadb.PersistentClient(path=CHROMA_DIR)
    return _chroma_client


def build_vector_store(
    api_key: str,
    force_rebuild: bool = False,
) -> Chroma:
    """
    ChromaDB vektör veritabanını oluşturur veya diskten yükler.

    Args:
        api_key: Google Gemini API anahtarı.
        force_rebuild: True ise mevcut koleksiyon silinip sıfırdan kurulur.

    Returns:
        Chroma: Hazır vektör veritabanı nesnesi.
    """
    embeddings = get_embeddings(api_key)

    # Yeniden oluşturulacaksa mevcut koleksiyonu sil
    if force_rebuild:
        client = _get_chroma_client(force_new=True)
        try:
            client.delete_collection(COLLECTION_NAME)
        except Exception:
            pass
    else:
        client = _get_chroma_client()

    # Mevcut koleksiyon var mı kontrol et
    try:
        db = Chroma(
            client=client,
            collection_name=COLLECTION_NAME,
            embedding_function=embeddings,
        )
        count = db._collection.count()
        if count > 0 and not force_rebuild:
            return db
    except Exception:
        pass

    # Yeni koleksiyon oluştur ve dökümanları ekle
    documents = parse_data_file()

    db = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        collection_name=COLLECTION_NAME,
        client=client,
    )

    return db


def get_document_stats(db: Chroma) -> Dict:
    """Veritabanı istatistiklerini döndürür."""
    count = db._collection.count()

    # Metadata'dan istatistik çıkar
    all_meta = db._collection.get()["metadatas"]
    types = {}
    depts = {}
    for m in all_meta:
        t = m.get("Dokuman_Tipi", "Bilinmiyor")
        d = m.get("Departman", "Bilinmiyor")
        types[t] = types.get(t, 0) + 1
        depts[d] = depts.get(d, 0) + 1

    return {
        "toplam_dokuman": count,
        "tip_dagilimi": types,
        "departman_dagilimi": depts,
    }

