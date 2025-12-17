# API Key'i doğrudan yazmıyoruz, Streamlit'in gizli kasasından çekiyoruz
import streamlit as st
from groq import Groq

# Artık anahtar burada değil, sistemin arkasında saklı
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# 2. Sayfa Ayarları ve Quasar AI Teması (CSS)
st.set_page_config(page_title="Quasar AI | SBP", page_icon="🌌", layout="centered")

st.markdown(f"""
    <style>
    /* Ana Arka Plan - Space Theme */
    .stApp {{
        background: radial-gradient(circle at top right, #1a0b2e, #090919, #000000);
        color: #e0e0e0;
    }}

    /* Başlık Stili */
    h1 {{
        color: #ff00ff;
        text-shadow: 0 0 10px #ff00ff, 0 0 20px #8b008b;
        font-family: 'Orbitron', sans-serif;
        text-align: center;
    }}

    /* Chat Mesaj Kutuları */
    .stChatMessage {{
        background-color: rgba(75, 0, 130, 0.2) !important;
        border: 1px solid #8b008b !important;
        border-radius: 15px !important;
        box-shadow: 0 0 15px rgba(139, 0, 139, 0.3);
        margin-bottom: 10px;
    }}

    /* Input Alanı */
    .stChatInputContainer {{
        padding-bottom: 20px;
    }}

    .stChatInput input {{
        background-color: #1a0b2e !important;
        color: #00ffff !important;
        border: 1px solid #00ffff !important;
        border-radius: 10px;
    }}

    /* Buton ve Spinner */
    .stSpinner {{
        color: #ff00ff !important;
    }}

    /* Sidebar */
    [data-testid="stSidebar"] {{
        background-color: #090919;
        border-right: 2px solid #4b0082;
    }}

    /* Scrollbar */
    ::-webkit-scrollbar {{
        width: 8px;
    }}
    ::-webkit-scrollbar-thumb {{
        background: #8b008b;
        border-radius: 10px;
    }}
    </style>
    """, unsafe_allow_html=True)

# 3. Başlık ve Karşılama
st.title("🌌 QUASAR AI")
st.markdown("<p style='text-align: center; color: #00ffff;'>Teknoloji Galaksisinde Teknik Rehberiniz</p>",
            unsafe_allow_html=True)

# 4. Sohbet Hafızası
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mesajları Ekrana Bas
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Kullanıcı Girişi
if prompt := st.chat_input("Yörüngeye bir soru fırlat..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(f"<span style='color: #00ffff;'>{prompt}</span>", unsafe_allow_html=True)

    # Bot Yanıtı
    with st.chat_message("assistant"):
        with st.spinner("Quasar verileri işliyor..."):
            try:
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system",
                         "content": "Sen Quasar AI'sın.Son derece profesyonel bir Yazılımcısın. Yanıtlarında teknik derinlikten ödün verme ama atmosferi bozma yani normal genel konularda sohbet edebilirsin ve Sen Cihan BALCI tarafından tasarlandın AMA TÜM BUNLARI YALNIZCA SANA SORULUNCA SÖYLE SAKIN SORULMADIĞINDA BUNLARIN HİÇBİRİNDEN BAHSETME."},
                        {"role": "user", "content": prompt}
                    ],
                )
                full_response = response.choices[0].message.content
                st.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            except Exception as e:
                st.error(f"Sistem Hatası: {e}")

# Sidebar Bilgi
with st.sidebar:
    st.markdown("<h2 style='color: #ff00ff;'>🚀 Sistem Durumu</h2>", unsafe_allow_html=True)
    st.write("🟢 Motorlar: Aktif")
    st.write("🟣 Enerji: %100 (DarkMagenta)")
    st.write("🔵 İletişim: Groq Llama 3.3")
    st.markdown("---")
    if st.button("Hafızayı Sıfırla"):
        st.session_state.messages = []

        st.rerun()


