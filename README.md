### Search Engine

This is the project repo for CS581 - Information Retrieval at UIC.

#### Running Instructions

Create a virtual environment using ```pip``` with the ```requirements.txt``` file -

```bash
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

For running the crawler, ```cd``` into the ```crawling``` directory and run -

```bash
scrapy crawl UIC
```

The above command will scrape 4000 webpages starting from [cs.uic.edu](cs.uic.edu) and store the scraped data in a jsonlines file called ```scraped_data.jl``` inside ```crawling```.

Once you have this data ready, you can run ```construct_index.py``` from the root directory with a ```--path``` parameter indicating the path to the scraped data -

```bash
python construct_index.py --path crawling/scraped_data.jl
```

The above command stores two JSON files - the inverted index ```inv_index.json``` and the norm of the TF-IDF vectors for each document ```doc_len.json```. These two files are needed to run for the next steps.

The next part is calculating the PageRank scores of the scraped web pages. For this, the scraped data is required along with ```doc_len.json``` -

```bash
python page_rank.py --path crawling/scraped_data.jl --doc_path doc_len.json
```

This calculates the PageRank scores of each document and stores them in ```page_rank.json```. For query processing, we need the inverted index, the page rank scores and ```doc_len.json``` to retrieve the ranked list of relevant documents -

```bash
python query.py --index_path inv_index.json --doc_path doc_len.json --page_rank page_rank.json
```

This runs the program on the terminal where the user can enter queries and get a ranked list of URLs relevant to the queries. Along with the ranked list, the relevance score and the PageRank score are also displayed.

