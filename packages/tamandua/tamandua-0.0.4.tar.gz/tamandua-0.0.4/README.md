# Tamandua

Assim como o bicho "aspira" formigas, estes códigos devem "aspirar" coisas da web.

## Instalar

Para instalar:

    pip install tamandua

Para atualizar:

    pip install --upgrade tamandua

## Rodar

```Python
from tamandua import Scraper
Scraper().deep_process_url('https://example.com/subfolder')
```

## PyPI

```
    python3 -m build
    twine upload dist/*
```

