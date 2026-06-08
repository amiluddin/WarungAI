import streamlit as st
from google import genai
from PIL import Image

# Setup konfigurasi halaman
st.set_page_config(page_title="WarungAI", page_icon="🏪", layout="centered")

# --- KUNCI TOKEN GEMINI ---
# Ganti teks di bawah ini dengan API Key asli yang lo dapet tadi!
GEMINI_API_KEY = "AQ.Ab8RN6LUqHajKnYZVLY6oaP6y3jrOqmJBkPu7HQTaLIm9dGzvw"

# Inisialisasi Google GenAI Client
try:
    client = genai.Client(api_key=GEMINI_API_KEY)
except Exception as e:
    st.error("Gagal terhubung ke Gemini API. Pastikan API Key lo bener, bro!")

# Judul Utama Aplikasi
st.title("🏪 WarungAI")
st.subheader("Asisten Pintar Keuangan & Konten UMKM")
st.write("Solusi cerdas berbasis Generative AI untuk memajukan usaha Anda.")

st.markdown("---")

# Bikin menu pilihan (Tab)
tab1, tab2 = st.tabs(["📊 Catat Keuangan (Teks/Suara)", "📸 Bikin Konten Promosi (Foto)"])

with tab1:
    st.header("Asisten Keuangan Cerdas")
    st.write("Tuliskan transaksi warung/toko Anda di bawah ini:")
    
    input_keuangan = st.text_area(
        "Contoh: Tadi laku sembako, indomie 3 bungkus sama telur total 25 ribu", 
        placeholder="Ketik di sini...",
        key="input_txt_keuangan"
    )
    
    if st.button("Proses & Catat Transaksi", key="btn_keuangan"):
        if input_keuangan:
            with st.spinner("AI sedang menganalisis dan mencatat transaksi..."):
                try:
                    # Prompt ketat agar Gemini mengembalikan format tabel rapi
                    prompt_keuangan = f"""
                    Anda adalah asisten akuntansi UMKM Indonesia yang cerdas. 
                    Tugas Anda adalah mengekstrak teks transaksi mentah menjadi laporan keuangan yang rapi dalam bentuk tabel.
                    Keluarkan output berupa tabel Markdown dengan kolom: No, Nama Barang/Kategori, Jumlah, Harga Satuan (jika ada), Total Harga.
                    Di akhir tabel, berikan kesimpulan total uang masuk atau keluar.

                    Teks Transaksi: "{input_keuangan}"
                    """
                    
                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=prompt_keuangan
                    )
                    
                    st.success("Transaksi Berhasil Dicatat!")
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Waduh ada error pas manggil AI: {e}")
        else:
            st.warning("Isi dulu teks transaksinya, bro!")

with tab2:
    st.header("Asisten Konten Otomatis")
    st.write("Unggah foto produk Anda untuk dibuatkan caption jualan otomatis:")
    
    foto_produk = st.file_uploader("Pilih foto produk (PNG, JPG, JPEG)", type=["png", "jpg", "jpeg"])
    
    if foto_produk:
        # Tampilkan gambar yang diunggah
        image = Image.open(foto_produk)
        st.image(image, caption="Foto Produk Anda", use_container_width=True)
        
        if st.button("Buat Caption Jualan", key="btn_konten"):
            with st.spinner("Gemini sedang melihat foto dan meracik caption cetar..."):
                try:
                    # Prompt agar Gemini membuat caption promosi medsos
                    prompt_konten = """
                    Anda adalah seorang Digital Marketer dan Copywriter ahli untuk UMKM Indonesia.
                    Lihat foto produk ini, analisis produk apa ini, lalu buatkan 3 pilihan caption promosi yang menarik, persuasif, dan relevan untuk jualan di WhatsApp Status atau Instagram.
                    Gunakan bahasa yang ramah, santai, namun tetap sopan. Tambahkan emoji yang sesuai dan hashtag (#) populer di akhir setiap pilihan.
                    """
                    
                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=[image, prompt_konten]
                    )
                    
                    st.success("Caption Promosi Siap Digunakan!")
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Waduh ada error pas manggil AI: {e}")