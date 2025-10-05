import re
import streamlit as st

class ContentFilter:
    """Content filtering system to handle sensitive content and ensure positive responses"""
    
    def __init__(self):
        # Sensitive words that should be filtered or transformed
        self.sensitive_patterns = [
            # Self-harm related
            r'\b(kill|suicide|die|death|hurt|harm|cut|blade|razor)\s+(myself|self|me)\b',
            r'\b(want\s+to\s+die|end\s+it\s+all|kill\s+myself)\b',
            r'\b(self\s+harm|self\s+injury|cutting)\b',
            
            # Violence related
            r'\b(kill|murder|hurt|harm)\s+(someone|others|people)\b',
            r'\b(violence|violent|attack|assault)\b',
            
            # Explicit content
            r'\b(hate|angry|furious)\s+(everyone|everything|world)\b',
            r'\b(fuck|shit|damn|bastard|bitch)\b',
            
            # Drug/substance abuse
            r'\b(drugs|cocaine|heroin|meth|overdose)\b',
        ]
        
        # Positive transformation phrases
        self.positive_transformations = {
            'hate': 'feel frustrated with',
            'angry': 'feeling upset about',
            'furious': 'very frustrated with',
            'terrible': 'challenging',
            'awful': 'difficult',
            'horrible': 'tough',
            'worst': 'most challenging',
            'failure': 'learning experience',
            'stupid': 'confused',
            'worthless': 'undervalued',
            'hopeless': 'looking for hope',
            'useless': 'feeling uncertain about my purpose'
        }
        
        # Emotion keywords for contextual responses
        self.emotion_keywords = {
            'stress': ['stress', 'stressed', 'pressure', 'overwhelmed', 'anxious', 'worried', 'tension', 'burden', 'exhausted'],
            'sadness': ['sad', 'depressed', 'down', 'blue', 'unhappy', 'grief', 'loss', 'hurt', 'pain', 'crying', 'tears', 'devastated', 'broken'],
            'anger': ['angry', 'mad', 'furious', 'rage', 'frustrated', 'annoyed', 'pissed', 'irritated', 'hate'],
            'happiness': ['happy', 'joy', 'excited', 'glad', 'cheerful', 'elated', 'amazing', 'great', 'wonderful', 'fantastic'],
            'fear': ['scared', 'afraid', 'terrified', 'nervous', 'panic', 'anxiety', 'worried', 'frightened', 'anxious'],
            'loneliness': ['lonely', 'alone', 'isolated', 'disconnected', 'abandoned', 'nobody', 'empty', 'void']
        }
    
    def filter_content(self, text):
        """Filter and transform sensitive content while preserving natural conversation"""
        if not text:
            return text
            
        filtered_text = text.lower()
        original_text = text
        
        # Check for severely sensitive patterns - mark as concerning but don't transform the text
        for pattern in self.sensitive_patterns:
            if re.search(pattern, filtered_text, re.IGNORECASE):
                # Log the concern (in a real app, this might trigger additional support)
                st.session_state.concern_detected = True
                # Keep the original text for natural conversation but flag for gentle response
                break
        
        # Only apply positive transformations for mild negative words, not severe ones
        mild_negative_words = ['terrible', 'awful', 'horrible', 'worst', 'stupid', 'worthless', 'useless']
        for negative_word in mild_negative_words:
            if negative_word in self.positive_transformations:
                pattern = r'\b' + re.escape(negative_word) + r'\b'
                original_text = re.sub(pattern, self.positive_transformations[negative_word], original_text, flags=re.IGNORECASE)
        
        return original_text
    
    def detect_emotion(self, text):
        """Detect the primary emotion in the text"""
        text_lower = text.lower()
        emotion_scores = {}
        
        for emotion, keywords in self.emotion_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            if score > 0:
                emotion_scores[emotion] = score
        
        if emotion_scores:
            return max(emotion_scores.keys(), key=lambda x: emotion_scores[x])
        return 'neutral'
    
    def get_emotion_support(self, emotion):
        """Get supportive message based on detected emotion"""
        support_messages = {
            'stress': "It sounds like you're feeling overwhelmed right now. That's completely understandable - stress is a natural response to challenges. Remember, you're stronger than you know. 💪",
            'sadness': "I can hear that you're going through a difficult time. It's okay to feel sad - emotions are valid and temporary. You're not alone in this. 🤗",
            'anger': "It sounds like something is really frustrating you. Those feelings are valid. Sometimes talking through what's bothering us can help lighten the load. 😌",
            'happiness': "It's wonderful to hear some positivity from you! I'm glad you're experiencing some joy. Those moments are precious. 😊",
            'fear': "Feeling scared or anxious is completely normal. You're brave for acknowledging these feelings. Let's work through this together. 🌟",
            'loneliness': "Feeling isolated can be really tough. Please know that you matter and you're not alone. I'm here to listen and support you. 💙",
            'neutral': "Thank you for sharing with me. I'm here to listen and support you in whatever way I can. 🌈"
        }
        
        return support_messages.get(emotion, support_messages['neutral'])
