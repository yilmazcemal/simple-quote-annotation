# Quote Extraction Labeler

A lightweight, local, browser-based tool for labeling and extracting political quotes from large datasets, powered by the Gemini API.

## Features
- **Client-Side Only**: Runs entirely in your browser via a single `labeler.html` file. 
- **Lightning Fast Preprocessing**: Convert massive CSV datasets into chunked JSON batches using `preprocess.py`.
- **Gemini AI Integration**: Highlight text and instantly extract speaker name, party, role, quote type, and event context using Gemini Flash models.
- **Dynamic Translation**: Translate original texts to English on-the-fly, with sentence-level synchronized hover highlighting.
- **Privacy First**: API keys are securely stored in your browser's `localStorage` and NEVER sent to a server (other than directly to Google's API). 
- **Import/Export**: Easily save your labeling progress as JSON and load it back later.

## Getting Started

### 1. Data Preparation
The tool expects data to be broken down into JSON batches. 

If you have a CSV file (e.g., from a Wayback Machine export), it must contain the following columns (see `template_data.csv` for an example):
* `crawl_date`
* `url`
* `last_modified_date`
* `domain`
* `mime_type_web_server`
* `language`
* `content`

Run the preprocessor to generate your batches:
```bash
python preprocess.py "your_data.csv" --batch-size 500 --output-dir batches
```
This will create a `batches/` folder containing your chunked JSON files which can be safely ignored in Git.

### 2. Running the Labeler
Because the tool is a static HTML file, you only need to run a local web server to avoid CORS issues when loading local files, or you can just open the file directly in your browser.

```bash
# Optional: run a simple local server
python -m http.server 8000
```
Then visit `http://localhost:8000/labeler.html`. (Or just double click `labeler.html`!)

### 3. Setup Gemini API
1. Click the **⚙️ Settings** button in the top left.
2. Enter up to 4 Gemini API keys. The app will automatically round-robin through them to help manage free-tier rate limits!
3. Select your preferred model (e.g. `gemini-2.0-flash`).
4. Click **Save Settings**. (Your keys are saved safely to your local browser storage).

## Usage
1. Click **📂 Load Batch JSON** and select one of the JSON files from your `batches/` folder.
2. **Translate** (Optional): Click the **🌐 Translate** button to fetch an English translation. The UI will split into a 2x2 grid, allowing you to hover over sentences to see their exact alignment.
3. **Analyze**: Highlight any text in the article. A sparkling "✨ Analyze Quote with Gemini" button will appear. Click it, and Gemini will automatically extract the entities and fill out the Quote Blocks on the right.
4. **Export**: When finished with a batch, click **💾 Export Labels** to save your work!

## Contributing & Git
The `.gitignore` is already configured to ignore your dataset CSVs, your generated `batches/` directory, and any `.env` files. Your API keys are safe.
