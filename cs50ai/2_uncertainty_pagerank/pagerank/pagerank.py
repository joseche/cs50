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
    print("PageRank Results from Iteration")
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
        pages[filename] = set(link for link in pages[filename] if link in pages)

    return pages


def transition_model(corpus, page, damping_factor) -> dict[str, float]:
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    probability_distribution = {}
    links_in_page = corpus[page]
    linked_prob = damping_factor / len(links_in_page) if len(links_in_page) else 0
    all_pages_prob = (1 - damping_factor) / len(corpus)
    for current_page in corpus:
        if current_page in links_in_page:
            probability_distribution[current_page] = linked_prob + all_pages_prob
        else:
            probability_distribution[current_page] = all_pages_prob
    return probability_distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    page_ranks = {}
    page_visits_counts = {p: 0 for p in list(corpus.keys())}
    current_page = random.choice(list(corpus.keys()))
    for _ in range(n):
        page_visits_counts[current_page] += 1
        probabilities = transition_model(corpus, current_page, damping_factor)
        current_page = random.choices(list(probabilities.keys()), weights=list(probabilities.values()))[0]

    for page in page_visits_counts:
        # for this algo is clear the sum add up to 1, also n is safely assumed to be >= 1
        page_ranks[page] = page_visits_counts[page] / n

    return page_ranks


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pages = list(corpus.keys())
    num_pages = len(pages)
    page_ranks = {p: 1 / num_pages for p in pages}
    normal_page_rank = (1 - damping_factor) / num_pages

    while True:
        new_page_ranks = {}
        for page in pages:
            linked_page_rank = 0
            for other_page, links in corpus.items():
                if page in links:
                    linked_page_rank += page_ranks[other_page] / len(links)
            new_page_ranks[page] = normal_page_rank + (damping_factor * linked_page_rank)
        # Add dangling mass redistribution, for pages without links
        dangling_sum = sum(page_ranks[page] for page, links in corpus.items() if len(links) == 0)
        for page in pages:
            new_page_ranks[page] += damping_factor * dangling_sum / num_pages

        if all(abs(page_ranks[page] - new_page_ranks[page]) < 0.001 for page in pages):
            break

        page_ranks = new_page_ranks.copy()
    return page_ranks


if __name__ == "__main__":
    main()
