import Game as g

def main():
    g.game.add_player(g.Player(g.game))
    g.game.add_entity(g.Entity(g.game))
    g.game.run()

if __name__ == '__main__':
    main()
