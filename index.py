import streamlit as st
import os

import open_ai
from exception import CustomException
from parser import get_video_script


def is_exist(target, error_message):
    if target == 'none':
        raise CustomException(error_message)


def length_can_not_over(target, limit, error_message):
    if len(target) > limit:
        raise CustomException(error_message)


st.title("YouTube Video to Documentation")
st.write("`YouTube URL`를 입력하세요.")

video_url = st.text_input("YouTube URL")
model_type = st.radio(
    "Generate model",
    ["llama-3.1-sonar-small-128k-online", "llama-3.1-sonar-large-128k-online"],
    index=1,
    captions=[
        "$0.2", "$1",
    ],
)

if st.button("생성하기"):
    try:
        video_script = get_video_script(video_url)
        api_key = os.getenv('OPEN_AI_TOKEN', 'none')

        is_exist(api_key, "none api key")
        length_can_not_over(video_script, 40000, "너무 긴 영상은 불가")
    except CustomException as e:
        st.error(e)
        st.stop()

    with st.spinner("문서를 생성 중입니다..."):
        try:
            response = open_ai.request_summery(api_key, model_type, video_script)

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
