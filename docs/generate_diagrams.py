"""
Generate UML/System diagrams for Capstone Report
Output: docs/images/*.png
"""
from PIL import Image, ImageDraw, ImageFont
import os

OUT_DIR = r"C:\Users\user\OneDrive\Documents\DOKUMEN-CODING\sistem-peminjaman-kunci-lab\docs\images"
os.makedirs(OUT_DIR, exist_ok=True)

# ── helpers ────────────────────────────────────────────────
def load_font(size):
    for path in [r"C:\Windows\Fonts\segoeui.ttf", r"C:\Windows\Fonts\arial.ttf"]:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                pass
    return ImageFont.load_default()

def draw_rounded_rect(draw, xy, radius, fill, outline=None, width=2):
    x0, y0, x1, y1 = xy
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)

def draw_oval(draw, xy, fill, outline=None, width=2):
    draw.ellipse(xy, fill=fill, outline=outline, width=max(1, int(width)))

def draw_line(draw, start, end, color="#333333", width=2):
    draw.line([start, end], fill=color, width=max(1, int(width)))

def draw_dashed_line(draw, start, end, color="#666666", width=1):
    x0, y0 = start
    x1, y1 = end
    dx, dy = x1-x0, y1-y0
    length = (dx**2 + dy**2) ** 0.5
    if length == 0:
        return
    segments = int(length / 8)
    seg_len = length / segments
    for i in range(segments):
        if i % 2 == 0:
            sx = x0 + (i/segments) * dx
            sy = y0 + (i/segments) * dy
            ex = x0 + ((i+1)/segments) * dx
            ey = y0 + ((i+1)/segments) * dy
            draw.line([(sx, sy), (ex, ey)], fill=color, width=width)

def draw_arrow_line(draw, start, end, color="#333333", width=2):
    """Draw line with arrowhead at end."""
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    length = (dx**2 + dy**2) ** 0.5
    if length == 0:
        draw_line(draw, start, end, color, width)
        return
    ux, uy = dx/length, dy/length
    # Arrow tip
    tip = end
    p1 = (end[0] - 12*ux + 5*uy, end[1] - 12*uy - 5*ux)
    p2 = (end[0] - 12*ux - 5*uy, end[1] - 12*uy + 5*ux)
    draw_line(draw, start, end, color, width)
    draw.polygon([(int(tip[0]), int(tip[1])), (int(p1[0]), int(p1[1])), (int(p2[0]), int(p2[1]))], fill=color)

