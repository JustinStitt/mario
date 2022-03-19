import Game as g
import Entity as e

def main():
    game = g.Game()
    game.add_entity(e.Entity(game))
    while game.go:
        game.update()
        game.render()

if __name__ == '__main__':
    main()
