# yukakinoki.com

Personal portfolio website powered by Google Sheets and GitHub Pages.

## 🚀 Quick Start

This site automatically updates from a Google Sheet. No need to edit HTML files manually!

### How It Works

1. **Edit Google Sheet** - Update your projects in a spreadsheet
2. **Auto-Deploy** - GitHub Actions rebuilds and deploys your site automatically
3. **Live Updates** - Changes appear on yukakinoki.com within minutes

## 📋 Setup Instructions

See [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed setup instructions.

**Quick setup:**
1. Create a Google Sheet using `google-sheets-template.csv`
2. Get your Sheet ID and API key
3. Add them as GitHub secrets (`GOOGLE_SHEET_ID` and `GOOGLE_API_KEY`)
4. Enable GitHub Actions with write permissions
5. Run the workflow manually or wait for auto-update

## 🛠️ Manual Build

To build the site locally:

```bash
export GOOGLE_SHEET_ID="your_sheet_id"
export GOOGLE_API_KEY="your_api_key"
python build_site.py
```

## 📁 Project Structure

```
yukakinoki.com/
├── build_site.py              # Build script
├── .github/workflows/build.yml # GitHub Actions workflow
├── index.html                 # Generated gallery page
├── archive.html               # Generated archive page
├── info.html                  # Static info page
├── style.css                  # Styles
├── images/                    # Project images and videos
└── templates/                 # HTML templates (optional)
```

## 🔄 Updating Content

### Option 1: Automatic (Recommended)
Edit your Google Sheet and wait up to 6 hours for auto-update.

### Option 2: Manual Trigger
1. Go to GitHub Actions tab
2. Select "Build Site from Google Sheets"
3. Click "Run workflow"

## 📝 License

All content © 2024 yukakinoki.com
