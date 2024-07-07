import streamlit as st
import requests
import base64
import io
from PIL import Image

st.set_page_config(
    page_title="VizGenie",
    page_icon="img/image_logo.png",
    layout="wide",
    initial_sidebar_state="expanded",
)
def img_to_base64(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()

def query(payload, url, headers):
    response = requests.post(url, headers=headers, json=payload)
    return response.content


img_path = "img/image_logo.png"
img_base64 = img_to_base64(img_path)


st.sidebar.markdown(
    f'<img src="data:image/png;base64,{img_base64}" class="cover-glow">',
    unsafe_allow_html=True,
)
st.sidebar.markdown("---")
HF_Token = st.sidebar.text_input("Enter your Hugging Face API key", type="password")
st.sidebar.write("[Get Hf API Key](https://huggingface.co/settings/tokens)")
col1, col2 = st.columns([3, 1])
with col1:
    st.title("VizGenie")
with col2:
     options = {
          "General": ["stabilityai/stable-diffusion-xl-base-1.0"],
          "Cartoon": ["alvdansen/midsommarcartoon"],
          "Sketch": ["alvdansen/sketchedoutmanga"],
          "Pokemon": ["justinpinkney/pokemon-stable-diffusion"]
     }
     type_image = st.selectbox("Select Type", list(options.keys()))

col1, col2 = st.columns([2, 1])
with col1:
    prompt = st.text_area("Describe the image you want to generate")

def generate_image(model, HF_Token, prompt):
    
                API_URL = f"https://api-inference.huggingface.co/models/{model}"
                headers = {"Authorization": f"Bearer {HF_Token}"}
                image_bytes = query({"inputs": prompt, "options": {"use_cache": False}}, API_URL, headers)
                image = Image.open(io.BytesIO(image_bytes))
                return image, image_bytes
                

generate = st.button("Generate Image")
if generate:
    if not HF_Token:
        st.error("Please enter your Hugging Face API key")
    else:
        try:
            with st.spinner("Generating your image...") as status:
                col1, col2, col3 = st.columns([1, 1, 1])
                with col1:
                    st.write(" ")
                with col2:
                    image, image_bytes = generate_image(options[type_image][0], HF_Token, prompt)
                    st.image(image, width=500)
                    st.download_button(label='Download',data= image_bytes, file_name=f'VizGenie.png')
                with col3:
                        st.write(" ")
        except Exception as e:
            st.error("An Error Occurred. Please try again later.")