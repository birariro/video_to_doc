package com.example.video2document.web;

import com.example.video2document.adapter.DocumentGenerator;
import com.example.video2document.adapter.UrlParser;
import com.example.video2document.adapter.VideoTranscriptParser;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.util.ObjectUtils;
import org.springframework.util.StringUtils;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.PostMapping;

@Controller
@RequiredArgsConstructor
public class WebController {

    private final VideoTranscriptParser videoTranscriptParser;
    private final DocumentGenerator documentGenerator;
    private final UrlParser urlParser;

    @GetMapping(value = {"/youtube/document", "/"})
    public String showForm(Model model) {
        model.addAttribute("videoRequest", new VideoRequest());
        return "index";
    }

    @PostMapping("/youtube/document")
    public String generateDocument(@ModelAttribute VideoRequest request, Model model) {
        try {
            if(!StringUtils.hasText(request.url())){
                return "index";
            }
            String videoId = urlParser.parseVideoId(request.url());
            String transcript = videoTranscriptParser.getTranscript(videoId);
            String document   = documentGenerator.generateDocument(transcript);

            model.addAttribute("videoRequest", new VideoRequest());
            model.addAttribute("markdown", document);

        } catch (Exception e) {
            model.addAttribute("error", "문서 생성 중 오류가 발생했습니다: " + e.getMessage());
        }
        return "index";

    }
}

