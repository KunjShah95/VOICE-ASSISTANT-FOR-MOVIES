# Voice Assistant for Movies

Welcome to the **Voice Assistant for Movies** project! This Python-based virtual assistant is designed to fetch movie information, including plots and ratings, using voice commands. The assistant communicates with IMDb to gather movie details and responds through text-to-speech output, making it easy to interact and get movie data hands-free.

## Features

- **Voice Recognition**: The assistant listens for movie search queries and converts speech to text.
- **Movie Information Fetching**: Retrieves movie plot, ratings, and other details using the IMDb API.
- **Voice Output**: Reads the movie information aloud to the user, creating a seamless hands-free experience.
- **Speech-to-Text Support**: Powered by `SpeechRecognition`, making it easy to search movies using your voice.

## Technologies Used

- **Python**: Main language for the project.
- **SpeechRecognition**: Converts user voice into text.
- **IMDbPy**: Fetches movie details from IMDb.
- **pyttsx3**: Converts text responses into speech output.
  
## Requirements

Make sure Python (version 3.7 or higher) is installed on your system. Install the necessary libraries using:

```bash
pip install -r requirements.txt
```

### Required Libraries:

- `SpeechRecognition`
- `IMDbPy`
- `pyttsx3`

## How to Use

1. **Clone the repository**:

   ```bash
   git clone https://github.com/KunjShah95/VOICE-ASSISTANT-FOR-MOVIES.git
   ```

2. **Install dependencies**:

   Navigate to the project directory and install the necessary libraries:

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Assistant**:

   To start the voice assistant, execute the following command:

   ```bash
   python movie_assistant.py
   ```

4. **Give Commands**:

   Once the assistant is running, speak your movie-related queries like:
   
   - "Tell me about the movie Inception."
   - "What is the plot of Titanic?"
   - "What's the rating of The Dark Knight?"

   The assistant will respond with the relevant movie details.

## Example Commands

- **Movie Information**: 
  - "What is the plot of Interstellar?"
  - "Give me the rating of Avengers: Endgame."
  
- **General Commands**: 
  - "Search for the movie The Godfather."
  - "Tell me about Avatar."

## Future Enhancements

- Add support for advanced natural language understanding.
- Provide additional movie details, such as cast and crew information.
- Improve the conversational flow of the assistant for more interactive communication.

## Contributions

Contributions are welcome! Feel free to fork this repository, create a new branch, and open a pull request to suggest any enhancements.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

