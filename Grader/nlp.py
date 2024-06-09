import nltk
nltk.download('stopwords')
nltk.download('punkt')

import language_tool_python
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation

# Load the Hugging Face model for sentiment analysis
tokenizer = AutoTokenizer.from_pretrained("nlptown/bert-base-multilingual-uncased-sentiment")
model = AutoModelForSequenceClassification.from_pretrained("nlptown/bert-base-multilingual-uncased-sentiment")
sentiment_analysis = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

# LanguageTool for grammar and vocabulary checking
tool = language_tool_python.LanguageTool('en-US')


def split_into_chunks(text, chunk_size=512):
    chunk_size -= 2
    tokens = tokenizer(text, return_tensors='pt', truncation=False).input_ids[0]
    chunks = [tokens[i:i + chunk_size] for i in range(0, len(tokens), chunk_size)]
    return [tokenizer.decode(chunk, skip_special_tokens=False) for chunk in chunks]

# Function to grade and assess mistakes in an essay
def grade_and_assess_mistakes(essay):
    chunks = split_into_chunks(essay, chunk_size=512)

    # Initialize aggregate results
    total_grade = 0
    total_chunks = len(chunks)
    total_errors = 0
    all_uncommon_words = set()
    total_punctuation = 0
    sentiment_scores = []
    sentiment_labels = []

    # Process each chunk
    for chunk in chunks:
        sentiment = sentiment_analysis(chunk)
        grade = int(sentiment[0]['label'].split()[0])  # Extract the grade from the label (1-5)
        total_grade += grade
        sentiment_scores.append(sentiment[0]['score'])  # Capture sentiment score
        sentiment_labels.append(sentiment[0]['label'])  # Capture sentiment label

        # Assess mistakes in the chunk
        matches = tool.check(chunk)
        total_errors += len(matches)

        words = chunk.split()
        common_words = set(["the", "and", "of", "to", "in", "a", "is", "for", "that", "with", "on", "as"])
        uncommon_words = set(words) - common_words
        all_uncommon_words.update(uncommon_words)

        total_punctuation += sum([1 for char in chunk if char in [".", ",", "!", "?", ";", ":"]])

    # Calculate average grade
    avg_grade = total_grade / total_chunks

    # Calculate average sentiment score
    avg_sentiment = sum(sentiment_scores) / len(sentiment_scores)

    # Determine sentiment label based on the distribution of sentiment labels
    sentiment_label_counts = {label: sentiment_labels.count(label) for label in set(sentiment_labels)}
    sentiment_label = max(sentiment_label_counts, key=sentiment_label_counts.get)

    # Detailed uncommon words (for more specific output)
    detailed_uncommon_words = list(all_uncommon_words - set(['media', 'social', 'society', 'information', 'people', 'health', 'negative', 'polarization', 'important', 'misinformation']))

    return avg_grade, total_errors, len(all_uncommon_words), total_punctuation, detailed_uncommon_words, avg_sentiment, sentiment_label

# Function to predict topic of an essay using LDA
def predict_topic(essay):
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    essay_tfidf = tfidf_vectorizer.fit_transform([essay])

    lda = LatentDirichletAllocation(n_components=5, random_state=42)
    lda.fit(essay_tfidf)

    topic_distribution = lda.transform(essay_tfidf)
    predicted_topic_index = topic_distribution.argmax()

    tfidf_feature_names = tfidf_vectorizer.get_feature_names_out()
    topic_words = get_top_words(lda, tfidf_feature_names, 10, predicted_topic_index)

    return predicted_topic_index, topic_words

# Function to get top words for a topic
def get_top_words(model, feature_names, n_top_words, topic_idx):
    return [feature_names[i] for i in model.components_[topic_idx].argsort()[:-n_top_words - 1:-1]]

# Take user input
new_essay = input("Enter your essay: ")

# Grade, assess mistakes, and predict topic for the input essay
grade, num_errors, num_uncommon_words, num_punctuation, detailed_uncommon_words, avg_sentiment, sentiment_label = grade_and_assess_mistakes(new_essay)
predicted_topic_index, topic_words = predict_topic(new_essay)

# Print results
print(f"\nPredicted Grade: {grade} out of 5")
print(f"Average Sentiment Score: {avg_sentiment}")
print(f"Sentiment Label: {sentiment_label}")
print(f"Number of Grammatical Errors: {num_errors}")
print(f"Number of Uncommon Words: {num_uncommon_words}")
print(f"Number of Punctuation Marks: {num_punctuation}")
print(f"Detailed Uncommon Words: {detailed_uncommon_words}")
print(f"Predicted Topic Index: {predicted_topic_index}")
print(f"Top words for Predicted Topic: {topic_words}")