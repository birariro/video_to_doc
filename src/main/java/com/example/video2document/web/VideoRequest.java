package com.example.video2document.web;


public record VideoRequest(String url){
    public VideoRequest() {
        this("");
    }

}
