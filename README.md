# Restaurant Review Analytics

A data-driven dashboard for analyzing restaurant reviews using NLP and AI techniques.


## Features

- **Interactive Dashboard**: Select restaurants to view personalized analytics
- **Sentiment Analysis**: Categorize reviews as positive or negative
- **Word Cloud Visualization**: Visualize the most common terms in reviews
- **AI-Generated Summaries**: Get pros and cons extracted from reviews using LLM
- **Comprehensive Analytics**: Explore ratings, reviews, and sentiment ratios

## Tech Stack

- **Data Collection**: SerpAPI, Google Maps Scraper
- **Data Processing**: Python, Pandas, NLTK
- **Visualization**: Streamlit, Matplotlib, Seaborn
- **NLP & AI**: WordCloud, Sentiment Analysis, LLM for summary generation

## Project Structure

```
restaurant-reviews/
├── data/                   # Restaurant reviews and processed data
├── notebooks/              # Jupyter notebooks for data exploration
├── app.py                  # Main Streamlit dashboard
├── summarize.py            # AI summary generation module
├── requirements.txt        # Project dependencies
└── README.md               # Project documentation
```

## Getting Started

### Prerequisites

- Python 3.8+
- Required Python packages (install with `pip install -r requirements.txt`)

## Data Collection Process

### Step 1: Restaurant Basic Information
- Collected place IDs, names, and addresses using SerpAPI (free trial)

### Step 2: Reviews Collection
- Utilized [Google Maps Scraper](https://github.com/gaspa93/googlemaps-scraper/tree/master) to extract reviews
- Created URLs file by combining restaurant names and addresses
- Modified the scraper script to include restaurant urls in the output

## Processing + cleaning + exploring
- ratings exploration (check notebook)
- reviews cleaning, exploration

## Dashboard Features

### Restaurant Selection
- Filter analysis by selecting specific restaurants

### Basic Statistics
- Average ratings
- Total review count
- Positive-to-negative review ratio

### Visual Analytics
- Word clouds showing prevalent terms in reviews
- Most frequent words bar chart

### AI-Powered Insights
- Automatically generated pros and cons based on review content


## Future Improvements
- Add geographic visualization of restaurants
- Add restaurants Stats using more filters
- Add an ML model to classify restaurants and recommend based on user taste
- Enhance AI summary generation with more advanced NLP techniques


## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- [SerpAPI](https://serpapi.com/) 
- [Google Maps Scraper](https://github.com/gaspa93/googlemaps-scraper)
- Streamlit for the dashboard

