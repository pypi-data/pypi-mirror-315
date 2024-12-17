# Tamandua

Assim como o bicho "aspira" formigas, estes códigos devem "aspirar" coisas da web.

## Instalar

Por enquanto ainda não consegui que liberem o nome `tamandua` no PyPI principal, então precisa usar o de teste:

    pip install -i https://test.pypi.org/simple/ tamandua

Para atualizar:

    pip install --upgrade -i https://test.pypi.org/simple/ tamandua

## Rodar

```Python
from tamandua import Scraper
Scraper().deep_process_url('https://example.com/subfolder')
```

## PyPI

```
    python3 -m build
    python3 -m twine upload dist/*
```