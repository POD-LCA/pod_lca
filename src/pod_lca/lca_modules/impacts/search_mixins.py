__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from functools import lru_cache
from numpy import abs
from numpy import array
from numpy import sort
from pandas import DataFrame

try:
    from sklearn.cluster import KMeans
    from sklearn.feature_extraction.text import TfidfVectorizer
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

    nltk.download("wordnet", quiet=True)
    nltk.download("omw-1.4", quiet=True)
    nltk.download("punkt", quiet=True)
    nltk.download("punkt_tab", quiet=True)

    NLTK_IMPORTED = True
except ImportError:
    NLTK_IMPORTED = False


@lru_cache(maxsize=50000)
def _cached_synsets(word, pos=None):
    return wordnet.synsets(word, pos=pos)


def expand_search_terms(search_term, data_set, max_edit_distance=2, max_senses=1, limit_to_noun=False):
    """Expand search term by correcting misspellings, adding synonyms, and stemming/lemmatizing.

    Parameters
    ----------
    search_term : str
        String looked-up.
    data_set : set
        The dataset on which the search is done.
    max_edit_distance : int
        Edit distance considered in correcting spelling mistakes.
    max_senses : int
        How many Wordnet senses (i.e., levels of depth) to consider when looking for synonyms.
    limit_to_noun : bool
        If true, limit the search terms to nouns only.

    Returns
    -------
    list of str
        Expanded list of search terms.
    """
    if not SKLEARN_IMPORTED or not NLTK_IMPORTED:
        raise ImportError("Please install the 'nltk' and 'sklearn' packages to use the search methods.")

    lemmatizer = WordNetLemmatizer()
    stemmer = PorterStemmer()

    tokens = nltk.word_tokenize(search_term.lower())
    expanded = set(tokens)
    add = expanded.add

    # Correct spelling
    for word in tokens:
        closest = min(data_set, key=lambda w: edit_distance(word, w))
        if edit_distance(word, closest) <= max_edit_distance:
            add(closest)

    # Check synonyms
    for word in tokens:
        synsets = _cached_synsets(word, "n")[:max_senses] if limit_to_noun else _cached_synsets(word)[:max_senses]
        for syn in synsets:
            lemmas = syn.lemmas()
            for lemma in lemmas:
                name = lemma._name
                add(name.replace("_", " "))

    # Stemming and lemmatization
    stems = {stemmer.stem(w) for w in expanded}
    lemmas = {lemmatizer.lemmatize(w) for w in expanded}
    expanded |= stems | lemmas

    return list(expanded)


def rank_entries(products, search_terms, support_data_set=None, support_data_weight=0.25, max_returns=25):
    """Rank products based on TF-IDF similarity to search terms.

    Parameters
    ----------
    products : ~pandas.Series
        Products being ranked.
    search_terms : list of str
        List of search terms being matched.
    support_data_set : ~pandas.Series
        Additional set of product information. This should be in the same order as products.
    support_data_weight : float
        The weightage given to the similarity of support data to search terms.
    max_returns : int
        Number of top ranked products returned.

    Returns
    -------
    ~pandas.DataFrame
        Ranked list of products with similarity values.
    """
    if not SKLEARN_IMPORTED or not NLTK_IMPORTED:
        raise ImportError("Please install the 'nltk'  and 'sklearn' packages to use the search methods.")

    docs = products.astype(str).tolist()
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(docs + [" ".join(search_terms)])

    search_vec = tfidf_matrix[-1]
    doc_vecs = tfidf_matrix[:-1]
    scores = cosine_similarity(search_vec, doc_vecs)[0]

    if support_data_set is not None:
        support_docs = support_data_set.astype(str).tolist()
        vectorizer = TfidfVectorizer(stop_words="english")
        tfidf_matrix = vectorizer.fit_transform(support_docs + [" ".join(search_terms)])

        search_vec = tfidf_matrix[-1]
        doc_vecs = tfidf_matrix[:-1]
        support_scores = cosine_similarity(search_vec, doc_vecs)[0]

    ranked = (
        DataFrame(
            {
                "product": docs,
                "similarity": (
                    scores
                    if support_data_set is None
                    else (scores * (1 - support_data_weight)) + (support_scores * support_data_weight)
                ),
            }
        )
        .loc[lambda df: df["similarity"] > 0]
        .sort_values(by="similarity", ascending=False)
        .head(max_returns)
        .reset_index(drop=True)
    )

    return ranked


def adaptive_kmeans_cutoff(products, impact_scores, n_initial=5, k_initial=2, k_max=3, move_thresh=0.1):
    """Dynamically find cutoff in ranked scores using adaptive k-means clustering.

    Parameters
    ----------
    products: ~pandas.DataFrame
        Ranked list of products with similarity values.
    impact_scores : ~numpy.ndarray
        Impact scores sorted in the descending similarity scores.
    n_initial : int
        Number of top products to start clustering with.
    k_initial : int
        Initial number of clusters.
    k_max : int
        Maximum number of clusters.
    move_thresh : float
        Threshold for mean shift before stopping.

    Returns
    -------
    ~pandas.DataFrame
            Ranked list of products with impact and similarity values.
    """
    impact_scores = array(impact_scores).reshape(-1, 1)
    prev_means = None
    k = k_initial

    # cluster by impact
    for i in range(n_initial, len(impact_scores) + 1):
        subset = impact_scores[:i]
        kmeans = KMeans(n_clusters=k, n_init="auto", random_state=0).fit(subset)
        means = sort(kmeans.cluster_centers_.flatten())

        if prev_means is not None:
            move_max = max(abs(means - prev_means) / prev_means)
            if move_max > move_thresh:
                if k < k_max:
                    k += 1
                    means = None
                else:  # clusters have stabilized or diverged
                    cutoff_index = i - 1
                    subset_scores = impact_scores[:cutoff_index]
                    items = products[:cutoff_index]
                    kmeans = KMeans(n_clusters=k, n_init="auto", random_state=0).fit(subset_scores)
                    cluster_labels = kmeans.labels_
                    break
        prev_means = means
    else:  # only single bin possible
        cutoff_index = len(impact_scores)
        subset_scores = impact_scores[:cutoff_index]
        items = products[:cutoff_index]
        cluster_labels = array([0] * len(impact_scores))

    df = DataFrame(
        {
            "item": items["product"].tolist(),
            "impact": subset_scores.flatten(),
            "similarity": items["similarity"].tolist(),
            "cluster": cluster_labels,
        }
    )

    # order by similarity
    cluster_mean_score = df.groupby("cluster")["similarity"].max().to_dict()
    df["cluster_mean"] = df["cluster"].map(cluster_mean_score)
    df_sorted = df.sort_values(["cluster_mean", "similarity"], ascending=[False, False]).reset_index(drop=True)
    df_sorted = df_sorted.drop(columns=["cluster", "cluster_mean"])

    return df_sorted


if __name__ == "__main__":
    pass
