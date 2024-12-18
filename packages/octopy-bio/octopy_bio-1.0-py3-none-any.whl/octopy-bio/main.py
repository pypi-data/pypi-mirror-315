def about():
    print('Octopy the Octopus Biographer v1.0 by Tomokawa Ran. All rights reserved')


def tutorial():
    print('Octopy biographer is very easy to use. Just type in your name, color, \nand Octopy will describe you as is.')


class Octopus:
    def __init__(self, name, color):
        self.name = name
        self.color = color

    def tell(self):
        print(f'\n{self.name} is an octopus with a color of {self.color}.')

        if self.color == 'red':
            print('Red octopuses are often serious and confident.')
        elif self.color == 'blue':
            print('Blue octopuses are known with their calmness and reliability.')
        elif self.color == 'green':
            print('Mostly harmony and sympathy characterize a true green octopus.')
        elif self.color == 'yellow':
            print('Yellow octopuses show their optimism and creativity in most cases.')
        elif self.color == 'black':
            print('Black octopuses are characterized with their strength and mystery.')
        elif self.color == 'white':
            print('White octopus\' character is mostly pure and fulfilled with a new life.')
        else:
            pass