def center_text(draw, text, x, y, font, fill="#000000", align="center"):
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2]-bbox[0], bbox[3]-bbox[1]
    if align == "center":
        draw.text((x - tw//2, y - th//2), text, font=font, fill=fill)
    else:
        draw.text((x, y), text, font=font, fill=fill)

# ── Palette ────────────────────────────────────────────────
C_BG = "#FFFFFF"
C_BOX = "#E8F0FE"
C_BOX_BORDER = "#1A73E8"
C_ACTOR = "#FFF3E0"
C_ACTOR_BORDER = "#E65100"
C_DARK_TEXT = "#212121"
C_GREY_TEXT = "#616161"
C_LINE = "#424242"
C_RELATION = "#FF6F00"


# ============================================================
# 1. USE CASE DIAGRAM
# ============================================================
def make_use_case_diagram():
    W, H = 800, 550
    img = Image.new("RGB", (W, H), C_BG)
    d = ImageDraw.Draw(img)
    f_title = load_font(16)
    f_box = load_font(13)
    f_small = load_font(11)
    f_actor = load_font(12)

    # System boundary
    sx, sy, ex, ey = 150, 60, 650, 490
    draw_rounded_rect(d, (sx, sy, ex, ey), 8, "#FAFAFA", C_LINE, 2)
    center_text(d, "Sistem Peminjaman Kunci Laboratorium", sx + (ex-sx)//2, sy + 10, f_title, C_GREY_TEXT)

    # Actors
    actors = [
        ("Admin / Laboran", 70, 275),
        ("Penanggung Jawab (PJ)", 720, 275),
    ]
    for name, ax, ay in actors:
        # stick figure head
        draw_oval(d, (ax-18, ay-30, ax+18, ay+2), C_ACTOR, C_ACTOR_BORDER, 2)
        # body
        d.line([(ax, ay+2), (ax, ay+45)], fill=C_ACTOR_BORDER, width=2)
        # arms
        d.line([(ax-25, ay+15), (ax+25, ay+15)], fill=C_ACTOR_BORDER, width=2)
        # legs
        d.line([(ax, ay+45), (ax-20, ay+80)], fill=C_ACTOR_BORDER, width=2)
        d.line([(ax, ay+45), (ax+20, ay+80)], fill=C_ACTOR_BORDER, width=2)
        # label
        label_x = ax if ax < 200 else ax
        d.text((ax - 50 if ax < 200 else ax + 25, ay + 90), name, font=f_actor, fill=C_DARK_TEXT)

    # Use cases (ellipses inside system boundary)
    use_cases = [
        ("Login",                     400, 110),
        ("Dashboard",                 400, 180),
        ("Kelola Data Mahasiswa",     280, 260),
        ("Kelola Data Dosen",         520, 260),
        ("Kelola Data Lab & Kunci",   400, 330),
        ("Peminjaman Kunci",          400, 400),
        ("Pengembalian Kunci",        400, 460),
        ("Riwayat & Laporan",         200, 460),
        ("Notifikasi Telegram",       600, 460),
    ]
    for label, cx, cy in use_cases:
        w, h = len(label) * 8 + 30, 28
        draw_oval(d, (cx-w//2, cy-h//2, cx+w//2, cy+h//2), C_BOX, C_BOX_BORDER, int(1.5))
        bbox = d.textbbox((0,0), label, font=f_box)
        tw = bbox[2]-bbox[0]
        d.text((cx-tw//2, cy-8), label, font=f_box, fill=C_DARK_TEXT)

    # Associations: Admin -> use cases
    admin_x, admin_y = 70, 275
    targets_admin = [("Login", 400, 110), ("Dashboard", 400, 180),
                     ("Kelola Data Mahasiswa", 280, 260), ("Kelola Data Dosen", 520, 260),
                     ("Kelola Data Lab & Kunci", 400, 330),
                     ("Peminjaman Kunci", 400, 400), ("Pengembalian Kunci", 400, 460),
                     ("Riwayat & Laporan", 200, 460)]
    for _, tx, ty in targets_admin:
        draw_arrow_line(d, (admin_x+25, admin_y), (tx-80, ty), C_LINE, 1)

    # Penanggung Jawab -> Notifikasi
    pj_x, pj_y = 720, 275
    draw_arrow_line(d, (pj_x-25, pj_y), (600, 460), C_LINE, 1)

    # <<include>> relation: Peminjaman -> Validasi Kunci
    vx, vy = 400, 360
    draw_dashed_line(d, (vx, vy-14), (vx, vy-30), C_RELATION, 1)
    center_text(d, "<<include>>", vx, vy-34, f_small, C_RELATION)

    img.save(os.path.join(OUT_DIR, "usecase.png"), "PNG")
    print("  [1/4] usecase.png done")


# ============================================================
# 2. ERD DIAGRAM
# ============================================================
def make_erd_diagram():
    W, H = 800, 520
    img = Image.new("RGB", (W, H), C_BG)
    d = ImageDraw.Draw(img)
    f_title = load_font(16)
    f_entity = load_font(13)
    f_attr = load_font(11)
    f_small = load_font(10)

    # Entities positioned in a circle-like layout
    entities = {
        "Mahasiswa":  (130, 120),
        "Dosen":     (130, 400),
        "Laboratorium": (400, 80),
        "Kunci":     (400, 400),
        "Peminjaman": (650, 260),
    }
    attrs = {
        "Mahasiswa": ["nim (PK)", "nama", "program_studi"],
        "Dosen":     ["nidn (PK)", "nama"],
        "Laboratorium": ["kode_lab (PK)", "nama_lab", "gedung", "lantai"],
        "Kunci":     ["nomor_kunci (PK)", "status", "fk_lab"],
        "Peminjaman": ["id (PK)", "tanggal_pinjam", "jam_pinjam",
                       "tanggal_kembali", "jam_kembali", "keperluan",
                       "status", "fk_mhs", "fk_dosen", "fk_lab", "fk_kunci"],
    }

    def draw_entity(name, pos, attrs_list):
        ex, ey = pos
        # box
        w, h = 150, 20 + len(attrs_list) * 18 + 10
        draw_rounded_rect(d, (ex-w//2, ey-h//2, ex+w//2, ey+h//2), 6, "#E3F2FD", "#1565C0", 2)
        # title bar
        d.rectangle([ex-w//2, ey-h//2, ex+w//2, ey-h//2+20], fill="#1565C0")
        bbox = d.textbbox((0,0), name, font=f_entity)
        tw = bbox[2]-bbox[0]
        d.text((ex-tw//2, ey-h//2+3), name, font=f_entity, fill="white")
        # attributes
        for i, a in enumerate(attrs_list):
            bbox_a = d.textbbox((0,0), a, font=f_attr)
            aw = bbox_a[2]-bbox_a[0]
            d.text((ex-aw//2, ey-h//2+24+i*18), a, font=f_attr, fill=C_DARK_TEXT)

    for name, pos in entities.items():
        draw_entity(name, pos, attrs.get(name, []))

    # Relationships (lines between entities)
    rels = [
        (("Mahasiswa", 130, 120), ("Peminjaman", 650, 260), "1:N"),
        (("Dosen",     130, 400), ("Peminjaman", 650, 260), "1:N"),
        (("Laboratorium", 400, 80), ("Peminjaman", 650, 260), "1:N"),
        (("Laboratorium", 400, 80), ("Kunci",      400, 400), "1:N"),
        (("Kunci",     400, 400), ("Peminjaman", 650, 260), "1:N"),
    ]
    for (n1, x1, y1), (n2, x2, y2), card in rels:
        mx, my = (x1+x2)//2, (y1+y2)//2
        draw_arrow_line(d, (x1, y1), (x2, y2), C_LINE, int(1.5))
        bbox_c = d.textbbox((0,0), card, font=f_small)
        cw = bbox_c[2]-bbox_c[0]
        d.text((mx-cw//2, my-8), card, font=f_small, fill=C_RELATION)

    img.save(os.path.join(OUT_DIR, "erd.png"), "PNG")
    print("  [2/4] erd.png done")


# ============================================================
# 3. ACTIVITY DIAGRAM (Peminjaman flow)
# ============================================================
def make_activity_diagram():
    W, H = 700, 620
    img = Image.new("RGB", (W, H), C_BG)
    d = ImageDraw.Draw(img)
    f_title = load_font(16)
    f_node = load_font(12)
    f_small = load_font(10)

    node_font = f_node
    small_font = f_small

    def node(x, y, text, shape="rect", w=140, h=40):
        """Draw activity node."""
        if shape == "start":
            draw_oval(d, (x-w//2, y-h//2, x+w//2, y+h//2), "#C8E6C9", "#2E7D32", 2)
        elif shape == "end":
            draw_oval(d, (x-w//2, y-h//2, x+w//2, y+h//2), "#FFCDD2", "#C62828", 2)
        elif shape == "decision":
            draw_rounded_rect(d, (x-w//2, y-h//2, x+w//2, y+h//2), 4, "#FFF9C4", "#F57F17", 2)
        else:
            draw_rounded_rect(d, (x-w//2, y-h//2, x+w//2, y+h//2), 6, C_BOX, C_BOX_BORDER, int(1.5))
        bbox = d.textbbox((0,0), text, font=node_font)
        tw = bbox[2]-bbox[0]
        d.text((x-tw//2, y-8), text, font=node_font, fill=C_DARK_TEXT)

    def arrow(start, end, label=None, label_pos=None):
        draw_arrow_line(d, start, end, C_LINE, int(1.5))
        if label:
            lx, ly = label_pos or ((start[0]+end[0])//2, (start[1]+end[1])//2)
            bbox_l = d.textbbox((0,0), label, font=small_font)
            lw = bbox_l[2]-bbox_l[0]
            d.rectangle([lx-lw//2-2, ly-8, lx+lw//2+2, ly+8], fill=C_BG)
            d.text((lx-lw//2, ly-7), label, font=small_font, fill="#C62828")

    # Start
    node(350, 40, "Mulai", "start", 60, 30)
    arrow((350, 55), (350, 95))

    # Login
    node(350, 110, "Login", "rect", 120, 36)
    arrow((350, 128), (350, 168))

    # Dashboard
    node(350, 185, "Dashboard", "rect", 120, 36)
    arrow((350, 203), (350, 243))

    # Decision: pilih transaksi
    node(350, 260, "Pilih\nTransaksi", "decision", 120, 60)
    # Left -> Peminjaman
    arrow((290, 260), (180, 260), "Peminjaman", (230, 250))
    # Right -> Pengembalian
    arrow((410, 260), (520, 260), "Pengembalian", (460, 250))

    # Peminjaman branch
    px = 180
    node(px, 300, "Isi Form\nPeminjaman", "rect", 120, 50)
    arrow((px, 325), (px, 375))
    node(px, 395, "Validasi\nKetersediaan", "rect", 120, 50)
    # Decision: tersedia?
    node(px, 465, "Kunci\nTersedia?", "decision", 120, 50)
    # Yes -> Simpan
    arrow((px, 490), (px, 530))
    node(px, 550, "Simpan & Update\nStatus Kunci", "rect", 120, 50)
    arrow((px, 570), (px-90, 570), label_pos=(px-45, 565))
    node(px-110, 570, "Kirim Notifikasi\nTelegram", "rect", 120, 50)
    arrow((px-110, 555), (px-110, 600))
    node(px-110, 610, "Selesai", "end", 80, 30)

    # No -> Tampil error
    arrow((px-60, 465), (px-60, 510), "Tidak", (px-80, 485))
    node(px-60, 530, "Tampil Pesan\nError", "rect", 110, 50)
    arrow((px-60, 555), (px-60, 595))
    node(px-60, 610, "Selesai", "end", 80, 30)

    # Pengembalian branch
    rx = 520
    node(rx, 300, "Cari Peminjaman\nAktif", "rect", 120, 50)
    arrow((rx, 325), (rx, 375))
    node(rx, 395, "Konfirmasi\nPengembalian", "rect", 120, 50)
    arrow((rx, 420), (rx, 470))
    node(rx, 490, "Update Status\nKunci = Tersedia", "rect", 120, 50)
    arrow((rx, 515), (rx, 555))
    node(rx, 575, "Kirim Notifikasi\nTelegram", "rect", 120, 50)
    arrow((rx, 600), (rx, 640))
    node(rx, 660, "Selesai", "end", 80, 30)

    img.save(os.path.join(OUT_DIR, "activity.png"), "PNG")
    print("  [3/4] activity.png done")


# ============================================================
# 4. SEQUENCE DIAGRAM (Peminjaman flow)
# ============================================================
def make_sequence_diagram():
    W, H = 720, 480
    img = Image.new("RGB", (W, H), C_BG)
    d = ImageDraw.Draw(img)
    f_title = load_font(15)
    f_participant = load_font(11)
    f_msg = load_font(10)
    f_small = load_font(9)

    # Participants
    participants = [
        ("Admin",       80),
        ("Form",        220),
        ("System",      380),
        ("Database",    530),
        ("Telegram Bot",660),
    ]
    px_list = [p[1] for p in participants]
    top_y, bot_y = 50, 440

    # Draw participant boxes
    for name, px in participants:
        bbox = d.textbbox((0,0), name, font=f_participant)
        nw = bbox[2]-bbox[0]
        draw_rounded_rect(d, (px-nw//2-5, top_y-5, px+nw//2+5, top_y+22), 4, C_BOX, C_BOX_BORDER, int(1.5))
        d.text((px-nw//2, top_y), name, font=f_participant, fill=C_DARK_TEXT)
        # Lifeline
        d.line([(px, top_y+22), (px, bot_y)], fill=C_LINE, width=1)

    # Messages (vertical position and horizontal targets)
    messages = [
        (top_y+50,  80,  220, "1. Input Data Peminjaman"),
        (top_y+100, 220, 380, "2. Kirim Form → Validasi"),
        (top_y+160, 380, 530, "3. Query Cek Kunci"),
        (top_y+220, 530, 380, "4. Return: status kunci"),
        (top_y+280, 380, 220, "5. Kirim response"),
        (top_y+330, 220, 80,  "6. Tampilkan pesan"),
        (top_y+100, 380, 530, "7. Insert Peminjaman"),
        (top_y+160, 530, 380, "8. Return: berhasil"),
        (top_y+220, 380, 660, "9. Kirim Notifikasi"),
        (top_y+390, 660, 80,  "10. Selesai"),
    ]

    for y, src, dst, label in messages:
        # message line
        if y >= top_y + 50 and y <= top_y + 440:
            draw_arrow_line(d, (src, y), (dst, y), C_LINE, 1)
        # label
        mid_x = (src + dst) // 2
        bbox_l = d.textbbox((0,0), label, font=f_msg)
        lw = bbox_l[2]-bbox_l[0]
        d.rectangle([mid_x-lw//2-2, y-7, mid_x+lw//2+2, y+7], fill=C_BG)
        d.text((mid_x-lw//2, y-6), label, font=f_msg, fill=C_DARK_TEXT)

    # Title
    bbox_t = d.textbbox((0,0), "Sequence Diagram – Proses Peminjaman Kunci", font=f_title)
    tw = bbox_t[2]-bbox_t[0]
    d.text(((W-tw)//2, 2), "Sequence Diagram – Proses Peminjaman Kunci", font=f_title, fill=C_DARK_TEXT)

    img.save(os.path.join(OUT_DIR, "sequence.png"), "PNG")
    print("  [4/4] sequence.png done")


if __name__ == "__main__":
    print("Generating diagrams...")
    make_use_case_diagram()
    make_erd_diagram()
    make_activity_diagram()
    make_sequence_diagram()
    print("All done!")
