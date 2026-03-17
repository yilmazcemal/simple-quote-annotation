# Quote Extraction Labeler

A lightweight, browser-based annotation tool for extracting and classifying communicative acts from news articles. Runs entirely from a single `labeler.html` file — no installation, no server, no data leaves your machine.

## Features

- **Zero Setup**: Open `labeler.html` directly in your browser. No dependencies, no build step.
- **Three Speech Types**: Classify each communicative act as **Direct Quote**, **Indirect Speech**, or **Paraphrase** (attributed acts like *threatened*, *demanded*, *refused* that are neither verbatim nor indirect).
- **Color-Coded Highlights**: Article text is highlighted by speech type — green (direct), orange (indirect), purple (paraphrase) — with blue dashed underlines marking unlabeled candidates (quoted text and speech verbs).
- **Gemini AI Integration**: Select any text, right-click, and use *Analyze with Gemini* to auto-fill speaker name, organization, role, speech type, and event context. Supports up to 4 API keys with automatic round-robin rotation for free-tier rate limits.
- **Speaker Popup**: Dedicated draggable popup for setting speaker metadata (name, role, organization) with N/A toggles.
- **Article-Scoped Autofill**: Autocomplete suggestions for speaker fields draw only from the current article's blocks, not the entire dataset.
- **Dynamic Translation**: Translate articles to English on-the-fly with sentence-level synchronized hover highlighting.
- **Privacy First**: API keys are stored in browser `localStorage` only. Nothing is sent to any server except directly to Google's Gemini API.
- **Import / Export**: Save and resume labeling progress as JSON at any time.

## Data Format

Each article in your JSON batch should have the following structure:

```json
{
  "article_id": "unique_id",
  "crawl_date": "...",
  "url": "...",
  "domain": "...",
  "content": "Full article text..."
}
```

### Preparing Data from CSV

If your source data is a CSV (e.g. from a Wayback Machine export), use `preprocess.py` to generate JSON batches:

```bash
python preprocess.py "your_data.csv" --batch-size 500 --output-dir batches
```

Required CSV columns: `crawl_date`, `url`, `last_modified_date`, `domain`, `mime_type_web_server`, `language`, `content`.

This creates a `batches/` folder of chunked JSON files ready to load into the labeler.

## Getting Started

### 1. Configure Gemini (optional but recommended)

1. Click **⚙️ Settings** in the top left.
2. Enter up to 4 Gemini API keys.
3. Select a model (e.g. `gemini-2.0-flash`).
4. Click **Save Settings**.

### 2. Load a Batch

Click **📂 Load Batch JSON** and select a file from your `batches/` folder (or any conforming JSON).

### 3. Label Articles

For each article:

1. **Select text** in the article body to open the context menu.
2. Choose **New Quote** to manually classify the selection, or **✨ Analyze with Gemini** to auto-fill all fields.
3. In the *New Quote* flow, pick the speech type — Direct Quote, Indirect Speech, or Paraphrase.
4. Use **Set Speaker** (or the speaker popup) to fill in name, role, and organization.
5. Add optional **Event Context** and **Reasoning** notes.
6. Use the article status buttons (**Labeled / Skipped**) to track progress.

Optionally, click **🌐 Translate** to load an English translation alongside the original, with sentence-level hover alignment.

### 4. Export

Click **💾 Export Labels** to download your annotations as `labeled_articles.json`.

## Output Schema

```json
{
  "article_id": {
    "status": "labeled | skipped | unlabeled",
    "reasoning": "Annotator notes",
    "quote_blocks": [
      {
        "quote_block_id": 1,
        "speaker_name": "string",
        "speaker_organization": "string or null",
        "speaker_role": "string or null",
        "quote_text": "string",
        "speech_type": "direct_quote | indirect_speech | paraphrase",
        "event_context": "string or null"
      }
    ]
  }
}
```

## Notes

- The `.gitignore` excludes dataset CSVs, the `batches/` directory, and `.env` files.
- The tool is optimized for Turkish-language news articles (speech verb detection, translation) but works for any language for manual annotation.
