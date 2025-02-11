package com.example.video2document.adapter.impl;

import com.example.video2document.adapter.VideoTranscriptParser;
import io.github.thoroldvix.api.TranscriptContent;
import io.github.thoroldvix.api.YoutubeTranscriptApi;
import io.github.thoroldvix.internal.TranscriptApiFactory;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;
import org.springframework.util.ObjectUtils;

@Component
@Slf4j
class YoutubeTranscript implements VideoTranscriptParser {

    public String getTranscript(String videoId){

        log.info("video id: {}", videoId);
        YoutubeTranscriptApi youtubeTranscriptApi = TranscriptApiFactory.createDefault();
        try{

            TranscriptContent transcriptContent = youtubeTranscriptApi.getTranscript(videoId, "ko","en");
            String content = String.join(" ", transcriptContent.getContent()
                    .stream()
                    .map(TranscriptContent.Fragment::getText)
                    .toList());

            if(ObjectUtils.isEmpty(content) || content.length() < 100){
                throw new IllegalStateException("empty transcript");
            }
            log.info("video id: {}, TranscriptContent length: ", content.length());
            return content;
        }catch (Exception e){
             throw new IllegalStateException(e);
        }
    }
}
