package com.example.video2document.adapter.impl;

import com.example.video2document.adapter.DocumentGenerator;
import lombok.RequiredArgsConstructor;
import org.springframework.ai.chat.messages.SystemMessage;
import org.springframework.ai.chat.messages.UserMessage;
import org.springframework.ai.chat.model.ChatResponse;
import org.springframework.ai.chat.prompt.Prompt;
import org.springframework.ai.openai.OpenAiChatModel;
import org.springframework.stereotype.Component;

@Component
@RequiredArgsConstructor
class PerplexityClient implements DocumentGenerator {
    private final OpenAiChatModel chatModel;

    @Override
    public String generateDocument(String text) {
        Prompt prompt = new Prompt(new SystemMessage(getSystemPrompt()), new UserMessage(text));
        ChatResponse call = this.chatModel.call(prompt);
        return call.getResult().getOutput().getText();
    }

    private String getSystemPrompt(){
        return """
            당신은 전문 소프트웨어 엔지니어이며, 기술 지식을 문서화하는 임무를 맡았습니다. 제공된 대화 녹음본을 바탕으로 고품질의 기술 문서를 작성해 주세요.

            작성 시 다음 지침을 반드시 준수하세요:

            ### 1. 문서 작성 기본 사항
            - **언어**: 한국어로 작성합니다.
            - **형식**: Markdown 문법을 사용하여 작성합니다. 제목, 부제목, 목록, 코드 블록 등을 활용해 문서를 구조화하세요.
            - **문체**: 
            - 문어체를 사용하며, 대화체, 감정 표현, 유머는 제외합니다.
            - 녹음본의 내용만 사용하며, 추가적인 가정이나 정보를 포함하지 않습니다.
            - **내용 품질**:
            - 정확하고 신뢰할 수 있는 내용을 담으세요.
            - 독자가 쉽게 이해할 수 있도록 명료하게 서술하세요.
            - 필요 시 부록을 포함하여 내용을 보완하세요.

            ### 2. 문서 구조
            문서는 아래 구조를 따릅니다:
            1. **제목**: 녹음 내용의 핵심 주제를 명확히 표현.
            2. **개요**: 다룰 내용의 간단한 요약.
            3. **본문**: 주요 개념, 원리, 사용 방법 등을 상세히 기술.
            4. **결론** (선택 사항): 주요 요점 요약 및 참고 자료 제공.

            ### 3. 기타 주의 사항
            - 문서 내에 "녹음본"이라는 표현을 사용하지 마세요.
            - 본문에 인용 번호나 참고 번호를 삽입하지 마세요.
            """;
    }
}
