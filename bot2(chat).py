import streamlit as st
import ollama
import re

# Streamlit UI setup
st.set_page_config(page_title="Mental Health Chatbot", page_icon="🧘", layout="centered")

st.markdown("""
    <style>
    .stApp {
        background-image: url("https://wallpaperaccess.com/full/3776356.jpg");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    </style>
    """, unsafe_allow_html=True)

# User authentication
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

users = {"user1": "password1", "user2": "password2"}  # Example user database

# Predefined emergency contacts (add or change as needed)
emergency_contacts = {
    "user1": ["himanikatari@gmail.com"],
    "user2": ["himanikatari@gmail.com"]
}

def login():
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username in users and users[username] == password:
            st.session_state.authenticated = True
            st.session_state.username = username
            st.success("Login successful!")
            st.rerun()
        else:
            st.error("Invalid username or password")

def signup():
    st.subheader("Sign Up")
    new_username = st.text_input("New Username")
    new_password = st.text_input("New Password", type="password")
    if st.button("Sign Up"):
        if new_username in users:
            st.error("Username already exists. Please choose another.")
        else:
            users[new_username] = new_password
            st.success("Account created successfully! Please log in.")
            st.experimental_rerun()

if not st.session_state.authenticated:
    page = st.radio("Select an option", ["Login", "Sign Up"])
    if page == "Login":
        login()
    else:
        signup()
else:
    st.title("🧘 Mental Health Chatbot")
    st.write("I'm here to listen and support you. How are you feeling today?")

    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Hello! How are you feeling today?"}]

    greetings = ["hello", "hi", "hey", "good morning", "good evening", "good afternoon"]

    def contains_sensitive_words(text):
        sensitive_patterns = ["suicide", "self-harm", "depression", "kill", "hopeless", "worthless",
                              "no purpose", "give up", "end it all", "alone", "nobody cares", "cutting", 
                              "hate myself", "empty", "lost", "pain", "trigger", "darkness", "suffocating",  
                              "broken", "unwanted", "helpless", "despair", "overdose", "drown", "numb",  
                              "unlovable", "tired of living", "unbearable", "nothing matters", "nobody cares",  
                              "die", "escape", "death", "feel nothing", "withdrawal", "no one understands", 
                              "goodbye", "no way out", "pushed to the edge", "can't take it anymore",  
                              "self-loathing", "end my life", "why bother", "hurt myself", "razor", "bleeding",  
                              "deep sadness", "sorrow", "give in", "give up on life", "pointless", "overwhelmed",  
                              "too much to handle", "unfixable", "shattered", "can't cope", "not strong enough",  
                              "breaking down", "worthless existence", "better off gone", "no second chances",  
                              "drowning in sadness", "crying all the time", "constant suffering", "silent pain",  
                              "running out of hope", "screaming inside", "wishing it would end", "drifting away",  
                              "let me go", "can't hold on", "dark thoughts", "nobody would miss me", "vanish forever",  
                              "disappear", "stop existing", "done trying", "end the suffering", "life is meaningless",  
                              "trapped in my mind", "exhausted from life", "giving up on everything", "emotional pain",  
                              "burden to others", "never good enough", "life is unfair", "I feel invisible",  
                              "everything is falling apart", "giving in to the pain", "drowning in tears",  
                              "I don't see a future", "nothing feels real", "I want out", "I'm broken inside",  
                              "no light at the end", "just want to sleep forever", "numb to everything",  
                              "pain never ends", "suffering alone", "nobody listens", "nobody understands my pain",  
                              "murder", "homicide", "kill someone", "take a life", "violent thoughts",  
                              "hurt others", "attack someone", "revenge killing", "massacre", "criminal intent",  
                              "harm others", "dangerous thoughts", "commit crime", "violent urges", "assault",  
                              "destructive thoughts", "cause pain", "plot revenge", "thinking of killing",  
                              "eliminate someone", "hate crime", "act of violence", "lethal plan",  
                              "deadly intentions", "torture", "manslaughter", "brutal attack", "violent plan" ]
        for pattern in sensitive_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        return False

    def notify_contacts(user):
        """ Simulate notifying emergency contacts when sensitive words are detected. """
        if user in emergency_contacts:
            contacts = emergency_contacts[user]
            for contact in contacts:
                # Here you would integrate actual notification (e.g., email or SMS)
                print(f"Notification sent to {contact}: 'Urgent: User {user} may need assistance. Please reach out.'")

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    user_input = st.chat_input("Type your message here...")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        if any(word in user_input.lower() for word in greetings):
            bot_message = "Hello! How can I support you today? 😊"
        elif contains_sensitive_words(user_input):
            bot_message = "I'm really sorry you're feeling this way. Please reach out to a trusted friend or professional. 💙"
            # Notify emergency contacts if sensitive words are found
            notify_contacts(st.session_state.username)
        elif "recommend" in user_input.lower():
            prompt = "Give any 3 recommendations for movies, music, tips, exercises, books and games that can help lift someone's mood."
            try:
                response = ollama.chat(model="gemma", messages=st.session_state.messages + [{"role": "system", "content": prompt}])
                if "message" in response:
                    bot_message = response["message"].get("content", "I recommend watching 'Forrest Gump' – it's an uplifting movie!")
                else:
                    bot_message = "I suggest listening to 'Imagine' by John Lennon – it's very soothing!"
            except Exception as e:
                bot_message = f"Oops, something went wrong while fetching recommendations: {e}. Please try again later."
        else:
            mood_keywords = {
                "happy": ["happy", "excited", "joyful", "good", "great"],
                "sad": ["sad", "down", "depressed", "unhappy", "lonely"],
                "anxious": ["anxious", "worried", "stressed", "overwhelmed"],
                "neutral": ["okay", "fine", "meh", "alright", "not sure"],
            }

            detected_mood = "neutral"
            for mood, keywords in mood_keywords.items():
                if any(word in user_input.lower() for word in keywords):
                    detected_mood = mood
                    break
            #always gives a positive response
            st.session_state.mood = detected_mood
            prompt = (
                f"The user seems to be feeling {detected_mood}. No matter what, respond with positivity, encouragement, and motivation. "
                "Reassure them and provide comforting words. Keep the response uplifting."
            )

            try:
                response = ollama.chat(model="gemma", messages=st.session_state.messages + [{"role": "system", "content": prompt}])
                if "message" in response:
                    bot_message = response["message"].get("content", "You're doing amazing, and I'm here for you!")
                else:
                    bot_message = "You're strong, and I believe in you!"
            except Exception as e:
                bot_message = f"Oops, something went wrong while processing your mood: {e}. Please try again later."

        st.session_state.messages.append({"role": "assistant", "content": bot_message})

        with st.chat_message("assistant"):
            st.write(bot_message)
