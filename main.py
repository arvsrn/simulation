from __future__ import annotations
import pyglet
from time import time
from typing import Tuple, List
from vector import Vec2
import math
from random import choice

def hex_to_rgb(h: str):
    return list(int(h[i:i+2], 16) / 255 for i in (0, 2, 4))

def hex_to_rgb_abs(h: str):
    return list(int(h[i:i+2], 16) for i in (0, 2, 4))

# i named this function l in my school notes, idk why but ill keep it
def l(time_step: float, distance: Vec2, velocity: Vec2):
    return Vec2(velocity.x + distance.x/time_step, velocity.y + distance.y/time_step)

class Atom:
    size: int # radius
    color: str # hex code
    position: Vec2
    velocity: Vec2
    bonds: List[Atom]
    valency: int
    name: str

    def __init__(self, size: int, color: str, position: Vec2, velocity: Vec2, valency: int, name: str = "Unnamed") -> None:
        self.size = size
        self.color = color
        self.position = position
        self.velocity = velocity
        self.bonds = []
        self.name = name
        self.valency = valency
    
    def add_bond(self, atom: Atom) -> Atom:
        self.bonds.append(atom)
        self.valency -= atom.valency        
        return self

    def can_bond(self, atom: Atom) -> bool:
        return self.valency != 0 and abs(self.valency) - abs(atom.valency) >= 0

    def draw(self, position: Vec2):
        for i, atom in enumerate(self.bonds):
            angle = 360/len(self.bonds) * i
            angle_radians = math.radians(angle)
            atom.draw(position + Vec2(math.cos(angle_radians), math.sin(angle_radians)) * atom.size)

        pyglet.shapes.Circle(
            position.x, 
            position.y, 
            self.size + 2, 
            color=tuple(hex_to_rgb_abs("000000")), 
            segments=128
        ).draw()

        pyglet.shapes.Circle(
            position.x, 
            position.y, 
            self.size, 
            color=tuple(hex_to_rgb_abs(self.color)), 
            segments=128
        ).draw()

