# CemantixSoluce
A solution in Python using NLP for find the solution of https://cemantix.certitudes.org.

To use this script you need to have the following model : https://embeddings.net/embeddings/frWac_no_postag_no_phrase_500_cbow_cut100.bin and put it in the folder with the notekbook.

# How it's working

The objective of Cemantix is to discover a new word each day by using other words to determine how close they are semantically to the word of the day. The solver uses an embedding model for text, which converts words into numerical vectors. Our goal is to find the vector of the day (the word of the day) by identifying the closest vector (the minimum distance).

*Algorithm*
1. **Initialization**: Generate scores for a set of random words and identify the word with the highest score (i.e., the closest vector).
2. **Iteration**: Use the model to determine the closest words (semantically, i.e., in vector space) to the chosen words. Score the new words and repeat the process.
3. **Termination**: Stop when the word with a score of one is found, indicating the word of the day has been identified.
