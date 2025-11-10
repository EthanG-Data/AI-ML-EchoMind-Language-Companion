# 🤖 EchoMind - Where Emotions Shape Words

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://streamlit.io)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

EchoMind is an intelligent AI companion that analyzes your emotions and responds with empathy. Share your thoughts, and EchoMind will listen, understand your sentiment, and provide thoughtful responses tailored to your emotional state.

## ✨ Features

- **🎭 Sentiment Analysis**: Automatically detects emotional tone (positive, neutral, negative) using state-of-the-art NLP models
- **🗣️ Language Detection**: Identifies the language of your input for better understanding
- **🤝 Empathetic Responses**: Generates contextually appropriate responses based on detected sentiment
- **🎨 Customizable Output**: Control response length and creativity levels
- **🔄 Tone Correction**: Regenerate responses with a different emotional approach
- **⚡ Real-time Processing**: Fast inference using optimized transformer models

*EchoMind analyzing sentiment and generating an empathetic response*

## 🛠️ Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/echomind-sentiment-ai.git
   cd echomind-sentiment-ai
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run App.py
   ```

4. **Open your browser**
   - The app will automatically open at `http://localhost:8501`
   - If it doesn't open automatically, navigate to the URL shown in your terminal

## 📦 Dependencies

Create a `requirements.txt` file with these dependencies:

```txt
streamlit>=1.28.0
transformers>=4.30.0
torch>=2.0.0
langdetect>=1.0.9
sentencepiece>=0.1.99
```

## 🎯 How It Works

### 1. Sentiment Analysis
EchoMind uses the **CardiffNLP Twitter RoBERTa** model to analyze the emotional content of your input:
- **Positive**: Optimistic, happy, encouraging content
- **Neutral**: Balanced, factual, objective content  
- **Negative**: Concerned, sad, or distressed content

### 2. Response Generation
Using **Google's FLAN-T5** model, EchoMind generates responses that:
- Match your emotional state
- Provide supportive and helpful content
- Ask engaging follow-up questions
- Maintain conversational flow

### 3. Tone Adjustment
If the initial response doesn't feel right, you can:
- Select a different emotional tone
- Regenerate the response instantly
- Compare different approaches

## 🎮 Usage

1. **Share Your Thoughts**: Type anything you're feeling or thinking about
2. **Customize Settings**: 
   - Adjust response length (40-150 words)
   - Control creativity level (0.0-1.5)
3. **Generate Response**: Click "Generate" to get an empathetic reply
4. **Fine-tune**: Use the tone correction feature if needed

### Example Interactions

**Input**: "I'm feeling overwhelmed with work lately"
- **Detected Sentiment**: Negative
- **Response**: *An empathetic paragraph acknowledging stress and offering support*

**Input**: "Just got a promotion at work!"
- **Detected Sentiment**: Positive  
- **Response**: *A celebratory and encouraging response*

## ⚙️ Technical Details

### Models Used
- **Sentiment Analysis**: `cardiffnlp/twitter-roberta-base-sentiment-latest`
- **Text Generation**: `google/flan-t5-base`
- **Language Detection**: `langdetect` library

### Hardware Support
- **GPU**: Automatically detects and uses CUDA if available
- **CPU**: Falls back to CPU processing for compatibility

### Performance Features
- **Caching**: Models are cached using `@st.cache_resource` for faster subsequent runs
- **Optimized Generation**: Uses repetition penalties for higher quality output
- **Memory Efficient**: Truncates long inputs to prevent memory issues

## 🔧 Configuration

### Model Settings
You can modify the models in the `get_pipelines()` function:

```python
# For different sentiment analysis models
sentiment_analyzer = pipeline(
    "sentiment-analysis", 
    model="your-preferred-model",
    device=DEVICE
)

# For different text generation models
text_generator = pipeline(
    "text2text-generation", 
    model="your-preferred-model",
    device=DEVICE
)
```

### UI Customization
Modify the Streamlit interface in the UI section:
- Change sliders ranges
- Adjust text areas
- Customize page layout

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/AmazingFeature`)
3. **Commit your changes** (`git commit -m 'Add some AmazingFeature'`)
4. **Push to the branch** (`git push origin feature/AmazingFeature`)
5. **Open a Pull Request**

### Ideas for Contributions
- 🌍 Multi-language support
- 📱 Mobile-responsive design
- 📊 Conversation history tracking
- 🎨 Custom themes and styling
- 🔍 Advanced sentiment categories
- 💾 Export conversation logs

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


## 🚨 Disclaimer

EchoMind is designed for supportive conversation and emotional reflection. It is not a replacement for professional mental health services. If you're experiencing serious emotional distress, please consult with qualified mental health professionals.

---

*EchoMind - Because everyone needs someone to listen.*
