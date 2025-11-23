# hostAgent_blobs.py
import os
import random
import spade
from spade.agent import Agent
from spade.behaviour import PeriodicBehaviour

from blob import Blob

WIDTH = 800
HEIGHT = 600

NUM_BLOBS_INICIAL = 20
NUM_FOOD_POR_DIA = 60    # más comida por día

PASOS_POR_DIA = 150     # el día dura menos pasos

ENERGIA_MIN_SUPERVIVENCIA = 40  # umbral más bajo
PROB_REPRODUCCION = 0.6

blobs: list[Blob] = []
food: list[tuple[float, float]] = []


def blob2dict(blob: Blob):
    return {
        "x": blob.x,
        "y": blob.y,
        "alive": blob.alive,
        "speed": blob.speed,
        "energy": blob.energy,
    }


def food2dict(point):
    x, y = point
    return {"x": x, "y": y}


class HostAgent(Agent):
    class WorldBehaviour(PeriodicBehaviour):
        async def on_start(self):
            self.agent.day = 0
            self.agent.step_in_day = 0
            self.agent.phase = "buscar"
            print(f"WorldBehaviour corre cada {self.period} segundos")

        async def run(self):
            # si es el inicio del día
            if self.agent.step_in_day == 0:
                self.agent.start_day()

            # avanzar un paso en todos los blobs
            for b in blobs:
                b.step()

            self.agent.step_in_day += 1

            # criterio para pasar de buscar -> volver
            if self.agent.phase == "buscar":
                if self.agent.step_in_day >= PASOS_POR_DIA * 0.85 or len(food) == 0:
                    self.agent.phase = "volver"

            # fin de día
            if self.agent.step_in_day >= PASOS_POR_DIA:
                self.agent.end_day()
                # si no quedan blobs vivos, reiniciamos población
                if not blobs:
                    self.agent.init_population()
                # nuevo día
                self.agent.step_in_day = 0
                self.agent.phase = "buscar"

    async def setup(self):
        print(f"Agente {self.jid} started...")
        self.day = 0
        self.phase = "buscar"

        self.init_population()          # llena la lista global blobs
        self.food = food                # 👈 enlace el atributo al listado global
        self.blobs = blobs              # opcional pero recomendable

        self.add_behaviour(self.WorldBehaviour(period=0.2))

        print("Host agent started!")

    # -------- lógica de mundo --------
    def init_population(self):
        blobs.clear()
        for _ in range(NUM_BLOBS_INICIAL):
            blobs.append(Blob(WIDTH, HEIGHT, self))

    def generar_comida(self):
        food.clear()
        for _ in range(NUM_FOOD_POR_DIA):
            x = random.uniform(0, WIDTH)
            y = random.uniform(0, HEIGHT)
            food.append((x, y))

    def start_day(self):
        self.day += 1
        print(f"=== Día {self.day} ===")
        self.generar_comida()
        for b in blobs:
            b.reset_for_new_day()

    def end_day(self):
        global blobs
        print(f"Fin del día {self.day}")
        nuevos = []
        sobrevivientes = []

        for b in blobs:
            if not b.alive:
                continue
            if b.energy >= ENERGIA_MIN_SUPERVIVENCIA:
                sobrevivientes.append(b)
                # reproducción con mutación en velocidad
                if random.random() < PROB_REPRODUCCION:
                    hijo = Blob(WIDTH, HEIGHT, self)
                    hijo.home_x = b.home_x
                    hijo.home_y = b.home_y
                    hijo.x = hijo.home_x
                    hijo.y = hijo.home_y
                    hijo.speed = max(0.1, b.speed + random.gauss(0, 0.3))
                    nuevos.append(hijo)
        blobs = sobrevivientes + nuevos
        print(f"Sobrevivientes: {len(sobrevivientes)}, nuevos: {len(nuevos)}")

    # -------- estado para la GUI --------
    def get_state(self):
        return {
            "day": self.day,
            "phase": self.phase,
            "blobs": [blob2dict(b) for b in blobs],
            "food": [food2dict(f) for f in food],
        }


async def main():
    host = HostAgent("dummy@localhost", "123456abcd.")
    await host.start()

    async def state_controller(_):
        return host.get_state()

    # API para la GUI
    host.web.add_get("/state", state_controller, template=None)
    host.web.start(port=10000)

    # archivos estáticos (html/js)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    static_folder = os.path.join(base_dir, "static")
    host.web.app.router.add_static("/static/", path=static_folder, name="static")

    print("HostAgent blobs lanzado...")
    await spade.wait_until_finished(host)


if __name__ == "__main__":
    spade.run(main())
