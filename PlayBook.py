import json

class DrivePlayBook:
    def __init__(self):
        self._gained_yards = 0
        self._plays = []
        self._play_count = 0
        self._total_plays = 0
        self._total_time = 0

    def add(self, play_type, players, gain, name, start, elapsed_time, direction):
        self._plays.append([play_type, players, gain, name, start, elapsed_time, direction])
        self._gained_yards += gain
        self._total_plays += 1
        self._total_time += elapsed_time

    def getPlay(self, number):
        return self._plays[number]

    def getPlays(self):
        return self._plays

    def getPlayCount(self):
        return self._play_count

    def getTotalPlayCount(self):
        return self._total_plays

    def getTotalTime(self):
        time = self._total_time*-1
        minutes = (time // 60) % 60
        seconds = time % 60
        return f"Minutes: {minutes}, seconds: {seconds}"

    def logger(self):
        i = 0
        for play in self._plays:
            print(f"{i}. play: { json.dumps(play) }")
            i += 1