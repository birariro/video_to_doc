package com.example.video2document.adapter;

import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;

import java.util.regex.Matcher;
import java.util.regex.Pattern;

@Slf4j
@Component
public class UrlParser {

    private static final String regex = "(?:v=|\\/)([0-9A-Za-z_-]{11}).*";

    public String parseVideoId(String url){
        if(!url.startsWith("https")){
            throw new IllegalArgumentException("not format url");
        }

        Pattern pattern = Pattern.compile(regex);
        Matcher matcher = pattern.matcher(url);
        if (matcher.find()) {
            String videoId = matcher.group(1);
            log.debug("detect video id: {} from url {}",videoId,  url);
            return videoId;
        }
        throw new IllegalArgumentException("not format url");

    }
}
