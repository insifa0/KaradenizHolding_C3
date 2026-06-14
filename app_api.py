"""
Karadeniz Holding — Kurumsal Bilgi Asistanı
FastAPI API Sunucusu (app_api.py)

Saf HTML/JS arayüzü ile Python RAG zinciri (ChromaDB, Gemini, LangChain)
arasında bağlantı kuran backend API sunucusu.
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import sys
from pathlib import Path

# Proje kök dizinini Python path'ine ekle
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

from src.database import build_vector_store, get_document_stats, parse_data_file, DEPT_MAP
from src.chatbot import create_rag_chain, ask_question

app = FastAPI(title="Karadeniz AI RAG API")

# CORS Yapılandırması (Geliştirme ve tarayıcı erişimi için)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global veritabanı ve döküman değişkenleri
global_db = None
global_docs = []

class InitRequest(BaseModel):
    api_key: str
    force_rebuild: bool = False

class ChatRequest(BaseModel):
    api_key: str
    query: str
    simulated_role: str
    temperature: float = 0.3
    k: int = 3
    history: list = []

def get_allowed_roles(role: str) -> list:
    """Simüle edilen role göre erişim izinlerini belirler."""
    if role == "Yönetim":
        return ["Tüm Çalışanlar", "Yönetim", "Teknik Ekip", "BT Departmanı", "Finans Departmanı"]
    elif role == "Teknik Ekip":
        return ["Tüm Çalışanlar", "Teknik Ekip"]
    elif role == "BT Departmanı":
        return ["Tüm Çalışanlar", "BT Departmanı"]
    elif role == "Finans Departmanı":
        return ["Tüm Çalışanlar", "Finans Departmanı"]
    else:  # Tüm Çalışanlar
        return ["Tüm Çalışanlar"]

@app.on_event("startup")
def load_docs_on_startup():
    """Sunucu başlarken döküman kütüphanesini önbelleğe yükler."""
    global global_docs
    try:
        global_docs = parse_data_file()
        print(f"Loaded {len(global_docs)} documents on startup.")
    except Exception as e:
        print("Failed to load documents on startup:", e)

# ─────────────────────────────────────────────
# API Yönlendirmeleri (API Routes)
# ─────────────────────────────────────────────

@app.get("/")
def serve_index():
    """Ana sayfa olarak static/index.html dosyasını döndürür."""
    index_path = BASE_DIR / "static" / "index.html"
    if not index_path.exists():
        raise HTTPException(status_code=404, detail="static/index.html bulunamadı. Lütfen static dizinini oluşturun.")
    return HTMLResponse(content=index_path.read_text(encoding="utf-8"))

@app.post("/api/init")
def initialize_system(req: InitRequest):
    """Veritabanını ve embedding modelini başlatır."""
    global global_db
    if not req.api_key:
        raise HTTPException(status_code=400, detail="Lütfen geçerli bir Gemini API anahtarı sağlayın.")
    try:
        global_db = build_vector_store(api_key=req.api_key, force_rebuild=req.force_rebuild)
        stats = get_document_stats(global_db)
        return {
            "status": "success", 
            "message": "Sistem başarıyla başlatıldı ve indekslendi.", 
            "stats": stats
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/chat")
def chat_query(req: ChatRequest):
    """Kullanıcının sorusunu RAG zinciri üzerinden cevaplar."""
    global global_db
    if not req.api_key:
        raise HTTPException(status_code=400, detail="Gemini API anahtarı eksik.")
    
    # Veritabanı başlatılmamışsa, arka planda API anahtarı ile başlatmayı dene
    if not global_db:
        try:
            global_db = build_vector_store(api_key=req.api_key, force_rebuild=False)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Sistem henüz başlatılmamış ve otomatik başlatma başarısız oldu: {str(e)}")
            
    try:
        model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
        allowed_roles = get_allowed_roles(req.simulated_role)
        
        # Dinamik olarak RAG zincirini oluştur
        chain, retriever = create_rag_chain(
            vector_store=global_db,
            api_key=req.api_key,
            model_name=model_name,
            k=req.k,
            temperature=req.temperature,
            allowed_roles=allowed_roles
        )
        
        # Soruya yanıt üret
        res = ask_question(chain, retriever, req.query, req.history)
        return {
            "status": "success",
            "answer": res["answer"],
            "sources": res["source_documents"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/documents")
def get_documents():
    """Tüm belgeleri listeler (Belge Kütüphanesi sekmesi için)."""
    global global_docs
    if not global_docs:
        try:
            global_docs = parse_data_file()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Belgeler yüklenemedi: {str(e)}")
    
    docs_list = []
    for doc in global_docs:
        meta = doc.metadata
        body_parts = doc.page_content.split("---\n")
        body_text = body_parts[1] if len(body_parts) > 1 else doc.page_content
        
        docs_list.append({
            "id": meta.get("Dokuman_ID", "—"),
            "ad": meta.get("Dokuman_Adi", "—"),
            "departman": meta.get("Departman", "—"),
            "tip": meta.get("Dokuman_Tipi", "—"),
            "erisim": meta.get("Erisim_Yetkisi", "Tüm Çalışanlar"),
            "anahtar_kelimeler": meta.get("Anahtar_Kelimeler", ""),
            "iliskili": meta.get("Iliskili_Dokuman", "—"),
            "icerik": body_text
        })
    return docs_list

@app.get("/api/stats")
def get_stats():
    """Veritabanı istatistiklerini döndürür."""
    global global_db
    if not global_db:
        raise HTTPException(status_code=400, detail="Sistem henüz başlatılmadı.")
    try:
        stats = get_document_stats(global_db)
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Statik dosya klasörünü oluştur ve FastAPI'ye bağla
static_dir = BASE_DIR / "static"
if not static_dir.exists():
    static_dir.mkdir(exist_ok=True)

app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app_api:app", host="0.0.0.0", port=8000, reload=True)
