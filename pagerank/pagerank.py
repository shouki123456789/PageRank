import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.

    """
    #initialize a dictionary
    transition_probability = {page_name : 0 for page_name in corpus}

    # If the page has no outgoing links, assign equal probabilities to all pages
    if len(corpus[page]) == 0:
        for page_name in transition_probability:
            transition_probability[page_name] = 1/len(corpus)
        return transition_probability
     
    for page_name in transition_probability:

        # If the page has outgoing links, calculate transition probabilities.
        if page_name in corpus[page]:
            transition_probability[page_name] += damping_factor/len(corpus[page])

        #probability for random jumping
        transition_probability[page_name] += (1-damping_factor) / len(corpus)
            
    return transition_probability


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Initialize PageRank scores
    pagerank = {page: 0 for page in corpus}

    # Create transition model for Markov Chain
    transition_matrix = {}
    
    # Create transition model for Markov Chain
    for page in corpus:
        transition_probabilities = transition_model(corpus, page, damping_factor)
        transition_matrix[page] = [transition_probabilities[linked_page] for linked_page in corpus]

    # Generate samples
    samples = generate_samples(transition_matrix, n)

    # Update PageRank scores
    for sample in samples:
        page = list(corpus.keys())[sample]
        pagerank[page] += 1

    # Normalize PageRank scores
    total_samples = sum(pagerank.values())
    pagerank = {page: (count / total_samples) for page, count in pagerank.items()}

    return pagerank

def generate_samples(transition_matrix, n):
    samples = []
    pages = list(transition_matrix.keys())

    for _ in range(n):
        # Choose a random page to start with
        sample = random.choice(pages)
        
        for _ in range(10):  # 10 steps as an example, you may adjust as needed
            # Use transition probabilities to determine next page
            sample = random.choices(pages, weights=transition_matrix[sample])[0]

        samples.append(pages.index(sample))

    return samples
 
def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    n =  len(corpus)

    # Initialize PageRank scores
    page_rank = {page: (1-damping_factor)/n for page in corpus}

    # Iterate until convergence
    while True:
        new_pagerank ={}
        max_diff = 0 # Track the maximum change in PageRank score
        for page in corpus:

            # Calculate new PageRank score for the current page
            new_score = 1-damping_factor/n
            for linking_page, linked_pages in corpus.items():
                if page in linked_pages:
                    num_out_links = len(linked_pages)
                    new_score += damping_factor * page_rank[linking_page] / num_out_links
            
            # Update the new PageRank score
            new_pagerank[page] = new_score

            # Update the maximum change in PageRank score
            max_diff = max(max_diff, abs(new_score - page_rank[page]))

        page_rank = new_pagerank
        
        # Check for convergence
        if max_diff < 0.001:
            break

    # Normalize PageRank scores
    total_pagerank = sum(page_rank.values())
    page_rank = {page: score / total_pagerank for page, score in page_rank.items()}

    return page_rank
        

if __name__ == "__main__":
    main()
