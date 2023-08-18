import crawler


urls = crawler.get_links_recursively(
    root_url="https://en.wikipedia.org/wiki/Coinbase",
    max_visited_pages=3,
)
print(urls)

path = crawler.get_path(
    source="https://en.wikipedia.org/wiki/Coinbase",
    target="https://en.wikipedia.org/wiki/State-owned_enterprise",
    max_visited_pages=200,
)
print(path)
