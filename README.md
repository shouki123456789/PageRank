# PageRank Algorithm
PageRank is an algorithm used to estimate the importance or relevance of web pages in a network. 
It was developed by Larry Page and Sergey Brin, the co-founders of Google, and is a key component of Google's search engine algorithm. This project implements the PageRank algorithm in Python.
## Overview
This implementation provides two methods for estimating PageRank: sampling and iterative calculation.

#### Sampling Method: 
This method simulates random walks on the web graph to estimate PageRank scores.
It randomly selects pages to visit based on the distribution of links and iterates through a large number of samples to estimate PageRank.

#### Iterative Method:
This method calculates PageRank scores by iteratively updating the scores of each page based on the PageRank formula until convergence.
It starts with initial PageRank scores for each page and updates them based on the scores of linking pages.
## Specification
For more information about the project specifications, please refer to the [Harvard CS50AI](https://cs50.harvard.edu/ai/) website.
Please avoid directly copying the source code as it is provided for reference purposes only. 
