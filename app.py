import streamlit as st

# --- KAMUS DATA ---
# Kamus ini untuk mengubah kode di dataset menjadi teks yang bisa dibaca manusia
# Ini membuat dropdown di aplikasi kita jadi lebih user-friendly.

odor_options = {
    'a': 'Almond',
    'l': 'Anise (Jintan Manis)',
    'c': 'Creosote (seperti bau tiang listrik)',
    'y': 'Fishy (Amis)',
    'f': 'Foul (Busuk)',
    'm': 'Musty (Apek)',
    'n': 'None (Tidak Berbau)',
    'p': 'Pungent (Pedas/Menyengat)',
    's': 'Spicy (Rempah)'
}

gill_size_options = {
    'b': 'Broad (Lebar)',
    'n': 'Narrow (Sempit)'
}

gill_color_options = {
    'k': 'Black (Hitam)',
    'n': 'Brown (Coklat)',
    'b': 'Buff (Krem)',
    'h': 'Chocolate (Coklat Tua)',
    'g': 'Gray (Abu-abu)',
    'r': 'Green (Hijau)',
    'o': 'Orange (Oranye)',
    'p': 'Pink',
    'u': 'Purple (Ungu)',
    'e': 'Red (Merah)',
    'w': 'White (Putih)',
    'y': 'Yellow (Kuning)'
}

stalk_root_options = {
    'b': 'Bulbous (Membesar di pangkal)',
    'c': 'Club (Seperti Gada)',
    'u': 'Cup (Seperti Cangkir)',
    'e': 'Equal (Sama Rata)',
    'z': 'Rhizomorphs (Seperti Akar)',
    'r': 'Rooted (Berakar)',
    '?': 'Missing (Tidak Ada)'
}


# --- LOGIKA SISTEM PAKAR ---
# Ini adalah inti dari sistem pakar kita.
# Aturan (rules) dibuat berdasarkan analisis data jamur yang sangat terkenal.

def diagnose_mushroom(odor, gill_size, gill_color, stalk_root):
    """
    Fungsi ini berisi aturan-aturan (knowledge base) untuk mendiagnosis jamur.
    Inputnya adalah ciri-ciri jamur, outputnya adalah tuple (status, alasan).
    """
    # Aturan #1: Bau (Odor) adalah penentu paling kuat.
    # Jika bau sudah jelas, kita bisa langsung ambil kesimpulan.
    if odor in ['a', 'l']:
        return ('AMAN', 'Jamur dengan bau Almond (a) atau Anise (l) hampir selalu aman untuk dimakan.')
    
    if odor in ['c', 'y', 'f', 'm', 'p', 's']:
        return ('BERACUN', f"Bau '{odor_options[odor]}' adalah indikator kuat jamur beracun.")

    # Aturan #2: Jika tidak berbau (odor = 'n'), kita butuh ciri lain.
    # Ini adalah contoh "chaining" atau aturan berantai.
    if odor == 'n':
        # Aturan #2a: Ukuran insang (gill-size) bisa jadi pembeda.
        if gill_size == 'n':
            return ('BERACUN', 'Jamur tidak berbau dengan insang yang sempit (narrow) seringkali beracun.')
        
        # Aturan #2b: Warna insang (gill-color) juga penting.
        if gill_color == 'b':
            return ('BERACUN', 'Jamur tidak berbau dengan insang berwarna krem/buff seringkali beracun.')

        # Aturan #2c: Akar (stalk-root) yang hilang/missing.
        if stalk_root == '?':
            return ('BERACUN', 'Jamur tidak berbau dan tidak memiliki akar yang jelas (missing) cenderung beracun.')
            
        # Jika tidak ada aturan di atas yang cocok, kemungkinan besar aman.
        return ('AMAN', 'Jamur tidak berbau dan memiliki ciri-ciri lain (insang lebar, warna insang aman, dll.) yang mengindikasikan jamur aman.')

    # Aturan Default: Jika tidak ada aturan yang cocok sama sekali.
    return ('TIDAK DIKETAHUI', 'Kombinasi ciri-ciri ini tidak ada dalam basis pengetahuan kami.')


# --- TAMPILAN APLIKASI STREAMLIT ---
# Bagian ini mengatur semua yang tampil di layar.

st.set_page_config(page_title="Sistem Pakar Jamur", page_icon="🍄")

st.title("🍄 Sistem Pakar Identifikasi Jamur")
st.write(
    "Aplikasi ini membantu Anda mengidentifikasi apakah sebuah jamur aman dimakan atau beracun "
    "berdasarkan ciri-ciri fisiknya. Ini adalah implementasi sederhana dari sistem pakar."
)
st.write("---")

# Membuat input di sidebar
st.sidebar.header("Masukkan Ciri-ciri Jamur:")

# Menggunakan kamus untuk menampilkan teks, tapi mengirim kode ke fungsi.
# `format_func` membuat dropdown menampilkan teks yang mudah dibaca.
input_odor = st.sidebar.selectbox(
    '1. Bau Jamur (Odor)',
    options=list(odor_options.keys()),
    format_func=lambda x: f"{x} - {odor_options[x]}"
)

input_gill_size = st.sidebar.selectbox(
    '2. Ukuran Insang (Gill Size)',
    options=list(gill_size_options.keys()),
    format_func=lambda x: f"{x} - {gill_size_options[x]}"
)

input_gill_color = st.sidebar.selectbox(
    '3. Warna Insang (Gill Color)',
    options=list(gill_color_options.keys()),
    format_func=lambda x: f"{x} - {gill_color_options[x]}"
)

input_stalk_root = st.sidebar.selectbox(
    '4. Bentuk Akar (Stalk Root)',
    options=list(stalk_root_options.keys()),
    format_func=lambda x: f"{x} - {stalk_root_options[x]}"
)

# Tombol untuk memproses
if st.sidebar.button("🔍 Cek Status Jamur"):
    # Panggil fungsi sistem pakar dengan input dari user
    status, reason = diagnose_mushroom(input_odor, input_gill_size, input_gill_color, input_stalk_root)

    st.subheader("Hasil Diagnosis:")

    if status == 'AMAN':
        st.success(f"✅ Status: **{status}**")
    elif status == 'BERACUN':
        st.error(f"☠️ Status: **{status}**")
    else:
        st.warning(f"❓ Status: **{status}**")
    
    st.info(f"**Alasan:** {reason}")

st.write("---")
st.markdown("_Disclaimer: Ini adalah proyek demo. Jangan gunakan aplikasi ini untuk menentukan apakah jamur liar aman untuk dimakan._")