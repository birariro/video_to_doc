package com.example.video2document.web;

import com.example.video2document.adapter.DocumentGenerator;
import com.example.video2document.adapter.UrlParser;
import com.example.video2document.adapter.VideoTranscriptParser;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequiredArgsConstructor
public class ApiController {

    private final VideoTranscriptParser videoTranscriptParser;
    private final DocumentGenerator documentGenerator;
    private final UrlParser urlParser;

    @ResponseStatus(HttpStatus.OK)
    @GetMapping("/api/youtube/document")
    public String youtubeDocument(@RequestParam String url) {

        String videoId = urlParser.parseVideoId(url);
        String transcript = videoTranscriptParser.getTranscript(videoId);
        String document   = documentGenerator.generateDocument(transcript);

        return document;
    }
}
