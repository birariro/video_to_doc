import streamlit as st
from openai import OpenAI
import os

from prompt import get_prompt
from parser import get_video_script

st.title("YouTube Video to Documentation")
st.write("`YouTube URL`를 입력하세요.")

videoUrl = st.text_input("YouTube URL")
model_type = st.radio(
    "Generate model",
    ["llama-3.1-sonar-small-128k-online", "llama-3.1-sonar-large-128k-online"],
    index=1,
    captions=[
        "$0.2","$1",
    ],
)

if st.button("생성하기"):

    video_script = get_video_script(videoUrl)
    apiKey = os.getenv('OPEN_AI_TOKEN', 'none')
    if apiKey == 'none':
        st.error("none api key")
        st.stop() 
    if len(video_script) > 40000:
        st.error("너무 긴 영상은 불가")
        st.stop() 

    with st.spinner("문서를 생성 중입니다..."):
        try:
        
            client = OpenAI(api_key=apiKey, base_url="https://api.perplexity.ai")
            messages = [
                {
                    "role": "system",
                    "content": (
                        get_prompt()
                    ),
                },
                {
                    "role": "user",
                    "content": video_script,
                },
            ]

            response = client.chat.completions.create(
                model=model_type,
                messages=messages,
            )

            generated_document = response.choices[0].message.content
            st.markdown(generated_document)

            st.download_button(
                label="다운로드",
                data=generated_document,
                file_name="doc.md",
                mime="text/markdown"
            )
        except Exception as e:
            st.error(f"오류가 발생했습니다: {e}")

