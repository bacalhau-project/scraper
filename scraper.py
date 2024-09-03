import json
import os
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urljoin, urlparse

import click
import trafilatura
from bs4 import BeautifulSoup
from trafilatura import fetch_url


def load_config(config_file):
    with open(config_file, "r") as f:
        return json.load(f)


def is_same_domain(url1, url2):
    return urlparse(url1).netloc == urlparse(url2).netloc


def extract_links(html_content, base_url):
    soup = BeautifulSoup(html_content, "html.parser")
    links = []
    for a in soup.find_all("a", href=True):
        link = urljoin(base_url, a["href"])
        if is_same_domain(base_url, link):
            links.append(link)
    return links


def scrape_website(url, site_name, max_depth, output_dir):
    is_wikipedia = "wikipedia.org" in url
    max_depth = 2 if is_wikipedia else max_depth
    max_pages = 5 if is_wikipedia else 100

    visited = set()
    to_visit = [(url, 0)]
    scraped_count = 0
    link_counts = Counter()

    while to_visit and scraped_count < max_pages:
        current_url, depth = to_visit.pop(0)
        if current_url in visited or depth >= max_depth:
            continue

        visited.add(current_url)
        try:
            downloaded = fetch_url(current_url)
            if downloaded is None:
                continue

            result = trafilatura.extract(
                downloaded, include_links=True, include_images=True, include_tables=True
            )
            if result:
                filename = f"{site_name}_{scraped_count}.txt"
                with open(
                    os.path.join(output_dir, filename), "w", encoding="utf-8"
                ) as f:
                    f.write(f"Source: {site_name}\nURL: {current_url}\n\n{result}")
                scraped_count += 1

            if depth < max_depth - 1:
                links = extract_links(downloaded, current_url)
                for link in links:
                    if link not in visited:
                        link_counts[link] += 1

        except Exception as e:
            click.echo(f"Error scraping {current_url}: {str(e)}")

        # Repopulate to_visit with the most linked pages
        if not to_visit:
            to_visit = [
                (link, depth + 1)
                for link, _ in link_counts.most_common(max_pages - scraped_count)
            ]
            link_counts.clear()

    return scraped_count


@click.command()
@click.option("--config", default="config.json", help="Path to the configuration file")
def main(config):
    config_data = load_config(config)
    output_dir = config_data["output_directory"]
    os.makedirs(output_dir, exist_ok=True)

    with ThreadPoolExecutor(max_workers=config_data.get("max_workers", 5)) as executor:
        futures = []
        for website in config_data["websites"]:
            futures.append(
                executor.submit(
                    scrape_website,
                    website["url"],
                    website["name"],
                    website.get("max_depth", config_data.get("max_depth", 6)),
                    output_dir,
                )
            )

        for future in as_completed(futures):
            result = future.result()
            click.echo(f"Scraped {result} pages")


if __name__ == "__main__":
    main()
