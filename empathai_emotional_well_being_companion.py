# -*- coding: utf-8 -*-
"""EmpathAI - Emotional Well-being Companion.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Jr6D3gPeGbyBzFOckAjoqcse47hSSENy
"""

# EmpathAI - Emotional Well-being Companion
# Compatible with older Gradio versions

import os
import numpy as np
import pandas as pd
import gradio as gr
import time
from datetime import datetime
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

# Install required packages if not already installed
try:
    import cv2
except ImportError:
    print("Installing required packages...")
    import sys
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install",
                          "opencv-python", "matplotlib"])
    import cv2

# Print Gradio version for debugging
import gradio as gr
print(f"Gradio version: {gr.__version__}")

# Global variables
session_history = []
user_name = "User"
current_mood = "neutral"
conversation_history = []

# ======== EMOTION DETECTION COMPONENTS ========

# Text-based emotion detection
def analyze_text_sentiment(text):
    """Analyze the emotion in text using a keyword-based approach"""
    emotion_keywords = {
        'happy': ['happy', 'joy', 'great', 'excellent', 'wonderful', 'glad', 'pleased', 'delighted', 'content'],
        'sad': ['sad', 'unhappy', 'depressed', 'down', 'blue', 'gloomy', 'miserable', 'upset'],
        'anxious': ['anxious', 'worried', 'nervous', 'tense', 'stressed', 'afraid', 'fearful', 'concerned'],
        'angry': ['angry', 'mad', 'furious', 'irritated', 'annoyed', 'frustrated', 'outraged'],
        'neutral': ['ok', 'fine', 'alright', 'neutral', 'normal', 'average'],
        'surprised': ['surprised', 'shocked', 'amazed', 'astonished', 'wow'],
        'upset': ['upset', 'troubled', 'disturbed', 'distressed', 'hurt']
    }

    # Count occurrences of emotion keywords
    text_lower = text.lower()
    emotion_counts = {emotion: 0 for emotion in emotion_keywords}

    for emotion, keywords in emotion_keywords.items():
        for keyword in keywords:
            if keyword in text_lower:
                emotion_counts[emotion] += 1

    # If no emotions detected, return neutral
    if sum(emotion_counts.values()) == 0:
        return "neutral", 1.0, {"neutral": 1.0}

    # Get the dominant emotion
    dominant_emotion = max(emotion_counts, key=emotion_counts.get)
    confidence = emotion_counts[dominant_emotion] / sum(emotion_counts.values())

    # Normalize the scores
    total = sum(emotion_counts.values())
    emotions = {emotion: count/total for emotion, count in emotion_counts.items()}

    return dominant_emotion, confidence, emotions

