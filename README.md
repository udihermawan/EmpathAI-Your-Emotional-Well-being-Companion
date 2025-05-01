# EmpathAI - Emotional Well-being Companion Using Multimodal AI 

> **"Where AI Meets Heart: Healing Isolation, One Conversation at a Time."**

EmpathAI is a groundbreaking AI-powered emotional well-being companion, designed to combat loneliness, social isolation, and mental health struggles. By integrating Generative AI, Computer Vision, NLP, and Hugging Face models, EmpathAI provides personalized emotional support, fosters human connections, and promotes mental resilience — while respecting privacy and cultural diversity.

---

## 🌟 Key Features

- **Emotion Detection & Mood Analysis**
  - 🎭 Real-time facial expression recognition (OpenCV + MediaPipe)
  - 🎤 Voice sentiment analysis (Wav2Vec2 by Hugging Face)
  - 📝 Text-based mood assessment (Fine-tuned BERT)

- **Generative AI Companion**
  - 💬 Personalized conversations based on CBT and mindfulness techniques (GPT-4)
  - 📖 Dynamic storytelling for emotional soothing
  - 🎨 Art & Music therapy (Stable Diffusion, MusicGen)

- **Community Connection**
  - 🤝 Safe peer-matching platform based on shared experiences
  - 🕊️ AI-moderated group discussions for conflict mediation

- **Proactive Mental Health Support**
  - 🚨 Crisis detection and emergency contact alerts
  - 🧘‍♀️ AI-guided self-care journeys with custom routines

- **Cultural Sensitivity & Accessibility**
  - 🌍 Multilingual support (100+ languages via Hugging Face’s NLLB)
  - ✋ Sign language and gesture recognition for non-verbal users

---

## 🛠️ Tech Stack

- **Backend:** Python, FastAPI, Hugging Face Transformers, PyTorch
- **Mobile App:** React Native + TensorFlow Lite (on-device models)
- **Computer Vision:** OpenCV, MediaPipe, Vision Transformer (ViT)
- **Generative AI:** GPT-4, Stable Diffusion, Meta’s MusicGen
- **NLP:** SpaCy, BERT, GPT-3.5 Turbo
- **Database:** Supabase (anonymized secure data storage)
- **Analytics Dashboard:** Tableau

---

## 🚀 How to Run Locally

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/EmpathAI.git
cd EmpathAI

2. Backend Setup
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload

3. Mobile App Setup
cd mobile
npm install
npm start

Ensure you have Expo CLI installed for React Native development.

4. Environment Variables
Create a .env file in the backend folder and add:

HUGGINGFACE_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key


📈 Impact Goals
🌍 By 2025, EmpathAI aims to provide 1 Million people a sense of belonging and emotional resilience.
🧡 Because loneliness isn't just a feeling — it's a silent pandemic we can heal together.

🤝 Partnerships
WHO Mental Health Initiatives
Crisis Text Line Integration

🧠 Ethical AI Principles
Privacy-first: All facial and voice data processed locally.
Culturally Inclusive: Supports non-Western mental health practices (e.g., Ubuntu philosophy, Ayurveda).
Empathy-driven: Designed to enhance, not replace, real human connection.

.

📝 License
This project is licensed under the MIT License.
📬 Contact
Name: Sudarshanam Yessasvini
Email: yessasvini.s@gmail.com
LinkedIn: www.linkedin.com/in/sudarshanam-yessasvini-358a72287



