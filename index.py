import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from openai import OpenAI
import re
import os

from prompt import get_prompt

# Streamlit App
st.title("YouTube Video to Technical Documentation")
st.write("`YouTube URL`를 입력하세요.")

# Input Fields
videoUrl = st.text_input("YouTube URL")

# Button to trigger the process
if st.button("문서 생성하기"):

    with st.spinner("문서를 생성 중입니다..."):
        # Extract video ID from URL
        match = re.search(r"v=([^&]+)", videoUrl)
        if match:
            video_id = match.group(1)
        else:
            st.error("유효한 YouTube URL을 입력하세요.")
            st.stop()  # 중단

        try:

            apiKey = os.getenv('OPEN_AI_TOKEN', 'abc')
            # Fetch transcript from YouTube
            transcription = YouTubeTranscriptApi.get_transcript(video_id, languages=['ko', 'en'])
            fullTranscript = "".join([content['text'] for content in transcription])

            if len(fullTranscript) > 9000:
                st.error("너무 긴 영상은 불가")
                st.stop()  # 중단

            # OpenAI API interaction
            client = OpenAI(api_key=apiKey, base_url="https://api.perplexity.ai")
            messages = [
                {
                    "role": "system",
                    "content": (
                        "You are an artificial intelligence assistant and you need to engage in a helpful, detailed, polite conversation with a user."
                    ),
                },
                {
                    "role": "user",
                    "content": get_prompt(fullTranscript),
                },
            ]

            response = client.chat.completions.create(
                model="llama-3.1-sonar-large-128k-online",
                messages=messages,
            )

            # Display the generated document
            st.markdown(response.choices[0].message.content)

        except Exception as e:
            st.error(f"오류가 발생했습니다: {e}")
