import networkx as nx
import jsonlines, json
import argparse

def get_page_rank(args):

    with open(args.doc_path, 'r') as f:
        doc_len = json.load(f)

    G = nx.DiGraph()
    reader = jsonlines.open(args.path)
    for file in reader:
        
        url = file["url"]
        outgoing_urls = file["outgoing_urls"]
        G.add_node(url)

        for node in outgoing_urls:
            if node in doc_len and node != url:
                G.add_edge(url, node)

    page_rank = nx.pagerank(G)
    with open("page_rank.json", 'w') as f:
        json.dump(page_rank, f)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="File for calculating PageRank score of nodes")
    parser.add_argument("--path", help="Path to jsonlines file containing scraped data", type=str)
    parser.add_argument("--doc_path", help="Path to JSON file containing TF-IDF vector norm for each of the scraped pages", type=str, default="doc_len.json")
    args = parser.parse_args()
    get_page_rank(args)