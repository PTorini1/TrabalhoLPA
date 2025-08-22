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
pip install pyinstaller
pyinstaller --onefile --windowed --add-data "assets;assets" --add-data "code;code" main.py
```

O executável será criado na pasta `dist/`.

## Controles

- **Clique esquerdo**: Revelar célula
- **Clique direito**: Alternar bandeira
- **Botão Menu**: Voltar ao menu principal
- **Botão Reiniciar**: Começar novo jogo com a mesma dificuldade
