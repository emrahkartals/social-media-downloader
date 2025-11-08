<div align="center">

# 🎵 Social Media Content Downloader 🎬

**Modern, smooth, and user-friendly social media content downloader with multi-platform support**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)](https://www.microsoft.com/windows)
[![yt-dlp](https://img.shields.io/badge/yt--dlp-2025.10.22-red.svg)](https://github.com/yt-dlp/yt-dlp)
[![Status](https://img.shields.io/badge/Status-Active-success.svg)](https://github.com/emrahkartals/social-media-downloader)

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Screenshots](#-screenshots) • [Troubleshooting](#-troubleshooting) • [Contributing](#-contributing)

</div>

---

## 📖 About

**Social Media Content Downloader** is a powerful, modern application that allows you to download videos and audio from multiple social media platforms. With both **GUI** and **Web** interfaces, it provides a seamless experience for downloading content from YouTube, Instagram, Twitter/X, TikTok, Facebook, and more.

### 🎯 Key Highlights

- 🚀 **Dual Interface**: Choose between a modern GUI application or a web-based interface
- 🌐 **Multi-Platform**: Support for 6+ major social media platforms
- 📦 **Batch Download**: Download multiple URLs simultaneously
- 🎨 **Smooth Modern UI**: Beautiful dark theme with gradient effects and hover animations
- ⚡ **Fast & Reliable**: Built on yt-dlp (latest version) for maximum compatibility
- 🔐 **Smart Cookie Support**: Automatic browser cookie detection for enhanced downloads
- 📊 **Real-time Statistics**: Track download success rates and progress

---

## ✨ Features

### Core Features

| Feature | Description |
|---------|-------------|
| 🎬 **Multi-Platform Support** | YouTube, YouTube Music, Instagram, Twitter/X, TikTok, Facebook |
| 📥 **Batch Downloads** | Download multiple URLs at once |
| 🎵 **Format Options** | MP4, MP3, WebM, MKV, AVI formats |
| 🎚️ **Quality Control** | Best, Worst, 720p, 480p, 360p quality options |
| 🔍 **Auto Platform Detection** | Automatically detects platform from URL |
| 📊 **Statistics Tracking** | Track successful/failed downloads with detailed stats |
| 📝 **Real-time Logs** | Detailed download logs with error analysis |
| ⚙️ **Customizable Settings** | Custom download folder, format preferences |
| 🎨 **Smooth Dark Theme** | Modern UI with gradient effects and smooth transitions |

### Advanced Features

- 🔐 **Smart Cookie Support**: Automatic detection and use of browser cookies (Firefox, Chrome, Edge)
- 🔄 **Intelligent Retry**: Multiple fallback methods for failed downloads
- ⏱️ **Timeout Management**: Configurable timeout settings (10 minutes default)
- 🎯 **Platform-Specific Optimization**: Custom settings for each platform
- 📱 **Responsive Web UI**: Mobile-friendly web interface
- 🔔 **Progress Tracking**: Real-time download progress indicators
- 🛡️ **Error Handling**: Comprehensive error detection with helpful tips
- 📁 **File Verification**: Automatic file detection after download

---

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- Windows 10/11 (Linux/macOS support with additional configuration)
- Internet connection
- 100 MB free disk space

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/emrahkartals/social-media-downloader.git
   cd social-media-downloader
   ```

2. **Install dependencies**

   For GUI application:
   ```bash
   pip install -r requirements.txt
   ```

   For Web application:
   ```bash
   pip install -r web_requirements.txt
   ```

3. **Run the application**

   GUI Mode:
   ```bash
   python main.py
   ```

   Web Mode:
   ```bash
   python web_app.py
   ```
   Then open `http://localhost:5000` in your browser.

---

## 📸 Screenshots

### GUI Application
> *Screenshots will be added here*

**Features shown:**
- Smooth dark theme with gradient effects
- Real-time platform detection
- Download statistics
- Detailed log area

### Web Application
> *Screenshots will be added here*

---

## 🎯 Usage

### Basic Usage

1. **Enter URLs**: Paste video/music URLs (one per line)
2. **Select Format**: Choose your preferred format (MP4, MP3, etc.)
3. **Set Quality**: Select video quality
4. **Choose Folder**: Set download destination (optional)
5. **Start Download**: Click "🚀 Start Download" button

### Supported URL Formats

| Platform | URL Examples |
|----------|--------------|
| **YouTube** | `https://www.youtube.com/watch?v=VIDEO_ID`<br>`https://youtu.be/VIDEO_ID` |
| **YouTube Music** | `https://music.youtube.com/watch?v=VIDEO_ID` |
| **Instagram** | `https://www.instagram.com/p/POST_ID/`<br>`https://www.instagram.com/reel/REEL_ID/` |
| **Twitter/X** | `https://twitter.com/USERNAME/status/TWEET_ID`<br>`https://x.com/USERNAME/status/TWEET_ID` |
| **TikTok** | `https://www.tiktok.com/@USERNAME/video/VIDEO_ID` |
| **Facebook** | `https://www.facebook.com/watch/?v=VIDEO_ID`<br>`https://fb.watch/VIDEO_ID` |

### Format Options

| Format | Description | Use Case |
|--------|-------------|----------|
| **MP4** | Video file (default) | Standard video playback |
| **MP3** | Audio file | Music/audio only |
| **WebM** | Web-optimized video | Web applications |
| **MKV** | High-quality video | Best quality preservation |
| **AVI** | Legacy format | Older devices |

### Quality Options

| Quality | Description | File Size |
|---------|-------------|-----------|
| **Best** | Highest available quality | Largest |
| **720p** | HD quality | Medium |
| **480p** | Standard quality | Small |
| **360p** | Low quality | Smallest |
| **Worst** | Lowest available quality | Smallest |

---

## 🏗️ Project Structure

```
social-media-downloader/
├── main.py                 # GUI application (Tkinter)
├── web_app.py              # Web application (Flask)
├── config.json             # Configuration file
├── requirements.txt        # GUI dependencies
├── web_requirements.txt    # Web dependencies
├── templates/
│   └── index.html          # Web UI template
├── Downloads/              # GUI download folder
└── MediaDownloads/         # Web download folder
```

---

## 🔧 Configuration

Edit `config.json` to customize default settings:

```json
{
    "default_settings": {
        "format": "mp4",
        "quality": "best",
        "download_folder": "~/Downloads/SocialMediaDownloads",
        "auto_open_folder": false,
        "timeout": 600
    }
}
```

---

## 🛠️ Troubleshooting

### Common Issues

#### ❌ "yt-dlp not found" error
**Solution:**
```bash
pip install yt-dlp
# Or upgrade to latest version
pip install --upgrade yt-dlp
```

#### ❌ YouTube 403 Forbidden Error
**This is a common issue with YouTube downloads. Solutions:**

1. **Update yt-dlp** (most important):
   ```bash
   pip install --upgrade yt-dlp
   ```

2. **Use Browser Cookies** (recommended):
   - Log in to YouTube in Firefox, Chrome, or Edge browser
   - The application will automatically detect and use cookies
   - This significantly improves success rate

3. **Wait and Retry**:
   - YouTube may rate-limit requests
   - Wait a few minutes and try again

4. **Check Video Availability**:
   - Ensure video is available in your region
   - Verify the URL is correct and accessible

#### ❌ Download fails
**Possible causes:**
- Internet connection issues
- Invalid URL
- Private/restricted content
- Platform API changes

**Solutions:**
- Check internet connection
- Verify URL is correct
- Ensure content is publicly accessible
- Update yt-dlp: `pip install --upgrade yt-dlp`

#### ❌ Instagram/Twitter downloads fail
**Solution:**
- Log in to the platform in Firefox, Chrome, or Edge browser
- The application will automatically use browser cookies
- Ensure the content is public (not private)

#### ❌ Program won't start
**Solutions:**
- Verify Python is installed: `python --version`
- Check dependencies: `pip list`
- Ensure antivirus isn't blocking the application
- Check console for error messages

---

## 📋 Dependencies

### GUI Application
- `yt-dlp>=2024.1.1` - Video download engine (latest version)
- `Pillow>=10.2.0` - Image processing
- `requests>=2.31.0` - HTTP requests
- `tkinter` - GUI framework (included with Python)

### Web Application
- `yt-dlp>=2024.1.1` - Video download engine
- `Flask>=2.3.0` - Web framework
- `Pillow>=10.2.0` - Image processing
- `requests>=2.31.0` - HTTP requests

---

## 🎨 UI Features

### Modern Design
- **Smooth Dark Theme**: Eye-friendly dark interface with gradient effects
- **Hover Animations**: Interactive buttons with smooth hover effects
- **Gradient Separators**: Beautiful multi-color gradient lines
- **Modern Cards**: Clean card-based layout with subtle borders
- **Responsive Layout**: Adapts to different window sizes

### User Experience
- **Real-time Platform Detection**: See detected platforms as you type
- **Detailed Logs**: Comprehensive download logs with error analysis
- **Statistics Dashboard**: Track your download success rate
- **Progress Indicators**: Visual feedback during downloads
- **Helpful Tips**: Platform-specific troubleshooting tips

---

## 🔐 Cookie Support

The application automatically tries to use browser cookies for enhanced downloads:

1. **Firefox** - First attempt
2. **Chrome** - Second attempt  
3. **Edge** - Third attempt
4. **No Cookies** - Fallback method

**To enable cookie support:**
- Simply log in to the platform (YouTube, Instagram, Twitter) in your browser
- The application will automatically detect and use cookies
- No manual configuration needed!

---

## 📊 Statistics

The application tracks:
- **Total Downloads**: Number of download attempts
- **Successful Downloads**: Successfully completed downloads
- **Failed Downloads**: Failed download attempts
- **Success Rate**: Automatic calculation

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Setup

```bash
# Clone repository
git clone https://github.com/emrahkartals/social-media-downloader.git
cd social-media-downloader

# Install development dependencies
pip install -r requirements.txt
pip install -r web_requirements.txt

# Run the application
python main.py  # GUI mode
python web_app.py  # Web mode
```

### Code Style

- Follow PEP 8 style guide
- Use meaningful variable names
- Add comments for complex logic
- Keep functions focused and small

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## ⚠️ Disclaimer

This tool is for **personal use only**. Please respect copyright laws and terms of service of the platforms you download from. Only download content that you have permission to download.

**Important Notes:**
- Download only publicly available content
- Respect content creators' rights
- Do not redistribute downloaded content without permission
- Use responsibly and ethically

---

## 🙏 Acknowledgments

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - The powerful download engine that makes this possible
- All contributors and users of this project
- The open-source community

---

## 🔄 Changelog

### Version 1.0.0 (Current)
- ✨ Initial release
- 🎨 Smooth modern dark theme
- 🔐 Smart cookie support (Firefox, Chrome, Edge)
- 📊 Real-time statistics tracking
- 🔍 Auto platform detection
- 📝 Detailed error logging
- 🎯 Platform-specific optimizations
- 🛡️ Comprehensive error handling

---

<div align="center">

### ⭐ If you like this project, give it a star! ⭐

Made with ❤️ for the open-source community

[Report Bug](https://github.com/emrahkartals/social-media-downloader/issues) • [Request Feature](https://github.com/emrahkartals/social-media-downloader/issues) • [View Issues](https://github.com/emrahkartals/social-media-downloader/issues)

**Happy Downloading! 🎵**

</div>
