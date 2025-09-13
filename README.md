# AI Whiteboard Summarizer

An intelligent web application that takes photos of classroom whiteboards and automatically extracts text to create organized, summarized notes using AI.

## Features

- 📸 **Image Upload**: Drag & drop or click to upload whiteboard photos
- 🔍 **OCR Text Extraction**: Advanced image preprocessing and OCR using Tesseract
- 🤖 **AI Summarization**: Intelligent text summarization using OpenAI GPT
- 📱 **Responsive Design**: Works on desktop and mobile devices
- 💾 **Export Options**: Copy to clipboard or download results
- 🎨 **Modern UI**: Clean, intuitive interface with beautiful animations

## How It Works

1. **Upload**: Take a photo of your classroom whiteboard and upload it
2. **Process**: The system preprocesses the image for better OCR results
3. **Extract**: Advanced OCR extracts all text from the whiteboard
4. **Summarize**: AI analyzes and summarizes the content into organized notes
5. **Export**: Copy or download the results for your study materials

## Installation

### Prerequisites

- Python 3.8 or higher
- Tesseract OCR installed on your system
- OpenAI API key

### Setup

1. **Clone or download this project**
   ```bash
   git clone <repository-url>
   cd WhiteBoard
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Tesseract OCR**
   
   **Windows:**
   - Download from: https://github.com/UB-Mannheim/tesseract/wiki
   - Add to PATH or set TESSERACT_CMD in your environment
   
   **macOS:**
   ```bash
   brew install tesseract
   ```
   
   **Linux (Ubuntu/Debian):**
   ```bash
   sudo apt-get install tesseract-ocr
   ```

4. **Set up OpenAI API key**
   - Copy `env_example.txt` to `.env`
   - Get your API key from: https://platform.openai.com/api-keys
   - Add your API key to the `.env` file:
     ```
     OPENAI_API_KEY=your_actual_api_key_here
     ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Open your browser**
   - Navigate to: http://localhost:5000
   - Start uploading whiteboard photos!

## Usage

1. **Take a clear photo** of your classroom whiteboard
2. **Upload the image** by dragging and dropping or clicking "Choose Photo"
3. **Wait for processing** - the system will extract text and generate a summary
4. **Review the results** - see both the extracted text and AI summary
5. **Export as needed** - copy to clipboard or download as a text file

## Tips for Best Results

- **Good lighting**: Ensure the whiteboard is well-lit
- **Clear handwriting**: The clearer the text, the better the extraction
- **High resolution**: Use a good camera for better image quality
- **Straight angle**: Try to photograph the whiteboard straight-on
- **Contrast**: Ensure good contrast between text and background

## Technical Details

### Image Processing Pipeline
1. **Preprocessing**: Grayscale conversion, noise reduction, adaptive thresholding
2. **OCR Configuration**: Optimized settings for educational content
3. **Text Cleaning**: Filtering and formatting extracted text
4. **AI Analysis**: Context-aware summarization using GPT-3.5-turbo

### Supported Formats
- **Image formats**: JPEG, PNG, GIF, BMP, TIFF
- **File size**: Up to 16MB
- **Languages**: English (can be extended for other languages)

## API Endpoints

- `GET /` - Main application interface
- `POST /upload` - Upload and process whiteboard images
- `GET /health` - Health check endpoint

## Configuration

### Environment Variables
- `OPENAI_API_KEY` - Your OpenAI API key (required)
- `TESSERACT_CMD` - Path to Tesseract executable (optional)

### Customization
- Modify OCR settings in `app.py` for different languages or accuracy
- Adjust AI prompt in `summarize_text()` function for different summary styles
- Customize UI styling in `templates/index.html`

## Troubleshooting

### Common Issues

1. **"Tesseract not found" error**
   - Ensure Tesseract is installed and in your system PATH
   - Or set the `TESSERACT_CMD` environment variable

2. **Poor text extraction**
   - Try better lighting or image quality
   - Ensure text is clearly visible and not too small

3. **OpenAI API errors**
   - Verify your API key is correct and has sufficient credits
   - Check your internet connection

4. **Large file uploads**
   - The system supports up to 16MB files
   - For larger files, compress the image before uploading

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve this application!

## License

This project is open source and available under the MIT License.

## Support

If you encounter any issues or have questions, please create an issue in the repository or contact the development team.
