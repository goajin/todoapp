import pygame
import os
import random
import sys

# 사운드 초기화 (소리 문제 방지)
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()

# 창 설정
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Stock Simulation Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 18)

# 경로 설정
ASSETS_PATH = os.path.join(os.getcwd(), "assets")
fail_sound_path = os.path.join(ASSETS_PATH, "fail.mp3")

# 사운드 불러오기
if os.path.exists(fail_sound_path):
    try:
        fail_sound = pygame.mixer.Sound(fail_sound_path)
    except Exception as e:
        print(f"Sound Load Error: {e}")
        fail_sound = None
else:
    print("fail.mp3 not found!")
    fail_sound = None

# 이미지 불러오기
def load_image(filename, scale=0.3):
    path = os.path.join(ASSETS_PATH, filename)
    image = pygame.image.load(path).convert_alpha()
    w, h = image.get_size()
    return pygame.transform.scale(image, (int(w * scale), int(h * scale)))

# 로고 이미지
companies = [
    {"name": "BONHA", "price": 100, "shares": 0, "img": load_image("bonha.png")},
    {"name": "EGIYA", "price": 120, "shares": 0, "img": load_image("egi.png")},
    {"name": "MUHYUN", "price": 150, "shares": 0, "img": load_image("muhyun.png")}
]

# 드럼통 이미지 (상장폐지 표시)
delist_img = load_image("drum.png", scale=0.2)

# 게임 상태
cash = 1000
day = 1
event_message = ""
event_image = None
event_percent = 0

# 버튼
next_day_btn = pygame.Rect(WIDTH - 140, HEIGHT - 60, 120, 40)

# 거래 함수
def buy_stock(company):
    global cash
    if cash >= company["price"]:
        cash -= company["price"]
        company["shares"] += 1

def sell_stock(company):
    global cash
    if company["shares"] > 0:
        company["shares"] -= 1
        cash += company["price"]

# 이벤트 발생
def apply_random_events():
    global event_message, event_image, event_percent
    event_message = ""
    event_image = None
    event_percent = 0

    for company in companies:
        chance = random.randint(1, 100)
        if chance <= 15:
            drop_percent = random.randint(20, 60)
            company["price"] = int(company["price"] * (1 - drop_percent / 100))
            if company["price"] < 20:
                company["price"] = 0
                company["shares"] = 0
                event_message = f"{company['name']} delisted!"
                event_image = delist_img
                if fail_sound:
                    fail_sound.play()
            else:
                event_message = f"Bad news: {company['name']} dropped by {drop_percent}%"
                event_percent = drop_percent
                event_image = delist_img
                if fail_sound:
                    fail_sound.play()

# 다음 날 진행
def next_day():
    global day
    day += 1
    for company in companies:
        if company["price"] > 0:
            change = random.randint(-15, 15)
            company["price"] = max(10, company["price"] + change)
    apply_random_events()

# UI 표시
def draw_ui():
    screen.fill((30, 30, 30))
    screen.blit(font.render(f"Cash: ${cash}", True, (255, 255, 255)), (20, 20))
    screen.blit(font.render(f"Day {day}", True, (255, 255, 255)), (20, 50))

    for i, company in enumerate(companies):
        x = 60 + i * 240
        y = 120
        screen.blit(company["img"], (x, y))

        screen.blit(font.render(company["name"], True, (255, 255, 0)), (x, y + 110))
        screen.blit(font.render(f"${company['price']}", True, (0, 255, 255)), (x, y + 135))
        screen.blit(font.render(f"Shares: {company['shares']}", True, (200, 200, 200)), (x, y + 160))

        buy_btn = pygame.Rect(x, y + 190, 60, 30)
        sell_btn = pygame.Rect(x + 80, y + 190, 60, 30)

        pygame.draw.rect(screen, (0, 200, 0), buy_btn)
        pygame.draw.rect(screen, (200, 0, 0), sell_btn)
        screen.blit(font.render("Buy", True, (0, 0, 0)), (x + 15, y + 195))
        screen.blit(font.render("Sell", True, (0, 0, 0)), (x + 95, y + 195))

        company["buy_btn"] = buy_btn
        company["sell_btn"] = sell_btn

    pygame.draw.rect(screen, (70, 130, 250), next_day_btn, border_radius=10)
    screen.blit(font.render("Next Day", True, (255, 255, 255)), (next_day_btn.x + 15, next_day_btn.y + 10))

    if event_message:
        screen.blit(font.render(event_message, True, (255, 100, 100)), (WIDTH // 2 - 120, HEIGHT - 100))
        if event_image:
            screen.blit(event_image, (WIDTH // 2 - event_image.get_width() // 2, HEIGHT - 200))

# 메인 루프
running = True
while running:
    clock.tick(60)
    draw_ui()
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if next_day_btn.collidepoint(pos):
                next_day()
            for company in companies:
                if company["buy_btn"].collidepoint(pos):
                    buy_stock(company)
                elif company["sell_btn"].collidepoint(pos):
                    sell_stock(company)

pygame.quit()
sys.exit()
