# Practica Calificada 4

**Integrantes:** Milagros Díaz Aguirre, Jorge Tarapa Peña, Franck Goñas Lopez

**Repositorio:** https://github.com/Largefilly/PC4TopicosCC

## Descripción general
La solución implementa una simulación inspirada en "Simulating Natural Selection" del canal Primer utilizando la arquitectura agente-host. 

- **Agente central (`hostAgent_blob.py`)**: instancia un `HostAgent` que administra días, fases, generación de comida, reproducción con mutaciones y expone `/state` para la GUI. Internamente ejecuta un `WorldBehaviour` periódico que orquesta los pasos de la simulación.
- **Agente criatura (`blob.py`)**: cada blob conoce sus coordenadas, energía, velocidad y hogar. Implementa desplazamiento dirigido a comida/casa, movimiento aleatorio cuando no hay objetivos cercanos, consumo de alimento y muerte por falta de energía.
- **Comida**: el agente central rellena la lista `food` con puntos aleatorios cada día (`generar_comida`). Los blobs consumen ítems cercanos usando `_try_eat`, lo que incrementa su energía.
- **GUI (`static/hello.html`, `static/blobs.js`)**: lienzo canvas que pinta blobs y comida en tiempo real. Consulta `/state`, calcula estadísticas (día, fase, vivos/muertos, energía y velocidad promedio) y permite ajustar la cadencia de actualización con un control deslizante.

## Cumplimiento de requisitos
1. **Blobs como agentes con atributos biológicos** (6 pts)  
   Los blobs tienen atributos como posición, velocidad, energía y estado de vida. Buscan comida, gastan energía al desplazarse, pueden morir por falta de energía y reproducirse con una ligera variación en la velocidad, simulando selección natural.

2. **Implementación de la comida** (2 pts)  
   Cada día el agente central genera puntos de comida en el mapa. Los blobs consumen esa comida cuando se acercan y recuperan energía.

3. **Agente central tipo host** (7 pts)  
   Un agente central controla el mundo: crea y resetea la población, genera la comida, avanza los días y mantiene la información necesaria para que la interfaz pueda mostrar el estado de la simulación.

4. **GUI con visualización y velocidad ajustable** (5 pts)  
   La interfaz web muestra en tiempo real la posición de los blobs y la comida, junto con estadísticas básicas de la simulación, y permite ajustar la velocidad de actualización mediante un control deslizante.

5. **Otras condiciones específicas**  
   Los blobs se comunican indirectamente con el agente central a través de su estado, comienzan en bordes aleatorios del mapa, salen cada día a buscar comida y vuelven a su punto de origen. La GUI se puede activar en cualquier momento y no necesita estar encendida todo el tiempo.

## Declaración de uso de IA
Se usó ChatGPT (modelo GPT-5.1) como apoyo para ajustar algunos parámetros de la simulación y recibir guía general sobre la estructura de la interfaz.
