# blob.py
import random
import math

class Blob:
    def __init__(self, width, height, parent):
        self.worldWidth = width
        self.worldHeight = height
        self.parent = parent  # referencia al HostAgent

        # Casa: un punto en el borde del mapa
        side = random.choice(["left", "right", "top", "bottom"])
        if side == "left":
            self.home_x = 0
            self.home_y = random.uniform(0, height)
        elif side == "right":
            self.home_x = width
            self.home_y = random.uniform(0, height)
        elif side == "top":
            self.home_x = random.uniform(0, width)
            self.home_y = 0
        else:  # bottom
            self.home_x = random.uniform(0, width)
            self.home_y = height

        # Posición actual (empieza en casa)
        self.x = self.home_x
        self.y = self.home_y

        # Atributos “biológicos”
        # ⬇️ Más velocidad mínima y más energía para que tengan chance
        self.speed = random.uniform(1.5, 3.0)     # velocidad base
        self.energy = 80                          # energía inicial
        self.alive = True
        self.food_eaten = 0

    # -------- utilitarios --------
    def dist_to(self, x, y):
        return math.hypot(self.x - x, self.y - y)

    def _move_towards(self, tx, ty):
        if not self.alive:
            return
        dx = tx - self.x
        dy = ty - self.y
        d = math.hypot(dx, dy)
        if d == 0:
            return
        step = min(self.speed, d)
        self.x += dx / d * step
        self.y += dy / d * step

        # limitar al mapa
        self.x = min(max(self.x, 0), self.worldWidth)
        self.y = min(max(self.y, 0), self.worldHeight)

        # costo (un poco más bajo)
        self.energy -= 0.4
        if self.energy <= 0:
            self.alive = False

    def _move_random(self):
        if not self.alive:
            return
        ang = random.uniform(0, 2 * math.pi)
        self.x += math.cos(ang) * self.speed
        self.y += math.sin(ang) * self.speed
        self.x = min(max(self.x, 0), self.worldWidth)
        self.y = min(max(self.y, 0), self.worldHeight)

        # costo (igual que en _move_towards)
        self.energy -= 0.4
        if self.energy <= 0:
            self.alive = False

    def reset_for_new_day(self):
        self.x = self.home_x
        self.y = self.home_y
        self.food_eaten = 0
        # la energía se mantiene (selección natural)

    # -------- interacción con comida / día --------
    def _try_eat(self):
        """Come comida si hay una suficientemente cerca."""
        if not self.alive:
            return

        # ⬇️ Comer es más fácil y da más energía
        eat_radius = 15
        for i, (fx, fy) in enumerate(self.parent.food):
            if self.dist_to(fx, fy) <= eat_radius:
                self.food_eaten += 1
                self.energy = min(100, self.energy + 25)
                del self.parent.food[i]
                break

    def step(self):
        """
        Un paso de simulación:
        - si la fase es 'buscar', va a la comida más cercana
        - si la fase es 'volver', va a su casa
        """
        if not self.alive:
            return

        if self.parent.phase == "buscar":
            # buscar comida más cercana
            target = None
            best_d = float("inf")
            for (fx, fy) in self.parent.food:
                d = self.dist_to(fx, fy)
                if d < best_d:
                    best_d = d
                    target = (fx, fy)
            if target:
                self._move_towards(*target)
            else:
                self._move_random()
            self._try_eat()
        else:  # volver a casa
            self._move_towards(self.home_x, self.home_y)
