import urllib.parse

from ordered_set import OrderedSet


def is_valid_wiki_page(url: str) -> bool:
    o = urllib.parse.urlparse(url)
    if o.scheme != "https":
        return False
    if not o.hostname.endswith("wikipedia.org"):
        return False
    if not o.path.startswith("/wiki/"):
        return False
    return True


def get_article_name(url: str) -> str:
    o = urllib.parse.urlparse(url)
    name = o.path.replace("/wiki/", "").replace("_", " ")
    if "%" in name:
        name = urllib.parse.unquote(name)
    return name


def filter_non_wiki_links(urls: OrderedSet[str]) -> OrderedSet[str]:
    filtered_list = OrderedSet()
    for url in urls:
        if is_valid_wiki_page(url):
            filtered_list.add(url)
    return filtered_list


def filter_non_wiki_links_and_defrag(urls: OrderedSet[str]) -> OrderedSet[str]:
    filtered_list = OrderedSet()
    for url in urls:
        if is_valid_wiki_page(url):
            defrag_result = urllib.parse.urldefrag(url)
            filtered_list.add(defrag_result.url)
    return filtered_list
