import pygame
import sys
from button import Button

# Inisialisasi pygame dan mixer
pygame.init()
pygame.mixer.init()

# Mengatur Ukuran layar
WIDTH, HEIGHT = 700, 500
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pomodoro Timer")

# Menagatur Font & clock
FONT = pygame.font.SysFont("arial", 120)
BUTTON_FONT = pygame.font.SysFont("arial", 20)
CLOCK = pygame.time.Clock()

# Mengatur Gambar & suara
BACKDROP = pygame.image.load("assets/bebek.jpg")
WHITE_BUTTON = pygame.image.load("assets/button.png")
ALARM_SOUND = pygame.mixer.Sound("assets/alarm.mp3")

# Membuat Tombol
START_STOP_BUTTON = Button(WHITE_BUTTON, (WIDTH / 2, HEIGHT / 2 + 100), 170, 60, "START", BUTTON_FONT, "#32aa3a", "#eb391a")
POMODORO_BUTTON = Button(WHITE_BUTTON, (WIDTH / 2 - 150, HEIGHT / 2 - 140), 120, 30, "Pomodoro", BUTTON_FONT, "#32aa3a", "#eb391a")
SHORT_BREAK_BUTTON = Button(WHITE_BUTTON, (WIDTH / 2, HEIGHT / 2 - 140), 120, 30, "Short Break", BUTTON_FONT, "#32aa3a", "#eb391a")
LONG_BREAK_BUTTON = Button(WHITE_BUTTON, (WIDTH / 2 + 150, HEIGHT / 2 - 140), 120, 30, "Long Break", BUTTON_FONT, "#32aa3a", "#eb391a")

# Durasi waktu
POMODORO_LENGTH = 1500        # Durasi 25 menit
SHORT_BREAK_LENGTH = 300      # Durasi 5 menit
LONG_BREAK_LENGTH = 900       # Durasi 15 menit

# Status timer
current_seconds = POMODORO_LENGTH
started = False
alarm_played = False
alarm_channel = None

# Timer event per detik
pygame.time.set_timer(pygame.USEREVENT, 1000)

# Posisi teks timer
timer_text_rect = pygame.Rect(0, 0, WIDTH, HEIGHT)
timer_text_rect.centery = HEIGHT // 2 - 25

# Fungsi: Mengubah teks tombol START/STOP
def update_start_stop_text():
    START_STOP_BUTTON.text_input = "STOP" if started else "START"
    START_STOP_BUTTON.text = BUTTON_FONT.render(START_STOP_BUTTON.text_input, True, START_STOP_BUTTON.base_color)

# Fungsi: Reset timer & stop alarm 
def reset_timer(duration):
    global current_seconds, started, alarm_played, alarm_channel
    current_seconds = duration
    started = False
    alarm_played = False
    if alarm_channel and alarm_channel.get_busy():
        alarm_channel.stop()
    update_start_stop_text()

# Loop utama
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Mendeteksi klik tombol
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            if START_STOP_BUTTON.check_for_input(mouse_pos):
                started = not started
                update_start_stop_text()

                # Menghentikan alarm jika sedang berbunyi
                if alarm_channel and alarm_channel.get_busy():
                    alarm_channel.stop()

            elif POMODORO_BUTTON.check_for_input(mouse_pos):
                reset_timer(POMODORO_LENGTH)

            elif SHORT_BREAK_BUTTON.check_for_input(mouse_pos):
                reset_timer(SHORT_BREAK_LENGTH)

            elif LONG_BREAK_BUTTON.check_for_input(mouse_pos):
                reset_timer(LONG_BREAK_LENGTH)

        # Menghitung waktu tiap detik jika aktif
        if event.type == pygame.USEREVENT and started and current_seconds > 0:
            current_seconds -= 1

    # Menghitung menit dan detik
    display_minutes = max(current_seconds, 0) // 60
    display_seconds = max(current_seconds, 0) % 60

    # Memainkan alarm satu kali saat waktu habis
    if current_seconds <= 0 and not alarm_played:
        alarm_channel = ALARM_SOUND.play()
        alarm_played = True

    # Gambar latar
    SCREEN.fill("#141313")
    SCREEN.blit(BACKDROP, BACKDROP.get_rect(center=(WIDTH / 2, HEIGHT / 2)))

    # Gambar semua tombol
    for btn in [START_STOP_BUTTON, POMODORO_BUTTON, SHORT_BREAK_BUTTON, LONG_BREAK_BUTTON]:
        btn.change_color(pygame.mouse.get_pos())
        btn.update(SCREEN)

    # Menampilkan timer
    timer_text = FONT.render(f"{display_minutes:02}:{display_seconds:02}", True, "#198120")
    SCREEN.blit(timer_text, timer_text.get_rect(center=timer_text_rect.center))

    # Merefresh layar
    pygame.display.update()