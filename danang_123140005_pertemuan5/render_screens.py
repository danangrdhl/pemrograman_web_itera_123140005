"""Script to render terminal output into clean PNG screenshots for documentation."""

import subprocess
from PIL import Image, ImageDraw, ImageFont


def render_terminal_image(
    text_lines: list[str],
    output_path: str,
    title: str = "danang@DESKTOP-ITERA: ~/danang_123140005_pertemuan5",
    font_size: int = 14,
):
    font_path = "C:/Windows/Fonts/consola.ttf"
    try:
        font = ImageFont.truetype(font_path, font_size)
    except Exception:
        font = ImageFont.load_default()

    line_height = int(font_size * 1.45)
    padding_x = 24
    padding_top = 44  # header bar height
    padding_bottom = 24

    # Calculate width
    max_line_len = max((len(line) for line in text_lines), default=80)
    # estimate char width roughly 8.5px for 14pt consola
    char_width = 8.5
    img_width = max(800, int(max_line_len * char_width) + padding_x * 2 + 20)
    img_height = padding_top + (len(text_lines) * line_height) + padding_bottom

    # Background
    bg_color = (30, 30, 30)  # VSCode / Modern Terminal dark
    header_color = (45, 45, 45)
    img = Image.new("RGB", (img_width, img_height), bg_color)
    draw = ImageDraw.Draw(img)

    # Header bar
    draw.rectangle([0, 0, img_width, padding_top], fill=header_color)

    # Window control circles (macOS/modern style)
    # Red, Yellow, Green
    draw.ellipse([16, 15, 28, 27], fill=(255, 95, 86))
    draw.ellipse([36, 15, 48, 27], fill=(255, 189, 46))
    draw.ellipse([56, 15, 68, 27], fill=(39, 201, 63))

    # Title text in header
    try:
        title_font = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 12)
    except Exception:
        title_font = font
    draw.text((80, 14), title, fill=(180, 180, 180), font=title_font)

    # Draw text lines
    y = padding_top + 12
    for line in text_lines:
        # Syntax/style coloring
        fill_color = (220, 220, 220)
        if line.startswith("===") or line.startswith("╔═") or line.startswith("╚═"):
            fill_color = (86, 156, 214)  # Soft blue
        elif "[BERHASIL]" in line or "[TERVALIDASI]" in line or "[TERLINDUNGI]" in line:
            fill_color = (78, 201, 176)  # Green / Cyan
        elif "[PERINGATAN]" in line:
            fill_color = (220, 160, 50)  # Orange / Yellow
        elif "[ERROR]" in line:
            fill_color = (244, 71, 71)  # Red
        elif line.strip().startswith("[BUKU]") or line.strip().startswith("[MAJALAH]"):
            fill_color = (206, 145, 120)  # Soft coral / peach
        elif line.strip().startswith("->"):
            fill_color = (156, 220, 254)  # Light cyan

        draw.text((padding_x, y), line, fill=fill_color, font=font)
        y += line_height

    img.save(output_path, "PNG")
    print(f"Saved: {output_path} ({img_width}x{img_height})")


def main():
    res = subprocess.run(["python", "main.py"], capture_output=True, text=True, encoding="utf-8")
    lines = res.stdout.splitlines()

    # Split into logical sections for screenshots
    # Section 1: Intro + Tambah Item + Seluruh Katalog
    # find lines for Section 1 to Section 4
    idx_sec4 = next(i for i, line in enumerate(lines) if "4. FITUR PENCARIAN ITEM" in line)
    idx_sec7 = next(i for i, line in enumerate(lines) if "7. PENERAPAN POLYMORPHISM" in line)

    sec1_lines = ["$ python main.py"] + lines[:idx_sec4]
    sec2_lines = lines[idx_sec4:idx_sec7]
    sec3_lines = lines[idx_sec7:]

    render_terminal_image(
        sec1_lines,
        "screenshots/01_penambahan_dan_katalog.png",
        title="Terminal - Fitur Penambahan Item & Tampilan Katalog Perpustakaan",
    )

    render_terminal_image(
        sec2_lines,
        "screenshots/02_pencarian_dan_peminjaman.png",
        title="Terminal - Fitur Pencarian Item & Status Ketersediaan",
    )

    render_terminal_image(
        sec3_lines,
        "screenshots/03_polymorphism_denda_enkapsulasi.png",
        title="Terminal - Polymorphism Hitung Denda & Pengujian Enkapsulasi",
    )


if __name__ == "__main__":
    main()
