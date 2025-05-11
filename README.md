# Pygame DesSoft

### Integrantes do grupo:

* Julián Esteban Vargas Montaño.
* Sophia Montecinos Kalil.
* Felipe Campos Leite Lima.

Este projeto é um jogo digital desenvolvido por estudantes do Insper como parte de uma atividade acadêmica. Foi implementado em Python utilizando a biblioteca Pygame, com o objetivo de explorar conceitos de programação, lógica de jogos e design interativo. Todos os recursos gráficos e sonoros utilizados foram obtidos de fontes livres e abertas disponíveis na internet, respeitando as licenças de uso e promovendo o uso ético de conteúdo digital.

## Estrutura de pastas e arquivos

```
PyGameDesSoft/
│
├── main.py                # Ponto de entrada principal do jogo (inicialização e loop principal)
├── config.py              # Arquivo de configurações globais (resolução, FPS, caminhos etc.)
│
├── assets/                # Pasta para recursos do jogo (imagens, sons, fontes)
│   ├── images/
│   │   ├── background.png
│   │   ├── player.png
│   │   └── ...
│   ├── sounds/
│   └── fonts/
│
├── src/                   # Código fonte principal do jogo
│   ├── screens/           # Telas do jogo (cada uma em um arquivo separado)
│   │   ├── init.py
│   │   ├── main_menu.py   # Tela inicial do jogo com botão de play
│   │   ├── level_select.py # Tela de seleção de nível/mapa
│   │   └── game_screen.py # Tela principal do jogo
│   │
│   ├── objects/           # Classes dos objetos do jogo
│   │   ├── player.py      # Classe do jogador principal
│   │   └── obstacles.py   # Classe dos obstáculos
│   │
│   └── utils/             # Utilitários do jogo
│       ├── collision.py   # Sistema de detecção de colisões
│       └── asset_loader.py # Carregador de recursos (imagens, sons)
│
└── requirements.txt       # Dependências do projeto (pygame etc.)
└── README.md              # Arquivo Readme
```

## 1. Ambiente virtual de Python

* Crie um ambiente virtual, para isso digite dentro da raiz os seguintes comandos em ordem (no Mac ou Linux):

```shell
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

* Caso use Windows:

```shell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

* Lembre-se de ativar o ambiente virtual antes de executar o jogo!

## 2. Fluxo de trabalho com Git – Pull Requests e Issues

### Para contribuir com o projeto:

1. **Crie uma branch a partir da `main`:**

```bash
git checkout main #Volta pra branch main
git pull origin main #Sincroniza o repositorio
git checkout -b sua-feature-aqui # Cria a branch donde vc quer trabalhar
```

2. **Desenvolva e faça commits claros (exemplo):**

```bash
git add . # Adiciona as mudanças do diretorio atual
git commit -m "feat: adiciona tela de contato" #Cria o commit
```

3. **Suba sua branch:**

```bash
git push origin sua-feature-aqui #Envia a branch com os commit para criar o Pull Request (PR) no Github 
```

4. **Abra um Pull Request no GitHub:**

- Base: `main`
- Compare: `sua-feature-aqui`
- Preencha o título e a descrição do PR (ligue a issue com `Closes #número_da_issue` na descrição, quando você digitar `Closes #` já irá listar as issues)

5. **Espere aprovação para merge.**

- O Admin irá testar o PR, e posteriormente aceitar ou recusar. Se tiver algum erro será comunicado pelo grupo de Whats.

## 3. Fontes usadas no trabalho

Exemplo: A função `funcao-do-jogo()` do arquivo   `diretorio/arquivo.py` foi desenvolvida pela IA [www.blackbox.ai](https://www.blackbox.ai/).

* A estrutura de pastas e arquivos foi obtida pela IA [chat.deepseek.com](chat.deepseek.com).
