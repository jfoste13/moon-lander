### SYSTEM CONSTANTS ###
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 720
SHIP_WIDTH = 20
SHIP_HEIGHT = 80

def test_x(SCREEN, fuel, ticks, landed):
    if fuel == 0:
        if ticks % 2 == 0 and not landed:
            SCREEN.fill([255, 0, 0])
        else:
            SCREEN.fill([0, 0, 0])
    else:
        SCREEN.fill([0, 0, 0])

### Number, Number --> Number
### Calculate altitude-pixel scale to fit window
def update_scale(max_altitude, window_height):
    return max_altitude // window_height

### Number, Number --> Number
### Return a new altitude based on velocity
def update_altitude(altitude, velocity):
    if altitude + velocity > 0:
        return altitude + velocity
    else:
        return 0

### Number, Number --> Number
### Return a new velocity based on acceleration
def update_velocity(velocity, acceleration):
    return velocity + acceleration

### Number, Number --> Number
### Return a new acceleration based on the current gravity and fuel rate
def update_acceleration(gravity, fuel_rate):
    return (gravity * ((fuel_rate / 5) - 1))

### Boolean, Boolean, Boolean, Number, Number -> Number
### Determine the fuel rate based on user-controlled variables
def update_fuel_rate(burning, releasing, maintaining, fuel_rate, burner_rate):
    if burning:
        if fuel_rate + (.01 * burner_rate) > 9:
            return 9
        else:
            return fuel_rate + (.01 * burner_rate)
    elif releasing:
        if fuel_rate - (.01 * burner_rate) < 0:
            return 0
        else:
            return fuel_rate - (.01 * burner_rate)
    elif maintaining:
        return fuel_rate
    else:
        if fuel_rate - (.01 * 1 * burner_rate) < 0:
            return 0
        else:
            return fuel_rate - (.01 * 1 * burner_rate)
