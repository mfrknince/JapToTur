import streamlit as st
from io import BytesIO
from WebScrapping import find_anime_picture, load_image
from mini_translator import MiniTranslator, list_to_srt, translate_text

from Translator import Translator


#st.set_page_config(layout="wide")
st.header("Anime Altyazı Çevirici")

col1, col2 = st.columns(2)

with col1:
    uploaded_file = st.file_uploader("SRT Dosyası Yükle", type=['srt'])

with col2:
    if uploaded_file is not None:
        image_url = find_anime_picture(uploaded_file.name.split(".")[0])
        st.image(load_image(image_url), caption=uploaded_file.name.split(".")[0])

option = st.selectbox('Kullanmak istediğiniz çeviri aracı',options=('HIZLI', 'YAVAS'))

if option == 'YAVAS':
    st.error('Yavaş çeviri aracı şu anda kullanılamıyor.')

placeholder = st.empty()


if st.button("Çevir"):
    if uploaded_file is not None:
        placeholder.image('https://i.gifer.com/origin/34/34338d26023e5515f6cc8969aa027bca_w200.gif',width=75, caption="Çeviri yapılıyor...")


        translated_srt = ""

        srt_content = uploaded_file.getvalue().decode("utf-8-sig")
        lines=srt_content.splitlines()
        translated_lines = translate_text(lines, option)
        translated_srt = list_to_srt(lines)

        placeholder.success("Çeviri tamamlandı.")

        st.download_button(
            label="Çevrilen SRT Dosyasını İndir",
            data=BytesIO(translated_srt.encode("utf-8")),
            file_name= uploaded_file.name.split(".")[0]+"-ceviri.srt",
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