# Music Recommendation System 🎵
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Jupyter Notebook](https://img.shields.io/badge/jupyter-%23FA0F00.svg?style=for-the-badge&logo=jupyter&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.2.0-FF4B4B.svg?style=flat&logo=Streamlit&logoColor=white)




🔮 Explore personalized music recommendations with this ML-powered system. Utilizing Spotify data, TF-IDF vectorization, and cosine similarity, discover your next favorite song effortlessly!

## Table of Contents

1. [Dataset Download](#dataset-download)
2. [Libraries Used](#libraries-used)
3. [How to Install and Run the Project](#how-to-install-and-run-the-project)
4. [How to Use the Project](#how-to-use-the-project)
5. [Results](#results)

## Dataset Download

- Download the dataset from [Kaggle: Spotify Million Song Dataset](https://www.kaggle.com/datasets/notshrirang/spotify-million-song-dataset).

## Libraries Used

- **pandas** -  Used for data manipulation and analysis.
- **nltk** - Provides natural language processing tools for text data.
- **scikit-learn** - Implements machine learning algorithms for TF-IDF vectorization and cosine similarity.
- **streamlit** - Utilized for creating an interactive web application.
- **spotipy** - Used to interact with the Spotify API for song information.

## How to Install and Run the Project

1. Clone the repository:

   ```bash
   git clone https://github.com/nithishravuvari/Music-Recommendation-System.git

2. Navigate to the project directory:
   ```bash
    cd music-recommendation-system
3. Install the required dependencies:
   ```bash
    pip install -r requirements.txt
4. Run the recommendation model script:
   ```bash
    python recommendation_model.ipynb
5. Run the web hosting script:
   ```bash
    streamlit run app.py

## How to Use the Project

- Open the web application by navigating to http://localhost:8501 in your web browser.

- Select a song from the dropdown menu.

- Click the "Show Recommendation" button to view recommended songs.

- The recommended songs along with their album covers will be displayed.

## Results
![Screenshot 2024-03-11 113306](https://github.com/nithishravuvari/Music-Recommendation-System/assets/104012893/a632f9b4-f2cf-4cce-aa70-30c3010a5efb)
![image](https://github.com/nithishravuvari/Music-Recommendation-System/assets/104012893/e9e20cc6-2b9f-43dd-abe7-adbac410594f)







