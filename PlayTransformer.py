from lark import Transformer, Tree
from datetime import time, datetime, timedelta

def getDirection(direction):
    if direction == 'left':
        return 3
    elif direction == 'center':
        return 2
    elif direction == 'right':
        return 1.5
    else:
        return 2

class FromPlayToAnimTransformer(Transformer):

    def __init__(self, playbook):
        super().__init__()
        self._ball_position = 0
        self._max_ball_position = 100
        self._is_finished = False
        self._playbook = playbook
        self._players = []
        self._time_elapsed = 0
        self._starting_clock = 0

    def program(self, items):
        return items

    def drive(self, items):
        return items

    def play_statement(self, items):
        self._playbook.add(
            items[2]['play_type'],
            self._players,
            items[2]['gained_yards'],
            items[0],
            items[3]['fieldposition'][0]['value'],
            self._time_elapsed,
            getDirection(items[2]['direction'])
        )
        self._ball_position += items[2]['gained_yards']
        return {
            "play": items[0],
            "setup": items[1],
            "execute": items[2],
            "fieldposition": items[3]
        }

    def setup_block(self, items):
        self._players = [
            items[0]['value'],
            items[1]['value'],
        ]
        return {"setup": items}

    def setup_declaration(self, items):
        return {"position": items[0], "value": items[1]}

    def execute_block(self, items):
        # if self._players[0] is not None and items[0].position != self._players[0]:
        if items[0]['args'][0] != self._players[0]:
            raise Exception("Player 1 doesnt match")
        # if self._players[1] is not None and items[1].position != self._players[1]:
        if items[0]['args'][1] != self._players[1]:
            raise Exception("Player 2 doesnt match")
        if items[0]['play_type'] == 'pass':
            direction = items[0]['args'][3]
        else:
            direction = 'center'
        return {
            "play_type": items[0]['play_type'],
            "gained_yards": items[0]['args'][2],
            "player1": items[0]['args'][0],
            "player2": items[0]['args'][1],
            "direction": direction
        }

    def command(self, items):
        return {
            "play_type": items[0],
            "args": items[1:]
        }

    def fieldposition_block(self, items):
        for identifier in items:
            if identifier['identifier'] == 'ball':
                if identifier['value'] != self._ball_position:
                    raise Exception(f"Ball position doesnt match (expected: {self._ball_position}, got: {identifier['value']})")
            elif identifier['identifier'] == 'clock':
                if self._starting_clock == 0:
                    self._starting_clock = identifier['value']
                else:
                    time1 = identifier['value'].split(':')
                    time2 = self._starting_clock.split(':')
                    time1 = time(0, int(time1[0]), int(time1[1]))
                    time2 = time(0, int(time2[0]), int(time2[1]))

                    datetime1 = datetime.combine(datetime.today(), time1)
                    datetime2 = datetime.combine(datetime.today(), time2)
                    time_elapsed = datetime1 - datetime2
                    self._time_elapsed = time_elapsed.total_seconds()
                    self._starting_clock = identifier['value']
        return {"fieldposition": items}

    def identifier(self, items):
        return {"identifier": items[0], "value": items[1]}

    def STRING(self, s):
        return str(s[1:-1])  # Remove quotes

    def NUMBER(self, n):
        return float(n) if '.' in n else int(n)

    def POSITION(self, p):
        return str(p)

    def KEYWORD(self, k):
        return str(k)

    def IDENTIFIER(self, i):
        return str(i)

    def TIME(self, t):
        return str(t[1:-1])  # Remove quotes

    def BOOLEAN(self, b):
        return b == "true"