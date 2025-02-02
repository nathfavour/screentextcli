# screentextz 🚀

**screentextz** is an exciting CLI tool that brings your screenshots and image files to life! 🎉 Imagine a tool that watches your designated folders in real-time for any new images, extracts text from them using the powerful Tesseract OCR engine, and copies the text directly to your clipboard. Whether you're a developer, researcher, or simply love efficiency, screentextz is your perfect companion!

## Key Features ✨

- **Real-Time Monitoring 🔍:**  
  Continuously monitors your chosen directories for new image files.  
  Only newly added images are processed – no surprise extractions on existing files!

- **OCR Powered by Tesseract 🖥️:**  
  Leverage Tesseract, a robust and proven OCR engine, to extract text from images with high accuracy.

- **Clipboard Integration 📋:**  
  Automatically copies extracted text to your system clipboard – ready for immediate use!

- **Customizable Settings ⚙️:**  
  Manage directories to monitor and scanning intervals via a simple JSON configuration file (`~/screentextz.json`).  
  Set your defaults once and let screentextz do the rest.

- **User-Friendly CLI Interface 💻:**  
  Utilize intuitive subcommands: display current configuration, override default directories, and start monitoring effortlessly.

## How It Works 🔄

1. **Setup Configuration:**  
   On first run, screentextz creates a configuration file (`~/screentextz.json`) with defaults:
   - Monitors the `~/Pictures/Screenshots` directory.
   - Scans every 5 seconds (adjustable to your needs).

2. **Live Scanning:**  
   The tool pre-scans directories to ignore existing images, then watches for any new additions.  
   As soon as a new image drops in, Tesseract OCR is triggered, text is extracted, and copied to your clipboard automatically.

3. **CLI Subcommands:**  
   - `screentextz start` – Start monitoring (default command when no subcommand is given).  
   - `screentextz config` – Display the current configuration settings.

## Installation 🚀

Installing screentextz is a breeze. Simply run:

