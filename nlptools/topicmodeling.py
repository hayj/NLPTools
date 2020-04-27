from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.datasets import fetch_20newsgroups
from sklearn.decomposition import NMF, LatentDirichletAllocation
from sklearn import metrics
from systemtools.printer import *
from nlptools.basics import *
from datatools.jsonutils import *
from systemtools.location import *
from machinelearning.metrics import *
from datastructuretools.processing import *


def nmfFeatures\
(
    # Data:
    docs,
    trainDocs=None,
    # Parameters:
    min_df=1,
    max_df=1.0,
    max_features=None,
    sublinear_tf=True,
    stop_words=None,
    useTrainDocs=False,
    n_components=100,
    init='nndsvd',
    l1_ratio=0,
    alpha=0.1,
    lowercase=True,
    # Others:
    max_iter=200,
    random_state=1,
    # Misc:
    logger=None, verbose=True,
):
    """
    	Docs must be a list of docs, sentences are not tokenized. If docs is a list of list, the function will consider the doc already tokenized by words.
        This function return TFIDF+NMF features of given docs
    """
    if useTrainDocs:
        assert trainDocs is not None
        assert len(trainDocs) > 0
        # if isinstance(trainDocs[0], list):
        #     trainDocs = flattenLists(trainDocs)
    assert len(docs) > 0
    # if isinstance(docs[0], list):
    #     docs = flattenLists(docs)
    tfidf_vectorizer = TfidfVectorizer\
    (
    	lowercase=lowercase,
        min_df=min_df,
        max_df=max_df,
        max_features=max_features,
        stop_words=stop_words,
        sublinear_tf=sublinear_tf,
        tokenizer=None if isinstance(docs[0], str) else lambda x: x,
        preprocessor=None if isinstance(docs[0], str) else lambda x: x,
    )
    if useTrainDocs:
        docs = docs + trainDocs 
    tfidf = tfidf_vectorizer.fit_transform(docs)
    tfidf_feature_names = tfidf_vectorizer.get_feature_names()
    nmf = NMF\
    (
        n_components=n_components,
        random_state=random_state,
        alpha=alpha,
        l1_ratio=l1_ratio,
        init=init,
        max_iter=max_iter,
    ).fit(tfidf)
    vectors = nmf.transform(tfidf)
    if useTrainDocs:
        vectors = list(vectors)
        vectors = vectors[:-len(trainDocs)]
        vectors = np.array(vectors)
    return np.array(vectors)


def nmfClustering\
(
    # Data:
    docs, labels,
    # Misc:
    logger=None, verbose=True,
    # NMF parameters:
    trainDocs=None,
    **nmfKwargs,
):
    from newssource.metrics.utils import pairwiseCosineSimilarity
    from newssource.metrics.ndcg import pairwiseSimNDCG
    report = dict()
    data = nmfFeatures(docs, **mergeDicts(nmfKwargs,
                        {'trainDocs': trainDocs, 'logger': logger, 'verbose': verbose}))
    simMatrix = pairwiseCosineSimilarity(data)
    score = pairwiseSimNDCG(simMatrix, labels)
    report['simrank'] = score
    score = metrics.calinski_harabasz_score(data, labels)
    report['calhar'] = score
    score = metrics.davies_bouldin_score(data, labels)
    report['davb'] = score
    report['params'] = nmfKwargs
    h = objectToHash(nmfKwargs)[:5]
    report['hash'] = h
    report['model'] = 'nmf-' + h
    return report




def ldaFeatures\
(
    # Data:
    docs,
    trainDocs=None,
    # Parameters for CountVectorizer:
    min_df=1,
    max_df=1.0,
    max_features=None,
    stop_words=None,
    # Other parameters:
    useTrainDocs=False,
    # Parameters for LatentDirichletAllocation:
    learning_method='online',
    learning_offset=1.0,
    n_components=100,
    lowercase=True,
    # Others parameters (only for performance or computation speed etc.):
    n_jobs=1, # 8
    max_iter=30,
    random_state=1,
    # Misc:
    logger=None, verbose=True,
):
    """
        This function return LDA features of given docs
    """
    if useTrainDocs:
        assert trainDocs is not None
        assert len(trainDocs) > 0
        # if isinstance(trainDocs[0], list):
        #     trainDocs = flattenLists(trainDocs)
    assert len(docs) > 0
    # if isinstance(docs[0], list):
    #     docs = flattenLists(docs)
    tf_vectorizer = CountVectorizer\
    (
        lowercase=lowercase,
        min_df=min_df,
        max_df=max_df,
        max_features=max_features,
        stop_words=stop_words,
        tokenizer=None if isinstance(docs[0], str) else lambda x: x,
        preprocessor=None if isinstance(docs[0], str) else lambda x: x,
    )
    if useTrainDocs:
        docs = docs + trainDocs
    tf = tf_vectorizer.fit_transform(docs)
    lda = LatentDirichletAllocation\
    (
        n_components=n_components,
        max_iter=max_iter,
        learning_method=learning_method,
        learning_offset=learning_offset,
        random_state=random_state,
        n_jobs=n_jobs,
    )
    lda.fit(tf)
    vectors = lda.transform(tf)
    if useTrainDocs:
        vectors = list(vectors)
        vectors = vectors[:-len(trainDocs)]
        vectors = np.array(vectors)
    return np.array(vectors)


def ldaClustering\
(
    # Data:
    docs, labels,
    logger=None, verbose=True,
    # LDA parameters:
    trainDocs=None,
    **ldaKwargs,
):
    from newssource.metrics.utils import pairwiseCosineSimilarity
    from newssource.metrics.ndcg import pairwiseSimNDCG
    report = dict()
    data = ldaFeatures(docs, **mergeDicts(ldaKwargs,
                        {'trainDocs': trainDocs, 'logger': logger, 'verbose': verbose}))
    simMatrix = pairwiseCosineSimilarity(data)
    score = pairwiseSimNDCG(simMatrix, labels)
    report['simrank'] = score
    score = metrics.calinski_harabasz_score(data, labels)
    report['calhar'] = score
    score = metrics.davies_bouldin_score(data, labels)
    report['davb'] = score
    report['params'] = ldaKwargs
    h = objectToHash(ldaKwargs)[:5]
    report['hash'] = h
    report['model'] = 'nmf-' + h
    return report








