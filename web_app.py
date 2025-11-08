from flask import Flask, render_template, request, jsonify, send_file
import subprocess
import os
import threading
import json
from datetime import datetime
import sys

app = Flask(__name__)

# Global değişkenler
download_status = {
    'is_downloading': False,
    'progress': 0,
    'current_url': '',
    'total_urls': 0,
    'completed_urls': 0,
    'logs': []
}

download_folder = "MediaDownloads"

# İndirme klasörünü oluştur
os.makedirs(download_folder, exist_ok=True)

# Platform tespiti
def detect_platform(url):
    platforms = {
        'youtube.com': 'YouTube',
        'youtu.be': 'YouTube',
        'music.youtube.com': 'YouTube Music',
        'instagram.com': 'Instagram',
        'twitter.com': 'Twitter/X',
        'x.com': 'Twitter/X',
        'tiktok.com': 'TikTok',
        'facebook.com': 'Facebook',
        'fb.watch': 'Facebook'
    }
    
    for domain, platform in platforms.items():
        if domain in url.lower():
            return platform
    return 'Bilinmeyen'

def log_message(message):
    """Log mesajını ekler"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    log_entry = f"[{timestamp}] {message}"
    download_status['logs'].append(log_entry)
    # Son 50 log'u tut
    if len(download_status['logs']) > 50:
        download_status['logs'] = download_status['logs'][-50:]

def download_single_video(url, format_type, quality):
    """Tek video indirme"""
    try:
        cmd = [
            sys.executable, '-m', 'yt_dlp',
            '--output', f'{download_folder}/%(title)s.%(ext)s',
            '--no-warnings',
            '--ignore-errors'
        ]
        
        # Format ayarları
        if format_type == 'mp3':
            cmd.extend([
                '--extract-audio',
                '--audio-format', 'mp3',
                '--audio-quality', '192K',
                '--format', 'bestaudio[ext=m4a]/bestaudio/best'
            ])
        elif format_type == 'mp4':
            if quality == 'best':
                cmd.extend(['--format', 'best[ext=mp4]/best'])
            elif quality == 'worst':
                cmd.extend(['--format', 'worst[ext=mp4]/worst'])
            else:
                cmd.extend(['--format', f'best[height<={quality.replace("p", "")}][ext=mp4]/best'])
        else:
            cmd.extend(['--format', f'best[ext={format_type}]/best'])
        
        cmd.append(url)
        
        log_message(f"🚀 İndirme başlatılıyor: {url}")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        
        if result.returncode == 0:
            log_message(f"✅ Başarıyla indirildi: {url}")
            return True
        else:
            log_message(f"❌ İndirme hatası: {url}")
            if result.stderr:
                log_message(f"🔴 Hata detayı: {result.stderr[:500]}")
            if result.stdout:
                log_message(f"ℹ️ Çıktı: {result.stdout[:500]}")
            return False
            
    except Exception as e:
        log_message(f"❌ Hata: {str(e)}")
        return False

def download_videos_thread(urls, format_type, quality):
    """İndirme thread'i"""
    global download_status
    
    download_status['is_downloading'] = True
    download_status['total_urls'] = len(urls)
    download_status['completed_urls'] = 0
    download_status['logs'] = []
    
    log_message(f"🎵 {len(urls)} URL için indirme başlatılıyor...")
    log_message(f"📋 Format: {format_type}, Kalite: {quality}")
    log_message("=" * 60)
    
    successful = 0
    failed = 0
    
    for i, url in enumerate(urls, 1):
        if not download_status['is_downloading']:
            break
            
        download_status['current_url'] = url
        download_status['progress'] = int((i-1) / len(urls) * 100)
        
        platform = detect_platform(url)
        log_message(f"\n[{i}/{len(urls)}] {platform}: {url}")
        
        if download_single_video(url, format_type, quality):
            successful += 1
        else:
            failed += 1
            
        download_status['completed_urls'] = i
        download_status['progress'] = int(i / len(urls) * 100)
    
    download_status['is_downloading'] = False
    download_status['progress'] = 100
    
    log_message(f"\n🎉 İndirme tamamlandı!")
    log_message(f"✅ Başarılı: {successful}")
    log_message(f"❌ Başarısız: {failed}")

@app.route('/')
def index():
    """Ana sayfa"""
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    """İndirme başlat"""
    global download_status
    
    if download_status['is_downloading']:
        return jsonify({'error': 'Zaten bir indirme işlemi devam ediyor!'})
    
    data = request.json
    urls = [url.strip() for url in data['urls'] if url.strip()]
    format_type = data.get('format', 'mp4')
    quality = data.get('quality', 'best')
    
    if not urls:
        return jsonify({'error': 'Lütfen en az bir URL girin!'})
    
    # İndirme thread'ini başlat
    thread = threading.Thread(target=download_videos_thread, args=(urls, format_type, quality))
    thread.daemon = True
    thread.start()
    
    return jsonify({'message': 'İndirme başlatıldı!'})

@app.route('/status')
def status():
    """İndirme durumu"""
    return jsonify(download_status)

@app.route('/stop', methods=['POST'])
def stop_download():
    """İndirmeyi durdur"""
    global download_status
    download_status['is_downloading'] = False
    log_message("⏹️ İndirme durduruldu!")
    return jsonify({'message': 'İndirme durduruldu!'})

@app.route('/clear')
def clear_logs():
    """Logları temizle"""
    global download_status
    download_status['logs'] = []
    return jsonify({'message': 'Loglar temizlendi!'})

@app.route('/files')
def list_files():
    """İndirilen dosyaları listele"""
    try:
        files = []
        for filename in os.listdir(download_folder):
            filepath = os.path.join(download_folder, filename)
            if os.path.isfile(filepath):
                files.append({
                    'name': filename,
                    'size': os.path.getsize(filepath),
                    'date': datetime.fromtimestamp(os.path.getmtime(filepath)).strftime("%Y-%m-%d %H:%M:%S")
                })
        return jsonify({'files': files})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/download_file/<filename>')
def download_file(filename):
    """Dosya indir"""
    try:
        filepath = os.path.join(download_folder, filename)
        return send_file(filepath, as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    print("🌐 Web sitesi başlatılıyor...")
    print("📱 Tarayıcıda http://localhost:5000 adresini açın")
    app.run(debug=True, host='0.0.0.0', port=5000)
