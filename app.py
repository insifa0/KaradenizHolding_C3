"""
Karadeniz Holding — Kurumsal Bilgi Asistanı
Streamlit Arayüzü (app.py)

Kurumsal kimliğe (lacivert/turkuaz) uygun, premium, glassmorphism ve
glowing tasarıma sahip, yetki simülatörlü ve belge kütüphaneli modern arayüz.

Çalıştırmak için:
    streamlit run app.py
"""

import os
import sys
import streamlit as st
from dotenv import load_dotenv
from pathlib import Path

# Proje kök dizinini Python path'ine ekle
sys.path.insert(0, str(Path(__file__).resolve().parent))

from src.database import build_vector_store, get_document_stats, parse_data_file, DEPT_MAP
from src.chatbot import create_rag_chain, ask_question

# ─────────────────────────────────────────────
# Yapılandırma
# ─────────────────────────────────────────────
load_dotenv()

# ─────────────────────────────────────────────
# Sayfa Yapılandırması
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Karadeniz Holding — Kurumsal Bilgi Asistanı",
    page_icon="🚢",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# Yardımcı Fonksiyonlar
# ─────────────────────────────────────────────
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

def export_chat_history() -> str:
    """Konuşma geçmişini Markdown formatında dışa aktarır."""
    md_content = "# 🚢 Karadeniz Holding Kurumsal Bilgi Asistanı - Sohbet Geçmişi\n\n"
    for msg in st.session_state.messages:
        role_name = "🧑‍💼 Kullanıcı" if msg["role"] == "user" else "🚢 Asistan (KaradenizBot)"
        md_content += f"### {role_name}\n{msg['content']}\n\n"
        if "sources" in msg and msg["sources"]:
            md_content += "**📄 Referans Belgeler:**\n"
            for src in msg["sources"]:
                md_content += f"- **{src['id']}** — {src['ad']} (Departman: {src['departman']} | Tip: {src['tip']})\n"
            md_content += "\n"
        md_content += "---\n\n"
    return md_content

