from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt
import pptx.oxml.ns as nsmap
from lxml import etree

# Slide dimensions: 16:9 widescreen
W = Inches(13.33)
H = Inches(7.5)

prs = Presentation()
prs.slide_width = W
prs.slide_height = H

DARK_BG     = RGBColor(0x0F, 0x17, 0x2A)
ACCENT      = RGBColor(0x38, 0xBD, 0xF8)   # sky blue
ACCENT2     = RGBColor(0x34, 0xD3, 0x99)   # emerald
LIGHT_TEXT  = RGBColor(0xE2, 0xE8, 0xF0)
DIM_TEXT    = RGBColor(0x94, 0xA3, 0xB8)
CARD_BG     = RGBColor(0x1E, 0x29, 0x3B)
WHITE       = RGBColor(0xFF, 0xFF, 0xFF)

blank_layout = prs.slide_layouts[6]  # completely blank


def add_slide():
    slide = prs.slides.add_slide(blank_layout)
    return slide


def fill_bg(slide, color: RGBColor):
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = color


def add_textbox(slide, text, left, top, width, height,
                font_size=18, bold=False, color=LIGHT_TEXT,
                align=PP_ALIGN.LEFT, italic=False, wrap=True):
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = wrap
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size = Pt(font_size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color
    return txBox


def add_rect(slide, left, top, width, height, fill_color, line_color=None, line_width=None):
    shape = slide.shapes.add_shape(
        1,  # MSO_SHAPE_TYPE.RECTANGLE
        left, top, width, height
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    if line_color:
        shape.line.color.rgb = line_color
        if line_width:
            shape.line.width = line_width
    else:
        shape.line.fill.background()
    return shape


def add_multiline_textbox(slide, lines, left, top, width, height,
                          font_size=14, color=LIGHT_TEXT, align=PP_ALIGN.LEFT,
                          line_spacing=1.2):
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    first = True
    for line in lines:
        if first:
            p = tf.paragraphs[0]
            first = False
        else:
            p = tf.add_paragraph()
        p.alignment = align
        run = p.add_run()
        run.text = line
        run.font.size = Pt(font_size)
        run.font.color.rgb = color
    return txBox


# ──────────────────────────────────────────────
# Slide 1 — Title
# ──────────────────────────────────────────────
s1 = add_slide()
fill_bg(s1, DARK_BG)

# Subtitle label
add_textbox(s1, "САМОПРЕЗЕНТАЦИЯ · 2025",
            Inches(0.5), Inches(1.2), Inches(12), Inches(0.4),
            font_size=11, color=ACCENT, align=PP_ALIGN.CENTER)

# Name
add_textbox(s1, "Адаменко Семён",
            Inches(0.5), Inches(1.8), Inches(12), Inches(1.2),
            font_size=52, bold=True, color=LIGHT_TEXT, align=PP_ALIGN.CENTER)

# Role
add_textbox(s1, "Golang Backend Developer",
            Inches(0.5), Inches(3.0), Inches(12), Inches(0.6),
            font_size=22, color=ACCENT, align=PP_ALIGN.CENTER)

# Tags row
tags = ["3+ года опыта", "Санкт-Петербург", "Remote-friendly", "English B2"]
tag_w = Inches(2.2)
tag_h = Inches(0.38)
total_tag_w = tag_w * 4 + Inches(0.2) * 3
start_x = (W - total_tag_w) / 2
for i, tag in enumerate(tags):
    tx = start_x + i * (tag_w + Inches(0.2))
    r = add_rect(s1, tx, Inches(3.8), tag_w, tag_h, CARD_BG, ACCENT)
    add_textbox(s1, tag, tx, Inches(3.82), tag_w, tag_h,
                font_size=11, color=ACCENT, align=PP_ALIGN.CENTER)

# Contacts
contacts = "semaadamenko13@gmail.com   ·   +7 (964) 391-75-35   ·   t.me/semaadamenko"
add_textbox(s1, contacts,
            Inches(0.5), Inches(4.5), Inches(12), Inches(0.4),
            font_size=13, color=DIM_TEXT, align=PP_ALIGN.CENTER)


# ──────────────────────────────────────────────
# Slide 2 — About
# ──────────────────────────────────────────────
s2 = add_slide()
fill_bg(s2, DARK_BG)

add_textbox(s2, "Обо мне",
            Inches(0.5), Inches(0.4), Inches(12), Inches(0.7),
            font_size=28, bold=True, color=LIGHT_TEXT, align=PP_ALIGN.CENTER)

cards = [
    ("Кто я",
     "Backend-разработчик с опытом в высоконагруженных системах.\nСпециализируюсь на Go-сервисах, событийной архитектуре\nи микросервисах. Учусь на 4 курсе РГПУ им. Герцена."),
    ("Профессиональная цель",
     "Развиваться как fullstack-разработчик и техлид\nв продуктовой IT-компании. Интересны задачи:\nпроизводительность, архитектура, менторство."),
    ("Ключевые навыки",
     "→ Golang — основной язык (3+ лет)\n→ Distributed systems, Kafka, gRPC\n→ PostgreSQL, Redis, ClickHouse\n→ Docker, Kubernetes, CI/CD\n→ Prometheus, Grafana, ELK"),
    ("Soft skills",
     "→ Менторство и онбординг\n→ Code review\n→ Командная разработка\n→ Техническое интервью\n→ Самообучение и инициатива"),
]

cols = 2
card_w = Inches(5.8)
card_h = Inches(2.4)
gap_x = Inches(0.4)
gap_y = Inches(0.3)
start_x = Inches(0.8)
start_y = Inches(1.3)

for idx, (title, body) in enumerate(cards):
    col = idx % cols
    row = idx // cols
    cx = start_x + col * (card_w + gap_x)
    cy = start_y + row * (card_h + gap_y)
    add_rect(s2, cx, cy, card_w, card_h, CARD_BG, RGBColor(0x2D, 0x3E, 0x50))
    add_textbox(s2, title, cx + Inches(0.2), cy + Inches(0.15), card_w - Inches(0.4), Inches(0.35),
                font_size=10, bold=True, color=ACCENT)
    add_textbox(s2, body, cx + Inches(0.2), cy + Inches(0.55), card_w - Inches(0.4), card_h - Inches(0.7),
                font_size=12, color=RGBColor(0xCB, 0xD5, 0xE1))


# ──────────────────────────────────────────────
# Slide 3 — Experience: ГрузовичкоФ
# ──────────────────────────────────────────────
s3 = add_slide()
fill_bg(s3, RGBColor(0x0F, 0x20, 0x27))

add_textbox(s3, "Опыт работы · 1/2",
            Inches(0.5), Inches(0.3), Inches(12), Inches(0.6),
            font_size=26, bold=True, color=LIGHT_TEXT, align=PP_ALIGN.CENTER)

# Card
cx, cy = Inches(0.7), Inches(1.1)
cw, ch = Inches(11.9), Inches(5.6)
r = add_rect(s3, cx, cy, cw, ch, CARD_BG, RGBColor(0x2D, 0x3E, 0x50))
# Blue left border
add_rect(s3, cx, cy, Inches(0.08), ch, ACCENT)

add_textbox(s3, "ГрузовичкоФ", cx + Inches(0.25), cy + Inches(0.2), Inches(6), Inches(0.55),
            font_size=22, bold=True, color=LIGHT_TEXT)
add_textbox(s3, "Golang Developer", cx + Inches(0.25), cy + Inches(0.75), Inches(6), Inches(0.4),
            font_size=14, color=ACCENT, bold=True)
add_textbox(s3, "Июнь 2023 — Февраль 2025 · 1 г. 9 мес.",
            cx + Inches(7), cy + Inches(0.25), Inches(4.5), Inches(0.4),
            font_size=12, color=DIM_TEXT, align=PP_ALIGN.RIGHT)

achievements = [
    "▸ Сервис управления заказами: тарифный расчёт, учёт грузов, биллинг",
    "▸ Кэширование геолокации транспорта (Redis) — повторное использование маршрутов",
    "▸ API Gateway с OTP-авторизацией через SMS-коды",
    "▸ Событийная архитектура на Kafka — обработка пиковых нагрузок",
    "▸ CI/CD в GitLab: линтеры, автотесты, сокращение времени релизов",
    "▸ Менторство: код-ревью, собеседования, онбординг новых разработчиков",
]
for i, ach in enumerate(achievements):
    col = i % 2
    row = i // 2
    ax = cx + Inches(0.25) + col * Inches(5.8)
    ay = cy + Inches(1.3) + row * Inches(0.55)
    add_textbox(s3, ach, ax, ay, Inches(5.6), Inches(0.5),
                font_size=11, color=RGBColor(0xCB, 0xD5, 0xE1))

stack = ["Go", "PostgreSQL", "Kafka", "Redis", "gRPC", "Protobuf", "Docker", "k8s", "GitLab CI/CD", "Prometheus", "Grafana", "ClickHouse"]
bx = cx + Inches(0.25)
by = cy + Inches(4.05)
badge_h = Inches(0.32)
badge_gap = Inches(0.1)
bw_map = [Inches(0.45), Inches(1.1), Inches(0.65), Inches(0.6), Inches(0.55),
          Inches(0.85), Inches(0.7), Inches(0.45), Inches(1.2), Inches(1.05), Inches(0.8), Inches(1.1)]
cur_x = bx
for tag, bw in zip(stack, bw_map):
    add_rect(s3, cur_x, by, bw, badge_h, RGBColor(0x0D, 0x2D, 0x22), RGBColor(0x34, 0xD3, 0x99))
    add_textbox(s3, tag, cur_x, by + Inches(0.03), bw, badge_h,
                font_size=9, color=ACCENT2, align=PP_ALIGN.CENTER)
    cur_x += bw + badge_gap


# ──────────────────────────────────────────────
# Slide 4 — Experience: Grow Food
# ──────────────────────────────────────────────
s4 = add_slide()
fill_bg(s4, RGBColor(0x0F, 0x20, 0x27))

add_textbox(s4, "Опыт работы · 2/2",
            Inches(0.5), Inches(0.3), Inches(12), Inches(0.6),
            font_size=26, bold=True, color=LIGHT_TEXT, align=PP_ALIGN.CENTER)

cx, cy = Inches(0.7), Inches(1.1)
cw, ch = Inches(11.9), Inches(5.6)
add_rect(s4, cx, cy, cw, ch, CARD_BG, RGBColor(0x2D, 0x3E, 0x50))
add_rect(s4, cx, cy, Inches(0.08), ch, ACCENT)

add_textbox(s4, "Grow Food", cx + Inches(0.25), cy + Inches(0.2), Inches(6), Inches(0.55),
            font_size=22, bold=True, color=LIGHT_TEXT)
add_textbox(s4, "Golang Developer", cx + Inches(0.25), cy + Inches(0.75), Inches(6), Inches(0.4),
            font_size=14, color=ACCENT, bold=True)
add_textbox(s4, "Декабрь 2021 — Май 2023 · 1 г. 6 мес.",
            cx + Inches(7), cy + Inches(0.25), Inches(4.5), Inches(0.4),
            font_size=12, color=DIM_TEXT, align=PP_ALIGN.RIGHT)

achievements4 = [
    "▸ Сервис рационов питания: категории, аллергены, спецпредложения",
    "▸ Управление заказами: связь с учётом склада, проверка ингредиентов",
    "▸ Автоматическое формирование меню по наличию ингредиентов",
    "▸ Docker + Kubernetes (Helm) — горизонтальное масштабирование",
    "▸ Prometheus + Grafana + ELK — мониторинг и диагностика",
    "▸ Интеграционные тесты, код-ревью, менторство коллег",
]
for i, ach in enumerate(achievements4):
    col = i % 2
    row = i // 2
    ax = cx + Inches(0.25) + col * Inches(5.8)
    ay = cy + Inches(1.3) + row * Inches(0.55)
    add_textbox(s4, ach, ax, ay, Inches(5.6), Inches(0.5),
                font_size=11, color=RGBColor(0xCB, 0xD5, 0xE1))

stack4 = ["Go", "PostgreSQL", "REST", "Docker", "k8s", "Redis", "Prometheus", "Grafana", "ELK"]
bw4_map = [Inches(0.45), Inches(1.1), Inches(0.55), Inches(0.7), Inches(0.45),
           Inches(0.6), Inches(1.05), Inches(0.8), Inches(0.45)]
bx4 = cx + Inches(0.25)
by4 = cy + Inches(4.05)
cur_x4 = bx4
for tag, bw in zip(stack4, bw4_map):
    add_rect(s4, cur_x4, by4, bw, badge_h, RGBColor(0x0D, 0x2D, 0x22), RGBColor(0x34, 0xD3, 0x99))
    add_textbox(s4, tag, cur_x4, by4 + Inches(0.03), bw, badge_h,
                font_size=9, color=ACCENT2, align=PP_ALIGN.CENTER)
    cur_x4 += bw + badge_gap


# ──────────────────────────────────────────────
# Slide 5 — Tech Stack
# ──────────────────────────────────────────────
s5 = add_slide()
fill_bg(s5, DARK_BG)

add_textbox(s5, "Технический стек",
            Inches(0.5), Inches(0.3), Inches(12), Inches(0.6),
            font_size=28, bold=True, color=LIGHT_TEXT, align=PP_ALIGN.CENTER)

stack_data = [
    ("Языки",               "Go · Python · SQL · Bash"),
    ("Базы данных",         "PostgreSQL · MySQL · MongoDB · Redis · ClickHouse"),
    ("Очереди и стриминг",  "Apache Kafka · RabbitMQ"),
    ("Протоколы и API",     "REST · gRPC · Protobuf"),
    ("Инфраструктура",      "Docker · Kubernetes · Helm · GitLab CI/CD · Linux"),
    ("Мониторинг и тесты",  "Prometheus · Grafana · ELK · Testify"),
]

sw = Inches(3.8)
sh = Inches(1.9)
sg_x = Inches(0.25)
sg_y = Inches(0.3)
s5_start_x = Inches(0.55)
s5_start_y = Inches(1.2)

for idx, (cat, techs) in enumerate(stack_data):
    col = idx % 3
    row = idx // 3
    sx = s5_start_x + col * (sw + sg_x)
    sy = s5_start_y + row * (sh + sg_y)
    add_rect(s5, sx, sy, sw, sh, CARD_BG, RGBColor(0x2D, 0x3E, 0x50))
    add_textbox(s5, cat, sx + Inches(0.2), sy + Inches(0.15), sw - Inches(0.4), Inches(0.35),
                font_size=10, bold=True, color=ACCENT)
    add_textbox(s5, techs, sx + Inches(0.2), sy + Inches(0.55), sw - Inches(0.4), sh - Inches(0.7),
                font_size=13, color=RGBColor(0xCB, 0xD5, 0xE1))


# ──────────────────────────────────────────────
# Slide 6 — Portfolio
# ──────────────────────────────────────────────
s6 = add_slide()
fill_bg(s6, RGBColor(0x0D, 0x1B, 0x2A))

add_textbox(s6, "Портфолио и достижения",
            Inches(0.5), Inches(0.3), Inches(12), Inches(0.6),
            font_size=28, bold=True, color=LIGHT_TEXT, align=PP_ALIGN.CENTER)

portfolio = [
    ("Сервис заказов · ГрузовичкоФ",
     "Полный цикл: тарифный расчёт, учёт по типу/весу груза,\nинтеграция с биллингом. Событийная обработка через Kafka.",
     "gruzovichkof.ru"),
    ("Сервис рационов питания · Grow Food",
     "Система категорий (диеты, аллергены), автогенерация меню,\nгоризонтальное масштабирование в k8s.",
     "growfood.pro"),
    ("API Gateway с OTP",
     "Защита критических эндпоинтов через SMS-авторизацию.\nГарантия доставки OTP-кодов, логирование попыток.",
     "github.com/paniccaaa"),
    ("CI/CD · GitLab Pipelines",
     "Пайплайны с линтерами (golangci-lint), юнит- и\nинтеграционными тестами, автодеплоем.",
     "github.com/paniccaaa"),
]

pw = Inches(5.8)
ph = Inches(2.5)
pg_x = Inches(0.4)
pg_y = Inches(0.3)
p6_sx = Inches(0.8)
p6_sy = Inches(1.2)

for idx, (title, desc, link) in enumerate(portfolio):
    col = idx % 2
    row = idx // 2
    px = p6_sx + col * (pw + pg_x)
    py = p6_sy + row * (ph + pg_y)
    add_rect(s6, px, py, pw, ph, CARD_BG, RGBColor(0x2D, 0x3E, 0x50))
    add_textbox(s6, title, px + Inches(0.2), py + Inches(0.15), pw - Inches(0.4), Inches(0.4),
                font_size=13, bold=True, color=ACCENT)
    add_textbox(s6, desc, px + Inches(0.2), py + Inches(0.6), pw - Inches(0.4), Inches(1.2),
                font_size=11, color=DIM_TEXT)
    add_textbox(s6, link, px + Inches(0.2), py + Inches(1.95), pw - Inches(0.4), Inches(0.35),
                font_size=11, color=ACCENT2)


# ──────────────────────────────────────────────
# Slide 7 — Personal Qualities
# ──────────────────────────────────────────────
s7 = add_slide()
fill_bg(s7, DARK_BG)

add_textbox(s7, "Личные качества",
            Inches(0.5), Inches(0.3), Inches(12), Inches(0.6),
            font_size=28, bold=True, color=LIGHT_TEXT, align=PP_ALIGN.CENTER)

qualities = [
    ("Аналит. мышление", 850),
    ("Обучаемость",      830),
    ("Упорство",         800),
    ("Алгоритм. подход", 780),
    ("Ответственность",  720),
    ("Решение задач",    700),
    ("Концентрация",     600),
    ("Коммуникаб-сть",   520),
    ("Инициативность",   470),
    ("Работа в команде", 420),
]

qw = Inches(2.2)
qh = Inches(1.8)
qg = Inches(0.18)
q_sx = Inches(0.55)
q_sy = Inches(1.2)

for idx, (label, score) in enumerate(qualities):
    col = idx % 5
    row = idx // 5
    qx = q_sx + col * (qw + qg)
    qy = q_sy + row * (qh + qg)
    add_rect(s7, qx, qy, qw, qh, CARD_BG, RGBColor(0x2D, 0x3E, 0x50))
    # Score
    add_textbox(s7, str(score), qx, qy + Inches(0.15), qw, Inches(0.4),
                font_size=18, bold=True, color=ACCENT, align=PP_ALIGN.CENTER)
    # Bar background
    bar_bg_h = Inches(0.07)
    bar_y = qy + Inches(0.65)
    add_rect(s7, qx + Inches(0.15), bar_y, qw - Inches(0.3), bar_bg_h, RGBColor(0x2D, 0x3E, 0x50))
    # Bar fill
    fill_ratio = score / 1000
    bar_fill_w = (qw - Inches(0.3)) * fill_ratio
    if bar_fill_w > 0:
        add_rect(s7, qx + Inches(0.15), bar_y, bar_fill_w, bar_bg_h, ACCENT)
    # Label
    add_textbox(s7, label, qx, qy + Inches(0.85), qw, Inches(0.5),
                font_size=10, color=RGBColor(0xCB, 0xD5, 0xE1), align=PP_ALIGN.CENTER)

add_textbox(s7, "Шкала: 0–1000 гр. по методике самооценки профессиональных качеств",
            Inches(0.5), Inches(6.9), Inches(12), Inches(0.35),
            font_size=9, color=RGBColor(0x47, 0x55, 0x69), align=PP_ALIGN.CENTER)


# ──────────────────────────────────────────────
# Slide 8 — Final
# ──────────────────────────────────────────────
s8 = add_slide()
fill_bg(s8, DARK_BG)

add_textbox(s8, "ГОТОВ К РАБОТЕ",
            Inches(0.5), Inches(1.2), Inches(12), Inches(0.4),
            font_size=11, color=ACCENT, align=PP_ALIGN.CENTER)

add_textbox(s8, "Возьмите меня в команду",
            Inches(0.5), Inches(1.8), Inches(12), Inches(1.1),
            font_size=42, bold=True, color=LIGHT_TEXT, align=PP_ALIGN.CENTER)

add_textbox(s8,
    "3+ года коммерческого опыта в highload Go-разработке.\n"
    "Строил и поддерживал распределённые сервисы в двух продуктовых компаниях.\n"
    "Готов развиваться и делиться опытом в сильной команде.",
    Inches(1.5), Inches(3.1), Inches(10), Inches(1.2),
    font_size=15, color=DIM_TEXT, align=PP_ALIGN.CENTER)

contacts_final = [
    "semaadamenko13@gmail.com",
    "t.me/semaadamenko",
    "github.com/paniccaaa",
]
for i, c in enumerate(contacts_final):
    add_textbox(s8, c,
                Inches(0.5), Inches(4.6) + i * Inches(0.45), Inches(12), Inches(0.4),
                font_size=14, color=ACCENT, align=PP_ALIGN.CENTER)


out = "/Users/semaadamenko/Desktop/projects/herzen/it_recruitment/self-presentation.pptx"
prs.save(out)
print("Saved:", out)
