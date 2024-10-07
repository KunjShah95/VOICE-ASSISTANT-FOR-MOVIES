import imdb
import pyttsx3
import speech_recognition as sr
import datetime
from googletrans import Translator
import requests
from bs4 import BeautifulSoup
import json
import tkinter as tk
from PIL import Image, ImageTk
from io import BytesIO

# Initialize IMDb and Speech Engine
moviesdb = imdb.IMDb()

# Initialize speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
rate = engine.getProperty('rate')
engine.setProperty('rate', rate - 20)

# Personalization and user preferences
user_name = "Alex"  # Replace with dynamic user input for a real scenario
user_preferences = {"genre": "action", "actor": "Leonardo DiCaprio"}
watchlist = []  # List to store movies the user wants to watch later

# Load watchlist from a file
def load_watchlist_from_file():
    global watchlist
    try:
        with open('watchlist.json', 'r') as f:
            watchlist = json.load(f)
    except FileNotFoundError:
        watchlist = []

# Save watchlist to a file
def save_watchlist_to_file():
    with open('watchlist.json', 'w') as f:
        json.dump(watchlist, f)

# Function for speaking
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Greet the user based on the time of day
def greet_user():
    current_hour = datetime.datetime.now().hour
    if current_hour < 12:
        greet = "Good morning"
    elif 12 <= current_hour < 18:
        greet = "Good afternoon"
    else:
        greet = "Good evening"
    speak(f"{greet}, {user_name}! How can I assist you with movies today?")

# Get user input through speech recognition
def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
        said = ""
    try:
        said = r.recognize_google(audio)
        print(said)
    except sr.UnknownValueError:
        speak("I didn't get that. Could you please repeat?")
    except sr.RequestError:
        speak("Sorry, I'm having trouble connecting to the internet.")
    return said.lower()

# Get user input through text or voice
def get_user_input():
    speak("Would you like to use voice input or text input?")
    choice = get_audio()

    if "text" in choice:
        speak("Please type your input.")
        user_input = input("Enter your input: ")
    else:
        speak("Using voice input.")
        user_input = get_audio()

    return user_input

# Function to translate text
def translate_text(text, target_lang='es'):
    translator = Translator()
    translated = translator.translate(text, dest=target_lang)
    return translated.text

# Add movie to the user's watchlist
def add_to_watchlist(movie_title):
    watchlist.append(movie_title)
    speak(f"{movie_title} has been added to your watchlist.")

# Function for searching movie and retrieving details
def search_movie():
    speak("Say the movie name")
    movie_name = get_audio()

    if not movie_name:
        speak("Sorry, I didn't catch the movie name.")
        return

    speak(f"Searching for {movie_name}")
    try:
        movies = moviesdb.search_movie(movie_name)
        if not movies:
            speak(f"No results found for {movie_name}")
            return

        speak(f"I found these results for {movie_name}:")
        for movie in movies[:5]:  # Limit to 5 results
            title = movie['title']
            year = movie['year']
            speak(f"{title}, released in {year}")

        movie_choice = movies[0]
        movie_id = movie_choice.movieID
        movie_details = moviesdb.get_movie(movie_id)

        # Movie details
        title = movie_details['title']
        year = movie_details['year']
        rating = movie_details.get('rating', 'N/A')
        plot = movie_details.get('plot outline', 'No plot summary available')

        # Speak out details based on the release year
        if year < int(datetime.datetime.now().strftime("%Y")):
            speak(f"{title} was released in {year} with an IMDb rating of {rating}. The plot summary is: {plot}")
        else:
            speak(f"{title} will release in {year}. The plot summary is: {plot}")
        
        add_to_watchlist(title)  # Add to watchlist

        # Get and display the movie poster
        get_movie_poster(movie_details)

        # Fetch reviews
        get_movie_reviews(title)

    except imdb.IMDbError as e:
        speak(f"An error occurred: {e}")

# Function to get movie poster
def get_movie_poster(movie):
    try:
        poster_url = movie['full-size cover url']
        speak("Here is the movie poster link.")
        print(poster_url)
    except KeyError:
        speak("Poster not available for this movie.")

# Function to get movie reviews (scrape from Rotten Tomatoes)
def get_movie_reviews(movie_title):
    try:
        url = f"https://www.rottentomatoes.com/m/{movie_title.replace(' ', '_')}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        reviews = soup.find_all('div', class_='review')
        speak(f"Here are some reviews for {movie_title}:")
        for review in reviews[:5]:  # Limit to 5 reviews
            speak(review.text)
    except Exception as e:
        speak("Sorry, I couldn't fetch the reviews.")

# Recommend a movie based on user preferences
def recommend_movie_based_on_preferences():
    try:
        genre_preference = user_preferences["genre"]
        actor_preference = user_preferences["actor"]
        speak(f"Recommending a {genre_preference} movie featuring {actor_preference}.")
        
        # Searching for movies with user preference
        movies = moviesdb.search_movie(actor_preference)
        filtered_movies = [movie for movie in movies if genre_preference.lower() in [g.lower() for g in movie.get('genres', [])]]
        
        if filtered_movies:
            recommended_movie = filtered_movies[0]  # Recommend the first matching movie
            speak(f"I recommend {recommended_movie['title']}.")
        else:
            speak(f"Sorry, I couldn't find any {genre_preference} movies with {actor_preference}.")

    except Exception as e:
        speak(f"An error occurred while recommending: {e}")

# Show movie details in a GUI window
def show_movie_details_gui(title, year, rating, plot, poster_url):
    root = tk.Tk()
    root.title("Movie Assistant")

    label_title = tk.Label(root, text=f"{title} ({year})", font=("Helvetica", 18))
    label_title.pack()

    label_rating = tk.Label(root, text=f"IMDb Rating: {rating}", font=("Helvetica", 14))
    label_rating.pack()

    label_plot = tk.Label(root, text=f"Plot: {plot}", wraplength=400, justify="left")
    label_plot.pack()

    try:
        response = requests.get(poster_url)
        img_data = response.content
        img = ImageTk.PhotoImage(Image.open(BytesIO(img_data)))
        label_poster = tk.Label(root, image=img)
        label_poster.pack()
    except:
        pass

    root.mainloop()

# Movie search with additional criteria (genre, year)
def search_movie_with_criteria():
    speak("Would you like to add criteria to your search like genre or release year?")
    user_input = get_audio()

    if "yes" in user_input:
        speak("Please say the genre.")
        genre = get_audio()
        speak("Now, please say the release year.")
        year = get_audio()

        # Filter movies by genre and year
        movies = moviesdb.search_movie(get_audio())
        filtered_movies = [movie for movie in movies if genre.lower() in movie['genres'] and movie['year'] == int(year)]
        
        if filtered_movies:
            for movie in filtered_movies[:5]:  # Show top 5
                speak(f"{movie['title']}, released in {movie['year']}")
        else:
            speak("No movies found with those criteria.")
    else:
        search_movie()  # Regular search if no criteria provided

# Main function to run the assistant
def run_assistant():
    load_watchlist_from_file()  # Load watchlist
    greet_user()  # Greet the user
    speak("Would you like me to recommend a movie or search for a specific one?")
    user_input = get_user_input()  # Allow user to choose between text or voice input

    if "recommend" in user_input:
        recommend_movie_based_on_preferences()
    elif "search" in user_input or "movie" in user_input:
        search_movie_with_criteria()  # Enhanced movie search with criteria
    else:
        speak("I didn't catch that. Please say 'recommend' or 'search'.")
    
    save_watchlist_to_file()  # Save the watchlist at the end of the session

# Run the virtual assistant
run_assistant()