# ─────────────────────────────────────────────
# Kurumsal CSS Teması
# ─────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@400;500;600;700;800&display=swap');

    /* ── Yazı Tipleri ve Genel Sayfa ── */
    html, body, [class*="css"], .stApp {
        font-family: 'Inter', sans-serif !important;
        background: linear-gradient(135deg, #060e1a 0%, #0a172c 50%, #0f2340 100%) !important;
        color: #e2f0fb !important;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Outfit', sans-serif !important;
    }

    /* ── Glassmorphic Sidebar ── */
    section[data-testid="stSidebar"] {
        background: rgba(10, 25, 47, 0.65) !important;
        backdrop-filter: blur(16px);
        border-right: 2px solid rgba(0, 168, 181, 0.3) !important;
        box-shadow: 5px 0 25px rgba(0, 0, 0, 0.3);
    }
    section[data-testid="stSidebar"] .stMarkdown h1,
    section[data-testid="stSidebar"] .stMarkdown h2,
    section[data-testid="stSidebar"] .stMarkdown h3 {
        color: #00d4e6 !important;
        font-weight: 700;
    }
    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] .stMarkdown li {
        color: #c8dbe8 !important;
    }

    /* ── Başlık Kutusu (Header Card) ── */
    .main-header {
        background: rgba(12, 35, 64, 0.45) !important;
        backdrop-filter: blur(12px);
        border: 1px solid rgba(0, 168, 181, 0.25);
        border-radius: 20px;
        padding: 1.5rem 2rem;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0, 168, 181, 0.15), inset 0 0 15px rgba(0, 168, 181, 0.05);
    }
    .main-header h1 {
        color: #ffffff !important;
        font-size: 2.2rem !important;
        margin: 0 0 0.5rem 0 !important;
        font-weight: 800;
        letter-spacing: 0.5px;
        text-shadow: 0 0 15px rgba(0, 212, 230, 0.2);
    }
    .main-header p {
        color: #00d4e6 !important;
        font-size: 1.1rem;
        margin: 0;
        font-weight: 500;
    }

    /* ── Sohbet Kutuları & Mesajlar ── */
    div[data-testid="stChatMessage"] {
        background-color: rgba(12, 35, 64, 0.3) !important;
        border: 1px solid rgba(0, 168, 181, 0.15) !important;
        border-radius: 16px !important;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15) !important;
        padding: 1.2rem !important;
        margin-bottom: 0.8rem !important;
        transition: all 0.3s ease;
    }
    
    div[data-testid="stChatMessage"]:hover {
        border-color: rgba(0, 212, 230, 0.45) !important;
        box-shadow: 0 6px 20px rgba(0, 212, 230, 0.1) !important;
    }

    /* ── Metrik ve İstatistik Kartları ── */
    .metric-card {
        background: rgba(12, 35, 64, 0.5) !important;
        backdrop-filter: blur(8px);
        border: 1px solid rgba(0, 168, 181, 0.25);
        border-radius: 14px;
        padding: 1.2rem 1rem;
        text-align: center;
        margin-bottom: 0.75rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
    }
    .metric-card:hover {
        border-color: rgba(0, 212, 230, 0.5);
        box-shadow: 0 6px 18px rgba(0, 212, 230, 0.15);
        transform: translateY(-2px);
    }
    .metric-card .metric-value {
        color: #00d4e6;
        font-size: 2.2rem;
        font-weight: 800;
        text-shadow: 0 0 10px rgba(0, 212, 230, 0.3);
    }
    .metric-card .metric-label {
        color: #8fa8c0;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-top: 0.25rem;
    }

    /* ── Kaynak Belge Kartı (Source Cards) ── */
    .source-card {
        background: rgba(0, 168, 181, 0.05);
        border: 1px solid rgba(0, 168, 181, 0.2);
        border-left: 4px solid #00a8b5;
        border-radius: 8px;
        padding: 0.8rem 1.2rem;
        margin: 0.5rem 0;
        font-size: 0.9rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        transition: all 0.2s ease;
    }
    .source-card:hover {
        background: rgba(0, 168, 181, 0.1);
        border-color: rgba(0, 212, 230, 0.4);
    }
    .source-card strong {
        color: #00d4e6;
    }

    /* ── Info Banner / İpuçları ── */
    .info-banner {
        background: rgba(0, 168, 181, 0.08) !important;
        border: 1px solid rgba(0, 168, 181, 0.25) !important;
        border-radius: 12px;
        padding: 1rem;
        margin: 0.75rem 0;
        color: #c8dbe8;
        font-size: 0.9rem;
        box-shadow: inset 0 0 10px rgba(0, 168, 181, 0.05);
    }

    /* ── Butonlar (Streamlit Buttons) ── */
    .stButton > button {
        background: linear-gradient(135deg, #00a8b5 0%, #008a95 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        padding: 0.6rem 1.2rem !important;
        box-shadow: 0 4px 15px rgba(0, 168, 181, 0.25) !important;
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        width: 100%;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #00d4e6 0%, #00a8b5 100%) !important;
        box-shadow: 0 6px 20px rgba(0, 212, 230, 0.45) !important;
        transform: translateY(-2px) !important;
    }
    .stButton > button:active {
        transform: translateY(0px) !important;
    }

    /* ── Azure Adımları ── */
    .azure-step {
        background: rgba(0, 120, 212, 0.05) !important;
        border: 1px solid rgba(0, 120, 212, 0.2) !important;
        border-left: 4px solid #0078d4 !important;
        border-radius: 8px;
        padding: 1rem 1.2rem;
        margin: 0.6rem 0;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        transition: all 0.2s ease;
    }
    .azure-step:hover {
        background: rgba(0, 120, 212, 0.1) !important;
        border-color: rgba(0, 120, 212, 0.4) !important;
    }
    .azure-step strong {
        color: #5ba7e6;
    }

    /* ── Canlı Durum Paneli (Status Badge) ── */
    .status-container {
        display: flex;
        align-items: center;
        background: rgba(0, 168, 181, 0.08);
        border: 1px solid rgba(0, 168, 181, 0.25);
        border-radius: 10px;
        padding: 0.6rem 0.8rem;
        margin-bottom: 1.2rem;
        box-shadow: inset 0 0 8px rgba(0, 168, 181, 0.05);
    }
    .status-badge {
        display: inline-block;
        width: 8px;
        height: 8px;
        background-color: #ff4d4d;
        border-radius: 50%;
        margin-right: 10px;
        box-shadow: 0 0 10px #ff4d4d;
    }
    .status-badge.active {
        background-color: #00d4e6 !important;
        box-shadow: 0 0 10px #00d4e6 !important;
    }
    .status-badge.pulse {
        animation: pulsing 1.8s infinite;
    }
    .status-text {
        font-size: 0.85rem;
        color: #e2f0fb;
        font-weight: 600;
    }
    @keyframes pulsing {
        0% {
            transform: scale(0.9);
            box-shadow: 0 0 0 0 rgba(0, 212, 230, 0.7);
        }
        70% {
            transform: scale(1.1);
            box-shadow: 0 0 0 8px rgba(0, 212, 230, 0);
        }
        100% {
            transform: scale(0.9);
            box-shadow: 0 0 0 0 rgba(0, 212, 230, 0);
        }
    }

    /* ── Belge Kütüphanesi Etiketleri ── */
    .doc-tag {
        display: inline-block;
        background: rgba(0, 168, 181, 0.1);
        border: 1px solid rgba(0, 168, 181, 0.25);
        padding: 0.2rem 0.6rem;
        border-radius: 6px;
        color: #00d4e6;
        font-size: 0.8rem;
        font-weight: 500;
    }
    .doc-tag.danger {
        background: rgba(220, 53, 69, 0.1) !important;
        border-color: rgba(220, 53, 69, 0.25) !important;
        color: #ff6b6b !important;
    }

    /* ── Chat Input Genişlik & Kenarlık ── */
    .stChatInput > div {
        border-color: rgba(0, 168, 181, 0.3) !important;
        background-color: rgba(12, 35, 64, 0.4) !important;
        backdrop-filter: blur(10px);
        border-radius: 12px !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2) !important;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Oturum Durumu (Session State)
# ─────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

if "db" not in st.session_state:
    st.session_state.db = None

if "db_stats" not in st.session_state:
    st.session_state.db_stats = None

if "system_ready" not in st.session_state:
    st.session_state.system_ready = False

if "all_docs" not in st.session_state:
    try:
        st.session_state.all_docs = parse_data_file()
    except Exception:
        st.session_state.all_docs = []

# ─────────────────────────────────────────────
# Sidebar
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🚢 Karadeniz Holding")
    st.markdown("**Kurumsal Bilgi Asistanı**")
    st.markdown("---")

    # Canlı Durum Paneli
    status_class = "active pulse" if st.session_state.system_ready else ""
    status_label = "Sistem Çevrimiçi / Hazır" if st.session_state.system_ready else "Sistem Başlatılmadı"
    st.markdown(f"""
    <div class="status-container">
        <span class="status-badge {status_class}"></span>
        <span class="status-text">{status_label}</span>
    </div>
    """, unsafe_allow_html=True)

    # API Anahtarı Girişi
    api_key = st.text_input(
        "🔑 Gemini API Anahtarı",
        type="password",
        value=os.getenv("GEMINI_API_KEY", ""),
        help="Google AI Studio'dan alınan API anahtarınızı girin.",
    )

    model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

    # Güvenlik Rol Simülatörü
    st.markdown("### 🔐 Yetki Simülatörü")
    simulated_role = st.selectbox(
        "Simüle Edilen Rolü Seçin",
        options=["Tüm Çalışanlar", "Teknik Ekip", "BT Departmanı", "Finans Departmanı", "Yönetim"],
        help="Simüle edilen role göre RAG sistemi sadece erişim izniniz olan dökümanları sorgular."
    )

    # Sistemi Başlat
    if st.button("🚀 Sistemi Başlat", use_container_width=True):
        if not api_key:
            st.error("⚠️ Lütfen Gemini API anahtarınızı girin.")
        else:
            with st.spinner("📚 Veri tabanı hazırlanıyor..."):
                try:
                    db = build_vector_store(api_key=api_key, force_rebuild=False)
                    st.session_state.db = db
                    st.session_state.db_stats = get_document_stats(db)
                    st.session_state.system_ready = True
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Hata: {str(e)}")

    # Veritabanını Yeniden Oluştur
    if st.session_state.system_ready:
        if st.button("🔄 Veritabanını Yeniden Oluştur", use_container_width=True):
            with st.spinner("♻️ Veritabanı yeniden oluşturuluyor..."):
                try:
                    db = build_vector_store(api_key=api_key, force_rebuild=True)
                    st.session_state.db = db
                    st.session_state.db_stats = get_document_stats(db)
                    st.success("✅ Veritabanı yeniden oluşturuldu!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Hata: {str(e)}")

    # Gelişmiş Ayarlar (Jüri için gizli sekme)
    st.markdown("---")
    with st.expander("🔧 Gelişmiş / Yönetici Ayarları", expanded=False):
        temp_val = st.slider(
            "Cevap Yaratıcılığı (Temp)",
            min_value=0.0,
            max_value=1.0,
            value=0.3,
            step=0.1,
            help="Düşük değerler kesin/tutarlı cevaplar, yüksek değerler daha yaratıcı cevaplar üretir."
        )
        k_val = st.slider(
            "Arama Derinliği (k)",
            min_value=1,
            max_value=5,
            value=3,
            step=1,
            help="Arka planda sorgulanan döküman sayısı."
        )

    # Sohbet Kontrolleri
    st.markdown("---")
    if st.session_state.system_ready and st.session_state.messages:
        chat_md = export_chat_history()
        st.download_button(
            label="📥 Sohbeti Dışa Aktar (MD)",
            data=chat_md,
            file_name="karadeniz_bot_sohbet_gecmisi.md",
            mime="text/markdown",
            use_container_width=True,
        )

    if st.button("🗑️ Sohbeti Temizle", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    # İstatistikler
    if st.session_state.db_stats:
        stats = st.session_state.db_stats
        st.markdown("---")
        with st.expander("📊 Bilgi Tabanı İstatistikleri", expanded=False):
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{stats['toplam_dokuman']}</div>
                <div class="metric-label">Toplam Döküman</div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("**📁 Tipe Göre Dağılım:**")
            type_icons = {"Prosedür": "📋", "Politika": "📜", "Talimat": "📝", "Form": "📄"}
            for tip, count in stats["tip_dagilimi"].items():
                icon = type_icons.get(tip, "📎")
                st.markdown(f"{icon} {tip}: **{count}**")

            st.markdown("**🏢 Departmana Göre:**")
            for dept, count in stats["departman_dagilimi"].items():
                st.markdown(f"• {dept}: **{count}**")

    # Bilgi Notu
    st.markdown("---")
    st.markdown("""
    <div class="info-banner">
        💡 <strong>İpucu:</strong> Doğal dilde sorularınızı yazabilirsiniz.<br>
        Örnek: <em>"VPN'e nasıl bağlanırım?"</em>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"<small style='color:#5a7a94'>Model: {model_name}</small>", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# Ana İçerik Alanı
# ─────────────────────────────────────────────

# Başlık
st.markdown("""
<div class="main-header">
    <h1>🚢 Karadeniz Holding — Kurumsal Bilgi Asistanı</h1>
    <p>Prosedürler • Politikalar • Talimatlar • Formlar — Yapay Zeka Destekli Erişim</p>
</div>
""", unsafe_allow_html=True)

# Tab yapısı
tab_chat, tab_library, tab_azure = st.tabs(["💬 Sohbet", "📁 Belge Kütüphanesi", "☁️ Azure Bulut Geçiş Planı"])

# ── 1. Tab: Sohbet (Chat) ──
with tab_chat:
    if not st.session_state.system_ready:
        st.markdown("""
        <div style="text-align:center; padding:3rem 2rem;">
            <p style="font-size:4rem; margin-bottom:1rem; text-shadow: 0 0 20px rgba(0,212,230,0.3);">🚢</p>
            <h3 style="color:#00d4e6; margin-bottom:0.5rem; font-size:1.6rem; font-family:'Outfit',sans-serif;">Hoş Geldiniz!</h3>
            <p style="color:#8fa8c0; max-width:550px; margin:0 auto; font-size:1rem; line-height:1.6;">
                Kurumsal Bilgi Asistanını kullanmaya başlamak için
                sol paneldeki <strong>API anahtarınızı</strong> girin ve
                <strong>"🚀 Sistemi Başlat"</strong> butonuna tıklayın.
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Sohbet Geçmişi
        for msg in st.session_state.messages:
            avatar = "🧑‍💼" if msg["role"] == "user" else "🚢"
            with st.chat_message(msg["role"], avatar=avatar):
                st.markdown(msg["content"])

                # Kaynak belgeler (sadece asistan mesajları için)
                if msg["role"] == "assistant" and "sources" in msg:
                    with st.expander("📄 Kaynak Belgeler", expanded=False):
                        for src in msg["sources"]:
                            st.markdown(f"""
                            <div class="source-card">
                                <strong>{src['id']}</strong> — {src['ad']}<br>
                                <span style="color:#7a9ab5;">📁 {src['departman']} | 📋 {src['tip']}</span>
                            </div>
                            """, unsafe_allow_html=True)

        # Kullanıcı Girişi
        if user_input := st.chat_input("Sorunuzu yazın... (Örn: 'İzin talebi nasıl oluşturulur?')"):
            # Kullanıcı mesajını ekle
            st.session_state.messages.append({"role": "user", "content": user_input})
            with st.chat_message("user", avatar="🧑‍💼"):
                st.markdown(user_input)

            # Asistan yanıtı
            with st.chat_message("assistant", avatar="🚢"):
                with st.spinner("🔍 Bilgi tabanı taranıyor..."):
                    try:
                        # Dinamik olarak RAG zincirini oluştur (parametre ve filtrelerle)
                        allowed_roles = get_allowed_roles(simulated_role)
                        chain, retriever = create_rag_chain(
                            vector_store=st.session_state.db,
                            api_key=api_key,
                            model_name=model_name,
                            k=k_val,
                            temperature=temp_val,
                            allowed_roles=allowed_roles,
                        )
                        
                        result = ask_question(
                            chain=chain,
                            retriever=retriever,
                            question=user_input,
                        )
                        answer = result["answer"]
                        sources = result["source_documents"]

                        st.markdown(answer)

                        # Kaynak belgeler
                        if sources:
                            with st.expander("📄 Kaynak Belgeler", expanded=False):
                                for src in sources:
                                    st.markdown(f"""
                                    <div class="source-card">
                                        <strong>{src['id']}</strong> — {src['ad']}<br>
                                        <span style="color:#7a9ab5;">📁 {src['departman']} | 📋 {src['tip']}</span>
                                    </div>
                                    """, unsafe_allow_html=True)

                        # Mesajı oturuma kaydet
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": answer,
                            "sources": sources,
                        })

                    except Exception as e:
                        error_msg = f"❌ Yanıt oluşturulurken bir hata meydana geldi: {str(e)}"
                        st.error(error_msg)
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": error_msg,
                        })


