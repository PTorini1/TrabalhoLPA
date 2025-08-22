# Campo Minado

Um jogo de Campo Minado implementado em Python usando Pygame.

## Características

- Interface gráfica intuitiva
- 3 níveis de dificuldade:
  - Fácil: 9x9 com 10 minas
  - Médio: 16x16 com 40 minas
  - Difícil: 16x30 com 99 minas
- Efeitos sonoros quando explode uma bomba
- Sprites visuais para bombas e bandeiras
- Sistema de bandeiras para marcar minas suspeitas

## Estrutura do Projeto

```
CampoMinado/
├── main.py              # Arquivo principal do jogo
├── requirements.txt     # Dependências do projeto
├── compile.py          # Script para compilar o executável
├── assets/              # Recursos visuais e sonoros (minúsculo)
│   ├── bomb.png        # Imagem da bomba
│   ├── flag.png        # Imagem da bandeira
│   └── bomb-sound.wav  # Som da explosão
└── code/               # Lógica do jogo (minúsculo)
    ├── __init__.py     # Pacote Python
    ├── game_logic.py   # Lógica do campo minado (nomes em português)
    └── gui.py          # Interface gráfica (nomes em português)
```

## Como Jogar

1. Execute o arquivo `main.py`
2. No menu principal, escolha a dificuldade
3. Clique em "JOGAR" para iniciar
4. No jogo:
   - **Clique esquerdo**: Revelar célula
   - **Clique direito**: Colocar/remover bandeira
   - **Objetivo**: Revelar todas as células que não são minas

## Instalação e Execução

1. Instale o Python 3.7 ou superior
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
3. Execute o jogo:
   ```bash
   python main.py
   ```

## Compilação

Para criar um executável do jogo, execute o script de compilação:

```bash
python compile.py
```

Ou usando PyInstaller diretamente:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --add-data "assets;assets" --add-data "code;code" main.py
```

O executável será criado na pasta `dist/`.

## Controles

- **Clique esquerdo**: Revelar célula
- **Clique direito**: Alternar bandeira
- **Botão Menu**: Voltar ao menu principal
- **Botão Reiniciar**: Começar novo jogo com a mesma dificuldade

## Assets

O jogo utiliza os seguintes recursos da pasta assets:
- `bomb.png`: Imagem exibida quando uma mina é revelada
- `flag.png`: Imagem das bandeiras colocadas pelo jogador
- `bomb-sound.wav`: Som reproduzido quando uma mina explode

## Arquitetura do Código

O código foi estruturado com nomes em português para facilitar a compreensão:

### Classes Principais:
- `CampoMinado` (em `game_logic.py`): Contém toda a lógica do jogo
- `InterfaceCampoMinado` (em `gui.py`): Interface gráfica do jogo

### Variáveis Traduzidas:
- `linhas`, `colunas`, `bombas` - dimensões do tabuleiro
- `tabuleiro`, `revelado`, `marcado` - matrizes do estado do jogo
- `jogo_terminado`, `jogo_ganho` - estados do jogo
- `posicoes_bombas` - conjunto com posições das bombas
