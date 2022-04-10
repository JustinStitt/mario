import Game as g
#from Goomba import Goomba
#from Muncher import Muncher

def main():
    g.game.add_player(g.Player(g.game))
    #g.game.add_entity(Goomba(game=g.game, pos=(200, 0)))
    #g.game.add_entity(Muncher(game=g.game, pos=(200, 444)))

    g.game.load_level(1, 1);
    g.game.run()

if __name__ == '__main__':
    main()