# ── 2. Tab: Belge Kütüphanesi (Document Library) ──
with tab_library:
    st.markdown("### 📁 Kurumsal Belge Kütüphanesi")
    st.markdown("Holding bünyesinde kayıtlı 120 belgenin tamamını departman ve türe göre filtreleyerek inceleyebilirsiniz.")

    # Arama ve Filtreleme Bölümü
    col_search, col_dept, col_type = st.columns([2, 1, 1])
    with col_search:
        search_query = st.text_input("Belge adı veya ID ile ara...", value="")
    with col_dept:
        dept_options = ["Tümü"] + list(DEPT_MAP.values())
        selected_dept_filter = st.selectbox("Departman Filtresi", options=dept_options)
    with col_type:
        type_options = ["Tümü", "Prosedür", "Politika", "Talimat", "Form"]
        selected_type_filter = st.selectbox("Belge Tipi Filtresi", options=type_options)

    # Belgeleri Filtrele
    filtered_docs = []
    if "all_docs" in st.session_state and st.session_state.all_docs:
        for doc in st.session_state.all_docs:
            meta = doc.metadata
            doc_id = meta.get("Dokuman_ID", "")
            doc_name = meta.get("Dokuman_Adi", "")
            dept = meta.get("Departman", "")
            doc_type = meta.get("Dokuman_Tipi", "")
            
            # Yazı arama filtresi
            if search_query:
                q = search_query.lower()
                if q not in doc_id.lower() and q not in doc_name.lower():
                    continue
            # Departman filtresi
            if selected_dept_filter != "Tümü" and dept != selected_dept_filter:
                continue
            # Belge tipi filtresi
            if selected_type_filter != "Tümü" and doc_type != selected_type_filter:
                continue
                
            filtered_docs.append(doc)
            
    # Filtrelenmiş belgeleri listele
    if not filtered_docs:
        st.info("Kriterlere uygun belge bulunamadı.")
    else:
        st.markdown(f"**Toplam Listelenen Belge:** {len(filtered_docs)}")
        
        for doc in filtered_docs:
            meta = doc.metadata
            doc_id = meta.get("Dokuman_ID", "")
            doc_name = meta.get("Dokuman_Adi", "")
            dept = meta.get("Departman", "")
            doc_type = meta.get("Dokuman_Tipi", "")
            access = meta.get("Erisim_Yetkisi", "Tüm Çalışanlar")
            keywords = meta.get("Anahtar_Kelimeler", "")
            related = meta.get("Iliskili_Dokuman", "—")
            
            # İçerik gövdesi (metadatadan arındırılmış)
            body_parts = doc.page_content.split("---\n")
            body_text = body_parts[1] if len(body_parts) > 1 else doc.page_content
            
            with st.expander(f"📄 {doc_id} — {doc_name}", expanded=False):
                st.markdown(f"""
                <div style="background: rgba(12, 35, 64, 0.2); padding: 1rem; border-radius: 8px; border: 1px dashed rgba(0, 168, 181, 0.25);">
                    <div style="margin-bottom: 0.5rem; display: flex; flex-wrap: wrap; gap: 8px;">
                        <span class="doc-tag">🏢 Departman: {dept}</span>
                        <span class="doc-tag">📋 Tip: {doc_type}</span>
                        <span class="doc-tag {'danger' if access != 'Tüm Çalışanlar' else ''}">🔐 Erişim Yetkisi: {access}</span>
                    </div>
                    <p style="white-space: pre-wrap; color: #c8dbe8; font-size: 0.95rem; line-height: 1.6;">{body_text}</p>
                    <hr style="border-color: rgba(0, 168, 181, 0.15); margin: 0.75rem 0;">
                    <div style="font-size: 0.8rem; color: #8fa8c0; line-height: 1.5;">
                        <strong>🔗 İlişkili Belgeler:</strong> {related} <br>
                        <strong>🔑 Anahtar Kelimeler:</strong> {keywords}
                    </div>
                </div>
                """, unsafe_allow_html=True)