class Simulation(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(resizable=False, *args, **kwargs)

        self.set_caption("Simulation v2.0")
        self.set_size(900, 600)

        self.last_frame = time()
        self.inspecting = ""
        self.time_scale = 1.0
        self.debug_mode = False

        self.mousex = 0
        self.mousey = 0

        self.atoms = [
            # Atom(10.0, "E45B44", Vec2.random(600), Vec2.random(50), -2, "Oxygen"),
            # Atom(10.0, "E45B44", Vec2.random(600), Vec2.random(50), -2, "Oxygen"),
            # Atom(10.0, "E45B44", Vec2.random(600), Vec2.random(50), -2, "Oxygen"),
            # Atom(10.0, "E45B44", Vec2.random(600), Vec2.random(50), -2, "Oxygen"),
            # Atom(10.0, "E45B44", Vec2.random(600), Vec2.random(50), -2, "Oxygen"),
            # Atom(6.00, "4D9F7F", Vec2.random(600), Vec2.random(50), 2, "Iron"),
            # Atom(6.00, "4D9F7F", Vec2.random(600), Vec2.random(50), 2, "Iron"),
            # Atom(6.00, "4D9F7F", Vec2.random(600), Vec2.random(50), 2, "Iron"),
            # Atom(6.00, "4D9F7F", Vec2.random(600), Vec2.random(50), 2, "Iron"),
            # Atom(6.00, "4D9F7F", Vec2.random(600), Vec2.random(50), 2, "Iron"),
        ]

        for i in range(25):
            self.atoms.append(Atom(8.00, choice(["E45B44", "4D9F7F", "2C6FF0"]), Vec2.random(600), Vec2.random(25), 1))

    def draw_HUD(self, dt: int):
        pyglet.text.Label(
            f"{round(1/dt, 1)}FPS · {self.time_scale}x {'· ' if self.inspecting else ''} {self.inspecting}", 
            font_name='Menlo', 
            font_size=12,
            x=24,
            y=24,
            color=tuple([*hex_to_rgb_abs("ededed"), 255])
        ).draw()

        pyglet.text.Label(
            f"← Slow down · → Speed up · SPACE Pause · d Debug · ESC Quit · TAB Fullscreen", 
            font_name='Menlo', 
            font_size=10, 
            x=24,
            y=self.height - 24 - 14,
            height=14,
            color=tuple([*hex_to_rgb_abs("a0a0a0"), 255])
        ).draw()

        pyglet.text.Label(
            f"Hover over the particles to view velocity and position. Restart if controls don't work.", 
            font_name='Menlo', 
            font_size=10, 
            x=24,
            y=self.height - 24 - 14 - 14,
            height=14,
            color=tuple([*hex_to_rgb_abs("a0a0a0"), 255])
        ).draw()
    
    def on_mouse_motion(self, x, y, dx, dy):
        self.mousex = x
        self.mousey = y

        for atom in self.atoms:
            pos = atom.position

            if ((x > pos.x - atom.size) and (x < pos.x + atom.size)) and ((y > pos.y - atom.size) and (y < pos.y + atom.size)):
                position_rounded = Vec2(int(atom.position.x), int(atom.position.y))
                velocity_rounded = Vec2(round(atom.velocity.x, 1), round(atom.velocity.y, 1))
                self.inspecting = f"{position_rounded} {velocity_rounded} | Valency: {atom.valency} | {atom.name}"  
                break
            else:
                self.inspecting = ""
            
    def on_key_press(self, symbol, modifiers):
        match symbol:
            case pyglet.window.key.RIGHT:
                self.time_scale += 0.5
            
            case pyglet.window.key.LEFT:
                self.time_scale -= 0.5
            
            case pyglet.window.key.D:
                self.debug_mode = not self.debug_mode

            case pyglet.window.key.SPACE:
                self.time_scale = 0.0 if self.time_scale != 0 else 1.0
            
            case pyglet.window.key.ESCAPE:
                pyglet.app.exit()

            case pyglet.window.key.TAB:
                self.set_fullscreen(not self.fullscreen)

    def draw_arrow(self, a: Vec2, b: Vec2):
        pyglet.shapes.Line(a.x, a.y, b.x, b.y, 1, tuple(hex_to_rgb_abs("7E7E7E"))).draw()

    def on_draw(self):
        current_time = time()
        delta = current_time - self.last_frame
        self.last_frame = current_time

        if self.inspecting:
            self.set_mouse_cursor(self.get_system_mouse_cursor(self.CURSOR_HAND))
        else:
            self.set_mouse_cursor(self.get_system_mouse_cursor(self.CURSOR_DEFAULT))

        self.clear()
        pyglet.gl.glClearColor(*hex_to_rgb("161616"), 1)
        self.draw_HUD(delta)

        batch = pyglet.graphics.Batch()

        if self.debug_mode:
            for atom in self.atoms:
                self.draw_arrow(atom.position, atom.position + atom.velocity)

        for atom in self.atoms:
            atom.position.x += atom.velocity.x * delta * self.time_scale
            atom.position.y += atom.velocity.y * delta * self.time_scale

            if atom.position.x >= self.width or atom.position.x <= 0:
                atom.velocity.x = -atom.velocity.x
                atom.position.x = self.width - 1 if atom.position.x >= self.width else 1
            if atom.position.y >= self.height or atom.position.y <= 0:
                atom.velocity.y = -atom.velocity.y
                atom.position.y = self.height - 1 if atom.position.y >= 600 else 1

            for i, atom2 in enumerate(self.atoms):
                euclid_distance = atom.position - atom2.position
                if euclid_distance == 0: continue # same particle

                if (euclid_distance < atom.size * 2.5) and atom.can_bond(atom2):
                    atom.add_bond(atom2)
                    del self.atoms[i]

                atom.velocity = l(
                    pow(euclid_distance, 2) * 0.05, 
                    Vec2(atom2.position.x - atom.position.x, atom2.position.y - atom.position.y), 
                    atom.velocity
                )

            # draw the atom
            atom.draw(atom.position)
        
        batch.draw()

    def run(self):
        pyglet.app.run()

simulation = Simulation()
simulation.run()