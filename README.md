# AMPHIBIA Web Prototype

This web interface **imports and calls the unchanged `evaluate()` function** from `amphibia_demo.py`. It is a simulation, not real sensor/actuator control.

## Windows / VS Code
1. Extract the ZIP and open the `AMPHIBIA_Web` folder in VS Code.
2. Open Terminal and run `py -m pip install -r requirements.txt`.
3. Run `py app.py`.
4. In a browser, open `http://127.0.0.1:5000`.
5. To stop, press Ctrl+C in the terminal.

If `py` does not work, try `python` instead. If Flask reports that port 5000 is occupied, stop the other server first.

## What is implemented
- Manual temperature/humidity/water level input and optional KST hour.
- The existing Python `evaluate()` logic for temperature, humidity, lighting, and water alerts.
- 40°C emergency handling as simulated actuator OFF commands.
- Previous low-water warning state stored in a browser session (cookie); each browser session has its own state.
- Numeric range and finite-number validation on the server.

## What is not implemented
- No real sensors or hardware; no continuous monitoring.
- No database, analytics, accounts, or multiple habitats.
- Session state is temporary, not durable storage. Development server is for local demonstration, not production deployment.

## Manual test cases
1. Normal: 23°C, 80%, 4cm, 14h → normal; misting OFF; no water warnings.
2. Boundary: 21°C, 85%, 3cm, 12h → heater ON, circulation ON, hot-zone ON.
3. Invalid: humidity 101 → error (server rejects it).
4. Emergency: 40°C, 80%, 4cm, 12h → EMERGENCY; all actuator commands OFF.
5. Hysteresis: water 2cm → 2.5cm → 3cm in the same browser session → low warning ON → ON → OFF.

The console version is still runnable independently with `py amphibia_demo.py`.
