from bs4 import BeautifulSoup


def clean_html(html_string: str) -> str:
    def remove_malicious_tags_and_attributes(html: str) -> str:
        soup = BeautifulSoup(html, "html.parser")
        with open('whitelist_tags.txt') as f:
            whitelist_tags = f.readlines()

        for tag in soup(whitelist_tags):
            tag.decompose()

        with open('whitelist_attributes.txt') as f:
            whitelist_attributes = f.readlines()
        for tag in soup.find_all(True):
            for attribute in whitelist_attributes:
                if attribute in tag.attrs:
                    del tag.attrs[attribute]

        return str(soup)

    cleaned_html = html_string
    previous_html = ""

    while cleaned_html != previous_html:
        previous_html = cleaned_html
        cleaned_html = remove_malicious_tags_and_attributes(cleaned_html)
    return cleaned_html
