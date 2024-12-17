import datetime
import re
import shelve
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Self

import pyrfc6266
import requests
from slugify import slugify

default_content_types = ['application/pdf']


@dataclass
class Results:
    response: requests.Response | None = None
    stored: int = 0
    sublinks: int = 0

    def __add__(self, results: Self):
        if results is not None:
            self.stored += results.stored
            self.sublinks += results.sublinks
        return self


class Scraper:
    '''Baixador de websites recursivo.'''

    def __init__(
        self,
        filter_url=None,
        store_folder: str | Path = Path('downloads'),
        store_content_types=None,
        delay=3,
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.3',
    ):
        # Usada para definir se baixa e processa URL.
        self.filter_url = filter_url

        # Formatos de arquivos que serão salvos.
        self.store_content_types = store_content_types or default_content_types

        # Pasta onde salvar arquivos baixados.
        self.store_folder = Path(store_folder)
        # Cria a pasta caso não exista.
        self.store_folder.mkdir(exist_ok=True)

        # Tempo entre cada requisição.
        self.delay = delay

        # User-Agent.
        self.user_agent = user_agent

        # Arquivo para registrar URLs já baixadas.
        self.state_filepath = self.store_folder / 'state.shelve'

        # Carrega lista de arquivos baixados anteriormente. Não dá para simplesmente olhar o nome
        # dos arquivos salvos localmente porque às vezes só se sabe o nome do arquivo depois de
        # baixá-lo. Então é preciso um lugar onde guardar os links baixados.
        with shelve.open(self.state_filepath) as db:  # type: ignore
            self.downloaded = set(db.keys())

    def check_filter(self, url: str) -> bool:
        '''Filtro simples, que "entra" em URLs "abaixo" da inicial.'''
        return url.startswith(self.filter_url)

    def process_page(self, text: str) -> Results:
        '''Analisa URLs na página e processa os que devem ser processados.'''
        results = Results()
        for link in re.findall(r'href="(.+?)"', text):
            # Resolve links relativos.
            # link = urljoin(url, link).replace('&amp;', '&')

            # Ignora URLs já processados ou que não passem no filtro.
            if link in self.downloaded or not self.check_filter(link):
                continue

            results += self.deep_process_url(link)
        return results

    def process_file(self, filepath: str | Path) -> Results:
        return self.process_page(Path(filepath).read_text(encoding='utf8'))

    def deep_process_url(self, url: str) -> Results:
        '''
        Baixa e analisa um URL.
        Se for do tipo de arquivo desejado, salva.
        Caso contrário busca por URLs na página e processa cada um.
        '''

        # Caso não tenha definido uma URL para a filtragem, usa a inicial.
        if self.filter_url is None:
            self.filter_url = url

        print(url)
        time.sleep(self.delay)
        response = requests.get(url, timeout=30, headers={'User-Agent': self.user_agent})

        # Registra por onde já passou.
        self.downloaded.add(url)

        results = Results(response, sublinks=1)

        if response.headers['Content-Type'] in self.store_content_types:
            # Extrai o nome do arquivo.
            filename = pyrfc6266.requests_response_to_filename(response)
            name, _, suffix = slugify(filename).rpartition('-')
            filepath = self.store_folder / f'{name}.{suffix}'

            # Salva.
            filepath.write_bytes(response.content)
            print('salvo')

            # Registra arquivos já baixados.
            with shelve.open(self.state_filepath) as db:  # type: ignore
                db[url] = datetime.datetime.now()

            results.stored += 1
        else:
            results += self.process_page(response.text)

        return results
