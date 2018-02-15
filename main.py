import pygame, sys
from pygame.locals import *
from helper import *

def game(a, f, w):

    ### GAME VARIABLES ###
    playing = True
    world_time = w
    ticks = 0
    final_ticks = 0

    ### SHIP VARIABLES ###
    fuel_rate = 0
    burner_rate = 50
    fuel = f
    burning = False
    releasing = False
    maintaining = False
    landed = False
    altitude = a
    velocity = 0
    final_velocity = 0
    acceleration = 0
    crashed = False
    alert = False

    ### PHYSICS VARIABLES ###
    gravity = 2.6
    scale = update_scale(altitude, WINDOW_HEIGHT)



    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Moon Lander')

    ### SOUNDS ###
    pygame.mixer.set_num_channels(8)
    thrust_channel = pygame.mixer.Channel(5)
    crash_sound = pygame.mixer.Sound('sounds/crash.wav')
    thrust_sound = pygame.mixer.Sound('sounds/thrust.wav')
    alert_track = pygame.mixer.music.load('sounds/alert.wav')

    while playing:

        ### EVENT LOOP ###
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == K_UP:
                    burning = True
                elif event.key == K_DOWN:
                    releasing = True
                elif event.key == K_RIGHT or event.key == K_LEFT:
                    maintaining = True
                elif event.key == K_r:
                    ticks = 0
                    final_ticks = 0
                    fuel = f
                    burning = False
                    releasing = False
                    maintaining = False
                    landed = False
                    altitude = a
                    velocity = 0
                    final_velocity = 0
                    acceleration = 0
                    crashed = False
                    alert = False
                    pygame.mixer.music.load('sounds/alert.wav')
            elif event.type == pygame.KEYUP:
                if event.key == K_UP:
                    burning = False
                elif event.key == K_DOWN:
                    releasing = False
                elif event.key == K_RIGHT or event.key == K_LEFT:
                    maintaining = False

        ### LOGIC ###

        thrust_sound.set_volume(fuel_rate * (1/9))
        if fuel == 0:
            if not alert:
                pygame.mixer.music.play(-1)
                alert = True
        if fuel - fuel_rate <= 0:
            burning = False
            maintaining = False
            fuel_rate = fuel
        else:
            fuel_rate = update_fuel_rate(burning, releasing, maintaining, fuel_rate, burner_rate)
        fuel -= fuel_rate

        if burning or maintaining:
            if fuel > 0:
                if not thrust_channel.get_busy():
                    thrust_channel.play(thrust_sound)
        else:
            #thrust_sound.set_volume(0)
            pass

        if altitude > 0:
            altitude = update_altitude(altitude, velocity)
            velocity = update_velocity(velocity, acceleration)
            acceleration = update_acceleration(gravity, fuel_rate)
            ticks += 1
        elif altitude == 0:
            pygame.mixer.music.stop()
            landed = True
            fuel_rate = 0
            final_velocity = velocity
            final_ticks = ticks



        ### DRAWING ###
        test_x(SCREEN, fuel, ticks, landed)




        # Rocket and attached components
        if not crashed:
            pygame.draw.circle(SCREEN, [255, 255, 255], [int(WINDOW_WIDTH / 2), int(WINDOW_HEIGHT - altitude / scale - SHIP_HEIGHT)], int(SHIP_WIDTH / 2))
            pygame.draw.rect(SCREEN, [255, 255, 255], [WINDOW_WIDTH / 2 - (SHIP_WIDTH / 2), (WINDOW_HEIGHT - altitude / scale - SHIP_HEIGHT), SHIP_WIDTH, SHIP_HEIGHT])
        else:
            pygame.draw.rect(SCREEN, [240, 240, 240], [WINDOW_WIDTH / 2 - 30, (WINDOW_HEIGHT - 20), 80, 20])
            pygame.draw.rect(SCREEN, [190, 190, 190], [WINDOW_WIDTH / 2 - 50, (WINDOW_HEIGHT - 40), 30, 40])
            pygame.draw.rect(SCREEN, [255, 255, 255], [WINDOW_WIDTH / 2 - 10, (WINDOW_HEIGHT - 30), 70, 30])
            pygame.draw.rect(SCREEN, [167, 167, 167], [WINDOW_WIDTH / 2 + 20, (WINDOW_HEIGHT - 50), 30, 50])

        # Rocket flames
        if burning or maintaining:
            if not fuel_rate == 0:
                pygame.draw.rect(SCREEN, [238, 118, 0], [- 1 + WINDOW_WIDTH / 2 - (SHIP_WIDTH / 2), (WINDOW_HEIGHT - altitude / scale), SHIP_WIDTH / 3, fuel_rate * 5])
                pygame.draw.rect(SCREEN, [255, 255, 0], [2 + WINDOW_WIDTH / 2 - (SHIP_WIDTH / 2), (WINDOW_HEIGHT - altitude / scale), SHIP_WIDTH / 3, fuel_rate * 6])
                pygame.draw.rect(SCREEN, [255, 51, 0], [1 + WINDOW_WIDTH / 2 - (SHIP_WIDTH / 6), (WINDOW_HEIGHT - altitude / scale), SHIP_WIDTH / 3, fuel_rate * 7])
                pygame.draw.rect(SCREEN, [238, 118, 0], [5 + WINDOW_WIDTH / 2, (WINDOW_HEIGHT - altitude / scale), SHIP_WIDTH / 3, fuel_rate * 5])
                pygame.draw.rect(SCREEN, [255, 255, 0], [1 + WINDOW_WIDTH / 2, (WINDOW_HEIGHT - altitude / scale), SHIP_WIDTH / 3, fuel_rate * 6])

        # The ground
        pygame.draw.rect(SCREEN, [192, 192, 192], [0, WINDOW_HEIGHT - 5, WINDOW_WIDTH, 5])

        # Mission control
        kinematics_font = pygame.font.Font('freesansbold.ttf', 20)


        altitude_display = kinematics_font.render('Altitude: %.2f' % altitude, True, (26, 255, 128))
        velocity_display = kinematics_font.render('Velocity: %.2f' % velocity, True, (26, 255, 128))
        acceleration_display = kinematics_font.render('Acceleration: %.2f' % acceleration, True, (26, 255, 128))

        fuel_display = kinematics_font.render('Fuel: %.3f' % fuel, True, (255, 182, 66))
        fuel_rate_display = kinematics_font.render('Fuel Rate: %.3f' % fuel_rate, True, (255, 182, 66))

        tick_display = kinematics_font.render('T = %d' % ticks, True, (46, 207, 255))

        SCREEN.blit(altitude_display, (10, 10))
        SCREEN.blit(velocity_display, (10, 40))
        SCREEN.blit(acceleration_display, (10, 70))
        SCREEN.blit(fuel_display, (10, 100))
        SCREEN.blit(fuel_rate_display, (10, 130))
        SCREEN.blit(tick_display, (10, 160))

        # Ending screen
        ending_font = pygame.font.Font('freesansbold.ttf', 20)
        if landed:
            if final_velocity <= -25:
                crash_sound.set_volume(1)
                ending_display = ending_font.render("The lander was completely destroyed! Whoops!", True, (255, 0, 0))
                if crashed == False:
                    crash_sound.play()
                    crashed = True
            elif final_velocity < -10:
                crash_sound.set_volume(0.25)
                ending_display = ending_font.render('Slight damage on the lander! Better luck next time!', True, (255, 255, 0))
            else:
                ending_display = ending_font.render('No damage on the lander! Great job!', True, (0, 255, 0))

            ending_rect = ending_display.get_rect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
            SCREEN.blit(ending_display, ending_rect)




        pygame.display.flip()
        pygame.display.update()
        FPSCLOCK.tick(world_time)







if __name__ == '__main__':
    game(3000, 1010, 15)
