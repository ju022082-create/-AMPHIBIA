"""AMPHIBIA: standalone environmental-control simulation (no hardware connected)."""
from datetime import datetime
from zoneinfo import ZoneInfo
import math

KST = ZoneInfo('Asia/Seoul')


def temperature_control(temp):
    if temp >= 40:
        return {'heater': False, 'cooler': False, 'circulation_fan': False, 'status': 'EMERGENCY', 'connected': False}
    return {
        'heater': temp <= 21,
        'cooler': temp >= 24,
        'circulation_fan': temp <= 21,
        'status': 'LOW TEMPERATURE' if temp <= 21 else 'HIGH TEMPERATURE' if temp >= 24 else 'NORMAL',
        'connected': True,
    }


def humidity_control(temp, humidity):
    if temp >= 27:
        return {'misting': False, 'ventilation_fan': True, 'target': 'HIGH-TEMP PROTECTION'}
    if temp <= 20:
        return {'misting': humidity < 85, 'ventilation_fan': False, 'target': '85-100%'}
    return {'misting': humidity < 70, 'ventilation_fan': humidity > 90, 'target': '70-90%'}


def lighting_control(temp, hour):
    return {
        'plant_light': 8 <= hour < 19,
        'uvb_light': 11 <= hour < 16,
        'hot_zone_light': 11 <= hour < 17 and temp <= 21,
    }


def water_control(level, low_warning_active=False):
    if level <= 2:
        low_warning_active = True
    elif level >= 3:
        low_warning_active = False
    return {'low_warning': low_warning_active, 'high_warning': level > 5}


def evaluate(temp, humidity, level, hour, previous_low_warning=False):
    temperature = temperature_control(temp)
    humidity_result = humidity_control(temp, humidity)
    lighting = lighting_control(temp, hour)
    water = water_control(level, previous_low_warning)
    if not temperature['connected']:
        humidity_result['misting'] = False
        humidity_result['ventilation_fan'] = False
        lighting = {key: False for key in lighting}
    return temperature, humidity_result, lighting, water


def read_number(label, minimum=None, maximum=None):
    while True:
        raw = input(label).strip()
        try:
            value = float(raw)
            if not math.isfinite(value) or (minimum is not None and value < minimum) or (maximum is not None and value > maximum):
                raise ValueError
            return value
        except ValueError:
            print('Invalid input. Please enter a valid number within the allowed range.')


def onoff(value):
    return 'ON' if value else 'OFF'


def main():
    print('=== AMPHIBIA | Environmental Control Simulator ===')
    print('Simulation only: no real equipment is connected or disconnected.')
    print('Lighting schedule uses Korea Standard Time (KST).')
    previous_low_warning = False
    while True:
        print('\n[1] Run simulation  [Q] Quit')
        choice = input('Select: ').strip().lower()
        if choice == 'q':
            print('Program ended.')
            break
        if choice != '1':
            print('Invalid menu selection.')
            continue
        temp = read_number('Temperature (C): ', -50, 100)
        humidity = read_number('Humidity (%): ', 0, 100)
        level = read_number('Water level (cm): ', 0, 1000)
        current = datetime.now(KST)
        print(f'Current KST: {current:%Y-%m-%d %H:%M}')
        use_custom = input('Use a custom simulation hour? (y/N): ').strip().lower()
        if use_custom == 'y':
            hour = int(read_number('Hour (0-23): ', 0, 23))
        else:
            hour = current.hour
        t, h, l, w = evaluate(temp, humidity, level, hour, previous_low_warning)
        previous_low_warning = w['low_warning']
        print('\n--- TEMPERATURE ---')
        print(f"Status: {t['status']} | Heater: {onoff(t['heater'])} | Cooler: {onoff(t['cooler'])} | Circulation fan: {onoff(t['circulation_fan'])}")
        print('--- HUMIDITY ---')
        print(f"Target: {h['target']} | Misting: {onoff(h['misting'])} | External ventilation fan: {onoff(h['ventilation_fan'])}")
        print('--- LIGHTING ---')
        print(f"Plant light: {onoff(l['plant_light'])} | UVB light: {onoff(l['uvb_light'])} | Hot-zone light: {onoff(l['hot_zone_light'])}")
        print('--- WATER LEVEL ---')
        print(f"Low warning: {onoff(w['low_warning'])} | High warning: {onoff(w['high_warning'])}")
        print('--- SAFETY ---')
        print('EMERGENCY: All actuator commands disabled (simulation).' if not t['connected'] else 'CONNECTED (simulation).')


if __name__ == '__main__':
    main()
