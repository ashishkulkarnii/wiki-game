import utils

import requests
import logging
import collections

import bs4
from ordered_set import OrderedSet

import selenium.webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions


logging.getLogger().setLevel(logging.INFO)


def get_links(url: str) -> OrderedSet[str]:
    # # getting links from response content using BeautifulSoup
    # response = requests.get(url)
    # soup = bs4.BeautifulSoup(response.text, "html.parser")
    # urls_from_response = [link.get("href") for link in soup.find_all("a")]

    # getting links from pages where the content requires JavaScript execution
    # running the browser without loading the GUI
    options = ChromeOptions()
    options.add_argument("--headless")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = selenium.webdriver.Chrome(options=options)
    driver.get(url)
    # elements = driver.find_elements(By.TAG_NAME, "a")
    content_div = driver.find_element(
        By.ID, "bodyContent"
    )  # narrowing down search to the part of the page containing article content
    a_tags = content_div.find_elements(By.TAG_NAME, "a")
    urls_from_js = [
        element.get_attribute("href") for element in a_tags
    ]  # element.get_attribute("innerHTML") would give us the text within the <a> </a> tags.
    driver.close()

    urls = urls_from_js  # + urls_from_response

    filtered_urls = utils.filter_non_wiki_links_and_defrag(urls)
    return OrderedSet(filtered_urls)


def get_links_recursively(
    root_url: str, max_visited_pages: int, verbose: bool = True
) -> OrderedSet[str]:
    """Using BFS to collect all unique links found at every level, and the path taken to get to the page."""
    crawled = set()
    seen = set()
    queue = [root_url]
    urls = OrderedSet()
    urls.add(root_url)
    child_parent = collections.OrderedDict()

    while queue and max_visited_pages:
        parent = queue.pop(0)
        if parent not in crawled:
            max_visited_pages -= 1
            crawled.add(parent)
            seen.add(parent)
            logging.info(f"Crawling {parent}")
            children = get_links(parent)
            for child in children:
                if not child in seen and not child in crawled:
                    urls.add(child)
                    queue.append(child)
                    seen.add(child)
                    child_parent[child] = parent

    logging.info(f"All URLs found: {list(urls)}")

    if verbose:
        print("Longest path:")
        depth = 0
        child, parent = list(child_parent.items())[-1]
        path = f"{parent}\n┖─────> {child}"
        while parent in child_parent.keys():
            depth += 1
            parent = child_parent[parent]
            path = f"{parent}\n┖─────> " + path
        print("seed──> " + path)
        print(f"Levels traversed: {depth}")

    return urls


def get_path(source: str, target: str, max_visited_pages: int = 200) -> list[str] | None:
    crawled = set()
    seen = set()
    queue = [source]
    urls = OrderedSet()
    urls.add(source)
    child_parent = collections.OrderedDict()

    while queue and max_visited_pages:
        parent = queue.pop(0)
        if parent not in crawled:
            max_visited_pages -= 1
            crawled.add(parent)
            seen.add(parent)
            logging.info(f"Crawling {parent}")
            children = get_links(parent)
            for child in children:
                if not child in seen and not child in crawled:
                    urls.add(child)
                    queue.append(child)
                    seen.add(child)
                    child_parent[child] = parent
                if target in seen:
                    queue.clear()
                    break
    
    if target not in seen:
        return None
    
    path = []
    print("Longest path:")
    depth = 1
    child = target
    parent = child_parent[child]
    path_str = f"{parent}\n┖─────> {child}"
    path = [parent, child]
    while parent in child_parent.keys():
        depth += 1
        parent = child_parent[parent]
        path_str = f"{parent}\n┖─────> " + path_str
        path = [parent] + path
    print("seed──> " + path_str)
    print(f"Levels traversed: {depth}")

    return path
