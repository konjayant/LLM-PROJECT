
import os
import re
import gradio as gr
from google import genai

# Connect to Gemini
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("Gemini API key not found!")

client = genai.Client(api_key=API_KEY)

MODEL = "gemini-3.5-flash"


def generate_captions(description, platform):

    if not description or not description.strip():
        return "Please enter a description.", "", ""

    styles = {
        "Instagram": "Creative, catchy, friendly and use suitable emojis.",
        "LinkedIn": "Professional, informative and business-oriented.",
        "X (Twitter)": "Short, engaging and conversational. Maximum 280 characters per caption, including hashtags."
    }

    prompt = f"""
    You are an expert social media content creator.

    Description: {description}
    Platform: {platform}
    Writing style: {styles[platform]}

    Generate exactly 3 unique captions.

    Each caption must have relevant hashtags.
    Include 5 relevant hashtags per caption.
    For X, keep the complete caption and hashtags within 280 characters.

    Follow this exact format:

    CAPTION 1:
    Caption text

    HASHTAGS:
    #tag1 #tag2 #tag3 #tag4 #tag5

    CAPTION 2:
    Caption text

    HASHTAGS:
    #tag1 #tag2 #tag3 #tag4 #tag5

    CAPTION 3:
    Caption text

    HASHTAGS:
    #tag1 #tag2 #tag3 #tag4 #tag5
    """

    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=prompt
        )

        result = response.text or ""

        parts = re.split(
            r"CAPTION\s*[1-3]\s*:",
            result,
            flags=re.IGNORECASE
        )

        captions = [p.strip() for p in parts if p.strip()]

        if len(captions) != 3:
            return result, "", ""

        return captions[0], captions[1], captions[2]

    except Exception as e:
        return f"Generation failed: {e}", "", ""


with gr.Blocks(theme=gr.themes.Soft()) as app:

    gr.Markdown("""
    # Social Media Caption Generator

    ### Generate creative captions and hashtags using Generative AI.

    Save time and create engaging social media content!
    """)

    description = gr.Textbox(
        label="Enter Your Post Description",
        placeholder="Example: Launching a new clothing brand...",
        lines=4
    )

    platform = gr.Dropdown(
        choices=["Instagram", "LinkedIn", "X (Twitter)"],
        value="Instagram",
        label="Select Social Media Platform"
    )

    generate_button = gr.Button(
        "Generate Captions",
        variant="primary"
    )

    gr.Markdown("## Generated Captions")

    caption1 = gr.Textbox(label="Caption 1", lines=5)
    caption2 = gr.Textbox(label="Caption 2", lines=5)
    caption3 = gr.Textbox(label="Caption 3", lines=5)

    generate_button.click(
        fn=generate_captions,
        inputs=[description, platform],
        outputs=[caption1, caption2, caption3]
    )

    gr.Markdown("""
    ---
    Powered by Google Gemini AI | Python | Gradio
    """)


if __name__ == "__main__":
    app.launch()
