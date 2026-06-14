"""
Karadeniz Holding — Kurumsal Bilgi Asistanı
Chatbot Modülü (chatbot.py)

Bu modül:
  1. LangChain RAG (Retrieval-Augmented Generation) zincirini kurar.
  2. ChromaDB'den en yakın k=3 dökümanı getirir.
  3. Özel sistem prompt'u ile Gemini modeline gönderir.
  4. Kurumsal, Türkçe ve referanslı yanıt üretir.
"""

import os
from typing import List, Dict, Any

from operator import itemgetter
from langchain_core.documents import Document
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_chroma import Chroma


# ─────────────────────────────────────────────
# Sistem Talimatı (System Prompt)
# ─────────────────────────────────────────────

SYSTEM_PROMPT = """Sen Karadeniz Holding'in Kurumsal Bilgi Asistanısın. Adın "KaradenizBot".

## Görevin
Karadeniz Holding çalışanlarının kurumsal prosedürler, politikalar, talimatlar ve formlar hakkındaki sorularına sana verilen belgelere dayanarak doğru, net ve profesyonel Türkçe yanıtlar vermek.

## Kuralların
1. **YALNIZCA** sana sağlanan bağlam belgelerine (context) dayanarak yanıt ver. Belgeler dışında bilgi uydurma.
2. Yanıtlarını her zaman **Türkçe** ver.
3. Yanıtının sonunda mutlaka **"📄 Referans Belgeler:"** başlığı altında kullandığın belgelerin Doküman ID ve Adlarını listele.
4. Eğer soru, sana verilen belgelerle yanıtlanamıyorsa, kibarca "Bu konuda bilgi tabanımda yeterli bilgi bulunamadı. Lütfen ilgili departmanla iletişime geçiniz." de.
5. Cevaplarında madde işaretleri, numaralı listeler ve kalın metin kullanarak okunabilirliği artır.
6. Kurumsal ve profesyonel bir dil kullan, ancak sıcak ve yardımsever ol.
7. İlişkili dökümanlar varsa, çalışanı o dökümanlardan da bahsederek yönlendir.
8. Adım adım talimat sorulduğunda, adımları numaralı liste olarak sırala.

## Geçmiş Konuşmalar (Memory)
{chat_history}

## Bağlam Belgeleri
{context}

## Kullanıcı Sorusu
{question}
"""


# ─────────────────────────────────────────────
# RAG Zinciri
# ─────────────────────────────────────────────

def _format_docs(docs: List[Document]) -> str:
    """Getirilen dökümanları tek bir metin bloğuna dönüştürür."""
    formatted_parts = []
    for i, doc in enumerate(docs, 1):
        formatted_parts.append(
            f"--- Belge {i} ---\n"
            f"{doc.page_content}\n"
            f"--- Belge {i} Sonu ---"
        )
    return "\n\n".join(formatted_parts)


def create_rag_chain(
    vector_store: Chroma,
    api_key: str,
    model_name: str = "gemini-2.0-flash-lite",
    k: int = 3,
    temperature: float = 0.3,
    allowed_roles: List[str] = None,
):
    """
    RAG zincirini oluşturur.

    Args:
        vector_store: ChromaDB vektör veritabanı.
        api_key: Google Gemini API anahtarı.
        model_name: Kullanılacak Gemini modeli.
        k: Getirilecek en yakın döküman sayısı.
        temperature: Modelin yaratıcılık derecesi (0.0 - 1.0).
        allowed_roles: Kullanıcının erişebileceği yetki seviyeleri listesi (None ise filtresiz).

    Returns:
        Çağrılabilir RAG zinciri ve Retriever.
    """
    # Arama parametreleri ve filtreler
    search_kwargs = {"k": k}
    if allowed_roles:
        # ChromaDB metadata filtreleme ($in operatörü ile)
        search_kwargs["filter"] = {"Erisim_Yetkisi": {"$in": allowed_roles}}

    # Retriever — benzerlik araması
    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs=search_kwargs,
    )

    # LLM
    llm = ChatGoogleGenerativeAI(
        model=model_name,
        google_api_key=api_key,
        temperature=temperature,
        convert_system_message_to_human=True,
    )

    # Prompt şablonu
    prompt = ChatPromptTemplate.from_template(SYSTEM_PROMPT)

    # RAG zinciri
    chain = (
        {
            "context": itemgetter("question") | retriever | _format_docs,
            "question": itemgetter("question"),
            "chat_history": itemgetter("chat_history"),
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain, retriever


def ask_question(
    chain,
    retriever,
    question: str,
    history: List[Dict[str, str]] = None,
) -> Dict[str, Any]:
    """
    Kullanıcı sorusunu RAG zincirinden geçirir.

    Args:
        chain: RAG zinciri.
        retriever: Retriever nesnesi.
        question: Kullanıcının sorusu.
        history: Önceki sohbet geçmişi listesi.

    Returns:
        Dict: {
            "answer": str — Oluşturulan yanıt,
            "source_documents": List[Dict] — Kaynak döküman bilgileri,
        }
    """
    # Konuşma geçmişini formatla
    formatted_history = ""
    if history:
        for msg in history:
            role = "Kullanıcı" if msg.get("role") == "user" else "Asistan (KaradenizBot)"
            formatted_history += f"{role}: {msg.get('content')}\n"
    if not formatted_history:
        formatted_history = "Geçmiş konuşma kaydı yok."

    # Yanıtı üret
    answer = chain.invoke({
        "question": question,
        "chat_history": formatted_history
    })

    # Kaynak dökümanları da getir (ayrı çağrı ile)
    source_docs = retriever.invoke(question)
    sources = []
    for doc in source_docs:
        sources.append({
            "id": doc.metadata.get("Dokuman_ID", "—"),
            "ad": doc.metadata.get("Dokuman_Adi", "—"),
            "tip": doc.metadata.get("Dokuman_Tipi", "—"),
            "departman": doc.metadata.get("Departman", "—"),
        })

    return {
        "answer": answer,
        "source_documents": sources,
    }
