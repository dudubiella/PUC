import neat.config
import pygame
import os
import random
import neat

ai_jogando = True
geracao = 0

# Constantes do tamanho da tela e imagens utilizadas
TELA_L, TELA_A = 500, 800

caminho = os.path.dirname(__file__) + '\\imgs'
print(caminho)
IMG_CANO = pygame.transform.scale2x(pygame.image.load(os.path.join(caminho,'pipe.png')))
IMG_CHAO = pygame.transform.scale2x(pygame.image.load(os.path.join(caminho,'base.png')))
IMG_BACKGROUND = pygame.transform.scale2x(pygame.image.load(os.path.join(caminho,'bg.png')))
IMGS_PASSARO = [
    pygame.transform.scale2x(pygame.image.load(os.path.join(caminho,'bird1.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join(caminho,'bird2.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join(caminho,'bird3.png')))
]

pygame.font.init()
FONTE_PONTOS = pygame.font.SysFont("arial", 50)

class Passaro:
    IMGS = IMGS_PASSARO

    # Constantes da animação da rotação
    ROTACAO_MAX = 25
    VEL_ROTACAO = 20
    TEMPO_ANIMAÇAO = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angulo = 0
        self.velocidade = 0
        self.altura = self.y
        self.tempo = 0
        self.cont_img = 0
        self.img = self.IMGS[0]
    
    def pular(self):
        self.velocidade = -10.5
        self.tempo = 0
        self.altura = self.y

    def mover(self):
        self.tempo += 1
        deslocamento = self.velocidade * self.tempo + 1.5 * (self.tempo ** 2)

        if deslocamento > 16:
            deslocamento = 16

        elif deslocamento < 0:
            deslocamento -= 2

        self.y += deslocamento

        if deslocamento < 0 or self.y < self.altura + 50:
            if self.angulo < self.ROTACAO_MAX:
                self.angulo = self.ROTACAO_MAX
        else:
            if self.angulo > -90:
                self.angulo -= self.VEL_ROTACAO

    def desenhar(self, tela):
        self.cont_img += 1

        if self.cont_img < self.TEMPO_ANIMAÇAO:
            self.img = self.IMGS[0]
        elif self.cont_img < self.TEMPO_ANIMAÇAO * 2:
            self.img = self.IMGS[1]
        elif self.cont_img < self.TEMPO_ANIMAÇAO * 3:
            self.img = self.IMGS[2]
        elif self.cont_img < self.TEMPO_ANIMAÇAO * 4:
            self.img = self.IMGS[1]
        elif self.cont_img < self.TEMPO_ANIMAÇAO * 4 + 1:
            self.img = self.IMGS[0]
            self.cont_img = 0

        if self.angulo <= -80:
            self.img = self.IMGS[1]
            self.cont_img = self.TEMPO_ANIMAÇAO * 2

        img_rot = pygame.transform.rotate(self.img, self.angulo)
        centro = self.img.get_rect(topleft = (self.x, self.y)).center
        retangulo = img_rot.get_rect(center = centro)

        tela.blit(img_rot, retangulo.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)

class Cano:
    DISTANCIA = 200
    VELOCIDADE = 5
    def __init__(self, x):
        self.tipo = random.randrange(0, 2)
        self.x = x
        self.altura = 0
        self.pos_topo = 0
        self.pos_base = 0
        self.CANO_TOPO = pygame.transform.flip(IMG_CANO, False, True)
        self.CANO_BASE = IMG_CANO
        self.passou = False
        self.def_altura()

    def def_altura(self):
        self.altura = random.randrange(100, 500)
        self.pos_topo = self.altura - self.CANO_TOPO.get_height()
        self.pos_base = self.altura + self.DISTANCIA

    def mover(self):
        self.x -= self.VELOCIDADE
        match self.tipo:
            case 0:
                self.pos_topo += 2
                self.pos_base += 2
            case 1:
                self.pos_topo -= 2
                self.pos_base -= 2
        
        if self.pos_base < 300 and self.tipo != 0:
            self.tipo = 0
        elif self.pos_base > 650 and self.tipo != 1:
            self.tipo = 1

    def desenhar(self, tela):
        tela.blit(self.CANO_TOPO, (self.x, self.pos_topo))
        tela.blit(self.CANO_BASE, (self.x, self.pos_base))

    def colidir(self, passaro):
        pass_mask = passaro.get_mask()
        topo_mask = pygame.mask.from_surface(self.CANO_TOPO)
        base_mask = pygame.mask.from_surface(self.CANO_BASE)

        distancia_topo = (self.x - passaro.x, self.pos_topo - round(passaro.y))
        distancia_base = (self.x - passaro.x, self.pos_base - round(passaro.y))

        topo_ponto = pass_mask.overlap(topo_mask, distancia_topo)
        base_ponto = pass_mask.overlap(base_mask, distancia_base)

        if base_ponto or topo_ponto:
            return True
        else:
            return False

class Chao:
    VELOCIDADE = 5
    LARGURA = IMG_CHAO.get_width()
    IMAGEM = IMG_CHAO

    def __init__(self, y):
        self.y = y
        self.x0 = 0
        self.x1 = self.LARGURA

    def mover(self):
        self.x0 -= self.VELOCIDADE
        self.x1 -= self.VELOCIDADE

        if self.x0 + self.LARGURA < 0:
            self.x0 = self.x1 + self.LARGURA
        if self.x1 + self.LARGURA < 0:
            self.x1 = self.x0 + self.LARGURA

    def desenhar(self, tela):
        tela.blit(self.IMAGEM, (self.x0, self.y))
        tela.blit(self.IMAGEM, (self.x1, self.y))

def desenha_tela(tela, passaros, canos, chao, pontos):
    tela.blit(IMG_BACKGROUND, (0, 0))

    for passaro in passaros:
        passaro.desenhar(tela)
    
    for cano in canos:
        cano.desenhar(tela)

    texto = FONTE_PONTOS.render(f"Pontos: {pontos}", 1, (255, 255, 255))
    tela.blit (texto, (TELA_L - 10 - texto.get_width(), 10))

    if ai_jogando:
        texto = FONTE_PONTOS.render(f"Geração: {geracao}", 1, (255, 255, 255))
        tela.blit (texto, (10, 10))

    chao.desenhar(tela)

    pygame.display.update()

def main(genomas = None, config = None):
    global geracao
    geracao += 1

    if ai_jogando:
        redes = []
        list_gen = []
        passaros = []
        for _, genoma in genomas:
            rede = neat.nn.FeedForwardNetwork.create(genoma, config)
            redes.append(rede)
            genoma.fitness = 0
            list_gen.append(genoma)
            passaros.append(Passaro(230, 350))
            
    else:
        passaros = [Passaro(230, 350)]

    chao = Chao(TELA_A - 70)
    canos = [Cano(TELA_L + 200)]
    tela = pygame.display.set_mode((TELA_L, TELA_A))
    pontos = 0
    relogio = pygame.time.Clock()

    rodando = True
    while rodando:
        relogio.tick(30)

        # Intereação com o usuário
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
                pygame.quit()
                return pontos

            if not ai_jogando:
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_SPACE:
                        for passaro in passaros:
                            passaro.pular()

        if ai_jogando:
            indece_cano = 0
            if len(passaros) > 0:
                if len(canos) > 1 and passaros[0].x > canos[0].x + canos[0].CANO_TOPO.get_width():
                    indece_cano = 1
            else:
                rodando = False
                break

        # Mover as coisas
        for i, passaro in enumerate(passaros):
            passaro.mover()
            list_gen[i].fitness += 0.1
            output = redes[i].activate((passaro.y, abs(passaro.y - canos[indece_cano].altura), abs(passaro.y - canos[indece_cano].pos_base)))
            if output[0] > 0.5:
                passaro.pular()

        chao.mover()
        
        adicionar_cano = False
        remover_canos = []

        for cano in canos:
            for i, passaro in enumerate(passaros):
                if cano.colidir(passaro):
                    passaros.pop(i)
                    if ai_jogando:
                        list_gen[i].fitness -= 1
                        list_gen.pop(i)
                        redes.pop(i)

                if not cano.passou and passaro.x > cano.x:
                    cano.passou = True
                    adicionar_cano = True
            
            cano.mover()
            
            if cano.x + cano.CANO_TOPO.get_width() < 0:
                remover_canos.append(cano)
            
        if adicionar_cano:
            pontos += 1
            canos.append(Cano(TELA_L + 100))
            for genima in list_gen:
                genima.fitness += 5

        for cano in remover_canos:
            canos.remove(cano)

        for i, passaro in enumerate(passaros):
            if passaro.y + passaro.img.get_height() > TELA_A - 70  or passaro.y < 0:
                passaros.pop(i)
                if ai_jogando:
                    list_gen[i].fitness -= 0.5
                    list_gen.pop(i)
                    redes.pop(i)

        if passaros == []:
            print(f"Você fez {pontos} pontos PARABÉNS")
            
        desenha_tela(tela, passaros, canos, chao, pontos)
    print(pontos)
    
def rodar(caminho):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, caminho)
    populacao = neat.Population(config)
    populacao.add_reporter(neat.StdOutReporter(True))
    populacao.add_reporter(neat.StatisticsReporter())
    
    if ai_jogando:
        populacao.run(main)
    else:
        main()

if __name__ == '__main__':
    caminho = os.path.dirname(__file__)
    caminho_config = os.path.join(caminho, "config.txt")
    rodar(caminho_config)