# Face detection
def detect_face_emotion(image):
    """Detect facial emotion from an image"""
    try:
        if image is None:
            return "neutral", None

        # Convert to grayscale for face detection
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)  # Use RGB2GRAY for Gradio

        # Load face detector
        face_cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        if not os.path.exists(face_cascade_path):
            print("Face cascade file not found, using backup method.")
            # Simulate a face in the center
            h, w = image.shape[:2]
            faces = [(w//4, h//4, w//2, h//2)]
        else:
            face_cascade = cv2.CascadeClassifier(face_cascade_path)
            faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        # Prepare a copy of the image for drawing
        output_image = image.copy()

        # If no face is detected, return neutral
        if len(faces) == 0:
            return "neutral", output_image

        # Mark the face on the image for visualization
        for (x, y, w, h) in faces:
            cv2.rectangle(output_image, (x, y), (x+w, y+h), (0, 255, 0), 2)
            # Add text label
            cv2.putText(output_image, "Face Detected", (x, y-10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        # Simulate emotion detection
        emotions = ["happy", "sad", "anxious", "neutral", "surprised"]
        detected_emotion = np.random.choice(emotions, p=[0.2, 0.2, 0.2, 0.3, 0.1])

        return detected_emotion, output_image

    except Exception as e:
        print(f"Error in face emotion detection: {e}")
        return "neutral", image if image is not None else None

# ======== GENERATIVE AI COMPANION ========

def initialize_chatbot():
    """Initialize the chatbot with response templates"""
    response_templates = {
        "happy": [
            "I'm glad you're feeling positive! What's been contributing to your good mood?",
            "It's wonderful to see you happy. Would you like to share what's bringing you joy?",
            "Your positive energy is great to see! How would you like to maintain this feeling?"
        ],
        "sad": [
            "I notice you seem down. Would you like to talk about what's on your mind?",
            "I'm here for you during difficult times. What's making you feel sad?",
            "Sometimes sharing what's troubling us can help. Is there something specific that's bothering you?"
        ],
        "anxious": [
            "I notice you might be feeling anxious. Would you like to try a quick breathing exercise?",
            "Anxiety can be challenging. Is there something specific that's causing you concern?",
            "I'm here to support you through anxious moments. What might help you feel calmer right now?"
        ],
        "angry": [
            "I sense you might be frustrated. Would you like to talk about what's bothering you?",
            "It's okay to feel anger sometimes. Is there a way I can help you process these feelings?",
            "When we're angry, it can help to take a step back. What might help you find some calm?"
        ],
        "neutral": [
            "How are you feeling today? I'm here to chat about whatever's on your mind.",
            "Is there something specific you'd like to talk about today?",
            "I'm here to support your emotional well-being. What would be helpful for you right now?"
        ],
        "surprised": [
            "You seem surprised! Did something unexpected happen?",
            "I notice a sense of surprise. What's on your mind?",
            "Sometimes surprises can be a lot to process. Would you like to talk about it?"
        ],
        "upset": [
            "I'm sorry to see you're upset. Would you like to talk about what happened?",
            "When we're upset, it can help to express our feelings. What's troubling you?",
            "I'm here to listen if you want to share what's making you feel this way."
        ]
    }

    return response_templates

def generate_companion_response(user_input, emotion, conversation_history):
    """Generate an empathetic response based on user input and detected emotion"""
    try:
        # Get the response templates
        response_templates = initialize_chatbot()

        # Basic conversation logic
        lower_input = user_input.lower()

        # Check for greetings
        if any(greeting in lower_input for greeting in ["hello", "hi", "hey", "greetings"]):
            return "Hello! I'm EmpathAI, your emotional well-being companion. How are you feeling today?"

        # Check for goodbyes
        if any(goodbye in lower_input for goodbye in ["bye", "goodbye", "see you", "talk later"]):
            return "Take care! Remember I'm here whenever you need someone to talk to."

        # Check for gratitude
        if any(thanks in lower_input for thanks in ["thanks", "thank you", "appreciate"]):
            return "You're welcome! I'm glad I could help. Is there anything else on your mind?"

        # Check for direct questions about what EmpathAI is
        if "what are you" in lower_input or "who are you" in lower_input:
            return "I'm EmpathAI, an emotional well-being companion designed to provide support, listen to your concerns, and help you navigate your feelings."

        # Check for help requests
        if "help" in lower_input or "can you help" in lower_input:
            return "I'd be happy to help. I can listen, offer support, or guide you through simple mindfulness exercises. What would be most helpful right now?"

        # For emotion-specific responses
        if emotion in response_templates:
            responses = response_templates[emotion]
            return np.random.choice(responses)

        # Default response if no specific condition is met
        default_responses = [
            "I'm here to listen. Would you like to tell me more?",
            "That's interesting. How does that make you feel?",
            "I appreciate you sharing that with me. Would you like to explore this further?",
            "I'm here to support you. What would be helpful for you right now?"
        ]
        return np.random.choice(default_responses)

    except Exception as e:
        print(f"Error generating response: {e}")
        return "I'm here to listen. Would you like to tell me more about how you're feeling?"

# ======== WELL-BEING SUGGESTIONS ========

def get_wellbeing_activities(emotion):
    """Suggest wellbeing activities based on the detected emotion"""
    activity_suggestions = {
        "sad": [
            "Take a short walk outside to change your surroundings.",
            "Listen to uplifting music that you enjoy.",
            "Call or message a friend who makes you laugh.",
            "Write down three things you're grateful for, no matter how small.",
            "Do a simple stretching routine to release physical tension."
        ],
        "anxious": [
            "Try this breathing exercise: breathe in for 4 counts, hold for 7, exhale for 8.",
            "Ground yourself by naming 5 things you can see, 4 you can touch, 3 you can hear, 2 you can smell, and 1 you can taste.",
            "Visualize a peaceful place where you feel safe and calm.",
            "Do a quick body scan meditation to release tension.",
            "Write down your worries, then note what's in your control and what isn't."
        ],
        "angry": [
            "Try physical activity to release tension - even a quick set of jumping jacks can help.",
            "Step away from the situation for a 10-minute break if possible.",
            "Practice deep, slow breathing while counting to 10.",
            "Write down what's upsetting you without censoring yourself.",
            "Visualize your anger as a wave that gradually subsides."
        ],
        "happy": [
            "Savor this positive moment by really being present in it.",
            "Share your happiness with someone else through a kind message.",
            "Note this good feeling in a happiness journal to revisit later.",
            "Channel your positive energy into a creative activity you enjoy.",
            "Practice gratitude by acknowledging what's contributing to your happiness."
        ],
        "neutral": [
            "Try a short mindfulness practice to check in with how you're feeling.",
            "Consider setting an intention for the rest of your day.",
            "Take a moment to stretch and check in with your body.",
            "Reflect on what would bring you joy or fulfillment right now.",
            "Practice a random act of kindness for someone else or yourself."
        ],
        "surprised": [
            "Take a moment to breathe and process what's happening.",
            "Write down your thoughts to help organize them.",
            "Consider talking through the surprise with someone you trust.",
            "Give yourself permission to take time to adjust.",
            "Practice acceptance of unexpected changes."
        ],
        "upset": [
            "Give yourself permission to feel your emotions without judgment.",
            "Try gentle self-compassion: what would you say to a friend feeling this way?",
            "Use physical comfort: wrap yourself in a blanket or hug a pillow.",
            "Make yourself a soothing drink like tea or warm water with lemon.",
            "Try a gentle distraction like a nature documentary or peaceful music."
        ]
    }

    if emotion in activity_suggestions:
        # Return 3 random suggestions for the detected emotion
        suggestions = np.random.choice(activity_suggestions[emotion],
                                      size=min(3, len(activity_suggestions[emotion])),
                                      replace=False)
        return suggestions
    else:
        # Default suggestions
        default_suggestions = [
            "Take a few deep breaths and check in with yourself.",
            "Drink a glass of water to stay hydrated.",
            "Stretch for a moment to release physical tension."
        ]
        return default_suggestions

# ======== TRACKING & VISUALIZATION ========

def track_mood(emotion, timestamp):
    """Track mood over time"""
    global session_history
    session_history.append({
        "timestamp": timestamp,
        "emotion": emotion
    })
    return session_history

def generate_mood_chart():
    """Generate a visualization of mood over the session"""
    global session_history

    if len(session_history) < 2:
        # Not enough data for meaningful visualization
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.text(0.5, 0.5, "Not enough mood data to generate chart.\nContinue interacting to track your emotions.",
                horizontalalignment='center', verticalalignment='center')
        ax.axis('off')
        return fig

    # Extract data
    emotions = [entry["emotion"] for entry in session_history]
    timestamps = [entry["timestamp"] for entry in session_history]

    # Create a numeric mapping for emotions for visualization
    emotion_map = {
        "happy": 5,
        "surprised": 4,
        "neutral": 3,
        "anxious": 2,
        "upset": 1.5,
        "angry": 1,
        "sad": 0
    }

    # Convert emotions to numeric values
    numeric_emotions = [emotion_map.get(e, 3) for e in emotions]  # Default to neutral (3) if not found

    # Calculate elapsed minutes for better visualization
    start_time = timestamps[0]
    elapsed_times = [(t - start_time).total_seconds() / 60 for t in timestamps]

    # Create the chart
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(elapsed_times, numeric_emotions, 'o-', markersize=8)

    # Set the y-ticks to match our emotion map
    ax.set_yticks(list(emotion_map.values()))
    ax.set_yticklabels(list(emotion_map.keys()))

    # Labels and title
    ax.set_xlabel('Time Elapsed (minutes)')
    ax.set_ylabel('Emotional State')
    ax.set_title('Your Emotional Journey During This Session')

    # Add a grid for readability
    ax.grid(True, linestyle='--', alpha=0.7)

    return fig

# ======== GRADIO INTERFACE FUNCTIONS ========

# Global variables for the Gradio interface
detected_emotions = []
messages = []

def reset_conversation():
    """Reset the conversation history"""
    global conversation_history, detected_emotions, messages, session_history
    conversation_history = []
    detected_emotions = []
    messages = []
    session_history = []
    return "", None, []

def webcam_capture(image):
    """Process webcam capture"""
    if image is None:
        return None, "neutral"

    emotion, processed_image = detect_face_emotion(image)
    return processed_image, emotion

def chat_response(message, image, history):
    """Main function to handle chat responses"""
    global current_mood, conversation_history

    # Skip empty messages
    if not message or message.strip() == "":
        return "", history

    # Add user message to conversation history
    conversation_history.append({"role": "user", "content": message})

    # Analyze text sentiment
    text_emotion, confidence, emotion_scores = analyze_text_sentiment(message)

    # If webcam image is available, use it for emotion detection
    if image is not None:
        processed_image, visual_emotion = webcam_capture(image)
        # Combine text and visual emotions - prioritize visual if available
        current_mood = visual_emotion if visual_emotion != "neutral" else text_emotion
    else:
        current_mood = text_emotion

    # Track the mood
    track_mood(current_mood, datetime.now())

    # Generate AI response
    ai_response = generate_companion_response(message, current_mood, conversation_history)

    # Add AI response to conversation history
    conversation_history.append({"role": "assistant", "content": ai_response})

    # Return for Gradio
    history = history + [(message, ai_response)]
    return "", history

def get_suggestions():
    """Get activity suggestions based on current mood"""
    global current_mood
    suggestions = get_wellbeing_activities(current_mood)
    return "\n• " + "\n• ".join(suggestions)

def update_mood_display():
    """Update the mood display"""
    global current_mood
    mood_emoji = {
        "happy": "😊 Happy",
        "sad": "😢 Sad",
        "anxious": "😰 Anxious",
        "angry": "😠 Angry",
        "neutral": "😐 Neutral",
        "surprised": "😮 Surprised",
        "upset": "😟 Upset"
    }
    return mood_emoji.get(current_mood, "😐 Neutral")

# ======== MAIN APPLICATION ========

def main():
    """Main function to run the Gradio interface"""
    # Define the block-based interface
    with gr.Blocks(theme=gr.themes.Soft()) as demo:
        gr.Markdown("# 🌟 EmpathAI - Emotional Well-being Companion")
        gr.Markdown("Talk to me about how you're feeling, and I'll provide empathetic support.")

        with gr.Row():
            # Left column - Main chat interface
            with gr.Column(scale=2):
                chatbot = gr.Chatbot(height=400, label="Conversation")

                with gr.Row():
                    msg = gr.Textbox(
                        placeholder="Type your message here...",
                        show_label=False,
                        lines=2
                    )
                    submit_btn = gr.Button("Send", variant="primary")

                clear_btn = gr.Button("Reset Conversation")

            # Right column - Emotion detection and well-being suggestions
            with gr.Column(scale=1):
                # Remove the webcam input since it's causing issues
                # We'll just use text-based emotion detection

                # Current mood display
                mood_display = gr.Textbox(label="Current Mood", value="😐 Neutral", interactive=False)

                # Well-being suggestions
                suggestion_box = gr.Textbox(label="Well-being Suggestions",
                                           value="• Take a few deep breaths\n• Stay hydrated\n• Stretch for a moment",
                                           interactive=False)

                get_suggestions_btn = gr.Button("Get Suggestions")

                # Mood chart
                mood_chart_btn = gr.Button("View Your Emotion Journey")
                mood_chart = gr.Plot(label="Emotion Over Time")

        # Set up event handlers - modify to work without webcam
        submit_btn.click(
            lambda message, history: chat_response(message, None, history),
            inputs=[msg, chatbot],
            outputs=[msg, chatbot]
        ).then(
            update_mood_display,
            outputs=[mood_display]
        )

        msg.submit(
            lambda message, history: chat_response(message, None, history),
            inputs=[msg, chatbot],
            outputs=[msg, chatbot]
        ).then(
            update_mood_display,
            outputs=[mood_display]
        )

        get_suggestions_btn.click(
            get_suggestions,
            outputs=[suggestion_box]
        )

        mood_chart_btn.click(
            generate_mood_chart,
            outputs=[mood_chart]
        )

        clear_btn.click(
            lambda: reset_conversation()[0:2] + [[]], # Modify to return just what's needed
            outputs=[msg, chatbot]
        )

        # Example conversation starters
        gr.Examples(
            [
                ["I'm feeling really anxious about a presentation tomorrow."],
                ["I had a great day today! Everything went so well!"],
                ["I'm feeling a bit down and don't know why."],
                ["I got into an argument with my friend and I'm upset."],
                ["I'm not sure how I'm feeling today."]
            ],
            inputs=[msg]
        )

    # Launch the interface
    demo.launch()

if __name__ == "__main__":
    main()