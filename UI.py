import streamlit as st
from io import BytesIO
from Translator import Translator
# İki sütun oluştur
col1, col2 = st.columns(2)

# İlk sütunda dosya yükleme widget'ı
with col1:
    uploaded_file = st.file_uploader("Dosya Yükle")

# İkinci sütunda dosyayı indirme butonu
with col2:
    if uploaded_file is not None:
        # Dosya adını göster
        st.write("Yüklenen Dosya:", uploaded_file.name)

        content = uploaded_file.getvalue().decode("utf-8-sig")
        lines = content.splitlines()

        sentences = []
        for i in range(len(lines)):
            if lines[i][0].isdigit():
                continue
            else:
                input_text = lines[i]
                translator = Translator()
                translated_text = translator.translate_jap_to_eng("こんにちは、朝食は食べましたか？")
                translated_text = translator.translate(translated_text)
                lines[i]=translated_text


            # uploaded_file = translated_file
            buf = BytesIO(lines.getvalue())
            st.download_button(
                label="Dosyayı İndir",
                data=buf,
                file_name=uploaded_file.name,
                mime=uploaded_file.type
            )


