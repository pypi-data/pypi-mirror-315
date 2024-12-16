---
title: 'TextDescriptives: A Python package for calculating a large variety of metrics from text'
tags:
  - Python
  - natural language processing
  - spacy
  - feature extraction
authors:
  - name: Lasse Hansen
    orcid: 0000-0003-1113-4779
    corresponding: true
    affiliation: "1, 2, 3" # (Multiple affiliations must be quoted)
  - name: Ludvig Renbo Olsen
    orcid: 0009-0006-6798-7454
    affiliation: "4, 2"
  - name: Kenneth Enevoldsen
    orcid: 0000-0001-8733-0966
    affiliation: "2, 3"

affiliations:
 - name: Department of Affective Disorders, Aarhus University Hospital - Psychiatry, Aarhus, Denmark
   index: 1
 - name: Department of Clinical Medicine, Aarhus University, Aarhus, Denmark
   index: 2
 - name: Center for Humanities Computing, Aarhus University, Aarhus, Denmark
   index: 3
 - name: Department of Molecular Medicine (MOMO), Aarhus University, Aarhus, Denmark
   index: 4
date: 1 March 2023
bibliography: paper.bib
---

# Summary

Natural language processing (NLP) tasks often require a thorough understanding and description of the corpus. Document-level metrics can be used to identify low-quality data, assess outliers, or understand differences between groups. Further, text metrics have long been used in fields such as the digital humanities where e.g. metrics of text complexity are commonly used to analyse, understand and compare text corpora. However, extracting complex metrics can be an error-prone process and is rarely rigorously tested in research implementations. This can lead to subtle differences between implementations and reduces the reproducibility of scientific results.

`TextDescriptives` offers a simple and modular approach to extracting both simple and complex metrics from text. It achieves this by building on the `spaCy` framework [@honnibal_spacy_2020]. This means that `TextDescriptives` can easily be integrated into existing workflows while leveraging the efficiency and robustness of the `spaCy` library. The package has already been used for analysing the linguistic stability of clinical texts [@hansen_lexical_2022], creating features for predicting neuropsychiatric conditions [@hansen_automated_2023], and analysing linguistic goals of primary school students [@tannert_skriftsproglig_2023].

# Statement of need

Computational text analysis is a broad term that refers to the process of analyzing and understanding text data. This often involves calculating a set of metrics that describe relevant properties of the data. Dependent on the task at hand, this can range from simple descriptive statistics related to e.g. word or sentence length to complex measures of text complexity, coherence, or quality. This often requires drawing on multiple libraries and frameworks or writing custom code. This can be time-consuming and prone to bugs, especially with more complex metrics. 

`TextDescriptives` seeks to unify the extraction of document-level metrics, in a modular fashion. The integration with spaCy allows the user to seamlessly integrate `TextDescriptives` in existing pipelines as well as giving the `TextDescriptives` package access to model-based metrics such as dependency graphs and part-of-speech tags. The ease of use and the variety of available metrics allows researchers and practitioners to extend the granularity of their analyses within a tested and validated framework.

Implementations of the majority of the metrics included in `TextDescriptives` exist, but none as feature complete. The `textstat` library [@ward_textstat_2022] implements the same readability metrics, however, each metric has to be extracted one at a time with no interface for multiple extractions. `spacy-readability` [@holtzscher_spacy-readability_2019] adds readability metrics to `spaCy` pipelines, but does not work for new versions of `spaCy` (>=3.0.0). The `textacy` [@dewilde_textacy_2021] package has some overlap with `TextDescriptives`, but with a different focus. `TextDescriptives` focuses on document-level metrics, and includes a large number of metrics not included in `textacy` (dependency distance, coherence, and quality), whereas `textacy` includes components for preprocessing, information extraction, and visualization that are outside the scope of `TextDescriptives`. What sets `TextDescriptives` apart is the easy access to document-level metrics through a simple user-facing API and exhaustive documentation. 


