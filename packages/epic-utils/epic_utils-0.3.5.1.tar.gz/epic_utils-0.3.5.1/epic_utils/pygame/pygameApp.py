from ..core import Vector2Int, Vector2, Color
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame as pg

class Application:
    def __init__(self, size : Vector2Int, title : str, updateFunction = None, fps_limit = 60, update_on_pause = False):
        pg.init()
        info = pg.display.Info()
        self.size : Vector2Int = size
        self.title : str = title
        self.paused = False
        self.running = True
        self.clock = pg.time.Clock()
        self.fps = fps_limit
        self.display = pg.display.set_mode(self.size.toTuple())
        self.updateFunction = updateFunction
        self.update_on_pause = update_on_pause
        pg.display.set_caption(self.title)

    def setFPS(self, fps : int):
        self.fps = fps

    def clearScreen(self):
        self.display.fill(Color.Black.toTuple())    

    def setSize(self, size : Vector2Int):
        self.size = size
        self.display = pg.display.set_mode(self.size.toTuple())

    def setPaused(self, paused : bool):
        self.paused = paused

    def stop(self):
        self.running = False

    def run(self):
        while self.running:
            pg.event.pump()
            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT:
                    self.running = False
                    break
            if self.paused:
                if self.update_on_pause and self.updateFunction != None:
                    self.updateFunction([])    
                self.clock.tick(self.fps)
                continue
            if self.updateFunction != None:
                self.updateFunction(events)
            pg.display.update()
            self.clock.tick(self.fps)
        pg.quit()