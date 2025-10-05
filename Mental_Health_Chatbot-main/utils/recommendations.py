import re
import random

class RecommendationEngine:
    """Recommendation engine for various types like movies, songs, books, activities, games, podcasts, exercises, recipes based on user requests and emotions"""

    def __init__(self):
        # Movie recommendations by category
        self.movies = {
            'uplifting': [
                "The Pursuit of Happyness - An inspiring story about perseverance",
                "Inside Out - A beautiful exploration of emotions and mental health",
                "Good Will Hunting - A touching story about healing and growth",
                "The Intouchables - A heartwarming friendship story",
                "A Beautiful Mind - An inspiring story of overcoming mental health challenges"
            ],
            'comedy': [
                "The Grand Budapest Hotel - Whimsical and visually stunning",
                "Parks and Recreation (series) - Optimistic and feel-good",
                "Brooklyn Nine-Nine (series) - Light-hearted police comedy",
                "Ted Lasso (series) - About kindness and positivity",
                "Paddington - Wholesome and charming"
            ],
            'relaxing': [
                "Studio Ghibli films (My Neighbor Totoro, Spirited Away) - Peaceful and magical",
                "The Great British Baking Show - Soothing competition series",
                "Planet Earth - Beautiful nature documentary",
                "Midnight in Paris - Gentle and romantic",
                "Julie & Julia - Comforting cooking story"
            ]
        }

        # Song recommendations by mood
        self.songs = {
            'calming': [
                "Weightless by Marconi Union - Scientifically designed to reduce anxiety",
                "Claire de Lune by Claude Debussy - Classical and peaceful",
                "Mad World by Gary Jules - Melancholic but beautiful",
                "The Night We Met by Lord Huron - Gentle and reflective",
                "Holocene by Bon Iver - Atmospheric and soothing"
            ],
            'uplifting': [
                "Here Comes the Sun by The Beatles - Classic feel-good song",
                "Three Little Birds by Bob Marley - Positive message",
                "Good as Hell by Lizzo - Empowering and fun",
                "Can't Stop the Feeling by Justin Timberlake - Energetic and happy",
                "Walking on Sunshine by Katrina and the Waves - Instant mood booster"
            ],
            'healing': [
                "Breathe (2 AM) by Anna Nalick - About getting through tough times",
                "The Mother by Brandi Carlile - About unconditional love",
                "Be Still by The Killers - Calming and reassuring",
                "Skinny Love by Bon Iver - Emotional and cathartic",
                "Mad at Disney by Salem Ilese - About processing emotions"
            ]
        }

        # Book recommendations by theme
        self.books = {
            'mental_health': [
                "The Anxiety and Worry Workbook by David A. Clark - Practical CBT techniques",
                "Maybe You Should Talk to Someone by Lori Gottlieb - Honest look at therapy",
                "The Body Keeps the Score by Bessel van der Kolk - Understanding trauma and healing",
                "Mindfulness for Beginners by Jon Kabat-Zinn - Introduction to mindfulness",
                "The Gifts of Imperfection by Brené Brown - About self-compassion and vulnerability"
            ],
            'fiction': [
                "Eleanor Oliphant Is Completely Fine by Gail Honeyman - About connection and healing",
                "The Alchemist by Paulo Coelho - Inspirational journey story",
                "A Man Called Ove by Fredrik Backman - Heartwarming story about community",
                "The Seven Husbands of Evelyn Hugo by Taylor Jenkins Reid - Engaging and uplifting",
                "Where the Crawdads Sing by Delia Owens - Beautiful coming-of-age story"
            ],
            'self_help': [
                "Atomic Habits by James Clear - Building positive habits",
                "The Power of Now by Eckhart Tolle - Mindfulness and presence",
                "Untamed by Glennon Doyle - About authenticity and self-discovery",
                "The 7 Habits of Highly Effective People by Stephen Covey - Personal development",
                "Big Magic by Elizabeth Gilbert - About creativity and living fearlessly"
            ]
        }

        # Activities for different emotional needs
        self.activities = {
            'stress_relief': [
                "Try a 5-minute breathing exercise: breathe in for 4, hold for 4, out for 6",
                "Take a warm bath with some calming essential oils",
                "Go for a gentle walk in nature, even if it's just around the block",
                "Practice progressive muscle relaxation",
                "Try some gentle yoga or stretching"
            ],
            'mood_boost': [
                "Dance to your favorite upbeat song for 3 minutes",
                "Call or text a friend you haven't spoken to in a while",
                "Do something creative - draw, write, or craft something",
                "Practice gratitude by listing 3 things you're thankful for",
                "Watch funny videos or animal videos online"
            ],
            'self_care': [
                "Make yourself a special cup of tea or coffee",
                "Write in a journal about your thoughts and feelings",
                "Do a skincare routine or take care of your physical self",
                "Organize a small space in your home",
                "Practice meditation for 10 minutes"
            ]
        }

        # Game recommendations by mood
        self.games = {
            'calming': [
                "Stardew Valley - Relaxing farming and life simulator",
                "Journey - A beautiful and meditative adventure game",
                "Animal Crossing - Lighthearted social simulation",
                "Spiritfarer - A soothing game about guiding spirits",
                "Abzû - Underwater exploration and calming visuals"
            ],
            'uplifting': [
                "Mario Kart - Fast-paced and fun racing game",
                "Super Mario Odyssey - Joyful and colorful platform adventure",
                "Overcooked! - Cooperative and chaotic cooking game",
                "Portal 2 - Clever puzzle-solving with humor",
                "Rocket League - Exciting vehicular soccer game"
            ],
            'relaxing': [
                "Firewatch - Story-driven and immersive exploration",
                "Gris - Artful platformer with calming music",
                "Celeste - Emotionally uplifting story and gameplay",
                "The Sims 4 - Create and control a virtual life",
                "Ori and the Blind Forest - Beautiful and relaxing platformer"
            ]
        }

        # Podcast recommendations by mood
        self.podcasts = {
            'uplifting': [
                "The Happy Hour with Jamie Ivey - Stories that inspire joy",
                "Good Life Project - Conversations about living meaningfully",
                "On Being with Krista Tippett - Deep reflections on life and kindness",
                "The Moth - True personal storytelling",
                "Hidden Brain - Exploring human behavior thoughtfully"
            ],
            'calming': [
                "Sleepy - Bedtime stories and relaxing readings",
                "Meditative Story - Mindfulness combined with storytelling",
                "Nothing much happens - Calm stories for busy minds",
                "On Meditation - Talks on mindfulness and peace",
                "LeVar Burton Reads - Soothing voice and literary tales"
            ]
        }

        # Exercise recommendations by mood
        self.exercises = {
            'stress_relief': [
                "Gentle yoga focusing on breath awareness",
                "15-minute mindfulness walking meditation",
                "Progressive muscle relaxation routine",
                "Tai chi for gentle flowing movement",
                "Breathing exercises for calming nerves"
            ],
            'mood_boost': [
                "Dance to your favorite upbeat songs for 10 minutes",
                "Quick cardio workout to elevate your energy",
                "Stretching routine to refresh your body",
                "Outdoor walk or jog to uplift your mood",
                "Bodyweight exercises for strength and vitality"
            ]
        }

        # Recipe recommendations by mood
        self.recipes = {
            'uplifting': [
                "Fresh fruit smoothie bowl packed with vitamins",
                "Colorful vegetable stir-fry with garlic and ginger",
                "Homemade guacamole with crunchy chips",
                "Bright citrus salad with mint and honey",
                "Easy avocado toast with a sprinkle of chili flakes"
            ],
            'comfort': [
                "Creamy macaroni and cheese",
                "Hearty chicken noodle soup",
                "Warm chocolate chip cookies",
                "Classic mashed potatoes with butter",
                "Slow-cooker beef stew"
            ]
        }

    def detect_recommendation_request(self, text):
        """Detect type of recommendation requested"""
        recommendation_patterns = {
            'movies': [r'\bmovies?\b', r'\bfilms?\b', r'\bwatch\b', r'\bnetflix\b', r'\bcinema\b'],
            'songs': [r'\bsongs?\b', r'\bmusic\b', r'\blisten\b', r'\bplaylist\b', r'\bspotify\b'],
            'books': [r'\bbooks?\b', r'\bread\b', r'\bnovel\b', r'\bstory\b', r'\bliterature\b'],
            'activities': [r'\bactivit(y|ies)\b', r'\bdo\b', r'\bhelp\b', r'\btry\b', r'\bsuggestion\b'],
            'games': [r'\bgames?\b', r'\bplay\b', r'\bgaming\b', r'\bvideo game\b', r'\bboard game\b'],
            'podcasts': [r'\bpodcast?\b', r'\blisten\b'],
            'exercises': [r'\bexercises?\b', r'\bworkout\b', r'\bfitness\b'],
            'recipes': [r'\brecipes?\b',r'\bcook?\b', r'\brecipe\b', r'\bfood\b', r'\bcooking\b'],
        }

        text_lower = text.lower()
        for category, patterns in recommendation_patterns.items():
            if any(re.search(pattern, text_lower) for pattern in patterns):
                return category
        return None

    def get_mood_based_category(self, text):
        """Determine sentiment/mood category based on user input"""
        text_lower = text.lower()

        if any(word in text_lower for word in ['sad', 'depressed', 'down', 'upset', 'crying']):
            return 'uplifting'
        elif any(word in text_lower for word in ['stressed', 'anxious', 'worried', 'overwhelmed']):
            return 'calming'
        elif any(word in text_lower for word in ['angry', 'frustrated', 'mad', 'furious']):
            return 'calming'
        elif any(word in text_lower for word in ['tired', 'exhausted', 'drained']):
            return 'relaxing'
        elif any(word in text_lower for word in ['lonely', 'alone', 'isolated']):
            return 'uplifting'
        elif any(word in text_lower for word in ['comfort', 'cozy', 'warm']):
            return 'comfort'
        else:
            return 'uplifting'

    def get_recommendation(self, text):
        """Get recommendations dynamically depending on request type and mood"""
        rec_type = self.detect_recommendation_request(text)
        if not rec_type:
            return None

        mood_category = self.get_mood_based_category(text)

        # Select recommendations based on type and mood 
        if rec_type == 'movies':
            category = mood_category if mood_category in self.movies else 'uplifting'
            recommendations = random.sample(self.movies[category], min(3, len(self.movies[category])))
            return f"🎬 **Movie Recommendations for you:**\n" + "\n".join(f"• {rec}" for rec in recommendations)

        elif rec_type == 'songs':
            category = 'calming' if mood_category in ['calming', 'relaxing'] else 'uplifting'
            if category not in self.songs:
                category = 'uplifting'
            recommendations = random.sample(self.songs[category], min(3, len(self.songs[category])))
            return f"🎵 **Song Recommendations for you:**\n" + "\n".join(f"• {rec}" for rec in recommendations)

        elif rec_type == 'books':
            if any(word in text.lower() for word in ['mental health', 'anxiety', 'depression', 'therapy', 'healing']):
                category = 'mental_health'
            else:
                category = 'fiction'
            recommendations = random.sample(self.books[category], min(3, len(self.books[category])))
            return f"📚 **Book Recommendations for you:**\n" + "\n".join(f"• {rec}" for rec in recommendations)

        elif rec_type == 'activities':
            if any(word in text.lower() for word in ['stressed', 'anxious', 'worried', 'overwhelmed']):
                activity_type = 'stress_relief'
            elif any(word in text.lower() for word in ['sad', 'down', 'depressed', 'low']):
                activity_type = 'mood_boost'
            else:
                activity_type = 'self_care'
            recommendations = random.sample(self.activities[activity_type], min(3, len(self.activities[activity_type])))
            return f"✨ **Activity Suggestions for you:**\n" + "\n".join(f"• {rec}" for rec in recommendations)

        elif rec_type == 'games':
            category = mood_category if mood_category in self.games else 'uplifting'
            recommendations = random.sample(self.games[category], min(3, len(self.games[category])))
            return f"🎮 **Game Recommendations for you:**\n" + "\n".join(f"• {rec}" for rec in recommendations)

        elif rec_type == 'podcasts':
            category = mood_category if mood_category in self.podcasts else 'uplifting'
            if category not in self.podcasts:
                category = 'uplifting'
            recommendations = random.sample(self.podcasts[category], min(3, len(self.podcasts[category])))
            return f"🎙️ **Podcast Recommendations for you:**\n" + "\n".join(f"• {rec}" for rec in recommendations)

        elif rec_type == 'exercises':
            category = mood_category if mood_category in self.exercises else 'mood_boost'
            if category not in self.exercises:
                category = 'mood_boost'
            recommendations = random.sample(self.exercises[category], min(3, len(self.exercises[category])))
            return f"🏋️ **Exercise Suggestions for you:**\n" + "\n".join(f"• {rec}" for rec in recommendations)

        elif rec_type == 'recipes':
            category = mood_category if mood_category in self.recipes else 'uplifting'
            if category not in self.recipes:
                category = 'comfort'
            recommendations = random.sample(self.recipes[category], min(3, len(self.recipes[category])))
            return f"🍳 **Recipe Suggestions for you:**\n" + "\n".join(f"• {rec}" for rec in recommendations)

        else:
            return None
