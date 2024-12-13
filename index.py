import streamlit as st
from openai import OpenAI
import os

from prompt import get_prompt
from parser import get_video_script

# Streamlit App
st.title("YouTube Video to Documentation")
st.write("`YouTube URL`를 입력하세요.")

videoUrl = st.text_input("YouTube URL")

if st.button("생성하기"):
    with st.spinner("문서를 생성 중입니다..."):
        try:
            video_script = get_video_script(videoUrl)
            apiKey = os.getenv('OPEN_AI_TOKEN', 'abc')
       
            if len(video_script) > 40000:
                st.error("너무 긴 영상은 불가")
                st.stop()  # 중단

            # OpenAI API interaction
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
                model="llama-3.1-sonar-large-128k-online",
                messages=messages,
            )

            # Display the generated document
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
