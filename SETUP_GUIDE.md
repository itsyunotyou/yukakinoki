# Google Sheets Setup Guide

## Step 1: Create Your Google Sheet

1. Go to [Google Sheets](https://sheets.google.com)
2. Create a new spreadsheet
3. Name it "yukakinoki Portfolio Content"

## Step 2: Set Up Your Sheets

### Sheet 1: "Projects"

Create a sheet called "Projects" with these columns (Row 1 headers):

| A | B | C | D | E | F | G | H |
|---|---|---|---|---|---|---|---|
| Name | Type | File Path | Thumbnail | Description | Category | Order | Visible |

**Column Details:**

- **Name**: Project name (for your reference)
- **Type**: Either `image` or `video`
- **File Path**: Path to the file (e.g., `images/push/jck1.png` or `images/haco/igstoryad.mp4`)
- **Thumbnail**: (Optional) For videos, path to thumbnail image
- **Description**: Alt text for images
- **Category**: Either `gallery` or `archive`
- **Order**: Number for sorting (1, 2, 3, etc.)
- **Visible**: `yes` or `no`

**Example Rows:**

| Name | Type | File Path | Thumbnail | Description | Category | Order | Visible |
|---|---|---|---|---|---|---|---|
| Push Campaign | image | images/push/jck1.png | | Push campaign visual | gallery | 1 | yes |
| Hoxton Ad | image | images/haco/hoxtonad.gif | | Hoxton advertisement | gallery | 2 | yes |
| Business Card | image | images/haco/business.png | | Business card design | gallery | 3 | yes |
| IG Story Ad | video | images/haco/igstoryad.mp4 | images/haco/igstoryad.png | Instagram story ad | gallery | 4 | yes |
| Gogo Video | video | images/haco/gogo.mp4 | images/haco/gogo.png | Gogo campaign | gallery | 5 | yes |

### Sheet 2: "Info"

For your info/about page content:

| A | B |
|---|---|
| Key | Value |
| Bio English | Yu Kakinoki is a billingual interdisciplinary designer, currently based in Tokyo... |
| Bio Japanese | 柿木優は、現在東京を拠点に活動している学際的なバイリンガルデザイナーです... |
| Contact Email | yukakinoki@gmail.com |
| Contact Text | contact |

**Note:** The bio text can be multiple paragraphs. Just put the entire text in the cell.

## Step 3: Make Sheet Public (Read-Only)

1. Click **Share** button (top right)
2. Click **Change to anyone with the link**
3. Set to **Viewer** (not Editor)
4. Copy the Sheet ID from the URL

   The URL looks like: `https://docs.google.com/spreadsheets/d/SHEET_ID_HERE/edit`
   
   Copy the `SHEET_ID_HERE` part

## Step 4: Get Google Sheets API Key

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or select existing)
3. Enable **Google Sheets API**:
   - Go to "APIs & Services" > "Library"
   - Search for "Google Sheets API"
   - Click "Enable"
4. Create API Key:
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "API Key"
   - Copy the API key
   - (Optional) Restrict the key to only Google Sheets API

## Step 5: Add Secrets to GitHub

1. Go to your GitHub repository
2. Click **Settings** > **Secrets and variables** > **Actions**
3. Click **New repository secret**
4. Add two secrets:
   - Name: `GOOGLE_SHEET_ID`, Value: (your sheet ID from step 3)
   - Name: `GOOGLE_API_KEY`, Value: (your API key from step 4)

## Step 6: Enable GitHub Actions

1. Go to your repository **Settings** > **Actions** > **General**
2. Under "Workflow permissions", select **Read and write permissions**
3. Click **Save**

## How to Use

### Update Your Site:

1. Edit the Google Sheet (add/remove/reorder projects)
2. Wait up to 6 hours for auto-update, OR
3. Go to GitHub > **Actions** > **Build Site from Google Sheets** > **Run workflow**

### Manually Trigger Build:

1. Go to your GitHub repository
2. Click **Actions** tab
3. Click **Build Site from Google Sheets** workflow
4. Click **Run workflow** button

The site will rebuild automatically and deploy to GitHub Pages!

## Testing

You can test locally before deploying:

```bash
export GOOGLE_SHEET_ID="your_sheet_id"
export GOOGLE_API_KEY="your_api_key"
python build_site.py
```

## Troubleshooting

- **Build fails**: Check the Actions tab for error messages
- **Sheet not found**: Verify Sheet ID and that sheet is publicly viewable
- **API errors**: Check that Google Sheets API is enabled and API key is correct
