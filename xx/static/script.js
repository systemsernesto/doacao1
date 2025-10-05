// Função para calcular distância simulada
function calcularDistancia(localizacaoUsuario, enderecoInstituicao) {
    const distancia = Math.floor(Math.random() * 20) + 1; // 1 a 20 km
    return distancia;
}

// Função para atualizar o botão de perfil
function atualizarBotaoPerfil() {
    const btnPerfil = document.getElementById('btn-perfil');
    const usuarioNome = document.getElementById('usuario-nome');
    
    if (usuarioNome) {
        btnPerfil.textContent = usuarioNome.textContent;
    } else {
        btnPerfil.textContent = 'Login';
    }
}

// Função para mostrar abas
function showTab(tabId) {
    // Esconder todas as abas
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active-tab');
    });
    
    // Remover classe ativa dos botões
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // Mostrar aba selecionada
    document.getElementById(tabId).classList.add('active-tab');
    
    // Destacar botão correspondente
    const botoes = document.querySelectorAll('.tab-btn');
    const nomesAbas = ['cadastro-usuario', 'login', 'cadastro-instituicao', 'busca-instituicoes'];
    const indice = nomesAbas.indexOf(tabId);
    if (indice !== -1) {
        botoes[indice].classList.add('active');
    }
}

// Busca de instituições
function buscarInstituicoes() {
    const localizacao = document.getElementById('localizacao-usuario').value || 'Minha Localização';
    const container = document.getElementById('instituicoes-list');
    
    // Fazer requisição para a API
    fetch(`/api/instituicoes_proximas?localizacao=${encodeURIComponent(localizacao)}`)
        .then(response => response.json())
        .then(data => {
            container.innerHTML = '';
            
            // Ordenar instituições por distância
            const instituicoesOrdenadas = [...data].sort((a, b) => {
                return a.distancia - b.distancia;
            });
            
            instituicoesOrdenadas.forEach(inst => {
                const item = document.createElement('div');
                item.className = 'instituicao-item';
                
                item.innerHTML = `
                    <div class="instituicao-info">
                        <h3>${inst.nome}</h3>
                        <div class="endereco-instituicao">Endereço: ${inst.endereco}</div>
                        <div class="contato-instituicao">Telefone: ${inst.telefone}</div>
                        <div class="contato-instituicao">CNPJ: ${inst.cnpj}</div>
                    </div>
                    <div class="distancia">${inst.distancia} km</div>
                    <div class="acoes">
                        <a href="${inst.url_doacao}" target="_blank">
                            <button>Acessar</button>
                        </a>
                    </div>
                `;
                
                container.appendChild(item);
            });
        })
        .catch(error => {
            console.error('Erro ao buscar instituições:', error);
            container.innerHTML = '<p>Erro ao carregar instituições. Tente novamente.</p>';
        });
}

// Executar cálculo de menor caminho ao carregar
document.addEventListener('DOMContentLoaded', function() {
    atualizarBotaoPerfil();
});