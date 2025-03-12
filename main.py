import os
import yt_dlp
import time
import csv
from datetime import datetime

DOWNLOADED_URLS_FILE = 'downloaded_urls.csv'


def load_downloaded_urls():
    if not os.path.exists(DOWNLOADED_URLS_FILE):
        return set()
    with open(DOWNLOADED_URLS_FILE, 'r', newline='') as file:
        reader = csv.reader(file)
        return set(row[0] for row in reader)


def save_downloaded_url(url, title):
    with open(DOWNLOADED_URLS_FILE, 'a', newline='') as file:
        writer = csv.writer(file, quoting=csv.QUOTE_MINIMAL)
        writer.writerow([url, title, datetime.now().strftime('%Y-%m-%d %H:%M:%S')])


def download_song(url, title, output_dir):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    save_downloaded_url(url, title)


def download_playlist(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': '%(playlist_title)s/%(title)s.%(ext)s',
        'yesplaylist': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        for entry in info_dict['entries']:
            song_url = entry['webpage_url']
            song_title = entry['title']
            save_downloaded_url(song_url, song_title)


def check_for_new_songs(playlists):
    downloaded_urls = load_downloaded_urls()
    for playlist_url in playlists:
        playlist_info = yt_dlp.YoutubeDL().extract_info(playlist_url, download=False)
        playlist_title = playlist_info['title']
        output_dir = os.path.join(os.getcwd(), playlist_title)
        os.makedirs(output_dir, exist_ok=True)
        
        for entry in playlist_info['entries']:
            song_url = entry['webpage_url']
            song_title = entry['title']
            if song_url not in downloaded_urls:
                print(f"Downloading {song_title}...")
                download_song(song_url, song_title, output_dir)


def main():
    playlists = [
        "https://www.youtube.com/watch?v=txJ69R9d9ig&list=PLHqT-Jyopsgnr2E30XnoQniWH6417q1EY",
        # Add more playlist URLs here
    ]

    # download_playlist(playlists[0])

    # check_for_new_songs(playlists)

    # schedule.every().day.at("03:00").do(check_for_new_songs, playlists)
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)


if __name__ == "__main__":
    main()
