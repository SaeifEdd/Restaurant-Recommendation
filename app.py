import os
import streamlit as st
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter
import seaborn as sns

# Set environment variables for Streamlit
os.environ["STREAMLIT_WATCH_USE_POLLING"] = "true"

# Configure page
st.set_page_config(
    page_title="Restaurant Review Analytics",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .reportview-container {
        background: #f0f2f6;
    }
    .sidebar .sidebar-content {
        background: #f9f9f9;
    }
    .metric-label {
        font-weight: bold;
    }
    h1, h2, h3 {
        color: #1E3A8A;
    }
</style>
""", unsafe_allow_html=True)


# Load data with caching
@st.cache_data(show_spinner=False)
def load_clean_revs():
    try:
        return pd.read_csv("data/clean_rews.csv")
    except Exception as e:
        st.error(f"Error loading data: {e}")
        # Return empty DataFrame with expected columns
        return pd.DataFrame(columns=['Name', 'caption', 'rating', 'sentiment_label'])


# Sidebar: Restaurant selection
st.sidebar.title("🍽️ Restaurant Review Analysis")
st.sidebar.markdown("---")
# st.sidebar.info(models.get("device_info", "Device information not available"))

df = load_clean_revs()

# Check if data loaded successfully
if df.empty:
    st.error("No data available. Please check your data file.")
    st.stop()

# Continue with filters
st.sidebar.title("Filters")
selected_restaurant = st.sidebar.selectbox(
    "Choose a Restaurant",
    df['Name'].unique()
)

# Filter data for selected restaurant
restaurant_data = df[df['Name'] == selected_restaurant]

# Main panel
st.title(f"🍽️ {selected_restaurant} Analytics")

# Section 1: Key Stats
st.header("📈 Basic Stats")
col1, col2, col3 = st.columns(3)

# Add error handling for metrics
try:
    col1.metric("Average Rating", f"{restaurant_data['rating'].mean():.1f} ⭐")
    col2.metric("Total Reviews", len(restaurant_data))

    positive_count = restaurant_data['sentiment_label'].value_counts().get('positive', 0)
    negative_count = restaurant_data['sentiment_label'].value_counts().get('negative', 0)
    ratio_text = f"{positive_count}:{max(negative_count, 1)}"
    col3.metric("Positive/Negative Ratio", ratio_text)
except Exception as e:
    st.error(f"Error calculating metrics: {e}")

# Section 2: Word Cloud
st.header("📊 Reviews Word Cloud")
try:
    if not restaurant_data.empty:
        all_reviews = " ".join(restaurant_data['caption'])
        if all_reviews.strip():  # Check if there's any text
            wordcloud = WordCloud(
                width=800,
                height=400,
                background_color='black',
                colormap='Spectral',
                contour_color='white',
                contour_width=1,
                random_state=42
            ).generate(all_reviews)

            plt.figure(figsize=(10, 5))
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis("off")
            st.pyplot(plt)
        else:
            st.info("No review text available to generate word cloud.")
    else:
        st.info("No reviews available for this restaurant.")
except Exception as e:
    st.error(f"Error generating word cloud: {e}")

# Section 3: Top Words
st.header("📊 Top Words in Reviews")
try:
    if not restaurant_data.empty:
        all_words = ' '.join(restaurant_data['caption']).split()

        # Filter out common stop words
        stop_words = ['the', 'and', 'a', 'to', 'is', 'in', 'that', 'it', 'with', 'for', 'as', 'was', 'on', 'are',
                      'this', 'be', 'at', 'by', 'i', 'you', 'of']
        filtered_words = [word.lower() for word in all_words if word.lower() not in stop_words and len(word) > 2]

        word_counts = Counter(filtered_words)
        most_common_words = word_counts.most_common(10)
        common_words_df = pd.DataFrame(most_common_words, columns=['Word', 'Frequency'])

        plt.style.use('dark_background')
        fig, ax = plt.subplots(figsize=(12, 6))

        # Create the barplot
        sns.barplot(
            x='Frequency',
            y='Word',
            data=common_words_df,
            hue='Word',  # Color by word
            palette='magma',
            errorbar=None,
            legend=False,  # Hide legend
            ax=ax
        )

        # Customize the plot
        ax.set_title(
            'Most Common Words in Reviews',
            fontsize=18,
            fontweight='bold',
            color='white'
        )
        ax.set_xlabel('Frequency', fontsize=14, color='lightgray')
        ax.set_ylabel('Words', fontsize=14, color='lightgray')

        # Grid and tick styling
        ax.grid(axis='x', color='gray', linestyle='--', linewidth=0.7)
        ax.tick_params(axis='x', colors='lightgray')
        ax.tick_params(axis='y', colors='lightgray')

        fig.patch.set_facecolor('black')
        ax.set_facecolor('black')

        # Display in Streamlit
        st.pyplot(fig)
    else:
        st.info("No reviews available to analyze word frequency.")
except Exception as e:
    st.error(f"Error analyzing word frequency: {e}")

# Section 4: LLM-Generated Pros/Cons
st.header("🤖 AI-Generated Pros & Cons")

try:
    with st.spinner("Analyzing reviews with AI models..."):
        # Import here to avoid circular import issues
        from summarize import extract_pros_and_cons

        # Extract reviews
        reviews = restaurant_data['caption'].tolist()

        # Get pros and cons summary
        summary = extract_pros_and_cons(reviews)

        # Display summary
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("✅ Pros")
            st.markdown(summary["pros"])

        with col2:
            st.subheader("❌ Cons")
            st.markdown(summary["cons"])

except Exception as e:
    st.error(f"Error generating pros and cons: {e}")

# Footer
st.markdown("---")
st.markdown("Restaurant Review Analytics Dashboard | Created with Streamlit")
