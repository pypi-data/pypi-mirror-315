from tamandua import Scraper


class GoogleSearchScraper(Scraper):
    def iterate(self, url):
        page = 0
        while True:
            results = self.deep_process_url(url + f'&start={page*10}')

            if (
                'não encontrou nenhum documento correspondente.'
                in results.response.text
                and results.sublinks == 0
            ):
                break

            print('Salvos:', results.stored, 'Sublinks:', results.sublinks)

            page += 1
