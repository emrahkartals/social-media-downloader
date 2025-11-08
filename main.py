import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import threading
import os
import subprocess
import json
from pathlib import Path
import webbrowser
from PIL import Image, ImageTk
import requests
from io import BytesIO
import re
import time
from datetime import datetime
import sys

class SocialMediaDownloader:
    def __init__(self, root):
        self.root = root
        
        # Ultra smooth ve modern karanlık tema - Gradient efektleri ile
        self.colors = {
            'primary': '#0f172a',           # Yumuşak koyu mavi (slate-900)
            'secondary': '#1e293b',         # Koyu mavi-gri (slate-800)
            'accent': '#334155',             # Orta mavi-gri (slate-700)
            'accent_light': '#475569',      # Açık mavi-gri (slate-600)
            'highlight': '#8b5cf6',          # Yumuşak mor (violet-500)
            'highlight_hover': '#a78bfa',  # Açık mor (hover) (violet-400)
            'highlight_light': '#c4b5fd',  # Çok açık mor (violet-300)
            'success': '#10b981',           # Emerald yeşil
            'success_hover': '#34d399',    # Açık yeşil (hover)
            'success_light': '#6ee7b7',    # Çok açık yeşil
            'warning': '#f59e0b',           # Amber turuncu
            'warning_hover': '#fbbf24',     # Açık turuncu (hover)
            'danger': '#ef4444',            # Kırmızı
            'info': '#3b82f6',              # Mavi
            'info_hover': '#60a5fa',        # Açık mavi
            'purple': '#a855f7',            # Mor
            'purple_hover': '#c084fc',      # Açık mor
            'text': '#f1f5f9',              # Yumuşak beyaz (slate-100)
            'text_secondary': '#e2e8f0',   # Açık gri (slate-200)
            'text_muted': '#cbd5e1',        # Gri (slate-300)
            'card': '#1e293b',              # Koyu mavi kart (slate-800)
            'card_hover': '#334155',        # Açık kart (hover) (slate-700)
            'card_light': '#475569',        # Daha açık kart (slate-600)
            'border': '#475569',            # Gri kenarlık (slate-600)
            'border_light': '#64748b',      # Açık gri kenarlık (slate-500)
            'border_lighter': '#94a3b8'     # Çok açık gri (slate-400)
        }
        
        # Pencere ayarları
        self.root.title("🎵 Social Media Content Downloader 🎬")
        self.root.geometry("1400x900")
        self.root.configure(bg=self.colors['primary'])
        self.root.resizable(True, True)
        self.root.minsize(1200, 800)
        
        # Pencereyi ekranın ortasına yerleştir
        self.center_window()
        
        # Stil ayarları
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Stil konfigürasyonları
        self.style.configure('Title.TLabel', font=('Segoe UI', 20, 'bold'), 
                           background=self.colors['primary'], foreground=self.colors['text'])
        self.style.configure('Header.TLabel', font=('Segoe UI', 12, 'bold'), 
                           background=self.colors['secondary'], foreground=self.colors['text'])
        self.style.configure('Custom.TButton', font=('Segoe UI', 10, 'bold'), 
                           padding=(15, 10), background=self.colors['accent'])
        self.style.configure('Success.TButton', font=('Segoe UI', 10, 'bold'), 
                           padding=(15, 10), background=self.colors['success'])
        self.style.configure('Warning.TButton', font=('Segoe UI', 10, 'bold'), 
                           padding=(15, 10), background=self.colors['warning'])
        self.style.configure('Danger.TButton', font=('Segoe UI', 10, 'bold'), 
                           padding=(15, 10), background=self.colors['highlight'])
        
        # İndirme klasörünü önce oluştur
        try:
            self.download_folder = os.path.join(os.path.expanduser("~"), "Downloads", "MediaDownloads")
            os.makedirs(self.download_folder, exist_ok=True)
        except PermissionError:
            # Eğer Downloads klasörüne erişim yoksa, mevcut dizini kullan
            self.download_folder = os.path.join(os.getcwd(), "Downloads")
            os.makedirs(self.download_folder, exist_ok=True)
        
        self.setup_ui()
        
        # İstatistikler
        self.total_downloads = 0
        self.successful_downloads = 0
        self.failed_downloads = 0
        
        # Platform desteği
        self.supported_platforms = {
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
    
    def center_window(self):
        """Pencereyi ekranın ortasına yerleştir"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_modern_button(self, parent, text, command, bg_color, hover_color=None, 
                           fg_color='#ffffff', font_size=10, padx=16, pady=10):
        """Modern buton oluşturur (hover efekti ile)"""
        if hover_color is None:
            hover_color = bg_color
        
        btn = tk.Button(parent, text=text, command=command,
                       font=('Segoe UI', font_size, 'bold'),
                       bg=bg_color, fg=fg_color,
                       relief='flat', bd=0,
                       padx=padx, pady=pady,
                       cursor='hand2',
                       activebackground=hover_color,
                       activeforeground=fg_color)
        
        # Hover efektleri
        def on_enter(e):
            btn.config(bg=hover_color)
        
        def on_leave(e):
            btn.config(bg=bg_color)
        
        btn.bind('<Enter>', on_enter)
        btn.bind('<Leave>', on_leave)
        
        return btn
        
    def setup_ui(self):
        # Ana başlık - Modern gradient efekti
        title_frame = tk.Frame(self.root, bg=self.colors['primary'], height=140)
        title_frame.pack(fill='x', padx=0, pady=0)
        title_frame.pack_propagate(False)
        
        # Gradient efekti için container
        title_container = tk.Frame(title_frame, bg=self.colors['primary'])
        title_container.pack(expand=True, fill='both', padx=40, pady=20)
        
        # Ana başlık - Daha büyük ve çekici
        title_label = tk.Label(title_container, 
                              text="🎵 Social Media Content Downloader 🎬", 
                              font=('Segoe UI', 28, 'bold'), 
                              bg=self.colors['primary'], 
                              fg=self.colors['text'])
        title_label.pack(pady=(10, 8))
        
        # Alt başlık - Daha modern
        subtitle_label = tk.Label(title_container, 
                                 text="Download videos and music from YouTube, Instagram, Twitter, TikTok, Facebook and more", 
                                 font=('Segoe UI', 11, 'normal'), 
                                 bg=self.colors['primary'], 
                                 fg=self.colors['text_secondary'])
        subtitle_label.pack(pady=(0, 15))
        
        # Dekoratif gradient çizgi
        separator_container = tk.Frame(title_frame, bg=self.colors['primary'])
        separator_container.pack(fill='x', padx=50, pady=(0, 15))
        
        # Smooth gradient efekti için 3 çizgi (daha yumuşak)
        separator1 = tk.Frame(separator_container, height=2, bg=self.colors['highlight'])
        separator1.pack(fill='x', pady=(0, 1))
        separator2 = tk.Frame(separator_container, height=1, bg=self.colors['highlight_light'])
        separator2.pack(fill='x', pady=(0, 1))
        separator3 = tk.Frame(separator_container, height=1, bg=self.colors['info'])
        separator3.pack(fill='x')
        
        # Ana içerik frame - Smooth gradient efekti için
        main_frame = tk.Frame(self.root, bg=self.colors['secondary'], relief='flat', bd=0)
        main_frame.pack(fill='both', expand=True, padx=40, pady=(0, 25))
        
        # İçerik container - Smooth kart (daha yumuşak renk)
        content_container = tk.Frame(main_frame, bg=self.colors['card'], relief='flat', bd=0,
                                    highlightthickness=1, highlightbackground=self.colors['border_light'])
        content_container.pack(fill='both', expand=True, padx=25, pady=25)
        
        # URL girişi - Modern kart
        url_frame = tk.Frame(content_container, bg=self.colors['card'], relief='flat', bd=0)
        url_frame.pack(fill='x', pady=(0, 20))
        
        # URL başlığı - Smooth gradient efekti
        url_header = tk.Frame(url_frame, bg=self.colors['accent'], height=48)
        url_header.pack(fill='x', pady=(0, 12))
        url_header.pack_propagate(False)
        
        # Başlık içinde gradient efekti için container
        header_content = tk.Frame(url_header, bg=self.colors['accent'])
        header_content.pack(expand=True, fill='both', padx=15, pady=10)
        
        tk.Label(header_content, text="🔗 Video & Music URLs", 
                font=('Segoe UI', 15, 'bold'), 
                bg=self.colors['accent'], fg=self.colors['text']).pack(side='left')
        
        tk.Label(header_content, text="(One URL per line)", 
                font=('Segoe UI', 10, 'normal'), 
                bg=self.colors['accent'], fg=self.colors['text_muted']).pack(side='left', padx=(10, 0))
        
        # URL girişi ve platform tespiti
        url_input_frame = tk.Frame(url_frame, bg=self.colors['card'])
        url_input_frame.pack(fill='x', pady=5)
        
        self.url_text = scrolledtext.ScrolledText(url_input_frame, height=7, font=('Segoe UI', 11),
                                                bg=self.colors['accent'], fg=self.colors['text'], 
                                                insertbackground=self.colors['highlight'],
                                                relief='flat', bd=0, highlightthickness=2,
                                                highlightcolor=self.colors['highlight_light'],
                                                highlightbackground=self.colors['border_light'],
                                                selectbackground=self.colors['highlight'],
                                                selectforeground=self.colors['text'])
        self.url_text.pack(side='left', fill='both', expand=True, padx=(0, 12))
        
        # Platform tespiti paneli - Daha modern kart
        platform_frame = tk.Frame(url_input_frame, bg=self.colors['accent'], width=240, 
                                 relief='flat', bd=0)
        platform_frame.pack(side='right', fill='y')
        platform_frame.pack_propagate(False)
        
        platform_header = tk.Frame(platform_frame, bg=self.colors['accent'])
        platform_header.pack(fill='x', padx=12, pady=(12, 8))
        
        tk.Label(platform_header, text="📱 Detected Platforms", 
                font=('Segoe UI', 12, 'bold'), 
                bg=self.colors['accent'], fg=self.colors['text']).pack(side='left')
        
        self.platform_listbox = tk.Listbox(platform_frame, height=7, font=('Segoe UI', 10),
                                          bg=self.colors['accent_light'], fg=self.colors['text'], 
                                          selectbackground=self.colors['highlight'],
                                          selectforeground=self.colors['text'],
                                          relief='flat', bd=0,
                                          highlightthickness=0)
        self.platform_listbox.pack(fill='both', expand=True, padx=12, pady=(0, 12))
        
        # URL değişikliklerini dinle
        self.url_text.bind('<KeyRelease>', self.detect_platforms)
        
        # Boş başlangıç - kullanıcı URL girecek
        
        # Program başlangıcında log mesajı
        self.root.after(1000, self._initial_log_message)
        
        # Format seçenekleri - Modern kart
        format_frame = tk.Frame(content_container, bg=self.colors['card'], relief='flat', bd=0)
        format_frame.pack(fill='x', pady=(0, 20))
        
        # Format başlığı - Smooth
        format_header = tk.Frame(format_frame, bg=self.colors['accent'], height=45)
        format_header.pack(fill='x', pady=(0, 12))
        format_header.pack_propagate(False)
        
        format_header_content = tk.Frame(format_header, bg=self.colors['accent'])
        format_header_content.pack(expand=True, fill='both', padx=15, pady=10)
        
        tk.Label(format_header_content, text="📁 Format & Quality Options", 
                font=('Segoe UI', 15, 'bold'), 
                bg=self.colors['accent'], fg=self.colors['text']).pack(side='left')
        
        # Format ve kalite seçenekleri - Tek satırda yan yana
        format_options_frame = tk.Frame(format_frame, bg=self.colors['card'])
        format_options_frame.pack(fill='x', pady=10)
        
        # Format türü
        format_label_frame = tk.Frame(format_options_frame, bg=self.colors['card'])
        format_label_frame.pack(side='left', padx=(0, 15))
        
        # Format başlığı
        format_title_frame = tk.Frame(format_label_frame, bg=self.colors['accent'], height=30)
        format_title_frame.pack(fill='x', pady=(0, 8))
        format_title_frame.pack_propagate(False)
        
        tk.Label(format_title_frame, text="🎬 Format", 
                font=('Segoe UI', 11, 'bold'), 
                bg=self.colors['accent'], fg=self.colors['text']).pack(expand=True)
        
        # Format seçimi - Smooth
        format_select_frame = tk.Frame(format_label_frame, bg=self.colors['accent'], relief='flat', bd=0,
                                       highlightthickness=1, highlightbackground=self.colors['border_light'])
        format_select_frame.pack(fill='x', padx=5, pady=(0, 5))
        
        self.format_var = tk.StringVar(value="mp4")
        format_combo = ttk.Combobox(format_select_frame, textvariable=self.format_var, 
                                   values=["mp4", "mp3", "webm", "mkv", "avi"], 
                                   width=10, font=('Segoe UI', 10), state='readonly')
        format_combo.pack(pady=8)
        
        # Progress durumu için
        self.progress_var = tk.StringVar(value="Hazır")
        
        # Progress bar için
        self.progress_bar = ttk.Progressbar(format_options_frame, mode='indeterminate')
        self.progress_bar.pack(side='right', padx=(10, 0), pady=5)
        
        # Kalite seçimi
        quality_label_frame = tk.Frame(format_options_frame, bg=self.colors['card'])
        quality_label_frame.pack(side='left', padx=(0, 15))
        
        # Kalite başlığı
        quality_title_frame = tk.Frame(quality_label_frame, bg=self.colors['accent'], height=30)
        quality_title_frame.pack(fill='x', pady=(0, 8))
        quality_title_frame.pack_propagate(False)
        
        tk.Label(quality_title_frame, text="⭐ Quality", 
                font=('Segoe UI', 11, 'bold'), 
                bg=self.colors['accent'], fg=self.colors['text']).pack(expand=True)
        
        # Kalite seçimi - Smooth
        quality_select_frame = tk.Frame(quality_label_frame, bg=self.colors['accent'], relief='flat', bd=0,
                                        highlightthickness=1, highlightbackground=self.colors['border_light'])
        quality_select_frame.pack(fill='x', padx=5, pady=(0, 5))
        
        self.quality_var = tk.StringVar(value="best")
        quality_combo = ttk.Combobox(quality_select_frame, textvariable=self.quality_var,
                                    values=["best", "worst", "720p", "480p", "360p"], 
                                    width=10, font=('Segoe UI', 10), state='readonly')
        quality_combo.pack(pady=8)
        
        # İndirme butonları - Format ve kalitenin yanında
        button_frame = tk.Frame(format_options_frame, bg=self.colors['card'])
        button_frame.pack(side='left', padx=(15, 0))
        
        # Modern butonlar - Hover efektleri ile
        download_btn = self.create_modern_button(button_frame, "🚀 Start Download", 
                                                 self.start_download,
                                                 self.colors['success'], 
                                                 self.colors['success_hover'],
                                                 font_size=11, padx=18, pady=11)
        download_btn.pack(side='left', padx=(0, 8))
        
        folder_select_btn = self.create_modern_button(button_frame, "📂 Select Folder", 
                                                     self.select_folder,
                                                     self.colors['info'],
                                                     '#60a5fa',
                                                     font_size=10, padx=16, pady=10)
        folder_select_btn.pack(side='left', padx=(0, 8))

        clear_btn = self.create_modern_button(button_frame, "🗑️ Clear", 
                                              self.clear_all,
                                              self.colors['warning'], 
                                              self.colors['warning_hover'],
                                              self.colors['text'],
                                              font_size=10, padx=16, pady=10)
        clear_btn.pack(side='left', padx=(0, 8))
        
        open_folder_btn = self.create_modern_button(button_frame, "📁 Open Folder", 
                                                    self.open_download_folder,
                                                    self.colors['highlight'], 
                                                    self.colors['highlight_hover'],
                                                    font_size=10, padx=16, pady=10)
        open_folder_btn.pack(side='left', padx=(0, 8))
        
        settings_btn = self.create_modern_button(button_frame, "⚙️ Settings", 
                                                 self.open_settings,
                                                 self.colors['purple'],
                                                 '#c084fc',
                                                 font_size=10, padx=16, pady=10)
        settings_btn.pack(side='left', padx=(0, 8))
        
        help_btn = self.create_modern_button(button_frame, "❓ Help", 
                                            self.open_help,
                                            self.colors['highlight'], 
                                            self.colors['highlight_hover'],
                                            font_size=10, padx=16, pady=10)
        help_btn.pack(side='left', padx=(0, 6))
        
       
        # İndirme klasörü ve loglar - Yan yana tasarım
        bottom_frame = tk.Frame(main_frame, bg=self.colors['primary'])
        bottom_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        # Sol taraf - İndirme klasörü ve istatistikler
        folder_frame = tk.Frame(bottom_frame, bg=self.colors['card'])
        folder_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        tk.Label(folder_frame, text="📁 Download Folder", 
                font=('Segoe UI', 13, 'bold'), 
                bg=self.colors['card'], fg=self.colors['text']).pack(anchor='w', pady=(12, 8))
        
        folder_info_frame = tk.Frame(folder_frame, bg=self.colors['accent'], 
                                    relief='flat', bd=0, highlightthickness=1,
                                    highlightbackground=self.colors['border_light'])
        folder_info_frame.pack(fill='x', padx=12, pady=(0, 12))
        
        self.folder_label = tk.Label(folder_info_frame, text=self.download_folder, 
                                    font=('Segoe UI', 10), 
                                    bg=self.colors['accent'], fg=self.colors['text_secondary'],
                                    wraplength=320, justify='left', anchor='w')
        self.folder_label.pack(padx=12, pady=10, fill='x')
        
        # Klasör değişkeni ekle
        self.folder_var = tk.StringVar(value=self.download_folder)
        
        # İstatistikler - Klasörün altında
        tk.Label(folder_frame, text="📊 Statistics", 
                font=('Segoe UI', 13, 'bold'), 
                bg=self.colors['card'], fg=self.colors['text']).pack(anchor='w', pady=(12, 8))
        
        stats_info_frame = tk.Frame(folder_frame, bg=self.colors['accent'], 
                                   relief='flat', bd=0, highlightthickness=1,
                                   highlightbackground=self.colors['border_light'])
        stats_info_frame.pack(fill='x', padx=12, pady=(0, 12))
        
        # İstatistik bilgileri - Smooth
        self.stats_label = tk.Label(stats_info_frame, 
                                   text="Total: 0  |  Success: 0  |  Failed: 0", 
                                   font=('Segoe UI', 11, 'bold'), 
                                   bg=self.colors['accent'], fg=self.colors['text'])
        self.stats_label.pack(pady=(12, 10))
        
        reset_stats_btn = self.create_modern_button(stats_info_frame, "🔄 Reset Stats", 
                                                    self.reset_stats,
                                                    self.colors['warning'], 
                                                    self.colors['warning_hover'],
                                                    self.colors['text'],
                                                    font_size=9, padx=12, pady=6)
        reset_stats_btn.pack(pady=(0, 12))
        
        # Sağ taraf - İndirme logları
        log_frame = tk.Frame(bottom_frame, bg=self.colors['card'])
        log_frame.pack(side='right', fill='both', expand=True, padx=(10, 0))
        
        tk.Label(log_frame, text="📋 Download Logs", 
                font=('Segoe UI', 13, 'bold'), 
                bg=self.colors['card'], fg=self.colors['text']).pack(anchor='w', pady=(12, 8))
        
        log_container = tk.Frame(log_frame, bg=self.colors['accent'], 
                                relief='flat', bd=0, highlightthickness=1,
                                highlightbackground=self.colors['border_light'])
        log_container.pack(fill='both', expand=True, padx=12, pady=(0, 12))
        
        self.log_text = scrolledtext.ScrolledText(log_container, height=10, 
                                                  font=('Consolas', 10),
                                                  bg=self.colors['accent'], 
                                                  fg=self.colors['text'],
                                                  insertbackground=self.colors['highlight'],
                                                  relief='flat', bd=0, 
                                                  highlightthickness=0,
                                                  selectbackground=self.colors['highlight'],
                                                  selectforeground=self.colors['text'])
        self.log_text.pack(fill='both', expand=True, padx=8, pady=8)
        
        # Log alanına başlangıç mesajı
        self.log_text.insert(tk.END, "🎵 Download Log Area\n")
        self.log_text.insert(tk.END, "=" * 60 + "\n")
        
        # Footer - Modern footer
        footer_frame = tk.Frame(self.root, bg=self.colors['primary'], height=50)
        footer_frame.pack(fill='x', side='bottom', pady=(15, 0))
        footer_frame.pack_propagate(False)
        
        footer_content = tk.Frame(footer_frame, bg=self.colors['primary'])
        footer_content.pack(expand=True, fill='both', padx=40, pady=12)
        
        footer_label = tk.Label(footer_content, 
                               text="🎵 Social Media Content Downloader - Made with ❤️", 
                               font=('Segoe UI', 10, 'italic'), 
                               bg=self.colors['primary'], 
                               fg=self.colors['text_muted'])
        footer_label.pack(side='left')
        
        version_label = tk.Label(footer_content, 
                               text="v1.0.0", 
                               font=('Segoe UI', 9, 'normal'), 
                               bg=self.colors['primary'], 
                               fg=self.colors['text_secondary'])
        version_label.pack(side='right')
                
    def select_folder(self):
        folder = filedialog.askdirectory(initialdir=self.download_folder)
        if folder:
            self.folder_var.set(folder)
            self.download_folder = folder
            # Label'ı da güncelle
            self.folder_label.config(text=folder)
            self.log_message(f"📂 İndirme klasörü değiştirildi: {folder}")
            
    def clear_all(self):
        self.url_text.delete(1.0, tk.END)
        self.log_text.delete(1.0, tk.END)
        self.progress_var.set("Hazır")
        self.platform_listbox.delete(0, tk.END)
        
    def detect_platforms(self, event=None):
        """URL'lerdeki platformları tespit eder"""
        self.platform_listbox.delete(0, tk.END)
        urls = self.url_text.get(1.0, tk.END).strip().split('\n')
        detected_platforms = set()
        
        for url in urls:
            url = url.strip()
            if url:
                for domain, platform in self.supported_platforms.items():
                    if domain in url:
                        detected_platforms.add(platform)
                        break
        
        for platform in sorted(detected_platforms):
            self.platform_listbox.insert(tk.END, f"✓ {platform}")
            
    def reset_stats(self):
        """İstatistikleri sıfırlar"""
        self.total_downloads = 0
        self.successful_downloads = 0
        self.failed_downloads = 0
        self.update_stats_display()
        
    def update_stats_display(self):
        """İstatistik görünümünü günceller"""
        self.stats_label.config(text=f"Total: {self.total_downloads}  |  Success: {self.successful_downloads}  |  Failed: {self.failed_downloads}")
        
    def open_settings(self):
        """Ayarlar penceresini açar"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("⚙️ Ayarlar")
        settings_window.geometry("400x300")
        settings_window.configure(bg='#2c3e50')
        settings_window.resizable(False, False)
        
        # Başlık
        title_label = tk.Label(settings_window, text="⚙️ Program Ayarları", 
                              font=('Arial', 14, 'bold'), bg='#2c3e50', fg='white')
        title_label.pack(pady=10)
        
        # Ayarlar içeriği
        settings_frame = tk.Frame(settings_window, bg='#34495e')
        settings_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Varsayılan format
        tk.Label(settings_frame, text="Varsayılan Format:", 
                font=('Arial', 10, 'bold'), bg='#34495e', fg='white').pack(anchor='w', pady=5)
        
        default_format_frame = tk.Frame(settings_frame, bg='#34495e')
        default_format_frame.pack(fill='x', pady=5)
        
        self.default_format_var = tk.StringVar(value=self.format_var.get())
        format_combo = ttk.Combobox(default_format_frame, textvariable=self.default_format_var,
                                   values=["mp4", "mp3", "webm", "mkv", "avi"])
        format_combo.pack(side='left')
        
        # Varsayılan kalite
        tk.Label(settings_frame, text="Varsayılan Kalite:", 
                font=('Arial', 10, 'bold'), bg='#34495e', fg='white').pack(anchor='w', pady=(10, 5))
        
        default_quality_frame = tk.Frame(settings_frame, bg='#34495e')
        default_quality_frame.pack(fill='x', pady=5)
        
        self.default_quality_var = tk.StringVar(value=self.quality_var.get())
        quality_combo = ttk.Combobox(default_quality_frame, textvariable=self.default_quality_var,
                                    values=["best", "worst", "720p", "480p", "360p"])
        quality_combo.pack(side='left')
        
        # Otomatik klasör açma
        self.auto_open_var = tk.BooleanVar()
        auto_open_check = tk.Checkbutton(settings_frame, text="İndirme tamamlandığında klasörü otomatik aç",
                                        variable=self.auto_open_var, bg='#34495e', fg='white',
                                        selectcolor='#3498db', activebackground='#34495e')
        auto_open_check.pack(anchor='w', pady=10)
        
        # Butonlar
        button_frame = tk.Frame(settings_frame, bg='#34495e')
        button_frame.pack(fill='x', pady=20)
        
        save_btn = tk.Button(button_frame, text="💾 Kaydet", 
                            command=lambda: self.save_settings(settings_window),
                            bg='#10b981', fg='white', font=('Arial', 10, 'bold'),
                            relief='flat', bd=0, padx=20, pady=5)
        save_btn.pack(side='left', padx=5)
        
        cancel_btn = tk.Button(button_frame, text="❌ Vazgeç", 
                             command=settings_window.destroy,
                             bg='#ef4444', fg='white', font=('Arial', 10, 'bold'),
                             relief='flat', bd=0, padx=20, pady=5)
        cancel_btn.pack(side='left', padx=5)
        
    def save_settings(self, window):
        """Ayarları kaydeder"""
        self.format_var.set(self.default_format_var.get())
        self.quality_var.set(self.default_quality_var.get())
        window.destroy()
        messagebox.showinfo("Başarılı", "Ayarlar kaydedildi!")
        
    def open_help(self):
        """Yardım penceresini açar"""
        help_window = tk.Toplevel(self.root)
        help_window.title("❓ Yardım")
        help_window.geometry("800x700")  # Daha büyük pencere
        help_window.configure(bg='#2c3e50')
        help_window.resizable(True, True)  # Yeniden boyutlandırılabilir
        
        # Scrollable frame için
        canvas = tk.Canvas(help_window, bg='#2c3e50')
        scrollbar = tk.Scrollbar(help_window, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#2c3e50')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Başlık
        title_label = tk.Label(scrollable_frame, text="Sanırım Yardıma İhtiyacınız Var❓", 
                              font=('Arial', 14, 'bold'), bg='#2c3e50', fg='white')
        title_label.pack(pady=10)
        
        # Yardım içeriği - Sekmeli tasarım
        help_frame = tk.Frame(scrollable_frame, bg='#34495e')
        help_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # YouTube sekmesi - Soft indigo
        youtube_header = tk.Frame(help_frame, bg='#6366f1', height=40, cursor='hand2')
        youtube_header.pack(fill='x', pady=(0, 2))
        youtube_header.pack_propagate(False)
        
        youtube_title = tk.Label(youtube_header, text="📺 YouTube İndirme", 
                               font=('Arial', 12, 'bold'), bg='#6366f1', fg='white')
        youtube_title.pack(expand=True)
        
        self.youtube_content = tk.Frame(help_frame, bg='#2c3e50', height=0)
        self.youtube_content.pack(fill='x', pady=(0, 2))
        
        youtube_text = tk.Text(self.youtube_content, height=8, font=('Arial', 9), 
                              bg='#34495e', fg='white', wrap=tk.WORD, state=tk.DISABLED)
        youtube_text.pack(fill='x', padx=10, pady=5)
        
        youtube_help = """1. YouTube'da istediğiniz videoyu bulun
2. Video URL'ini kopyalayın
3. URL formatları:
   • https://www.youtube.com/watch?v=VIDEO_ID
   • https://youtu.be/VIDEO_ID (kısaltılmış)
   • https://music.youtube.com/watch?v=VIDEO_ID (YouTube Music)
4. Programda URL'i yapıştırın ve format seçin:
   • MP4: Video indirme
   • MP3: Sadece ses indirme
5. Kalite seçin ve indirmeyi başlatın

✅ Özellikler:
• Playlist'ler desteklenir (tüm videoları indirir)
• YouTube Music şarkıları MP3 olarak indirilebilir
• Kalite seçenekleri: Best, 720p, 480p, 360p
• Özel URL'ler ve kısaltılmış linkler çalışır"""
        
        youtube_text.config(state=tk.NORMAL)
        youtube_text.insert(tk.END, youtube_help)
        youtube_text.config(state=tk.DISABLED)
        
        # Facebook sekmesi - Soft mavi
        facebook_header = tk.Frame(help_frame, bg='#3b82f6', height=40, cursor='hand2')
        facebook_header.pack(fill='x', pady=(0, 2))
        facebook_header.pack_propagate(False)
        
        facebook_title = tk.Label(facebook_header, text="📘 Facebook İndirme", 
                                font=('Arial', 12, 'bold'), bg='#3b82f6', fg='white')
        facebook_title.pack(expand=True)
        
        self.facebook_content = tk.Frame(help_frame, bg='#2c3e50', height=0)
        self.facebook_content.pack(fill='x', pady=(0, 2))
        
        facebook_text = tk.Text(self.facebook_content, height=8, font=('Arial', 9), 
                              bg='#34495e', fg='white', wrap=tk.WORD, state=tk.DISABLED)
        facebook_text.pack(fill='x', padx=10, pady=5)
        
        facebook_help = """1. Facebook'ta istediğiniz videoyu bulun
2. Video URL'ini kopyalayın
3. URL formatları:
   • https://www.facebook.com/watch/?v=VIDEO_ID
   • https://fb.watch/VIDEO_ID (Facebook Watch)
   • https://www.facebook.com/kullanici/videos/VIDEO_ID
4. Programda URL'i yapıştırın ve indirmeyi başlatın

⚠️ Önemli:
• Video'nun herkese açık olması gerekir
• Özel grupların videoları indirilemez
• Canlı yayınlar indirilemez, sadece kayıtlı videolar
• Facebook'a giriş yapmış olmanız gerekebilir
• Grup ve sayfa videoları da desteklenir"""
        
        facebook_text.config(state=tk.NORMAL)
        facebook_text.insert(tk.END, facebook_help)
        facebook_text.config(state=tk.DISABLED)
        
        # Instagram sekmesi - Soft pembe
        instagram_header = tk.Frame(help_frame, bg='#ec4899', height=40, cursor='hand2')
        instagram_header.pack(fill='x', pady=(0, 2))
        instagram_header.pack_propagate(False)
        
        instagram_title = tk.Label(instagram_header, text="📷 Instagram İndirme", 
                                 font=('Arial', 12, 'bold'), bg='#ec4899', fg='white')
        instagram_title.pack(expand=True)
        
        self.instagram_content = tk.Frame(help_frame, bg='#2c3e50', height=0)
        self.instagram_content.pack(fill='x', pady=(0, 2))
        
        instagram_text = tk.Text(self.instagram_content, height=8, font=('Arial', 9), 
                                bg='#34495e', fg='white', wrap=tk.WORD, state=tk.DISABLED)
        instagram_text.pack(fill='x', padx=10, pady=5)
        
        instagram_help = """1. Instagram'da istediğiniz videoyu bulun
2. Video URL'ini kopyalayın
3. URL formatları:
   • https://www.instagram.com/p/POST_ID/
   • https://www.instagram.com/reel/REEL_ID/
   • https://www.instagram.com/tv/TV_ID/
4. Programda URL'i yapıştırın ve indirmeyi başlatın

⚠️ Önemli:
• Video'nun herkese açık olması gerekir
• Özel hesapların videoları indirilemez
• Instagram'a giriş yapmış olmanız gerekebilir
• Reels, IGTV ve normal postlar desteklenir
• Story'ler indirilemez"""
        
        instagram_text.config(state=tk.NORMAL)
        instagram_text.insert(tk.END, instagram_help)
        instagram_text.config(state=tk.DISABLED)
        
        # Twitter/X sekmesi - Soft gri
        twitter_header = tk.Frame(help_frame, bg='#6b7280', height=40, cursor='hand2')
        twitter_header.pack(fill='x', pady=(0, 2))
        twitter_header.pack_propagate(False)
        
        twitter_title = tk.Label(twitter_header, text="🐦 Twitter/X İndirme", 
                                font=('Arial', 12, 'bold'), bg='#6b7280', fg='white')
        twitter_title.pack(expand=True)
        
        self.twitter_content = tk.Frame(help_frame, bg='#2c3e50', height=0)
        self.twitter_content.pack(fill='x', pady=(0, 2))
        
        twitter_text = tk.Text(self.twitter_content, height=8, font=('Arial', 9), 
                              bg='#34495e', fg='white', wrap=tk.WORD, state=tk.DISABLED)
        twitter_text.pack(fill='x', padx=10, pady=5)
        
        twitter_help = """1. Twitter/X'te istediğiniz videoyu bulun
2. Video URL'ini kopyalayın
3. URL formatları:
   • https://twitter.com/kullanici/status/TWEET_ID
   • https://x.com/kullanici/status/TWEET_ID
4. Programda URL'i yapıştırın ve indirmeyi başlatın

⚠️ Önemli:
• Video'nun herkese açık olması gerekir
• Özel hesapların videoları indirilemez
• Twitter/X'e giriş yapmış olmanız gerekebilir
• Tweet'lerdeki videolar, GIF'ler ve resimler indirilebilir
• Retweet'ler ve quote tweet'ler de desteklenir"""
        
        twitter_text.config(state=tk.NORMAL)
        twitter_text.insert(tk.END, twitter_help)
        twitter_text.config(state=tk.DISABLED)
        
        # TikTok sekmesi - Soft kırmızı
        tiktok_header = tk.Frame(help_frame, bg='#ef4444', height=40, cursor='hand2')
        tiktok_header.pack(fill='x', pady=(0, 2))
        tiktok_header.pack_propagate(False)
        
        tiktok_title = tk.Label(tiktok_header, text="🎵 TikTok İndirme", 
                               font=('Arial', 12, 'bold'), bg='#ef4444', fg='white')
        tiktok_title.pack(expand=True)
        
        self.tiktok_content = tk.Frame(help_frame, bg='#2c3e50', height=0)
        self.tiktok_content.pack(fill='x', pady=(0, 2))
        
        tiktok_text = tk.Text(self.tiktok_content, height=8, font=('Arial', 9), 
                             bg='#34495e', fg='white', wrap=tk.WORD, state=tk.DISABLED)
        tiktok_text.pack(fill='x', padx=10, pady=5)
        
        tiktok_help = """1. TikTok'ta istediğiniz videoyu bulun
2. Video URL'ini kopyalayın
3. URL formatları:
   • https://www.tiktok.com/@kullanici/video/VIDEO_ID
   • https://vm.tiktok.com/KISA_URL/
   • https://tiktok.com/@kullanici/video/VIDEO_ID
4. Programda URL'i yapıştırın ve indirmeyi başlatın

⚠️ Önemli:
• Video'nun herkese açık olması gerekir
• Özel hesapların videoları indirilemez
• TikTok'a giriş yapmış olmanız gerekebilir
• Kısaltılmış URL'ler de desteklenir
• Müzik videoları ve dans videoları indirilebilir"""
        
        tiktok_text.config(state=tk.NORMAL)
        tiktok_text.insert(tk.END, tiktok_help)
        tiktok_text.config(state=tk.DISABLED)
        
        # Sekme tıklama olayları
        youtube_header.bind('<Button-1>', lambda e: self.toggle_section('youtube'))
        facebook_header.bind('<Button-1>', lambda e: self.toggle_section('facebook'))
        instagram_header.bind('<Button-1>', lambda e: self.toggle_section('instagram'))
        twitter_header.bind('<Button-1>', lambda e: self.toggle_section('twitter'))
        tiktok_header.bind('<Button-1>', lambda e: self.toggle_section('tiktok'))
        
        # Başlık tıklama olayları
        youtube_title.bind('<Button-1>', lambda e: self.toggle_section('youtube'))
        facebook_title.bind('<Button-1>', lambda e: self.toggle_section('facebook'))
        instagram_title.bind('<Button-1>', lambda e: self.toggle_section('instagram'))
        twitter_title.bind('<Button-1>', lambda e: self.toggle_section('twitter'))
        tiktok_title.bind('<Button-1>', lambda e: self.toggle_section('tiktok'))
        
        # Aktif sekme durumu
        self.active_section = None
        
        # Canvas ve scrollbar'ı pack et
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Mouse wheel ile scroll - Güvenli versiyon
        def _on_mousewheel(event):
            try:
                canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            except:
                pass  # Canvas yoksa hata verme
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Kapat butonu
        close_btn = tk.Button(scrollable_frame, text="❌ Kapat", 
                             command=help_window.destroy,
                             font=('Arial', 10, 'bold'),
                             bg='#e74c3c', fg='white',
                             relief='flat', bd=0, padx=20, pady=10,
                             cursor='hand2')
        close_btn.pack(pady=20)
        
    def toggle_section(self, section_name):
        """Sekmeli yardım sisteminde bölümleri aç/kapat"""
        # Eğer aynı bölüm tıklanırsa kapat
        if self.active_section == section_name:
            self.close_section(section_name)
            self.active_section = None
        else:
            # Önceki aktif bölümü kapat
            if self.active_section:
                self.close_section(self.active_section)
            
            # Yeni bölümü aç
            self.open_section(section_name)
            self.active_section = section_name
    
    def open_section(self, section_name):
        """Belirtilen bölümü açar"""
        content_frame = getattr(self, f'{section_name}_content')
        content_frame.config(height=200)  # İçerik yüksekliği
        content_frame.pack_propagate(False)
    
    def close_section(self, section_name):
        """Belirtilen bölümü kapatır"""
        content_frame = getattr(self, f'{section_name}_content')
        content_frame.config(height=0)
        content_frame.pack_propagate(False)
        
    def open_download_folder(self):
        os.startfile(self.download_folder)
        
    def log_message(self, message):
        """Log mesajını GUI'ye ekler"""
        try:
            # Thread-safe GUI güncellemesi
            self.root.after(0, self._update_log, message)
        except Exception as e:
            print(f"Log hatası: {e}")
    
    def _update_log(self, message):
        """GUI'yi günceller (ana thread'de çalışır)"""
        try:
            timestamp = time.strftime("%H:%M:%S")
            self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
            self.log_text.see(tk.END)
            self.root.update_idletasks()
        except Exception as e:
            print(f"GUI güncelleme hatası: {e}")
    
    def _initial_log_message(self):
        """Program başlangıcında log mesajı"""
        self.log_message("🎵 Social Media Content Downloader started!")
        self.log_message("📋 Ready - Enter URLs and start downloading")
        self.log_message("=" * 60)
        
    def start_download(self):
        urls = self.url_text.get(1.0, tk.END).strip().split('\n')
        urls = [url.strip() for url in urls if url.strip()]
        
        if not urls:
            messagebox.showerror("Hata", "Lütfen en az bir URL girin!")
            return
            
        # İndirme işlemini ayrı thread'de başlat
        self.log_message(f"🚀 {len(urls)} URL için indirme başlatılıyor...")
        self.log_message("📁 İndirme klasörü: " + self.download_folder)
        self.log_message("📋 Format: " + self.format_var.get() + ", Kalite: " + self.quality_var.get())
        self.log_message("=" * 60)
        
        download_thread = threading.Thread(target=self.download_videos, args=(urls,))
        download_thread.daemon = True
        download_thread.start()
        
    def download_videos(self, urls):
        try:
            self.progress_bar.start()
            self.progress_var.set("İndirme başlatılıyor...")
            
            total_urls = len(urls)
            successful_downloads = 0
            failed_downloads = 0
            
            # İstatistikleri güncelle
            self.total_downloads += total_urls
            
            self.log_message(f"🚀 {total_urls} URL için indirme başlatılıyor...")
            self.log_message(f"📁 İndirme klasörü: {self.download_folder}")
            self.log_message(f"📋 Format: {self.format_var.get()}, Kalite: {self.quality_var.get()}")
            self.log_message("=" * 60)
            
            for i, url in enumerate(urls, 1):
                self.progress_var.set(f"İndiriliyor ({i}/{total_urls}): {url[:50]}...")
                self.log_message(f"\n[{i}/{total_urls}] İndiriliyor: {url}")
                
                # Platform tespiti
                platform = self.detect_platform_from_url(url)
                if platform:
                    self.log_message(f"📱 Platform: {platform}")
                
                try:
                    start_time = time.time()
                    success = self.download_single_video(url)
                    end_time = time.time()
                    duration = end_time - start_time
                    
                    if success:
                        successful_downloads += 1
                        self.successful_downloads += 1
                        self.log_message(f"✅ Başarılı ({duration:.1f}s): {url}")
                    else:
                        failed_downloads += 1
                        self.failed_downloads += 1
                        self.log_message(f"❌ Başarısız ({duration:.1f}s): {url}")
                        
                except Exception as e:
                    failed_downloads += 1
                    self.failed_downloads += 1
                    self.log_message(f"❌ Hata: {url} - {str(e)}")
                    
            self.progress_bar.stop()
            self.progress_var.set(f"Tamamlandı! {successful_downloads}/{total_urls} başarılı")
            
            # İstatistikleri güncelle
            self.update_stats_display()
            
            # Sonuç mesajı
            self.log_message("\n" + "=" * 60)
            self.log_message(f"📊 İndirme Tamamlandı!")
            self.log_message(f"✅ Başarılı: {successful_downloads}")
            self.log_message(f"❌ Başarısız: {failed_downloads}")
            self.log_message(f"📁 Dosyalar: {self.download_folder}")
            
            if successful_downloads > 0:
                messagebox.showinfo("Başarılı", 
                                  f"İndirme tamamlandı!\n{successful_downloads}/{total_urls} dosya başarıyla indirildi.")
                
                # Otomatik klasör açma
                if hasattr(self, 'auto_open_var') and self.auto_open_var.get():
                    self.open_download_folder()
            else:
                messagebox.showerror("Hata", "Hiçbir dosya indirilemedi!")
                
        except Exception as e:
            self.progress_bar.stop()
            self.progress_var.set("Hata oluştu!")
            self.log_message(f"❌ Genel hata: {str(e)}")
            messagebox.showerror("Hata", f"İndirme sırasında hata oluştu: {str(e)}")
            
    def detect_platform_from_url(self, url):
        """URL'den platformu tespit eder"""
        for domain, platform in self.supported_platforms.items():
            if domain in url:
                return platform
        return None
        
    def download_twitter_video(self, cmd, url):
        """Twitter/X için özel indirme fonksiyonu"""
        try:
            # İlk önce cookie olmadan dene
            self.log_message("🐦 Twitter/X indirme deneniyor (cookie olmadan)...")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                return result
                
            # Cookie olmadan başarısızsa, Firefox ile dene
            self.log_message("🦊 Firefox cookie ile deneniyor...")
            cmd_firefox = cmd.copy()
            cmd_firefox.insert(-1, '--cookies-from-browser')
            cmd_firefox.insert(-1, 'firefox')
            
            result = subprocess.run(cmd_firefox, capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                return result
                
            # Firefox da başarısızsa, Edge ile dene
            self.log_message("🌐 Edge cookie ile deneniyor...")
            cmd_edge = cmd.copy()
            cmd_edge.insert(-1, '--cookies-from-browser')
            cmd_edge.insert(-1, 'edge')
            
            result = subprocess.run(cmd_edge, capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                return result
                
            # Son çare: basit indirme
            self.log_message("🔄 Basit indirme yöntemi deneniyor...")
            simple_cmd = [
                sys.executable, '-m', 'yt_dlp',
                '--output', os.path.join(self.download_folder, '%(title)s.%(ext)s'),
                '--format', 'best',
                '--no-playlist',
                url
            ]
            
            result = subprocess.run(simple_cmd, capture_output=True, text=True, timeout=300)
            return result
            
        except Exception as e:
            self.log_message(f"❌ Twitter/X indirme hatası: {str(e)}")
            # Hata durumunda basit bir result döndür
            class SimpleResult:
                def __init__(self):
                    self.returncode = 1
                    self.stdout = ""
                    self.stderr = str(e)
            return SimpleResult()
            
    def download_instagram_video(self, cmd, url):
        """Instagram için özel indirme fonksiyonu"""
        try:
            # İlk önce cookie olmadan dene
            self.log_message("📷 Instagram indirme deneniyor (cookie olmadan)...")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                return result
                
            # Cookie olmadan başarısızsa, Firefox ile dene
            self.log_message("🦊 Firefox cookie ile deneniyor...")
            cmd_firefox = cmd.copy()
            cmd_firefox.insert(-1, '--cookies-from-browser')
            cmd_firefox.insert(-1, 'firefox')
            
            result = subprocess.run(cmd_firefox, capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                return result
                
            # Firefox da başarısızsa, Edge ile dene
            self.log_message("🌐 Edge cookie ile deneniyor...")
            cmd_edge = cmd.copy()
            cmd_edge.insert(-1, '--cookies-from-browser')
            cmd_edge.insert(-1, 'edge')
            
            result = subprocess.run(cmd_edge, capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                return result
                
            # Son çare: basit indirme
            self.log_message("🔄 Basit indirme yöntemi deneniyor...")
            simple_cmd = [
                sys.executable, '-m', 'yt_dlp',
                '--output', os.path.join(self.download_folder, '%(title)s.%(ext)s'),
                '--format', 'best',
                '--no-playlist',
                url
            ]
            
            result = subprocess.run(simple_cmd, capture_output=True, text=True, timeout=300)
            return result
            
        except Exception as e:
            self.log_message(f"❌ Instagram indirme hatası: {str(e)}")
            # Hata durumunda basit bir result döndür
            class SimpleResult:
                def __init__(self):
                    self.returncode = 1
                    self.stdout = ""
                    self.stderr = str(e)
            return SimpleResult()
            
    def download_single_video(self, url):
        try:
            # yt-dlp'nin yüklü olup olmadığını kontrol et
            try:
                import yt_dlp
                try:
                    version = yt_dlp.version.__version__
                except:
                    version = "installed"
                self.log_message(f"✅ yt-dlp version: {version}")
            except ImportError:
                self.log_message("❌ yt-dlp module not found!")
                self.log_message("💡 Solution: pip install yt-dlp")
                return False
            
            # İndirme klasörünün var olduğundan emin ol
            os.makedirs(self.download_folder, exist_ok=True)
            self.log_message(f"📁 Download folder: {self.download_folder}")
            
            # Dosya adı için güvenli karakterler
            safe_filename = '%(title)s.%(ext)s'
            output_path = os.path.join(self.download_folder, safe_filename)
            
            # yt-dlp komutunu oluştur (Python modülü olarak)
            cmd = [
                sys.executable, '-m', 'yt_dlp',
                '--output', output_path,
                '--no-playlist',
                '--progress',
                '--newline',
                '--no-mtime',  # Dosya zamanını değiştirme
                # YouTube için özel ayarlar (403 hatası için)
                '--user-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                '--extractor-args', 'youtube:player_client=android,ios,web',  # Farklı client'lar dene
                '--no-check-certificate'  # SSL sorunları için
            ]
            
            # Format'a göre ayarlar
            if self.format_var.get() == 'mp3':
                cmd.extend([
                    '--extract-audio',
                    '--audio-format', 'mp3',
                    '--audio-quality', '192K',  # Sabit bitrate (192 kbps)
                    '--format', 'bestaudio/best'
                ])
            elif self.format_var.get() == 'mp4':
                quality = self.quality_var.get()
                if quality == 'best':
                    cmd.extend(['--format', 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'])
                elif quality == 'worst':
                    cmd.extend(['--format', 'worstvideo[ext=mp4]+worstaudio/worst[ext=mp4]/worst'])
                else:
                    height = quality.replace('p', '')
                    cmd.extend([f'--format', f'bestvideo[height<={height}][ext=mp4]+bestaudio[ext=m4a]/best[height<={height}][ext=mp4]/best'])
            else:
                cmd.extend(['--format', self.get_format_string()])
            
            # Platform özel ayarları
            platform = self.detect_platform_from_url(url)
            result = None  # Result değişkenini başlat
            
            if platform == 'YouTube' or platform == 'YouTube Music':
                # YouTube için özel ayarlar (403 hatası için)
                self.log_message("📺 Applying YouTube-specific settings...")
                
                # Önce cookie ile dene (en iyi yöntem)
                cookie_browsers = ['firefox', 'chrome', 'edge']
                cookie_success = False
                
                for browser in cookie_browsers:
                    try:
                        # Cookie parametrelerini ekle (URL henüz cmd'de yok)
                        cmd_cookie = cmd.copy()
                        cmd_cookie.extend(['--cookies-from-browser', browser, url])
                        
                        self.log_message(f"🦊 Trying with {browser.capitalize()} cookies...")
                        result_cookie = subprocess.run(cmd_cookie, capture_output=True, text=True, timeout=600, encoding='utf-8', errors='ignore')
                        
                        if result_cookie.returncode == 0:
                            self.log_message(f"✅ Success with {browser.capitalize()} cookies!")
                            result = result_cookie
                            cookie_success = True
                            break
                        else:
                            # Hata varsa logla ama devam et
                            if result_cookie.stderr and ('ERROR' in result_cookie.stderr or 'error' in result_cookie.stderr.lower()):
                                error_preview = result_cookie.stderr[-200:] if result_cookie.stderr else ""
                                if '403' not in error_preview:  # 403 değilse başka bir hata var
                                    self.log_message(f"⚠️ {browser.capitalize()} cookie method failed")
                    except Exception as e:
                        # Cookie yoksa veya hata varsa devam et
                        continue
                
                if not cookie_success:
                    self.log_message("⚠️ Cookie methods failed, trying without cookies...")
                    result = None
                    
            # URL'i komuta ekle (tüm platformlar için)
            cmd.append(url)
            
            if platform == 'Instagram':
                # Instagram için özel ayarlar - cookie olmadan
                cmd.extend([
                    '--user-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    '--referer', 'https://www.instagram.com/',
                    '--format', 'best[ext=mp4]/best',
                    '--sleep-interval', '2',
                    '--max-sleep-interval', '10',
                    '--retries', '3',
                    '--fragment-retries', '3'
                ])
                self.log_message("📷 Instagram için özel ayarlar uygulandı (cookie olmadan)")
            elif platform == 'Twitter/X':
                # Twitter/X için özel ayarlar - cookie olmadan
                cmd.extend([
                    '--user-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    '--referer', 'https://twitter.com/',
                    '--format', 'best[ext=mp4]/best',
                    '--sleep-interval', '2',
                    '--max-sleep-interval', '10',
                    '--retries', '3',
                    '--fragment-retries', '3'
                ])
                self.log_message("🐦 Twitter/X için özel ayarlar uygulandı (cookie olmadan)")
                
                # Cookie alternatifi dene
                try:
                    cmd_cookie = cmd.copy()
                    cmd_cookie.insert(-1, '--cookies-from-browser')
                    cmd_cookie.insert(-1, 'firefox')  # Firefox'u dene
                    self.log_message("🦊 Firefox cookie desteği deneniyor...")
                except:
                    pass
                
            cmd.append(url)
            
            # Komutu çalıştır
            self.log_message(f"🔧 Executing command...")
            self.log_message(f"📋 URL: {url[:80]}...")
            self.log_message(f"📋 Format: {self.format_var.get()}, Quality: {self.quality_var.get()}")
            
            # Platform özel indirme mantığı
            if platform == 'Twitter/X':
                result = self.download_twitter_video(cmd, url)
            elif platform == 'Instagram':
                result = self.download_instagram_video(cmd, url)
            else:
                # Normal platformlar için
                self.log_message(f"🚀 Starting download for {platform}...")
            
            # Eğer result henüz set edilmediyse (cookie denemesi başarısız olduysa veya diğer platformlar)
            if result is None:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=600, encoding='utf-8', errors='ignore')
            
            # Debug için çıktıları logla
            self.log_message(f"📤 Return code: {result.returncode}")
            
            # Tüm çıktıyı birleştir (stdout + stderr)
            full_output = ""
            if result.stdout:
                full_output += result.stdout
            if result.stderr:
                full_output += "\n" + result.stderr
            
            # Stdout'u analiz et
            if result.stdout:
                # Son 2000 karakteri al (daha fazla bilgi için)
                stdout_preview = result.stdout[-2000:]
                
                # Önemli satırları bul
                important_lines = []
                for line in stdout_preview.split('\n'):
                    if any(keyword in line.lower() for keyword in ['download', 'error', 'warning', '100%', 'destination', 'merging']):
                        important_lines.append(line)
                
                if important_lines:
                    self.log_message("📤 Important output lines:")
                    for line in important_lines[-5:]:  # Son 5 önemli satır
                        if line.strip():
                            self.log_message(f"   {line[:150]}")
                else:
                    # Eğer önemli satır yoksa, son satırları göster
                    last_lines = stdout_preview.split('\n')[-3:]
                    for line in last_lines:
                        if line.strip():
                            self.log_message(f"📤 {line[:150]}")
            
            # Stderr'ı analiz et
            if result.stderr:
                stderr_lower = result.stderr.lower()
                
                # Hata mesajlarını bul
                error_keywords = ['error', 'unable', 'failed', 'cannot', 'unavailable', 'private', 'restricted']
                error_lines = []
                for line in result.stderr.split('\n'):
                    if any(keyword in line.lower() for keyword in error_keywords):
                        error_lines.append(line.strip())
                
                if error_lines:
                    self.log_message("❌ Error messages found:")
                    for error_line in error_lines[:5]:  # İlk 5 hata satırı
                        if error_line:
                            self.log_message(f"   {error_line[:200]}")
                else:
                    # Eğer hata satırı yoksa, stderr'ın sonunu göster
                    stderr_preview = result.stderr[-500:]
                    if stderr_preview.strip():
                        self.log_message(f"⚠️ Stderr output: {stderr_preview[:300]}...")
            
            if result.returncode == 0:
                # Başarılı indirme loglarını kontrol et
                full_output_lower = full_output.lower()
                
                # Başarı işaretleri (daha kapsamlı)
                success_indicators = [
                    'has already been downloaded',
                    'already been downloaded',
                    '[download] 100%',
                    '[download] 100.0%',
                    'downloaded',
                    'merging formats',
                    'merger',
                    'deleting original file',
                    'writing video metadata',
                    'destination:',
                    'finished downloading'
                ]
                
                has_success_indicator = any(indicator in full_output_lower for indicator in success_indicators)
                
                if has_success_indicator:
                    self.log_message("✅ Download completed successfully!")
                    # İndirilen dosyayı kontrol et
                    file_found = self._check_downloaded_file()
                    if file_found:
                        return True
                    else:
                        self.log_message("⚠️ Success indicator found but file not detected yet")
                        # Biraz bekle ve tekrar kontrol et
                        import time
                        time.sleep(2)
                        if self._check_downloaded_file():
                            return True
                
                # Dosya kontrolü yap (return code 0 ise genelde başarılıdır)
                file_found = self._check_downloaded_file()
                if file_found:
                    self.log_message("✅ Download successful (file found)!")
                    return True
                else:
                    # Dosya bulunamadı ama return code 0 - detaylı kontrol
                    self.log_message("⚠️ Return code 0 but checking for files...")
                    
                    # Klasördeki tüm dosyaları listele
                    if os.path.exists(self.download_folder):
                        all_files = os.listdir(self.download_folder)
                        if all_files:
                            self.log_message(f"📁 Found {len(all_files)} file(s) in download folder")
                            # En son değiştirilen dosyayı göster
                            files_with_time = []
                            for file in all_files:
                                file_path = os.path.join(self.download_folder, file)
                                if os.path.isfile(file_path):
                                    mtime = os.path.getmtime(file_path)
                                    files_with_time.append((file, mtime))
                            
                            if files_with_time:
                                files_with_time.sort(key=lambda x: x[1], reverse=True)
                                latest_file, latest_time = files_with_time[0]
                                file_size = os.path.getsize(os.path.join(self.download_folder, latest_file))
                                time_diff = time.time() - latest_time
                                
                                if time_diff < 120:  # Son 2 dakika
                                    self.log_message(f"📁 Latest file: {latest_file} ({file_size / 1024 / 1024:.2f} MB, {int(time_diff)}s ago)")
                                    return True
                    
                    # Eğer hala dosya yoksa, muhtemelen başarısız
                    self.log_message("❌ No file found after download attempt")
                    return False
            else:
                # Return code != 0 - Hata var
                error_msg = result.stderr if result.stderr else result.stdout
                self.log_message(f"❌ yt-dlp error (code: {result.returncode})")
                
                # Hata mesajını parse et
                if error_msg:
                    error_lines = error_msg.split('\n')
                    for line in error_lines:
                        if 'ERROR' in line or 'error' in line.lower() or 'unable' in line.lower():
                            self.log_message(f"❌ {line[:200]}")
                            break
                
                # Platform özel hata mesajları
                if platform == 'Twitter/X':
                    self.log_message("🐦 Twitter/X Tips:")
                    self.log_message("1. Log in to Twitter/X in Firefox/Edge browser")
                    self.log_message("2. Ensure video is public (not private)")
                    self.log_message("3. Verify URL is correct")
                    self.log_message("4. Try updating yt-dlp: pip install --upgrade yt-dlp")
                elif platform == 'Instagram':
                    self.log_message("📷 Instagram Tips:")
                    self.log_message("1. Log in to Instagram in Firefox/Edge browser")
                    self.log_message("2. Ensure post is public")
                    self.log_message("3. Verify URL is correct")
                    self.log_message("4. Try updating yt-dlp: pip install --upgrade yt-dlp")
                elif platform == 'YouTube' or platform == 'YouTube Music':
                    self.log_message("📺 YouTube Tips (403 Forbidden Error):")
                    self.log_message("1. Update yt-dlp: pip install --upgrade yt-dlp")
                    self.log_message("2. Try logging into YouTube in Firefox browser")
                    self.log_message("3. Check if video is available in your region")
                    self.log_message("4. Try a different video URL")
                    self.log_message("5. Wait a few minutes and try again (rate limiting)")
                    self.log_message("6. Check your internet connection and VPN if used")
                else:
                    self.log_message("💡 General Tips:")
                    self.log_message("1. Update yt-dlp: pip install --upgrade yt-dlp")
                    self.log_message("2. Check internet connection")
                    self.log_message("3. Verify URL is correct and accessible")
                    self.log_message("4. Try a different format/quality")
                
                return False
                
        except subprocess.TimeoutExpired:
            self.log_message("⏰ Download timeout (10 minutes)")
            self.log_message("💡 Try again or use a shorter video")
            return False
        except FileNotFoundError as e:
            self.log_message(f"❌ yt-dlp not found: {str(e)}")
            self.log_message("💡 Solution: pip install yt-dlp")
            self.log_message("💡 Or: python -m pip install --upgrade yt-dlp")
            return False
        except Exception as e:
            error_type = type(e).__name__
            self.log_message(f"❌ Download error ({error_type}): {str(e)}")
            import traceback
            self.log_message(f"📋 Details: {traceback.format_exc()[:300]}")
            return False
    
    def _check_downloaded_file(self):
        """İndirme klasöründe yeni dosya olup olmadığını kontrol eder"""
        try:
            if not os.path.exists(self.download_folder):
                self.log_message(f"⚠️ Download folder does not exist: {self.download_folder}")
                return False
            
            import time
            current_time = time.time()
            files = os.listdir(self.download_folder)
            
            if not files:
                return False
            
            # Son 2 dakikada oluşturulan/değiştirilen dosyaları kontrol et
            recent_files = []
            for file in files:
                file_path = os.path.join(self.download_folder, file)
                if os.path.isfile(file_path):
                    file_time = os.path.getmtime(file_path)
                    time_diff = current_time - file_time
                    if time_diff < 120:  # Son 2 dakika
                        file_size = os.path.getsize(file_path)
                        recent_files.append((file, file_size, time_diff))
            
            if recent_files:
                # En yeni dosyayı göster
                recent_files.sort(key=lambda x: x[2])  # En yeni önce
                latest_file, file_size, time_diff = recent_files[0]
                self.log_message(f"📁 Found file: {latest_file} ({file_size / 1024 / 1024:.2f} MB, {int(time_diff)}s ago)")
                return True
            
            return False
        except Exception as e:
            self.log_message(f"⚠️ File check error: {str(e)}")
            import traceback
            self.log_message(f"📋 Traceback: {traceback.format_exc()[:200]}")
            return False
            
    def get_format_string(self):
        if self.format_var.get() == 'mp3':
            return 'bestaudio'
        elif self.format_var.get() == 'mp4':
            quality = self.quality_var.get()
            if quality == 'best':
                return 'best[ext=mp4]/best'
            elif quality == 'worst':
                return 'worst[ext=mp4]/worst'
            else:
                return f'best[height<={quality.replace("p", "")}][ext=mp4]/best'
        else:
            return 'best'

def main():
    root = tk.Tk()
    app = SocialMediaDownloader(root)
    root.mainloop()

if __name__ == "__main__":
    main()
