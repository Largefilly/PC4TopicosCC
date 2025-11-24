# Practica Calificada 4

**Integrantes:** Milagros Díaz Aguirre, Jorge Tarapa Peña, Franck Goñas Lopez

**Repositorio:** https://github.com/Largefilly/PC4TopicosCC

## Descripción general
La solución implementa una simulación inspirada en "Simulating Natural Selection" del canal Primer utilizando la arquitectura agente-host vista en clase. El archivo `hostAgent_blob.py` corre un agente SPADE que mantiene el estado global del mundo, expone un servicio web para la GUI y coordina a los blobs. Cada criatura se define en `blob.py`, donde se le asignan atributos biológicos, comportamiento diario y la lógica para buscar alimento y volver a casa. La interfaz web (`static/hello.html` + `static/blobs.js`) consulta periódicamente al agente para visualizar la simulación y ajustar la velocidad de refresco.

## Componentes principales
- **Agente central (`hostAgent_blob.py`)**: instancia un `HostAgent` que administra días, fases, generación de comida, reproducción con mutaciones y expone `/state` para la GUI. Internamente ejecuta un `WorldBehaviour` periódico que orquesta los pasos de la simulación.
- **Agente criatura (`blob.py`)**: cada blob conoce sus coordenadas, energía, velocidad y hogar. Implementa desplazamiento dirigido a comida/casa, movimiento aleatorio cuando no hay objetivos cercanos, consumo de alimento y muerte por falta de energía.
- **Comida**: el agente central rellena la lista `food` con puntos aleatorios cada día (`generar_comida`). Los blobs consumen ítems cercanos usando `_try_eat`, lo que incrementa su energía.
- **GUI (`static/hello.html`, `static/blobs.js`)**: lienzo canvas que pinta blobs y comida en tiempo real. Consulta `/state`, calcula estadísticas (día, fase, vivos/muertos, energía y velocidad promedio) y permite ajustar la cadencia de actualización con un control deslizante.

## Cumplimiento de requisitos
1. **Blobs como agentes con atributos biológicos** (6 pts)  
   - Cada blob mantiene velocidad, energía, estado de vida, contador de comida y un hogar en el borde del mapa (`Blob.__init__`).  
   - Métodos `step`, `_move_towards`, `_move_random` y `_try_eat` implementan buscar alimento, gastar energía, morir por agotamiento y regresar a casa durante la fase "volver".  
   - Reproducción con mutación de velocidad ocurre al final del día en `HostAgent.end_day`, cumpliendo el desarrollo de nuevas características (extra velocidad).

2. **Implementación de la comida** (2 pts)  
   - `HostAgent.generar_comida` crea `NUM_FOOD_POR_DIA` puntos aleatorios en el mapa.  
   - Cada blob verifica colisiones a un radio de 15 px (`_try_eat`), incrementando energía y removiendo la comida ingerida.

3. **Agente central tipo host** (7 pts)  
   - `HostAgent` hereda de `spade.agent.Agent` y ejecuta `WorldBehaviour` para avanzar pasos, cambiar fases (buscar/volver) y cerrar el día tras `PASOS_POR_DIA`.  
   - Mantiene listas globales de blobs y comida, reinicia población cuando es necesario y expone `get_state` para la GUI.  
   - Ofrece un endpoint `/state` más un servidor estático para la interfaz HTML, replicando la función del host de "pececitos".

4. **GUI con visualización y velocidad ajustable** (5 pts)  
   - `static/hello.html` monta un `<canvas>` y un slider (50–500 ms) que actualiza la variable `delay` en `blobs.js`.  
   - `blobs.js` pinta blobs con colores dependientes de su velocidad y muestra estadísticas detalladas, permitiendo observar la selección natural en tiempo real.  
   - La GUI es opcional: el agente corre de forma independiente y la vista solo se activa cuando el usuario abre la página, cumpliendo el requisito de no mantenerla el 100% del tiempo.

5. **Otras condiciones específicas**  
   - **Comunicación**: los blobs interactúan con el agente central mediante la referencia `parent`, consultando `parent.food` y `parent.phase` para actuar, lo que satisface el canal de comunicación requerido.  
   - **Inicio en bordes**: el constructor de `Blob` asigna un hogar aleatorio sobre cualquiera de los cuatro bordes, asegurando que todos parten desde extremos del mapa.  
   - **Ciclos de día**: `HostAgent.start_day`/`end_day` resetean posiciones, generan comida y evalúan supervivencia, garantizando que cada blob sale, busca alimento y retorna a casa diariamente.  
   - **Desarrollo de características**: la mutación gaussiana en `end_day` altera la velocidad de los descendientes, creando diversidad evolutiva similar al video de referencia.

## Declaración de uso de IA
Se usó Chat gpt (modelo GPT-5.1) como apoyo para ajustar parámetros de la simulación y recibir guía lógica sobre la interfaz. 
