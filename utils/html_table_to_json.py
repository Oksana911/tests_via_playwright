from bs4 import BeautifulSoup


class HtmlTableParser:
    def __init__(self, html: str):
        self.html = html

    def _get_table_headers(self, soup: BeautifulSoup) -> list[str] | None:
        thead = soup.find('thead')
        if thead:
            headers = []
            thead = soup.find_all('th')
            for head in thead:
                headers.append(head.string.strip().lower().replace('\xa0', ' ').replace(':', ''))
            return headers
        return None

    def _get_json_with_headers(self, soup: BeautifulSoup, headers: list[str]) -> list[dict[str, str]]:
        result: list[dict[str, str]] = []
        rows = soup.find('tbody').find_all('tr')
        for row in rows:
            row_result = {}
            columns = row.find_all('td')
            for i, header in enumerate(headers):
                row_result[header] = columns[i].text.strip()
            result.append(row_result)
        return result

    def get_json(self) -> dict[str, str]:
        soup = BeautifulSoup(self.html, 'html.parser')
        headers = self._get_table_headers(soup)
        if headers:
            return self._get_json_with_headers(soup, headers)
        raise NotImplementedError('Не могу распарсить таблицу без заголовков')
