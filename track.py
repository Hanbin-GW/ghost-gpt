import ssl
import certifi
from pytube import YouTube
import urllib.request

def download_video(video_url):
    # urllib의 기본 SSL 컨텍스트를 certifi의 인증서로 설정
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    urllib.request.urlopen(video_url, context=ssl_context)
    
    yt = YouTube(video_url, use_oauth=False, allow_oauth_cache=True)
    yt.streams.first().download()


if __name__ == '__main__':
    video_url = 'https://www.youtube.com/watch?v=ErKQ1Nmgw9s'
    download_video(video_url)

