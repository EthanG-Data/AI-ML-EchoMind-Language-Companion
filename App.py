import streamlit as st
from transformers import pipeline
from langdetect import detect, DetectorFactory
import torch

# ---------- Config ----------
DetectorFactory.seed = 0
st.set_page_config(page_title="EchoMind - Where Emotions Shape Words", page_icon="🤖", layout="centered")

DEVICE = 0 if torch.cuda.is_available() else -1

# ---------- Pipelines ----------
@st.cache_resource
def get_pipelines():
    sentiment_analyzer = pipeline( "sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment-latest", tokenizer="cardiffnlp/twitter-roberta-base-sentiment-latest", device=DEVICE
    )
    t5_ckpt= "google/flan-t5-base"
    text_generator = pipeline( task="text2text-generation", model=t5_ckpt, tokenizer=t5_ckpt, device=DEVICE
    )
    return sentiment_analyzer, text_generator

# ---------- Utils ----------
def normalize_3way(label: str) -> str:
    s = label.lower()
    if "neg" in s or s.endswith("_0"):
        return "negative"
    if "neu" in s or s.endswith("_1"):
        return "neutral"
    return "positive"

def detect_language(text: str) -> str:
    try:
        return detect(text)  
    except Exception:
        return "unknown"


def build_prompt(user_prompt: str, sentiment: str) -> str:
    tone = {
        "positive": "Write a warm, optimistic paragraph like a supportive friend.",
        "neutral":  "Write a balanced, calm, factual paragraph.",
        "negative": "Write an empathetic paragraph that acknowledges concerns and offers reassurance.",
    }.get(sentiment, "Write a clear, helpful paragraph.")

    return (
        f"{tone} Keep it cohesive (4–6 sentences). "
        f"Do not quote or repeat the user's wording verbatim. "
        f"Acknowledge what they said, add something helpful, and end with one open-ended question. "
        f"User message: {user_prompt.strip()}"
    )

# ---------- UI ----------

st.title("🤖 EchoMind the Friendly AI")
st.write("Welcome to EchoMind! Share your thoughts, everyone needs someone to hear them out.")

with st.form("gen"):
    user_prompt = st.text_area( "Your Thoughts:", height=160, placeholder="e.g., Tell me How you're feeling")
    c1, c2 = st.columns(2)
    with c1:
        length = st.slider("How Long Do You Want the Response to Be?", 40, 150, 90, step=10)
    with c2:
        temp = st.slider("How Creative Should I Be?", 0.0, 1.5, 0.7, step=0.1)
    go = st.form_submit_button("Generate")

if go:
    if not user_prompt.strip():
        st.warning("Please enter a prompt.")
        st.stop()

    with st.spinner("Thinking..."):
        sentiment_analyzer, text_generator = get_pipelines()

    lang = detect_language(user_prompt)


    res = sentiment_analyzer(user_prompt[:256])[0]
    sentiment = normalize_3way(res["label"])

    lang_display = (lang.upper() if lang != "unknown" else "UNKNOWN")
    st.info(f" Sentiment: **{sentiment.capitalize()}**")

    full_prompt = build_prompt(user_prompt, sentiment)

    with st.spinner("Thinking deeper..."):
        try:
            target_words = int(length)
            max_new_tokens= int(target_words * 1.5)
            min_new_tokens= int(target_words * 0.5)
            
            result = text_generator(
                full_prompt,
                max_new_tokens=max_new_tokens,
                min_new_tokens=min_new_tokens,
                do_sample=True,
                no_repeat_ngram_size=3,
                encoder_no_repeat_ngram_size=3,
                repetition_penalty=1.1,
                early_stopping=True
            )[0]["generated_text"].strip()
        except Exception as e:
            st.error(f"Generation error: {e}")
            st.stop()

    out = result
    st.write(out)

    st.session_state.last_run = { "user_prompt": user_prompt, "detected": sentiment, "length": length, "temp": temp, "lang": lang }

# ---------- Tone correction / regeneration ----------
if "last_run" in st.session_state:
    with st.expander("Did I say the wrong thing? Fix my tone!"):
        desired = st.selectbox(
            "Choose how you think I should've responded:",
            ["positive", "neutral", "negative"],
            index=["positive", "neutral", "negative"].index(st.session_state["last_run"]["detected"])
        )
        if st.button("Let me think deeper about it"):
            _, text_generator = get_pipelines()
            reprompt = build_prompt(st.session_state["last_run"]["user_prompt"], desired)
            with st.spinner("Rethinking…"):
                try:
                    result2 = text_generator(
                        reprompt,
                        max_new_tokens=st.session_state["last_run"]["length"],
                        do_sample=True,
                        temperature=st.session_state["last_run"]["temp"],
                        pad_token_id=text_generator.tokenizer.eos_token_id
                    )[0]["generated_text"]
                    
                    # Extract only the response part
                    if "### Response" in result2:
                        out2 = result2.split("### Response")[-1].strip()
                    else:
                        out2 = result2.strip()
                        
                except Exception as e:
                    st.error(f"Generation error: {e}")
                else:
                    st.success(f"Regenerated with tone: **{desired.capitalize()}**")
                    st.write(out2)
