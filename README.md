# Space Escape Game

Jogo desenvolvido em Python com gráficos e sons, onde o objetivo é sobreviver desviando de inimigos e obstáculos enquanto avança de nível. 

--------------
## Alunos / Colaboradores 
- Carlos Ramiro Trejes — GitHub: rtrejes 
- Gabriel Ribeiro — GitHub: gabrielribeirodc 
- Artur Teixeira dos Santos — GitHub: artur5anto5 
- João Pedro Fonseca — GitHub: ThawneFB

-----
## Como Clonar o Projeto
Clone o repositório usando o comando do git no terminal:
```bash
  git clone https://github.com/rtrejes/SpaceEscapeGame.git
```
Ou baixe o ZIP pelo próprio GitHub.
    
## Como Instalar e rodar o jogo
### Pré-requisitos:

- Python 3 instalado
- Pip instalado (já vem com o Python)

Maiores informações de como instalar Python podem ser encontradas no site oficial:
- [Windows](https://docs.python.org/3/using/windows.html)
- [macOS](https://docs.python.org/3/using/mac.html)
- [Linux](https://docs.python.org/3/using/unix.html)


### Instalando dependências: 
No terminal, execute:

```bash
  pip install pygame
```
Em sistemas onde o Python usa python3:
```bash
  pip3 install pygame
```

### Clone o repositório ou baixe o ZIP pelo GitHub e extraia
```bash
  git clone https://github.com/rtrejes/SpaceEscapeGame.git
```

### Entre na pasta do projeto conforme o exemplo:
````bash
  cd caminho\para\projeto\SpaceEscapeGame
````

### Execute o jogo com o código abaixo:
````bash
  python spaceScape.py
````
Ou, se necessário:
````bash
  python3 spaceScape.py
````

    
## Estrutura do projeto
Os arquivos necessários para rodar spaceScape.py devem ficar todos na mesma pasta. 

Entre esses arquivos, temos: 

    - Arquivos de imagens e sprites do jogo 
    - Efeitos sonoros e música do jogo 
    - spaceScape.py: O Arquivo principal do jogo

## Como Jogar 
- Movimentação: Pelas setas do teclado 
- Atirar: automaticamente ao pegar o power-up de míssil 
- Objetivo do jogo: Desviar dos meteoros e tentar se manter vivo por mais tempo 
- Pontuação: Ocorre quando um meteoro não colide com o jogador e sai da tela. 
  - Cada meteoro vale 1 ponto 
- Níveis e dificuldade: Nível de dificuldade sobe automaticamente na medida que o jogador progride no jogo.
  - Cada nível aumenta a dificuldade acelerando meteoros e/ou adicionando novos meteoros na tela. Também ocorre uma redução de chance de aparecer meteoros de vida e powerups na medida que o jogador progride. 
        
## Funcionalidades implementadas
    - Movimento vertical da nave pelo jogador 
    - Spawn de power-up ou meteoro de vida 
    - Arma para a nave com tempo definido 
    - Capacidade de destruir meteoros 
    - Animação de explosão de meteoros 
    - Colisão com meteoro de vida aumenta vidas do jogador 
    - Dificuldade progressiva 
    - Menu inicial 
    - Menu Game Over 
    - Registro de estatísticas de jogo (tempo, pontos, nível...)