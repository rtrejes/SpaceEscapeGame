# SpaceEscapeGame 

## Alunos / Colaboradores 
    - Ramiro Trejes — GitHub: rtrejes 
    - Gabriel Ribeiro — GitHub: gabrielribeirodc 
    - Artur Teixeira dos Santos — GitHub: artur5anto5 
    - João Pedro Fonseca — GitHub: ThawneFB
    
---------------------------------------------------------------------------------------------- 
# 🎮 Space Escape Game 
    Jogo desenvolvido em Python com gráficos e sons, onde o objetivo é sobreviver desviando de inimigos e obstáculos enquanto avança de nível. 

---------------------------------------------------------------------------------------------- 
# 1. Como Clonar o Projeto 
    1 - Crie um projeto novo na sua IDE favorita 
    2 - Clone o repositório usando o comando do git no terminal: 
    git clone https://github.com/rtrejes/SpaceEscapeGame.git 
    Ou baixe o ZIP pelo próprio GitHub. 
    
# 2. Como Abrir, Configurar e Rodar no PyCharm ou VS Code 

- No PyCharm: 
    1 - Abra o projeto que você criou no PyCharm 
    2 - Instale dependências 
        2.1 - Vá em File > Settings > Project > Python Interpreter 
        2.2 - Clique em Add Package e instale pygame
            ou 
            2.2.1 - Abra o terminal do PyCharm e execute: pip install pygame 
    3 - No painel esquerdo, abra o arquivo spaceScape.py 
    4 - Clique com o botão direito no arquivo e, em seguida, em "Run 'spaceScape'" 
    
- No VS Code 
    1 - Abra o VS Code 
    2 - Vá em File > Open Folder e selecione a pasta SpaceEscapeGame. 
    3 - Instale as extensões recomendadas: - Python (Microsoft) - Pylance 
    4 - Instale dependências no terminal com o comando: pip install pygame 
    5 - Abra o arquivo spaceScape.py 
    6 - No canto superior direito, clique no botão Run Dessa forma, o jogo será iniciado. 
    
# 3. Estrutura do projeto 
    Os arquivos necessários para rodar spaceScape.py devem ficar todos na mesma pasta. 
    Entre esses arquivos, temos: 
        - Arquivos de imagens e sprites do jogo 
        - Efeitos sonoros e música do jogo 
        - spaceScape.py: O Arquivo principal do jogo 
        - Recursos adicionais 

# 4. Como Jogar 
    - Movimentação: Pelas setas do teclado 
    - Atirar: automaticamente ao pegar o power-up de míssil 
    - Objetivo do jogo: Desviar dos meteoros e tentar se manter vivo por mais tempo 
    - Pontuação: Ocorre quando um meteoro não colide com o jogador e sai da tela. 
        - Cada meteoro vale 1 ponto 
    - Níveis e dificuldade: Nível de dificuldade sobe automaticamente na medida que o jogador progride no jogo.
        - Cada nível aumenta a dificuldade acelerando meteoros e/ou adicionando novos meteoros na tela. Também ocorre uma redução de chance de aparecer meteoros de vida e powerups na medida que o jogador progride. 
        
# 5. Funcionalidades implementadas 
    - Movimento vertical da nave pelo jogador 
    - Spawn de power-up ou meteoro de vida 
    - Arma para a nave com tempo definido 
    - Capacidade de destruir meteoros 
    - Animação de explosão de meteoros 
    - Colisão com meteoro de vida adiciona mais vidas ao jogador 
    - Dificuldade progressiva 
    - Menu inicial 
    - Menu Game Over 
    - Registro de estatísticas de jogo (tempo, pontos, nível...)