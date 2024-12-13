import re
from youtube_transcript_api import YouTubeTranscriptApi

from exception import CustomException


# youtube url parser videoId
# https://www.youtube.com/watch?v=sGmhaizFA&list=PLe6 -> "sGmhaizFA"
# https://youtu.be/sGmhaizFA?si=cygoVRsuy -> "sGmhaizFA"

def get_video_id(url):
    pattern = r'(?:v=|\/)([0-9A-Za-z_-]{11}).*'
    match = re.search(pattern, url)

    if not match:
        raise CustomException("유효한 YouTube URL을 입력하세요.")

    return match.group(1)


def get_video_script(video_url):
    video_id = get_video_id(video_url)
    print("video_id" + video_id)
    transcription = YouTubeTranscriptApi.get_transcript(video_id, languages=['ko', 'en'])

    return "".join([content['text'] for content in transcription])
