// Script para ir descendo um infinite scroll e exportar dados ao fim.
// Primeiro abrir a página desejada e depois rodá-lo no console do navegador.
// Pode ser bom fechar o console enquanto estiver rodando, para que o navegador não fique lento.

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

// Exporta a página inteira incluindo modificações feitas pelo JS.
function exportPage() {
  var a = document.createElement('a');
  a.download = 'page.html';
  var bb = new Blob([document.body.innerHTML], { type: 'text/plain' });
  a.href = window.URL.createObjectURL(bb);
  document.body.appendChild(a);
  a.click();
}

function scroll(top) {
  window.scrollTo({
    top,
    left: 0,
    behavior: 'instant',
  });
}

async function run() {
  attempts = 0;
  // Vai descendo a página até carregar todos os dados.
  while (true) {
    console.log('rodando...');
    var height = document.body.offsetHeight;

    // Se a altura atual é igual à anterior, quer dizer que não carregou mais dados.
    // Pode ser só porque não deu tempo, e nesse caso tentamos de novo.
    // Mas se já tentou 10 vezes, considera que acabou e finaliza expontardo a página.
    if (height === prevHeight) {
      console.log(`Parece não ter carregado mais nada (${attempts}).`);
      attempts++;

      if (attempts > 20) {
        console.log('Não está carregando mais nada, exportando página.');
        exportPage();
        break;
      }
    } else {
      console.log('Voltou a carregar dados, continuando.');
      attempts = 0;
    }

    // Desce até o fim da página.
    scroll(height);

    // Espera dados carregarem.
    await sleep(1000);

    // Sobe e desce para diminuir a chance de que emperre.
    scroll(0);
    await sleep(1000);
    scroll(height);
    await sleep(1000);

    var prevHeight = height;
  }
}

run();
