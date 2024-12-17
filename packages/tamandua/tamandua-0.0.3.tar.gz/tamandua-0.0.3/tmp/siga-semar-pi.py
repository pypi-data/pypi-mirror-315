from tamandua import GoogleSearchScraper

GoogleSearchScraper(filter_url='https://siga.semar.pi.gov.br/media/uploads/').iterate(
    'https://www.google.com/search?q=site:siga.semar.pi.gov.br/media/uploads/'
)