# Features & Functionality

`TextDescriptives` is a Python package and provides the following `spaCy` pipeline components:

- `textdescriptives.descriptive_stats`: Calculates the total number of tokens, number of unique tokens, number of characters, and the proportion of unique tokens, as well as the mean, median, and standard deviation of token length, sentence length, and the number of syllables per token.
- `textdescriptives.readability`: Calculates the Gunning-Fog index, the SMOG index, Flesch reading ease, Flesch-Kincaid grade, the Automated Readability Index, the Coleman-Liau index, the Lix score, and the Rix score.
-`textdescriptives.dependency_distance`: Calculates the mean and standard deviation of the dependency distance (the average distance between a word and its head word), and the mean and the standard deviation of the proportion adjacent dependency relations on the sentence level. 
- `textdescriptives.pos_proportions`: Calculates the proportions of all part-of-speech tags in the documents. 
- `textdescriptives.coherence`: Calculates the first- and second-order coherence of the document based on word embedding similarity between sentences.
- `textdescriptives.information_theory`: Calculates the Shannon entropy and the perplexitiy of the documents.
- `textdescriptives.quality`: Calculates the text-quality metrics proposed in @rae_scaling_2022 and @raffel_exploring_2020. These measures can be used for filtering out low-quality text prior to model training or text analysis. These include heuristics such as the number of stop words, ratio of words containing alphabetic characters, proportion of lines ending with an ellipsis, proportion of lines starting with a bullet point, ratio of symbols to words, and whether the document contains a specified string (e.g. “lorem ipsum”), as well as repetitious text metrics such as the proportion of lines that are duplicates, the proportion of paragraphs in a document that are duplicates, the proportion of n-gram duplicates, and the proportion of characters in a document that are contained within the top n-grams. 


All the components can be added to an existing `spaCy` pipeline with a single line of code, and jointly extracted to a dataframe or dictionary with a single call to `textdescriptives.extract_{df|dict}(doc)`. 

To assist users who lack coding experience and to showcase the tool's capabilities, the core features of TextDescriptives are available as a web app on [https://huggingface.co/spaces/HLasse/textdescriptives](https://huggingface.co/spaces/HLasse/textdescriptives). With the web app, users can extract metrics from their own texts and download the results in a .csv file format.

# Example Use Cases

Descriptive statistics can be used to summarize and understand data, such as by exploring patterns and relationships within the data, getting a better understanding of the data set, or identifying any changes in the distribution of the data. Readability metrics, which assess the clarity and ease of understanding of written text, have a variety of applications, including the design of educational materials and the improvement of legal or technical documents [@dubay_principles_2004]. Dependency distance can be used as a measure of language comprehension difficulty or of sentence complexity and has been used for analysing properties of natural language or for similar purposes as readability metrics [@gibson_how_2019; @liu_dependency_2008]. The proportions of different parts of speech in a document have been found to be predictive of certain mental disorders and can also be used to assess the quality and complexity of text [@tang_natural_2021]. Semantic coherence, or the logical connection between sentences, has primarily been used in the field of computational psychiatry to predict the onset of psychosis or schizophrenia [@parola_speech_2022; @bedi_automated_2015], but it also has other applications in the digital humanities.  Measures of text quality are useful cleaning and identifying low-quality data [@rae_scaling_2022; @raffel_exploring_2020]. 


# Target Audience

The package is mainly targeted at NLP researchers and practitioners. In particular, researchers from fields new to NLP such as the digital humanities and social sciences as researchers might benefit from the readability metrics as well as the more complex, but highly useful, metrics such as coherence and dependency distance. 


# Acknowledgements
The authors thank the [contributors](https://github.com/HLasse/TextDescriptives/graphs/contributors) of the package including Martin Bernstorff for his work on the part-of-speech component, and Frida Hæstrup and Roberta Rocca for important fixes. The authors would also like to Dan Sattrup Nielsen for helpful reviews on early iterations of the text quality implementations.

