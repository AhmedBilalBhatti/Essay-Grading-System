from transformers import BartTokenizer, BartForConditionalGeneration
from gensim import corpora, models
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

tokenizer = BartTokenizer.from_pretrained('facebook/bart-large-cnn')
model = BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn')


def topic_modelling(text):
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(text)
    filtered_text = [w for w in word_tokens if not w in stop_words]

    texts = [filtered_text]
    dictionary = corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]

    lda_model = models.LdaModel(corpus, num_topics=3, id2word = dictionary, passes=50)
    topics = lda_model.print_topics(num_words=10)
    for topic in topics:
        print(topic)

    inputs = tokenizer.encode(text, return_tensors='pt')
    summary_ids = model.generate(inputs, num_beams=4, max_length=20, early_stopping=True)
    final = [tokenizer.decode(g, skip_special_tokens=True, clean_up_tokenization_spaces=False) for g in summary_ids]
    final_string = " ".join(final)
    final_resp = final_string.split('.')[0] + '.'
    return final_resp