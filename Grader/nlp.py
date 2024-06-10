import nltk
# nltk.download('stopwords')
# nltk.download('punkt')

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
    total_grade = 0
    total_chunks = len(chunks)
    total_errors = 0
    all_uncommon_words = set()
    total_punctuation = 0
    sentiment_scores = []
    sentiment_labels = []

    for chunk in chunks:
        sentiment = sentiment_analysis(chunk)
        grade = int(sentiment[0]['label'].split()[0])
        total_grade += grade
        sentiment_scores.append(sentiment[0]['score'])
        sentiment_labels.append(sentiment[0]['label'])

        matches = tool.check(chunk)
        total_errors += len(matches)

        words = chunk.split()
        common_words = set(["the", "and", "of", "to", "in", "a", "is", "for", "that", "with", "on", "as"])
        uncommon_words = set(words) - common_words
        all_uncommon_words.update(uncommon_words)
        total_punctuation += sum([1 for char in chunk if char in [".", ",", "!", "?", ";", ":"]])

    avg_grade = total_grade / total_chunks
    avg_sentiment = sum(sentiment_scores) / len(sentiment_scores)
    sentiment_label_counts = {label: sentiment_labels.count(label) for label in set(sentiment_labels)}
    sentiment_label = max(sentiment_label_counts, key=sentiment_label_counts.get)
    detailed_uncommon_words = list(all_uncommon_words - set(['media', 'social', 'society', 'information', 'people', 'health', 'negative', 'polarization', 'important', 'misinformation']))

    return avg_grade, total_errors, len(all_uncommon_words), total_punctuation, detailed_uncommon_words, avg_sentiment, sentiment_label
def improvement_suggestions(essay):
    suggestions = []
    _, total_errors, _, _, _, _ = grade_and_assess_mistakes(essay)

    if total_errors > 10:
        suggestions.append("Your essay contains numerous grammatical errors. Consider using grammar-checking tools to review your essay.")
    else:
        suggestions.append("Your essay has few grammatical errors. Keep up the good work!")

    _, _, num_uncommon_words, _, detailed_uncommon_words, _ = grade_and_assess_mistakes(essay)
    
    if num_uncommon_words > 10:
        suggestions.append("Your essay contains many uncommon words. Try to use simpler language to ensure clarity.")
    else:
        suggestions.append("Your essay uses common words appropriately. Great job!")

    return suggestions

def get_top_words(model, feature_names, n_top_words, topic_idx):
    return [feature_names[i] for i in model.components_[topic_idx].argsort()[:-n_top_words - 1:-1]]