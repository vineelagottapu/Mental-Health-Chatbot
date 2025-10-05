import requests
import json
import os
import streamlit as st
from utils.content_filter import ContentFilter

class OllamaClient:
    """Client for interacting with Ollama Gemma model"""
    
    def __init__(self):
        self.base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.model = "gemma:latest"
        self.content_filter = ContentFilter()
        
        # System prompt for mental health support
        self.system_prompt = """You are MindfulChat, a compassionate AI mental health companion. Your role is to:

1. Always respond with empathy, warmth, and understanding
2. Use a supportive, non-judgmental tone
3. Encourage positive coping strategies and self-care
4. Include appropriate emojis to convey warmth (but don't overuse them)
5. Keep responses conversational and friend-like
6. If someone seems in crisis, gently suggest professional help while being supportive
7. Focus on the person's strengths and resilience
8. Ask follow-up questions to show you're listening and engaged
9. Never provide medical advice, but offer emotional support
10. End responses with encouragement or a question to continue the conversation

Remember: You're a friend who listens without judgment and always tries to find the positive while acknowledging difficult emotions."""
    
    def get_response(self, user_message):
        """Generate AI response using natural conversation logic"""
        try:
            # Always use natural conversation approach instead of trying Ollama
            # This ensures consistent, natural responses
            emotion = self.content_filter.detect_emotion(user_message)
            
            # Check if this is concerning content but respond naturally
            is_concerning = hasattr(st.session_state, 'concern_detected') and st.session_state.concern_detected
            
            # Generate natural response based on sentiment and content
            return self._get_sentiment_based_response(user_message, emotion, is_concerning)
                
        except Exception as e:
            return self._get_fallback_response(user_message, 'neutral')
    
    def _get_sentiment_based_response(self, user_message, emotion, is_concerning=False):
        """Generate response based on sentiment analysis of the message"""
        import random
        
        message_lower = user_message.lower()
        
        # Handle greetings naturally
        if any(word in message_lower for word in ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening']):
            return random.choice([
                "Hi there! How are you doing today?",
                "Hello! What's on your mind?",
                "Hey! How can I support you today?",
                "Hi! It's good to hear from you. How are things going?"
            ])
        
        # Handle specific emotional contexts with supportive suggestions
        if emotion == 'sadness':
            if 'depressed' in message_lower or 'sad' in message_lower:
                responses = [
                    "I can hear you're going through a really tough time. When I feel overwhelmed like this, I find that taking small steps can help - maybe try going for a short walk or listening to some calming music. Remember, you don't have to carry all of this alone.",
                    "Depression can make everything feel so much heavier. One thing that often helps is focusing on just getting through today, not worrying about tomorrow. Have you tried doing something small that usually brings you a bit of comfort?",
                    "Those feelings are completely valid. Sometimes when I'm struggling, I remind myself that feelings are temporary, even when they don't feel that way. Maybe try writing down one small thing you're grateful for today."
                ]
            elif any(word in message_lower for word in ['death', 'die', 'kill']):
                if is_concerning:
                    responses = [
                        "I can hear how much pain you're in right now. When thoughts get this heavy, it can help to reach out to someone you trust or call a crisis line. You matter more than you know, and there are people who want to help you through this.",
                        "Those thoughts must feel so overwhelming. Sometimes when everything feels impossible, talking to a counselor or trusted friend can provide a different perspective. You don't have to face this alone - there are people who care about you.",
                        "I'm really concerned about you right now. Please consider reaching out to a mental health professional or crisis helpline. You deserve support and care, and there are people trained to help with exactly what you're going through."
                    ]
                else:
                    responses = [
                        "That sounds like you've been dealing with something really difficult. Sometimes talking through these heavy feelings with someone can help lighten the load. Have you considered speaking with a counselor or someone you trust?",
                        "I can sense there's a lot weighing on your mind. When I'm processing difficult thoughts, I find it helps to focus on small, immediate things I can control. Maybe try doing one small thing that feels manageable today.",
                        "Those are some heavy thoughts to carry. Remember that difficult times don't last forever, even when they feel endless. Consider reaching out to someone who can provide professional support."
                    ]
            else:
                responses = [
                    "I can see you're going through something difficult. Sometimes when I'm feeling down, I try to do one small thing that usually makes me feel a bit better - like making tea, calling a friend, or watching something funny.",
                    "That sounds really tough to deal with. One thing that helps me is remembering that tough times teach us how strong we really are. Maybe try doing something kind for yourself today, even if it's small.",
                    "I'm sorry you're dealing with this. When I'm struggling, I find it helps to focus on just getting through today. Have you tried any activities that usually help you feel a bit better?"
                ]
            return random.choice(responses)
        
        elif emotion == 'anger':
            responses = [
                "That sounds really frustrating. When I'm angry, I find it helps to take some deep breaths or go for a walk to cool down. Sometimes physical activity like exercise can help release that intense energy.",
                "I can hear your frustration. Anger often means something important to us has been affected. Try taking a few minutes to step back and think about what you can actually control in this situation.",
                "That would definitely make me angry too. When I'm feeling this way, I sometimes write down my thoughts or talk to someone I trust. It helps get those intense feelings out in a healthy way."
            ]
            return random.choice(responses)
        
        elif emotion == 'stress':
            responses = [
                "That sounds overwhelming. When I'm stressed, I try breaking things down into smaller, manageable pieces. Maybe make a list of what needs to be done and tackle just one thing at a time.",
                "Stress can be exhausting. I find it helps to take short breaks throughout the day - even just 5 minutes of deep breathing or stepping outside can make a difference.",
                "I can hear you're feeling a lot of pressure. Remember it's okay to ask for help when you need it. Sometimes just talking through what's stressing you can help you see solutions you hadn't thought of."
            ]
            return random.choice(responses)
        
        elif emotion == 'fear':
            responses = [
                "That does sound scary. When I'm anxious, I try to focus on what I can control right now, rather than all the 'what ifs.' Sometimes grounding techniques like naming 5 things you can see around you can help.",
                "Anxiety can feel so overwhelming. I find it helps to remember that most of the things we worry about never actually happen. Try taking some slow, deep breaths - it can help calm your nervous system.",
                "Those worried feelings are completely understandable. When I'm feeling anxious, I sometimes do a quick body scan and consciously relax any tense muscles. It's amazing how much physical tension anxiety creates."
            ]
            return random.choice(responses)
        
        elif emotion == 'loneliness':
            responses = [
                "Feeling alone can be so hard. Sometimes when I'm lonely, I reach out to an old friend or do something in public like going to a coffee shop. Even small interactions can help you feel more connected.",
                "I'm glad you reached out - that takes courage when you're feeling isolated. Sometimes volunteering or joining a group activity can help you meet people who share similar interests.",
                "That isolation feeling is really tough. Remember that reaching out like this shows strength. Maybe try doing one small thing today that gets you around other people, even if it's just a quick trip to the store."
            ]
            return random.choice(responses)
        
        elif emotion == 'happiness':
            responses = [
                "That's wonderful to hear! It's great that you're taking time to notice the good things. Celebrating these positive moments, even small ones, can help build resilience for tougher times.",
                "I love hearing some positivity! When good things happen, I try to really savor them and maybe share the joy with someone else. Positive emotions can be contagious in the best way.",
                "That sounds amazing! It's so important to acknowledge and appreciate these happy moments. They remind us that good things do happen, even when life gets challenging."
            ]
            return random.choice(responses)
        
        # Default neutral responses with gentle suggestions
        else:
            responses = [
                "I'm here to listen. Sometimes just talking through what's on our minds can help us see things more clearly. What's been occupying your thoughts lately?",
                "Thanks for sharing with me. I find that when something's bothering us, it often helps to get it out rather than keeping it bottled up inside.",
                "I'm listening. Whatever you're going through, remember that you don't have to handle everything alone. Sometimes a fresh perspective can be really helpful."
            ]
            return random.choice(responses)
    
    def _is_response_appropriate(self, response):
        """Check if the AI response is appropriate and supportive"""
        response_lower = response.lower()
        
        # Check for inappropriate content
        inappropriate_phrases = [
            'i cannot help', 'i can\'t help', 'seek professional help immediately',
            'i am not qualified', 'consult a doctor', 'this is serious'
        ]
        
        if any(phrase in response_lower for phrase in inappropriate_phrases):
            return False
        
        # Check for positive supportive language
        positive_indicators = [
            'understand', 'here for you', 'support', 'listen', 'care',
            'strength', 'brave', 'important', 'matter', 'valid'
        ]
        
        return any(indicator in response_lower for indicator in positive_indicators)
    
    def _get_fallback_response(self, user_message, emotion):
        """Generate natural conversational response when AI is unavailable or inappropriate"""
        import random
        
        # Analyze the user message for context
        message_lower = user_message.lower()
        
        # Greeting responses
        greeting_words = ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening']
        if any(word in message_lower for word in greeting_words):
            greetings = [
                "Hi there! How are you doing today?",
                "Hello! It's nice to meet you. What's on your mind?",
                "Hey! Thanks for reaching out. How can I support you today?",
                "Hi! I'm glad you're here. What would you like to talk about?"
            ]
            return random.choice(greetings)
        
        # Question responses
        question_words = ['what', 'how', 'why', 'when', 'where', 'can you', 'do you', 'should i']
        if any(word in message_lower for word in question_words):
            question_responses = [
                "That's a really thoughtful question. Let me think about that with you. What's your take on it?",
                "I appreciate you asking. What's been making you think about this?",
                "That's interesting. Tell me more about what's behind this question.",
                "Good question! What's your perspective on this so far?"
            ]
            return random.choice(question_responses)
        
        # Movie/song/book recommendation requests
        if any(word in message_lower for word in ['movie', 'song', 'book', 'recommend', 'suggest']):
            return self._handle_recommendation_request(message_lower)
        
        # Emotion-based responses (more natural)
        emotion_responses = {
            'stress': [
                "Sounds like you're dealing with a lot right now. Want to talk about what's weighing on you?",
                "That sounds stressful. What's been the hardest part?",
                "I hear you. Stress can be overwhelming. What's going on?"
            ],
            'sadness': [
                "I can hear that you're going through something difficult. Want to share what's happening?",
                "That sounds really tough. I'm here to listen if you want to talk about it.",
                "I'm sorry you're feeling this way. What's been going on?"
            ],
            'anger': [
                "That sounds frustrating. What's got you feeling this way?",
                "I can hear your frustration. Want to tell me what happened?",
                "Sounds like something really got to you. What's going on?"
            ],
            'happiness': [
                "That's wonderful! I'd love to hear what's making you happy.",
                "It's great to hear some positivity! What's going well for you?",
                "That sounds amazing! Tell me more about what's bringing you joy."
            ],
            'fear': [
                "That sounds scary. Do you want to talk about what's worrying you?",
                "I can understand feeling anxious about that. What's on your mind?",
                "That must feel overwhelming. Want to share what's making you feel this way?"
            ],
            'loneliness': [
                "I'm glad you reached out. Feeling alone can be really hard. What's been going on?",
                "Thanks for sharing that with me. Want to talk about what's been making you feel lonely?",
                "I'm here with you. What's been on your mind lately?"
            ],
            'neutral': [
                "I'm listening. What's been on your mind?",
                "Thanks for sharing with me. Tell me more about what's going on.",
                "I'm here for you. What would you like to talk about?",
                "How are you feeling today? What's happening in your world?"
            ]
        }
        
        responses = emotion_responses.get(emotion, emotion_responses['neutral'])
        return random.choice(responses)
    
    def _handle_recommendation_request(self, message_lower):
        """Handle recommendation requests naturally"""
        import random
        
        if 'movie' in message_lower or 'film' in message_lower:
            responses = [
                "I'd love to suggest some movies! What kind of mood are you in? Something uplifting, funny, or relaxing?",
                "Movies are great! Are you looking for something to lift your spirits or help you unwind?",
                "Sure! What type of movies do you usually enjoy? I have some great suggestions."
            ]
        elif 'song' in message_lower or 'music' in message_lower:
            responses = [
                "Music can be so healing! What kind of vibe are you going for - something calming or more upbeat?",
                "I love talking about music! Are you looking for something to match your mood or change it?",
                "Great choice! Music can really help. What's your usual style, or are you open to trying something new?"
            ]
        elif 'book' in message_lower:
            responses = [
                "Books are amazing! Are you interested in something for personal growth, fiction, or maybe mental health related?",
                "I have some wonderful book suggestions! What kind of reading are you in the mood for?",
                "Perfect! Reading can be so therapeutic. What genres do you usually enjoy?"
            ]
        else:
            responses = [
                "I'd be happy to suggest some activities! What are you hoping to feel - more relaxed, energized, or just something different?",
                "Great idea! Are you looking for something to do at home or maybe get you out and about?",
                "I have lots of ideas! What kind of activities usually appeal to you?"
            ]
        
        return random.choice(responses)
    
    def _get_offline_response(self, user_message):
        """Response when Ollama service is not available"""
        # Use the same natural conversation logic as fallback
        emotion = self.content_filter.detect_emotion(user_message)
        return self._get_fallback_response(user_message, emotion)

    def test_connection(self):
        """Test connection to Ollama service"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False
