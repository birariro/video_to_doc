package com.example.video2document.adapter;

import org.assertj.core.api.Assertions;
import org.junit.jupiter.api.Test;

class UrlParserTestClass {

    @Test
    void parsingTest(){

        UrlParser urlParser = new UrlParser();
        String[] testStrings = {
                "https://www.youtube.com/watch?v=abcdefghijk",
                "https://youtu.be/abcdefghijk",
                "https://www.youtube.com/embed/abcdefghijk?autoplay=1",
                "https://youtube.com/v/abcdefghijk",
                "https://youtube.com/watch?v=abcdefghijk&feature=youtu.be"
        };
        for (String testString : testStrings) {
            String videoId = urlParser.parseVideoId(testString);
            Assertions.assertThat(videoId).isEqualTo("abcdefghijk");
        }

    }
}
