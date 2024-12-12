import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from openai import OpenAI
import re
import os

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
            # Prepare prompt for OpenAI
            prompt = f"""
            아래의 내용은 전문 소프트웨어 엔지니어가 자신의 기술적 지식을 나누는 대화의 녹음본입니다.  
            이 내용을 기반으로 기술 문서를 작성해 주세요.

            작성 시 반드시 다음 지침을 준수하세요:  
            - 이것이 녹음본이라고 이야기 하지 마세요
            - 문서 작성 언어: 한국어로 작성합니다.  
            - 문서의 형식: Markdown 형태로 작성합니다.  
                - 제목, 부제목, 목록, 코드 블록 등을 적절히 사용하여 문서를 구조화하세요.  
            - 문체 및 품격: 기술 문서의 형식을 따르며, 다음을 준수하세요:  
                - 대화체, 감정 표현, 유머 등은 배제하고 문어체를 사용합니다.  
                - 기술적 내용만 포함하며, 녹음 내용에 없는 정보를 추가하지 않습니다.  
                - 부록이 필요하다면 추가로 작성하세요.
                - 신뢰 가능한 문서가 되도록 노력하세요.
            - 문서 제목: 녹음 내용의 핵심 키워드로 제목을 선정합니다.  
            - 문서 구조: 다음 구조를 따르세요:  
                1. 제목: 핵심 주제를 명확히 표현.  
                2. 개요: 다룰 내용의 요약.  
                3. 본문: 주요 개념, 원리, 사용 방법 등을 상세히 설명.  
                4. 결론 (선택 사항): 주요 요점 정리 및 참고 자료 제공.  

            ```
            {fullTranscript}
            ```
            """

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
                    "content": prompt,
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
