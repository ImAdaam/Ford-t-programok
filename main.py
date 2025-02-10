from lark import Lark, Transformer
from PlayTransformer import FromPlayToAnimTransformer
from PlayBook import DrivePlayBook
from Animator import DriveAnimator

with open('grammar.txt', 'r') as file:
    grammar = file.read()

playbook = DrivePlayBook()
# Initialize the parser
parser = Lark(grammar, parser="lalr", transformer=FromPlayToAnimTransformer(playbook))

with open('input.txt', 'r') as file:
    script = file.read()

tree = parser.parse(script)
print(tree.pretty())

# animate
animator = DriveAnimator(playbook)
animator.start()

print(playbook.getTotalTime())