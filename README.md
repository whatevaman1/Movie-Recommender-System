# Movie Recommender System

## Project Overview
Movie Recommender System is a Streamlit-based web application that delivers personalized movie recommendations, trending movies, top-rated films, and a robust search feature using data from TMDB. The app leverages content-based filtering alongside real-time API data to create an engaging, interactive user experience.

This repository includes the application code and a Jupyter Notebook that guides you through data preprocessing. You will need to download the TMDB-5000 dataset from Kaggle and run the notebook to generate the processed data files required by the app.

## Features
- **Personalized Recommendations:** Get 5 movie suggestions based on your selected title using a precomputed similarity matrix.
- **TMDB Integration:** Real-time data fetching for:
  - **Trending Movies:** Weekly updated trending list.
  - **Top Rated Movies:** Explore all-time highest rated films.
  - **Movie Search:** Find any movie in TMDB's extensive database.
- **Interactive UI:**
  - Responsive grid layout with smooth hover effects.
  - Clickable movie posters and titles linking directly to TMDB.
  - Detailed overview expanders for movie plots.
  - A sleek, dark-themed design.
- **Data Preprocessing Notebook:** Follow the provided Jupyter Notebook to process the raw TMDB-5000 dataset and generate the necessary pickle files.

## Prerequisites
- Python 3.9+
- Kaggle account (to download the dataset)

## Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/Movie-Recommender-System.git
cd Movie-Recommender-System
```
### 2. Download the TMDB-5000 Dataset from Kaggle
- Visit the [TMDB 5000 Movie Dataset](https://www.kaggle.com/datasets/tmdb/tmdb-5000-movie-dataset) page.
- Download the dataset files:
  - `tmdb_5000_movies.csv`
  - `tmdb_5000_credits.csv`
- Place these CSV files in the project root directory.

### 3. Data Preprocessing
- Open the Jupyter Notebook `Movie-Recommender-System.ipynb` located in the repository.
- Follow the steps in the notebook to:
  - Load and clean the CSV files.
  - Generate the movie dictionary (`movie_dict.pkl`).
  - Compute the similarity matrix (`similarity.pkl`).
- Ensure that `movie_dict.pkl` and `similarity.pkl` are created and saved in the project root.

### 4. Set Up the Environment

1. **Create a Virtual Environment (Recommended):**
   ```bash
   python -m venv .venv
   ```
2. **Activate the Virtual Environment:**
   - On Windows:
     ```powershell
     .\.venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source .venv/bin/activate
     ```
3. **Install Dependencies:**
   ```bash
   pip install streamlit pandas requests python-dotenv
   pip install -r requirements.txt
   ```

### 5. Configure Environment Variables
- Create a `.env` file in the project root with your TMDB API key:
  ```env
  TMDB_API_KEY=your_api_key_here
  ```

### 6. Run the Application
```bash
streamlit run app.py
```

## Project Structure
```
Movie-Recommender-System/
├── app.py                          # Main Streamlit application
├── Movie-Recommender-System.ipynb  # Data preprocessing notebook
├── movie_dict.pkl                  # Processed movie data (generated by notebook)
├── similarity.pkl                  # Similarity matrix (generated by notebook)
├── tmdb_5000_movies.csv            # Raw movie dataset (download from Kaggle)
├── tmdb_5000_credits.csv           # Raw credits dataset (download from Kaggle)
├── requirements.txt                # Python dependencies
├── .env                            # Environment variables
├── .gitignore                      # Excludes sensitive files (e.g., .env, .venv)
```

## Contributing
Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature/your-feature
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add brief description"
   ```
4. Push your branch:
   ```bash
   git push origin feature/your-feature
   ```
5. Open a pull request describing your changes.

## Contact
For queries or contributions, contact [amans11221@gmail.com] or visit the GitHub repository.