# ── 3. Tab: Azure Bulut Yol Haritası ──
with tab_azure:
    st.markdown("### ☁️ Azure Bulut Geçiş Yol Haritası")
    st.markdown("""
    Bu bölüm, jüriye sunulmak üzere hazırlanan yerel RAG mimarisinin
    Azure bulut ortamına nasıl taşınacağını göstermektedir.
    """)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="azure-step">
            <strong>📦 Veri Depolama</strong><br>
            <em>Şu an:</em> Yerel CSV / TXT dosyası<br>
            <em>Azure:</em> Azure Blob Storage + SharePoint entegrasyonu
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="azure-step">
            <strong>🔍 Vektör Arama</strong><br>
            <em>Şu an:</em> ChromaDB (Yerel)<br>
            <em>Azure:</em> Azure AI Search<br>
            <small>Otomatik döküman indeksleme ve hibrit arama</small>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="azure-step">
            <strong>🔐 Güvenlik ve Yetkilendirme</strong><br>
            <em>Şu an:</em> Basit erişim simülasyonu<br>
            <em>Azure:</em> Microsoft Entra ID (Active Directory)<br>
            <small>Çalışanlar sadece yetkili belgelere erişir</small>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="azure-step">
            <strong>🤖 Yapay Zeka Modeli</strong><br>
            <em>Şu an:</em> Google Gemini API (Yerel)<br>
            <em>Azure:</em> Azure OpenAI Service<br>
            <small>Güvenli, şirket dışına veri sızdırmayan özel GPT-4o modeli</small>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="azure-step">
            <strong>📊 İzleme ve Analitik</strong><br>
            <em>Şu an:</em> Streamlit istatistikleri<br>
            <em>Azure:</em> Azure Monitor + Application Insights<br>
            <small>Kullanım analitiği, yanıt kalitesi takibi</small>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="azure-step">
            <strong>🔄 Orkestrasyon</strong><br>
            <em>Şu an:</em> LangChain (Python)<br>
            <em>Azure:</em> Azure AI Studio + Prompt Flow<br>
            <small>Görsel akış tasarımı, A/B test desteği</small>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Mimari Diyagramı
    st.markdown("### 🏗️ Mevcut vs. Azure Mimarisi")

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("#### 🖥️ Mevcut (Yerel) Mimari")
        st.code("""
┌─────────────────────────┐
│   Kullanıcı (Streamlit) │
└───────────┬─────────────┘
            │
┌───────────▼─────────────┐
│   LangChain RAG Zinciri │
│   ┌─────────────────┐   │
│   │  ChromaDB (Yerel)│   │
│   └─────────────────┘   │
│   ┌─────────────────┐   │
│   │ Gemini API (Dış) │   │
│   └─────────────────┘   │
└─────────────────────────┘
        """, language=None)

    with col_b:
        st.markdown("#### ☁️ Hedef Azure Mimarisi")
        st.code("""
┌─────────────────────────┐
│  Kullanıcı (Azure Web)  │
│  + Entra ID Auth        │
└───────────┬─────────────┘
            │
┌───────────▼─────────────┐
│  Azure AI Studio        │
│   ┌─────────────────┐   │
│   │ Azure AI Search  │   │
│   │ (Vektör + Hibrit)│   │
│   └─────────────────┘   │
│   ┌─────────────────┐   │
│   │ Azure OpenAI     │   │
│   │ Service (GPT-4o) │   │
│   └─────────────────┘   │
└─────────────────────────┘
        """, language=None)
