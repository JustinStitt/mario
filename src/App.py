import Game as g

def main():
    g.game.add_player(g.Player(g.game))
    g.game.load_level(1, 1)
    g.game.run()

if __name__ == '__main__':
    main()
