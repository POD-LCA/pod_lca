
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from numpy import abs
from numpy import array
from numpy import mean
from numpy import sort
from pandas import DataFrame

try:
    from sklearn.cluster import KMeans
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics import pairwise_distances_argmin_min
    from sklearn.metrics.pairwise import cosine_similarity

    SKLEARN_IMPORTED = True
except ImportError:
    SKLEARN_IMPORTED = False

try:
    import nltk
    from nltk.corpus import wordnet
    from nltk.metrics import edit_distance
    from nltk.stem import PorterStemmer
    from nltk.stem import WordNetLemmatizer

    nltk.download('wordnet', quiet=True)
    nltk.download('omw-1.4', quiet=True)
    nltk.download('punkt', quiet=True)
    nltk.download('punkt_tab', quiet=True)

    NLTK_IMPORTED = True
except ImportError:
    NLTK_IMPORTED = False



def expand_search_terms(search_term, vocabulary=None, max_edit_distance=3):
    """Expand search term by correcting misspellings, adding synonyms, and stemming/lemmatizing.
    """
    if not SKLEARN_IMPORTED or not NLTK_IMPORTED:
        raise ImportError("Please install the 'nltk'  and 'sklearn' packages to use the search methods.")
    
    lemmatizer = WordNetLemmatizer()
    stemmer = PorterStemmer()
    
    tokens = nltk.word_tokenize(search_term.lower())
    expanded = set(tokens)

    # Correct spelling
    if vocabulary:
        for word in tokens:
            closest = min(vocabulary, key=lambda w: edit_distance(word, w))
            if edit_distance(word, closest) <= max_edit_distance:
                expanded.add(closest)

    # Check synonyms
    for word in tokens:
        for syn in wordnet.synsets(word):
            for lemma in syn.lemmas():
                expanded.add(lemma.name().replace('_', ' '))

    # Stemming and Lemmatization
    stems = {stemmer.stem(w) for w in expanded}
    lemmas = {lemmatizer.lemmatize(w) for w in expanded}
    expanded |= stems | lemmas

    return list(expanded)

def rank_documents(series, search_terms, top_n=25):
    """Rank documents in a pandas Series based on TF-IDF similarity to search terms.
    """
    if not SKLEARN_IMPORTED or not NLTK_IMPORTED:
        raise ImportError("Please install the 'nltk'  and 'sklearn' packages to use the search methods.")
    
    docs = series.astype(str).tolist()
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(docs + [' '.join(search_terms)])

    # Last vector = search term vector
    search_vec = tfidf_matrix[-1]
    doc_vecs = tfidf_matrix[:-1]

    scores = cosine_similarity(search_vec, doc_vecs)[0]
    ranked =  (
        DataFrame({
            'product': docs,
            'similarity': scores
        })
        .loc[lambda df: df['similarity'] > 0]  # remove zero similarity items
        .sort_values(by='similarity', ascending=False)
        .head(top_n)
        .reset_index(drop=True)
    )

    return ranked

def adaptive_kmeans_cutoff(products, scores, start_i=5, k_init=2, max_k=3, move_thresh=0.05, impact_weight=0.5):
    """
    Dynamically find cutoff in ranked scores using adaptive k-means clustering.
    
    Parameters
    ----------
    scores : list or np.array
        Sorted descending cosine similarity or relevance scores.
    start_i : int
        Number of top scores to start clustering with.
    k_init : int
        Initial number of clusters.
    max_k : int
        Maximum allowed clusters.
    move_thresh : float
        Threshold for mean shift before stopping.
        
    Returns
    -------
    dict with:
        cutoff_index : int
        clusters : np.ndarray
        means : np.ndarray
    """
    scores = array(scores).reshape(-1, 1)
    prev_means = None
    k = k_init

    for i in range(start_i, len(scores) + 1):
        subset = scores[:i]
        kmeans = KMeans(n_clusters=k, n_init='auto', random_state=0).fit(subset)
        means = sort(kmeans.cluster_centers_.flatten())

        if prev_means is not None:
            move = mean(abs(means - prev_means[:len(means)]))
            if move > move_thresh:
                if k < max_k:
                    k += 1  # add a bin and re-evaluate
                    means = None
                else:
                    # Stop — clusters have stabilized or diverged
                    cutoff_index = i - 1
                    subset_scores = scores[:cutoff_index]
                    items = products[:cutoff_index]
                    kmeans = KMeans(n_clusters=k, n_init='auto', random_state=0).fit(subset_scores)
                    cluster_centers = kmeans.cluster_centers_
                    cluster_labels = kmeans.labels_
                    break
        prev_means = means
    else:
        # only single bin possible
        cutoff_index = len(scores)
        subset_scores = scores[:cutoff_index]
        items = products[:cutoff_index]
        cluster_labels = array([0] * len(scores))
        cluster_centers = array([[subset_scores.mean()]])

    # Compute distances to cluster centers
    _, distances = pairwise_distances_argmin_min(subset_scores, cluster_centers)
    
    df = DataFrame({
        'item': items['product'].tolist(),
        'impact': subset_scores.flatten(),
        'similarity': items['similarity'].tolist(),
        'cluster': cluster_labels,
        'distance_to_center': distances
    })
    
    # Order by cluster then distance to center
    cluster_stats = (
        df.groupby('cluster')[['impact', 'similarity']]
        .max()
        .reset_index()
    )
    cluster_stats['cluster_rank_value'] = (
        impact_weight * cluster_stats['impact'] + (1 - impact_weight) * cluster_stats['similarity'] # FIXME: This weighting scheme does not give a balanced view... try something else "Order by similarity cluster by GWP"
    )
    cluster_rank_map = cluster_stats.set_index('cluster')['cluster_rank_value'].to_dict()

    df['cluster_rank'] = df['cluster'].map(cluster_rank_map)
    df_sorted = df.sort_values(['cluster_rank', 'distance_to_center'], ascending=[False, True]).reset_index(drop=True)
    df_sorted = df_sorted.drop(columns=['cluster', 'distance_to_center', 'cluster_rank'])
    
    return df_sorted
