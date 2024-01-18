import streamlit as st
from io import BytesIO
from WebScrapping import find_anime_picture, load_image
from mini_translator import MiniTranslator
from Translator import Translator

st.set_page_config(layout="wide")
st.header("Anime Altyazı Çevirici")

col1, col2 = st.columns(2)

with col1:
    uploaded_file = st.file_uploader("SRT Dosyası Yükle", type=['srt'])

with col2:
    if uploaded_file is not None:
        image_url = find_anime_picture(uploaded_file.name.split(".")[0])
        st.image(load_image(image_url), caption=uploaded_file.name.split(".")[0])

if st.button("Çevir ve İşle"):
    if uploaded_file is not None:
        # SRT dosyasını oku ve çevir
        mini = MiniTranslator()
        big = Translator()
        srt_content = uploaded_file.getvalue().decode("utf-8-sig")
        #translated_lines = [mini.minitranslate(line, ) for line in srt_content.splitlines()]
        #translated_lines = [big.translate(line) for line in srt_content.splitlines()]
        translated_lines = srt_content


        # Çevrilen metni bir dosya olarak indirmeye hazırla
        translated_srt = "\n".join(translated_lines)
        translated_buf = BytesIO(translated_srt.encode("utf-8"))
        st.download_button(
            label="Çevrilen SRT Dosyasını İndir",
            data=translated_buf,
            file_name="cevrilen.srt",
            mime="text/plain"
        )
st.write("\n" * 5)

col1, col2, col3 = st.columns(3)


with col1:
    st.markdown("<h6 style='text-align: center;'>200601037 - Dinçer Kaan Turanlı</h6>", unsafe_allow_html=True)

with col2:
    st.markdown("<h6 style='text-align: center;'>200601057 - Ragıp Kaan Söylev</h6>", unsafe_allow_html=True)

with col3:
    st.markdown("<h6 style='text-align: center;'>200601059 - Muhammet Furkan İnce</h6>", unsafe_allow_html=True)