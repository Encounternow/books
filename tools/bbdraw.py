#!/usr/bin/env python3
"""
bbdraw.py — 從 JSON 規格畫出 Fritzing 風格的麵包板接線圖（SVG）。

用法：
  tools/bbdraw.py spec.json out.svg
  tools/bbdraw.py --all electric/diagrams electric/src/images   # 批次

規格格式（JSON）：
{
  "title": "實驗 1-2：點亮一顆 LED",
  "boards": ["uno"],                 # 可為 [] / ["uno"] / ["esp32"] / ["uno","esp32"]
  "parts": [
    {"type": "resistor", "value": "1kΩ", "pins": ["c5", "c8"]},
    {"type": "led", "color": "red", "pins": ["d8", "d9"]},          # [長腳(+), 短腳(−)]
    {"type": "capacitor", "value": "100µF", "polar": true, "pins": ["e12", "e14"]},  # [+, −]
    {"type": "ceramic", "value": "100nF", "pins": ["e12", "e14"]},
    {"type": "diode", "label": "1N4007", "pins": ["g5", "g9"]},     # [陽極, 陰極(色環)]
    {"type": "inductor", "value": "1mH", "pins": ["g5", "g9"]},
    {"type": "ldr", "pins": ["c3", "c6"]},
    {"type": "buzzer", "pins": ["h20", "h22"]},                      # [+, −]
    {"type": "button", "pins": ["e10", "f10"]},                      # 左上腳、左下腳（跨中央溝）
    {"type": "pot", "pins": ["f3", "f4", "f5"]},                     # 左、中(滑動端)、右
    {"type": "transistor", "label": "2N2222", "pins": ["f15","f16","f17"]},   # E, B, C
    {"type": "mosfet", "label": "IRLZ44N", "pins": ["f15","f16","f17"]},      # G, D, S
    {"type": "dht11", "pins": ["f24","f25","f26"]},                  # +, out, −
    {"type": "oled", "pins": ["f20","f21","f22","f23"]},              # GND, VCC, SCL, SDA
    {"type": "jumper", "pins": ["a5", "a9"], "color": "green"},      # 麵包板上的短跳線
    {"type": "motor", "id": "motor"},            # 板外零件：馬達、servo、battery9v、aa4、relay、coil、meter、scope、logic、usb
    {"type": "battery9v", "id": "bat"}
  ],
  "wires": [
    ["uno:D9", "a5", "orange"],                  # [起點, 終點, 顏色]
    ["bat:+", "a5", "red"], ["motor:1", "j20", "red"]
  ],
  "probes": [ {"ch": "CH1", "tip": "a5", "gnd": "a9"} ],   # 示波器探棒
  "breadboard": false,                         # 純板外零件的實驗可以不畫麵包板（預設 true）
  "notes": ["LED 長腳是正極"]
}
三用電表：放進 parts {"type":"meter","mode":"V","display":"3.28"}，再用 wires 接 "meter:red" / "meter:black"。
{
}

座標：麵包板孔 = 列字母 + 行號，例如 "c5"（a–e 在上半、f–j 在下半，行 1–30）。
電源軌：T+5 / T-5（上方 + / − 軌第 5 孔）、B+5 / B-5（下方）。
板子腳位：uno:D9、uno:5V、uno:GND、uno:A0；esp:18、esp:3V3、esp:GND、esp:VIN。
板外零件腳位：motor:1、motor:2、servo:sig/servo:vcc/servo:gnd、bat:+、bat:-、aa4:+、aa4:-、
relay:IN/VCC/GND/COM/NO/NC、coil:1/coil:2、logic:CH0..CH7/logic:GND。
"""
import json, math, sys
from pathlib import Path

P = 20  # 孔距（像素）
ROW_Y = {"T+": 0, "T-": 1, "a": 3, "b": 4, "c": 5, "d": 6, "e": 7,
         "f": 10, "g": 11, "h": 12, "i": 13, "j": 14, "B+": 16, "B-": 17}
NCOL = 30

WIRE_COLORS = {
    "red": "#d7261e", "black": "#222222", "orange": "#f08a1d", "yellow": "#e8c21a",
    "green": "#2e9e44", "blue": "#2b6fd6", "purple": "#8a4fc9", "white": "#eeeeee",
    "gray": "#888888", "brown": "#8b5a2b", "pink": "#e879b9", "cyan": "#2bb5c9",
}
LED_COLORS = {"red": "#ff3b30", "green": "#34c759", "blue": "#3b82f6", "yellow": "#f5d90a", "white": "#fffbe6"}
LED_ZH = {"red": "紅光", "green": "綠光", "blue": "藍光", "yellow": "黃光", "white": "白光"}
BAND = {0: "#000000", 1: "#8b4513", 2: "#e02020", 3: "#f08a1d", 4: "#f0d020",
        5: "#2e9e44", 6: "#2b6fd6", 7: "#8a4fc9", 8: "#888888", 9: "#ffffff"}

UNO_TOP = ["SCL", "SDA", "AREF", "GND", "D13", "D12", "D11", "D10", "D9", "D8", None,
           "D7", "D6", "D5", "D4", "D3", "D2", "D1", "D0"]
UNO_BOT = [None, "IOREF", "RESET", "3.3V", "5V", "GND", "GND2", "VIN", None, "A0", "A1", "A2", "A3", "A4", "A5"]
ESP_LEFT = ["EN", "36", "39", "34", "35", "32", "33", "25", "26", "27", "14", "12", "13", "GND", "VIN"]
ESP_RIGHT = ["23", "22", "TX0", "RX0", "21", "19", "18", "5", "17", "16", "4", "0", "2", "15", "3V3"]


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


class Drawing:
    def __init__(self, spec):
        self.spec = spec
        self.boards = spec.get("boards", [])
        self.layers = {"board": [], "wire": [], "part": [], "label": [], "top": []}
        self.points = {}        # 名稱 → (x, y)
        self.externals = []     # 板外零件
        self.layout()

    # ---------- 版面 ----------
    def layout(self):
        self.margin = 2 * P
        y = self.margin + 2.0 * P   # 標題空間
        self.uno = None
        self.esp = None
        self.bx = self.margin + 1.5 * P
        if "esp32" in self.boards:
            self.esp = (self.margin, y)
            self.bx = self.margin + 11 * P
        if "uno" in self.boards:
            self.uno = (self.bx + 3 * P, y)
            y += 12 * P + 3.2 * P
        self.by = y + 0.8 * P
        self.has_bb = self.spec.get("breadboard", True)
        ext_types = [p for p in self.spec.get("parts", []) if p["type"] in EXTERNAL]
        self.ext_y = self.by + 20 * P if self.has_bb else self.by + 1 * P
        self.ext_x0 = self.bx
        x = self.ext_x0
        for p in ext_types:
            w = EXTERNAL[p["type"]][0]
            self.externals.append((p, x))
            x += (w + 1.5) * P
        self.width = max(self.bx + (NCOL + 2) * P, x) + self.margin
        self.height = (self.ext_y + 7 * P if ext_types else (self.by + 19 * P if self.has_bb else self.by + 2 * P))
        if self.spec.get("notes"):
            self.height += (len(self.spec["notes"]) + 0.5) * 1.1 * P
        self.height += self.margin
        if self.esp and self.height < self.esp[1] + 18 * P + self.margin:
            self.height = self.esp[1] + 18 * P + self.margin

    # ---------- 座標 ----------
    def hole(self, ref):
        """麵包板孔或電源軌 → (x, y)"""
        if ref[:2] in ("T+", "T-", "B+", "B-"):
            row, col = ref[:2], int(ref[2:])
        else:
            row, col = ref[0], int(ref[1:])
        return (self.bx + col * P, self.by + ROW_Y[row] * P)

    def pos(self, ref):
        if ref in self.points:
            return self.points[ref]
        if ":" not in ref:
            return self.hole(ref)
        raise KeyError(f"未知的接點：{ref}")

    # ---------- 基本繪圖 ----------
    def add(self, layer, s):
        self.layers[layer].append(s)

    def text(self, layer, x, y, s, size=11, anchor="middle", color="#222", weight="normal", rotate=None):
        tr = f' transform="rotate({rotate} {x} {y})"' if rotate else ""
        self.add(layer, f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" text-anchor="{anchor}" '
                        f'fill="{color}" font-weight="{weight}"{tr}>{esc(s)}</text>')

    def circle(self, layer, x, y, r, fill, stroke="none", sw=1):
        self.add(layer, f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')

    def rect(self, layer, x, y, w, h, fill, stroke="none", sw=1, rx=0, extra=""):
        self.add(layer, f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" '
                        f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>')

    def line(self, layer, x1, y1, x2, y2, stroke, sw=2, cap="round"):
        self.add(layer, f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                        f'stroke="{stroke}" stroke-width="{sw}" stroke-linecap="{cap}"/>')

    # ---------- 麵包板 ----------
    def draw_breadboard(self):
        x0, y0 = self.bx + 0.3 * P, self.by - 0.7 * P
        w, h = (NCOL + 0.4) * P, 18.4 * P
        self.rect("board", x0, y0, w, h, "#f3f1e6", "#c9c5b4", 1.5, rx=6)
        # 中央溝
        self.rect("board", x0, self.by + 8.2 * P, w, 1.6 * P, "#e2dfd0")
        # 電源軌線
        for row, col, col_label in (("T+", "#d7261e", "+"), ("T-", "#2b6fd6", "−"), ("B+", "#d7261e", "+"), ("B-", "#2b6fd6", "−")):
            y = self.by + ROW_Y[row] * P
            off = -0.55 * P if row.endswith("+") else 0.55 * P
            self.line("board", self.bx + 0.6 * P, y + off, self.bx + (NCOL + 0.4) * P, y + off, col, 1.5)
            self.text("board", self.bx + 0.1 * P, y + 4, col_label, 12, color=col, weight="bold")
            self.text("board", self.bx + (NCOL + 0.9) * P, y + 4, col_label, 12, color=col, weight="bold")
        # 孔
        for row, ry in ROW_Y.items():
            for c in range(1, NCOL + 1):
                x, y = self.bx + c * P, self.by + ry * P
                self.rect("board", x - 3.5, y - 3.5, 7, 7, "#3a3a3a", rx=1.5)
        # 列字母與行號
        for row in "abcdefghij":
            y = self.by + ROW_Y[row] * P + 4
            self.text("board", self.bx + 0.1 * P, y, row, 10, color="#777")
            self.text("board", self.bx + (NCOL + 0.9) * P, y, row, 10, color="#777")
        for c in range(1, NCOL + 1):
            if c == 1 or c % 5 == 0:
                self.text("board", self.bx + c * P, self.by + 2.45 * P, str(c), 9, color="#777")
                self.text("board", self.bx + c * P, self.by + 15.3 * P, str(c), 9, color="#777")
        # 連通示意（淡線）
        for c in range(1, NCOL + 1):
            x = self.bx + c * P
            self.line("board", x, self.by + 3 * P, x, self.by + 7 * P, "#dedbcc", 5)
            self.line("board", x, self.by + 10 * P, x, self.by + 14 * P, "#dedbcc", 5)
        # 把連通線放到孔後面：重新排序（線先畫）
        holes = [s for s in self.layers["board"] if s.startswith("<rect") and 'fill="#3a3a3a"' in s]
        others = [s for s in self.layers["board"] if s not in holes]
        self.layers["board"] = others + holes

    # ---------- Arduino UNO ----------
    def draw_uno(self):
        x0, y0 = self.uno
        W, H = 21 * P, 12 * P
        self.rect("board", x0, y0, W, H, "#1f6fb2", "#15507f", 2, rx=10)
        # USB 與電源插座
        self.rect("board", x0 - 0.6 * P, y0 + 1.2 * P, 2.2 * P, 2.4 * P, "#c8c8c8", "#888", 1, rx=2)
        self.rect("board", x0 - 0.6 * P, y0 + 8.4 * P, 2.2 * P, 2.2 * P, "#222", "#000", 1, rx=2)
        # 晶片
        self.rect("board", x0 + 11 * P, y0 + 5 * P, 7 * P, 2 * P, "#222", "#000", 1, rx=2)
        self.text("board", x0 + 14.5 * P, y0 + 6.2 * P, "ATmega328P", 9, color="#ccc")
        self.text("board", x0 + 6 * P, y0 + 6.6 * P, "Arduino UNO", 16, color="#fff", weight="bold")
        # 板上 LED L、ON
        self.rect("board", x0 + 8.5 * P, y0 + 1.6 * P, 0.6 * P, 0.4 * P, "#f5d90a")
        self.text("board", x0 + 8.8 * P, y0 + 1.3 * P, "L", 8, color="#fff")
        # 上排腳位（數位）
        xs = x0 + 1.4 * P
        for i, name in enumerate(UNO_TOP):
            x = xs + i * P
            if name is None:
                continue
            self.rect("board", x - 4, y0 - 2, 8, 14, "#111", rx=1)
            self.points[f"uno:{name}"] = (x, y0 + 2)
            lab = name[1:] if name.startswith("D") else name
            self.text("board", x, y0 + 2.6 * P, lab, 8, color="#fff", rotate=-90)
            if name == "GND":
                self.points["uno:GND0"] = (x, y0 + 2)
        self.text("board", xs + 4 * P, y0 + 3.6 * P, "DIGITAL (PWM ~)", 8, color="#cfe3f5")
        # 下排腳位（電源、類比）
        for i, name in enumerate(UNO_BOT):
            x = xs + i * P
            if name is None:
                continue
            self.rect("board", x - 4, y0 + H - 12, 8, 14, "#111", rx=1)
            self.points[f"uno:{name}"] = (x, y0 + H - 2)
            lab = "GND" if name == "GND2" else name
            self.text("board", x, y0 + H - 1.6 * P, lab, 8, color="#fff", rotate=-90)
        self.text("board", xs + 4 * P, y0 + H - 3.4 * P, "POWER", 8, color="#cfe3f5")
        self.text("board", xs + 11.5 * P, y0 + H - 3.4 * P, "ANALOG IN", 8, color="#cfe3f5")

    # ---------- ESP32 ----------
    def draw_esp(self):
        x0, y0 = self.esp
        W, H = 8 * P, 17 * P
        self.rect("board", x0, y0, W, H, "#1a1a1a", "#000", 2, rx=6)
        self.rect("board", x0 + 2.2 * P, y0 - 0.4 * P, 3.6 * P, 1.6 * P, "#bbb", "#888", 1, rx=2)   # USB
        self.rect("board", x0 + 1.2 * P, y0 + 4 * P, 5.6 * P, 5 * P, "#c8c8c8", "#999", 1, rx=2)   # 金屬殼
        self.text("board", x0 + 4 * P, y0 + 6.8 * P, "ESP32", 13, color="#333", weight="bold")
        self.text("board", x0 + 4 * P, y0 + 10.8 * P, "DevKit V1", 9, color="#ddd")
        self.rect("board", x0 + 1 * P, y0 + 13.5 * P, 1.2 * P, 1.2 * P, "#555", "#333", 1, rx=2)
        self.text("board", x0 + 1.6 * P, y0 + 15.5 * P, "EN", 7, color="#ddd")
        self.rect("board", x0 + 5.8 * P, y0 + 13.5 * P, 1.2 * P, 1.2 * P, "#555", "#333", 1, rx=2)
        self.text("board", x0 + 6.4 * P, y0 + 15.5 * P, "BOOT", 7, color="#ddd")
        self.rect("board", x0 + 3.2 * P, y0 + 2.2 * P, 0.5 * P, 0.4 * P, "#3b82f6")               # 板上 LED
        self.text("board", x0 + 3.45 * P, y0 + 3.3 * P, "LED(2)", 6, color="#ddd")
        for i, name in enumerate(ESP_LEFT):
            y = y0 + 1.6 * P + i * P
            self.rect("board", x0 - 6, y - 4, 10, 8, "#d4af37", rx=1)
            self.points[f"esp:{name}"] = (x0 - 4, y)
            self.text("board", x0 + 0.9 * P, y + 3, name, 7, anchor="start", color="#fff")
        for i, name in enumerate(ESP_RIGHT):
            y = y0 + 1.6 * P + i * P
            self.rect("board", x0 + W - 4, y - 4, 10, 8, "#d4af37", rx=1)
            self.points[f"esp:{name}"] = (x0 + W + 4, y)
            self.text("board", x0 + W - 0.9 * P, y + 3, name, 7, anchor="end", color="#fff")
        self.points["esp:1"] = self.points["esp:TX0"]
        self.points["esp:3"] = self.points["esp:RX0"]
        self.points["esp:VP"] = self.points["esp:36"]
        self.points["esp:VN"] = self.points["esp:39"]
        self.points["esp:3.3V"] = self.points["esp:3V3"]

    # ---------- 板上零件 ----------
    def legs(self, p1, p2, body_len):
        """回傳 (中心, 角度, 單位向量)，並畫出兩隻腳"""
        (x1, y1), (x2, y2) = p1, p2
        dx, dy = x2 - x1, y2 - y1
        L = math.hypot(dx, dy) or 1
        ux, uy = dx / L, dy / L
        cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
        half = body_len / 2
        self.line("part", x1, y1, cx - ux * half, cy - uy * half, "#9a9a9a", 2.5)
        self.line("part", x2, y2, cx + ux * half, cy + uy * half, "#9a9a9a", 2.5)
        ang = math.degrees(math.atan2(dy, dx))
        return (cx, cy), ang, (ux, uy), L

    def group(self, cx, cy, ang, inner):
        self.add("part", f'<g transform="translate({cx:.1f} {cy:.1f}) rotate({ang:.1f})">{inner}</g>')

    def label_near(self, cx, cy, ang, s, size=10, off=14):
        # 標籤放在零件旁邊（垂直於零件方向）
        rad = math.radians(ang)
        nx, ny = -math.sin(rad), math.cos(rad)
        self.text("label", cx + nx * off, cy + ny * off + 4, s, size, weight="bold", color="#333")

    def resistor_bands(self, value):
        v = value.replace("Ω", "").replace("ohm", "").strip()
        mult = 1
        if v.lower().endswith("k"):
            mult, v = 1000, v[:-1]
        elif v.upper().endswith("M"):
            mult, v = 1_000_000, v[:-1]
        try:
            ohms = float(v) * mult
        except ValueError:
            return ["#8b4513", "#000", "#e02020"]
        if ohms <= 0:
            return ["#000", "#000", "#000"]
        e = int(math.floor(math.log10(ohms)))
        sig = int(round(ohms / 10 ** (e - 1)))
        if sig >= 100:
            sig, e = sig // 10, e + 1
        d1, d2 = sig // 10, sig % 10
        return [BAND[d1], BAND[d2], BAND[max(0, e - 1)]]

    def part_resistor(self, p):
        a, b = self.pos(p["pins"][0]), self.pos(p["pins"][1])
        (cx, cy), ang, _, _ = self.legs(a, b, 2.2 * P)
        bands = self.resistor_bands(p.get("value", "1kΩ"))
        inner = f'<rect x="{-1.1*P}" y="-7" width="{2.2*P}" height="14" rx="6" fill="#e9d8a6" stroke="#b89b5a"/>'
        for i, c in enumerate(bands + ["#d4af37"]):
            inner += f'<rect x="{-0.8*P + i*0.42*P}" y="-7" width="5" height="14" fill="{c}"/>'
        self.group(cx, cy, ang, inner)
        self.label_near(cx, cy, ang, p.get("value", ""))

    def part_led(self, p):
        a, b = self.pos(p["pins"][0]), self.pos(p["pins"][1])
        (cx, cy), ang, (ux, uy), _ = self.legs(a, b, 0.9 * P)
        col = LED_COLORS.get(p.get("color", "red"), "#ff3b30")
        inner = (f'<circle cx="0" cy="0" r="11" fill="{col}" stroke="#555" stroke-width="1.5" opacity="0.95"/>'
                 f'<circle cx="-3" cy="-3" r="3" fill="#fff" opacity="0.7"/>')
        self.group(cx, cy, ang, inner)
        # 長腳 + 記號
        self.text("label", a[0] - ux * 10 - uy * 10, a[1] - uy * 10 + ux * 10 + 4, "+", 11, weight="bold", color="#d7261e")
        self.label_near(cx, cy, ang, p.get("label", f"{LED_ZH.get(p.get('color','red'), '')} LED"), off=24)

    def part_capacitor(self, p):
        a, b = self.pos(p["pins"][0]), self.pos(p["pins"][1])
        (cx, cy), ang, (ux, uy), _ = self.legs(a, b, 1.2 * P)
        if p.get("polar", True):
            inner = (f'<rect x="{-0.6*P}" y="-9" width="{1.2*P}" height="18" rx="4" fill="#1d3b8f" stroke="#0f2458"/>'
                     f'<rect x="{0.25*P}" y="-9" width="6" height="18" fill="#dcdcdc"/>'
                     f'<text x="{0.4*P}" y="4" font-size="10" fill="#333" text-anchor="middle">−</text>')
        else:
            inner = f'<ellipse cx="0" cy="0" rx="9" ry="8" fill="#f0b23a" stroke="#b07d1a"/>'
        self.group(cx, cy, ang, inner)
        if p.get("polar", True):
            self.text("label", a[0] - ux * 10 - uy * 10, a[1] - uy * 10 + ux * 10 + 4, "+", 11, weight="bold", color="#d7261e")
        self.label_near(cx, cy, ang, p.get("value", ""), off=18)

    def part_ceramic(self, p):
        p = dict(p); p["polar"] = False
        self.part_capacitor(p)

    def part_diode(self, p):
        a, b = self.pos(p["pins"][0]), self.pos(p["pins"][1])
        (cx, cy), ang, _, _ = self.legs(a, b, 1.6 * P)
        inner = (f'<rect x="{-0.8*P}" y="-6" width="{1.6*P}" height="12" rx="3" fill="#2a2a2a" stroke="#000"/>'
                 f'<rect x="{0.45*P}" y="-6" width="5" height="12" fill="#ddd"/>')
        self.group(cx, cy, ang, inner)
        self.label_near(cx, cy, ang, p.get("label", "1N4007"))

    def part_inductor(self, p):
        a, b = self.pos(p["pins"][0]), self.pos(p["pins"][1])
        (cx, cy), ang, _, _ = self.legs(a, b, 1.6 * P)
        inner = f'<rect x="{-0.8*P}" y="-8" width="{1.6*P}" height="16" rx="6" fill="#4b8f6a" stroke="#2d5c43"/>'
        for i in range(4):
            inner += f'<rect x="{-0.6*P + i*0.35*P}" y="-8" width="3" height="16" fill="#2d5c43" opacity="0.6"/>'
        self.group(cx, cy, ang, inner)
        self.label_near(cx, cy, ang, p.get("value", "1mH"))

    def part_ldr(self, p):
        a, b = self.pos(p["pins"][0]), self.pos(p["pins"][1])
        (cx, cy), ang, _, _ = self.legs(a, b, 1.0 * P)
        inner = ('<circle cx="0" cy="0" r="10" fill="#e0734a" stroke="#8a3f22"/>'
                 '<path d="M-6,-5 L6,-5 M-6,-2 L6,-2 M-6,1 L6,1 M-6,4 L6,4" stroke="#5a2410" stroke-width="1.5"/>')
        self.group(cx, cy, ang, inner)
        self.label_near(cx, cy, ang, "光敏電阻", off=18)

    def part_buzzer(self, p):
        a, b = self.pos(p["pins"][0]), self.pos(p["pins"][1])
        (cx, cy), ang, (ux, uy), _ = self.legs(a, b, 0.6 * P)
        inner = '<circle cx="0" cy="0" r="14" fill="#222" stroke="#000"/><circle cx="0" cy="0" r="3" fill="#777"/>'
        self.group(cx, cy, ang, inner)
        self.text("label", a[0] - ux * 10 - uy * 10, a[1] - uy * 10 + ux * 10 + 4, "+", 11, weight="bold", color="#d7261e")
        self.label_near(cx, cy, ang, "蜂鳴器", off=22)

    def part_button(self, p):
        a, b = self.pos(p["pins"][0]), self.pos(p["pins"][1])   # e10, f10
        x, y1, y2 = a[0], a[1], b[1]
        cx, cy = x + P, (y1 + y2) / 2
        for px, py in ((x, y1), (x + 2 * P, y1), (x, y2), (x + 2 * P, y2)):
            self.line("part", px, py, px + (cx - px) * 0.35, py + (cy - py) * 0.35, "#9a9a9a", 2.5)
        self.rect("part", cx - 0.9 * P, cy - 0.9 * P, 1.8 * P, 1.8 * P, "#333", "#000", 1, rx=3)
        self.circle("part", cx, cy, 0.5 * P, "#8b5a2b", "#5a3a1a")
        self.text("label", cx + 1.5 * P, cy + 4, p.get("label", "按鈕"), 10, anchor="start", weight="bold", color="#333")

    def part_pot(self, p):
        a, b, c = [self.pos(q) for q in p["pins"]]
        top = b[1] < self.by + 8 * P
        cx, cy = b[0], (b[1] + 1.4 * P if top else b[1] - 1.4 * P)
        for q in (a, b, c):
            self.line("part", q[0], q[1], q[0], cy, "#9a9a9a", 2.5)
        self.rect("part", cx - 1.6 * P, cy - 0.9 * P, 3.2 * P, 1.8 * P, "#2b6fd6", "#1b4a90", 1, rx=4)
        self.circle("part", cx, cy, 0.55 * P, "#ddd", "#888")
        self.line("part", cx - 6, cy, cx + 6, cy, "#555", 2)
        self.text("label", cx + 1.8 * P, cy + 4, p.get("value", "10kΩ 可變電阻"), 10, anchor="start", weight="bold", color="#333")
        self.text("label", b[0], b[1] + (-8 if top else 14), "中", 8, color="#555")

    def part_three(self, p, names, body, label):
        pins = [self.pos(q) for q in p["pins"]]
        top = pins[1][1] < self.by + 8 * P          # 在上半部 → 本體往下（朝中央溝）
        cy = pins[1][1] + (1.5 * P if top else -1.5 * P)
        cx = pins[1][0]
        for q in pins:
            self.line("part", q[0], q[1], q[0], cy, "#9a9a9a", 2.5)
        if not top:
            body = f'<g transform="scale(1 -1)">{body}</g>'.replace('<text', '<text transform="scale(1 -1)"') if False else body
        self.add("part", f'<g transform="translate({cx:.1f} {cy:.1f})">{body}</g>')
        for q, n in zip(pins, names):
            self.text("label", q[0], q[1] + (-7 if top else 14), n, 8, weight="bold", color="#333")
        if label:
            self.text("label", cx + 1.15 * P, cy + 4, label, 10, anchor="start", weight="bold", color="#333")

    def part_transistor(self, p):
        body = ('<path d="M-16,8 L16,8 L16,-2 A16,16 0 0 0 -16,-2 Z" fill="#2a2a2a" stroke="#000"/>'
                f'<text x="0" y="4" font-size="7" fill="#ddd" text-anchor="middle">{esc(p.get("label","2N2222"))}</text>')
        self.part_three(p, ["E", "B", "C"], body, p.get("label", "2N2222"))

    def part_mosfet(self, p):
        body = ('<rect x="-18" y="-16" width="36" height="12" fill="#999" stroke="#666"/>'
                '<circle cx="0" cy="-10" r="3" fill="#eee"/>'
                '<rect x="-18" y="-4" width="36" height="14" fill="#2a2a2a" stroke="#000"/>'
                f'<text x="0" y="6" font-size="7" fill="#ddd" text-anchor="middle">{esc(p.get("label","IRLZ44N"))}</text>')
        self.part_three(p, ["G", "D", "S"], body, p.get("label", "IRLZ44N"))

    def part_dht11(self, p):
        body = ('<rect x="-20" y="-28" width="40" height="34" rx="3" fill="#1f6fb2" stroke="#15507f"/>'
                '<rect x="-14" y="-24" width="28" height="22" fill="#3b82f6" stroke="#1b4a90"/>'
                '<text x="0" y="-9" font-size="8" fill="#fff" text-anchor="middle">DHT11</text>')
        pins = [self.pos(q) for q in p["pins"]]
        top = pins[1][1] < self.by + 8 * P
        if top:
            body = body.replace('y="-28"', 'y="-6"').replace('y="-24"', 'y="-2"').replace('y="-9"', 'y="12"')
        self.part_three(p, ["+", "out", "−"], body, "")

    def part_oled(self, p):
        pins = [self.pos(q) for q in p["pins"]]
        up = pins[0][1] >= self.by + 8 * P           # 下半部 → 本體往上
        cx = (pins[0][0] + pins[3][0]) / 2
        cy = pins[0][1] + (-2.4 * P if up else 2.4 * P)
        for q in pins:
            self.line("part", q[0], q[1], q[0], cy + (1.4 * P if up else -1.4 * P), "#9a9a9a", 2.5)
        self.rect("part", cx - 2.6 * P, cy - 1.5 * P, 5.2 * P, 3 * P, "#1d3b8f", "#0f2458", 1, rx=3)
        self.rect("part", cx - 2.2 * P, cy - 1.1 * P, 4.4 * P, 2 * P, "#111", "#000")
        self.text("part", cx, cy + 0.1 * P, "OLED 0.96\"", 8, color="#9ad8ff")
        for q, n in zip(pins, ["GND", "VCC", "SCL", "SDA"]):
            self.text("label", q[0], q[1] + (14 if up else -7), n, 7, weight="bold", color="#333")

    def part_jumper(self, p):
        self.wire(p["pins"][0], p["pins"][1], p.get("color", "green"), bend=0.35)

    # ---------- 板外零件 ----------
    def draw_externals(self):
        for p, x in self.externals:
            w, fn = EXTERNAL[p["type"]]
            fn(self, p, x, self.ext_y, w * P)

    def ext_motor(self, p, x, y, w):
        pid = p.get("id", "motor")
        cx, cy = x + w / 2, y + 2 * P
        self.rect("part", cx - 1.6 * P, cy - 1.1 * P, 3.2 * P, 2.2 * P, "#9a9a9a", "#666", 1, rx=6)
        self.circle("part", cx + 1.6 * P, cy, 0.5 * P, "#ccc", "#666")
        self.rect("part", cx + 1.9 * P, cy - 3, 0.9 * P, 6, "#777")
        self.text("part", cx - 0.2 * P, cy + 4, "馬達", 11, color="#fff", weight="bold")
        self.points[f"{pid}:1"] = (cx - 1.1 * P, cy - 1.1 * P)
        self.points[f"{pid}:2"] = (cx - 0.3 * P, cy - 1.1 * P)
        self.text("label", cx - 0.7 * P, cy + 2.2 * P, p.get("label", "小直流馬達"), 10, weight="bold", color="#333")

    def ext_servo(self, p, x, y, w):
        pid = p.get("id", "servo")
        cx, cy = x + w / 2, y + 2 * P
        self.rect("part", cx - 1.5 * P, cy - 0.9 * P, 3 * P, 1.8 * P, "#2b6fd6", "#1b4a90", 1, rx=3)
        self.rect("part", cx - 2.1 * P, cy - 0.3 * P, 4.2 * P, 0.6 * P, "#2b6fd6", "#1b4a90", 1)
        self.circle("part", cx - 0.6 * P, cy - 1.2 * P, 0.5 * P, "#ddd", "#888")
        self.rect("part", cx - 0.7 * P, cy - 2.4 * P, 0.2 * P, 1.3 * P, "#eee", "#888")
        self.text("part", cx + 0.3 * P, cy + 4, "SG90", 9, color="#fff", weight="bold")
        for i, (n, col) in enumerate((("gnd", "#8b5a2b"), ("vcc", "#d7261e"), ("sig", "#f08a1d"))):
            px = cx - 0.6 * P + i * 0.6 * P
            self.points[f"{pid}:{n}"] = (px, cy - 0.9 * P)
        self.text("label", cx, cy + 2.2 * P, "伺服馬達（棕 GND・紅 5V・橘 訊號）", 9, weight="bold", color="#333")

    def ext_battery9v(self, p, x, y, w):
        pid = p.get("id", "bat")
        cx, cy = x + w / 2, y + 2.2 * P
        self.rect("part", cx - 1.1 * P, cy - 1.6 * P, 2.2 * P, 3.4 * P, "#333", "#000", 1, rx=4)
        self.text("part", cx, cy + 0.3 * P, "9V", 12, color="#fff", weight="bold")
        self.circle("part", cx - 0.45 * P, cy - 1.6 * P, 5, "#ccc", "#666")
        self.circle("part", cx + 0.45 * P, cy - 1.6 * P, 7, "#ccc", "#666")
        self.points[f"{pid}:+"] = (cx - 0.45 * P, cy - 1.9 * P)
        self.points[f"{pid}:-"] = (cx + 0.45 * P, cy - 1.9 * P)
        self.text("label", cx - 0.45 * P, cy - 2.2 * P, "+", 10, weight="bold", color="#d7261e")
        self.text("label", cx + 0.45 * P, cy - 2.2 * P, "−", 10, weight="bold", color="#222")
        self.text("label", cx, cy + 2.4 * P, "9V 電池 + 電池扣", 10, weight="bold", color="#333")

    def ext_aa4(self, p, x, y, w):
        pid = p.get("id", "aa4")
        cx, cy = x + w / 2, y + 2.2 * P
        n = int(p.get("cells", 4))
        self.rect("part", cx - 2 * P, cy - 1.2 * P, 4 * P, 2.6 * P, "#333", "#000", 1, rx=4)
        for i in range(n):
            self.rect("part", cx - 1.8 * P + i * (3.6 * P / n), cy - 1 * P, 3.6 * P / n - 4, 2.2 * P, "#5aa0e6", "#2b6fd6", 1, rx=3)
        self.text("part", cx, cy + 0.2 * P, f"{n}×AA  {1.5*n:.1f}V", 10, color="#fff", weight="bold")
        self.points[f"{pid}:+"] = (cx - 1.6 * P, cy - 1.2 * P)
        self.points[f"{pid}:-"] = (cx + 1.6 * P, cy - 1.2 * P)
        self.text("label", cx - 1.6 * P, cy - 1.5 * P, "+", 10, weight="bold", color="#d7261e")
        self.text("label", cx + 1.6 * P, cy - 1.5 * P, "−", 10, weight="bold", color="#222")
        self.text("label", cx, cy + 2.2 * P, p.get("label", f"3 號電池盒（{n} 顆）"), 10, weight="bold", color="#333")

    def ext_relay(self, p, x, y, w):
        pid = p.get("id", "relay")
        cx, cy = x + w / 2, y + 2.2 * P
        self.rect("part", cx - 2.4 * P, cy - 1.4 * P, 4.8 * P, 3 * P, "#1f6fb2", "#15507f", 1, rx=3)
        self.rect("part", cx - 1.4 * P, cy - 1 * P, 2.8 * P, 1.6 * P, "#2b6fd6", "#1b4a90", 1)
        self.text("part", cx, cy + 0.1 * P, "RELAY 5V", 8, color="#fff", weight="bold")
        for i, n in enumerate(("IN", "VCC", "GND")):
            px = cx - 1.6 * P + i * 0.8 * P
            self.points[f"{pid}:{n}"] = (px, cy - 1.4 * P)
            self.text("label", px, cy - 1.7 * P, n, 7, weight="bold", color="#333")
        for i, n in enumerate(("COM", "NO", "NC")):
            px = cx + 0.6 * P + i * 0.8 * P
            self.points[f"{pid}:{n}"] = (px, cy - 1.4 * P)
            self.text("label", px, cy - 1.7 * P, n, 7, weight="bold", color="#333")
        self.text("label", cx, cy + 2.4 * P, "繼電器模組", 10, weight="bold", color="#333")

    def ext_coil(self, p, x, y, w):
        pid = p.get("id", "coil")
        cx, cy = x + w / 2, y + 2.2 * P
        self.rect("part", cx - 2.2 * P, cy - 0.25 * P, 4.4 * P, 0.5 * P, "#888", "#555", 1, rx=2)
        self.add("part", f'<path d="M{cx+2.2*P:.1f},{cy:.1f} L{cx+2.8*P:.1f},{cy:.1f}" stroke="#666" stroke-width="3"/>')
        for i in range(12):
            px = cx - 1.8 * P + i * 0.3 * P
            self.add("part", f'<ellipse cx="{px:.1f}" cy="{cy:.1f}" rx="4" ry="9" fill="none" stroke="#b5651d" stroke-width="2"/>')
        self.points[f"{pid}:1"] = (cx - 1.9 * P, cy - 0.5 * P)
        self.points[f"{pid}:2"] = (cx + 1.6 * P, cy - 0.5 * P)
        self.text("label", cx, cy + 1.6 * P, p.get("label", "鐵釘 + 漆包線（自製線圈）"), 10, weight="bold", color="#333")

    def ext_meter(self, p, x, y, w):
        pid = p.get("id", "meter")
        cx, cy = x + w / 2, y + 2.2 * P
        self.rect("part", cx - 1.8 * P, cy - 1.6 * P, 3.6 * P, 3.4 * P, "#f5c518", "#b08900", 1, rx=5)
        self.rect("part", cx - 1.4 * P, cy - 1.3 * P, 2.8 * P, 1 * P, "#cfe3c9", "#777", 1)
        self.text("part", cx, cy - 0.55 * P, p.get("display", "0.00"), 10, color="#222", weight="bold")
        self.circle("part", cx, cy + 0.5 * P, 0.5 * P, "#ddd", "#777")
        self.text("part", cx, cy + 1.5 * P, p.get("mode", "V"), 9, color="#222", weight="bold")
        self.points[f"{pid}:red"] = (cx + 1.2 * P, cy - 1.6 * P)
        self.points[f"{pid}:black"] = (cx - 1.2 * P, cy - 1.6 * P)
        self.text("label", cx, cy + 2.5 * P, "三用電表", 10, weight="bold", color="#333")

    def ext_scope(self, p, x, y, w):
        pid = p.get("id", "scope")
        cx, cy = x + w / 2, y + 2.2 * P
        self.rect("part", cx - 2.4 * P, cy - 1.6 * P, 4.8 * P, 3.4 * P, "#555", "#222", 1, rx=5)
        self.rect("part", cx - 2.1 * P, cy - 1.3 * P, 3.2 * P, 2.6 * P, "#0b2a1f", "#000", 1)
        self.add("part", f'<path d="M{cx-2.0*P:.1f},{cy+0.6*P:.1f} h8 v-16 h12 v16 h12 v-16 h12 v16 h8" fill="none" stroke="#5cf28a" stroke-width="1.5"/>')
        self.text("part", cx + 1.65 * P, cy - 0.6 * P, "CH1", 6, color="#fe0")
        self.text("part", cx + 1.65 * P, cy + 0.2 * P, "CH2", 6, color="#6cf")
        self.points[f"{pid}:CH1"] = (cx - 1.0 * P, cy - 1.6 * P)
        self.points[f"{pid}:CH2"] = (cx + 0.2 * P, cy - 1.6 * P)
        self.points[f"{pid}:GND"] = (cx + 1.4 * P, cy - 1.6 * P)
        self.text("label", cx, cy + 2.5 * P, "示波器", 10, weight="bold", color="#333")

    def ext_logic(self, p, x, y, w):
        pid = p.get("id", "logic")
        cx, cy = x + w / 2, y + 2.2 * P
        self.rect("part", cx - 2.4 * P, cy - 1.2 * P, 4.8 * P, 2.4 * P, "#222", "#000", 1, rx=4)
        self.text("part", cx, cy + 0.2 * P, "邏輯分析儀", 9, color="#fff", weight="bold")
        names = ["CH0", "CH1", "CH2", "CH3", "CH4", "CH5", "CH6", "CH7", "GND"]
        for i, n in enumerate(names):
            px = cx - 2.0 * P + i * 0.5 * P
            self.points[f"{pid}:{n}"] = (px, cy - 1.2 * P)
            self.text("label", px, cy - 1.45 * P, n.replace("CH", ""), 6, color="#333")
        self.text("label", cx, cy + 2.0 * P, "USB 邏輯分析儀（接電腦）", 9, weight="bold", color="#333")

    def ext_usb(self, p, x, y, w):
        cx, cy = x + w / 2, y + 2.2 * P
        self.rect("part", cx - 1.2 * P, cy - 0.8 * P, 2.4 * P, 1.6 * P, "#444", "#222", 1, rx=3)
        self.text("part", cx, cy + 4, "USB 5V", 9, color="#fff", weight="bold")
        pid = p.get("id", "usb")
        self.points[f"{pid}:+"] = (cx - 0.5 * P, cy - 0.8 * P)
        self.points[f"{pid}:-"] = (cx + 0.5 * P, cy - 0.8 * P)
        self.text("label", cx, cy + 2.0 * P, "USB 電源", 10, weight="bold", color="#333")

    # ---------- 導線與探棒 ----------
    def wire(self, a, b, color="red", bend=0.25):
        (x1, y1), (x2, y2) = self.pos(a), self.pos(b)
        col = WIRE_COLORS.get(color, color)
        dx, dy = x2 - x1, y2 - y1
        L = math.hypot(dx, dy) or 1
        # 控制點：垂直方向外凸，讓線看起來像杜邦線
        nx, ny = -dy / L, dx / L
        k = min(60, L * bend)
        c1 = (x1 + dx * 0.25 + nx * k, y1 + dy * 0.25 + ny * k)
        c2 = (x1 + dx * 0.75 + nx * k, y1 + dy * 0.75 + ny * k)
        d = f"M{x1:.1f},{y1:.1f} C{c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {x2:.1f},{y2:.1f}"
        self.add("wire", f'<path d="{d}" fill="none" stroke="#00000055" stroke-width="6" stroke-linecap="round"/>')
        self.add("wire", f'<path d="{d}" fill="none" stroke="{col}" stroke-width="4" stroke-linecap="round"/>')
        for x, y in ((x1, y1), (x2, y2)):
            self.circle("top", x, y, 3.2, col, "#333", 0.8)

    def probe(self, pr):
        ch = pr.get("ch", "CH1")
        tip = self.pos(pr["tip"])
        col = "#e8c21a" if ch.endswith("1") else "#2bb5c9"
        # 探棒：從上方斜插下來的灰色尖頭
        x, y = tip
        self.add("top", f'<path d="M{x:.1f},{y:.1f} l12,-26 l6,3 l-10,24 z" fill="#777" stroke="#333" stroke-width="1"/>')
        self.add("top", f'<path d="M{x+12:.1f},{y-26:.1f} l6,3 l12,-26 l-6,-3 z" fill="{col}" stroke="#333" stroke-width="1"/>')
        self.text("top", x + 30, y - 50, f"示波器 {ch} 探棒", 10, anchor="start", weight="bold", color="#333")
        if pr.get("gnd"):
            gx, gy = self.pos(pr["gnd"])
            self.add("top", f'<path d="M{gx-5:.1f},{gy-2:.1f} l-3,-16 l16,0 l-3,16 z" fill="#333" stroke="#000"/>')
            self.add("top", f'<path d="M{gx-6:.1f},{gy-18:.1f} q-4,-22 -26,-30" fill="none" stroke="#222" stroke-width="4" stroke-linecap="round"/>')
            self.text("top", gx - 30, gy - 52, f"{ch} 接地夾", 9, anchor="end", weight="bold", color="#333")

    def meter(self, m):
        # 三用電表畫在板外區（若規格有 meter 但沒列在 parts，自動加）
        pass

    # ---------- 組裝 ----------
    def render(self):
        spec = self.spec
        if self.has_bb:
            self.draw_breadboard()
        if self.uno:
            self.draw_uno()
        if self.esp:
            self.draw_esp()
        self.draw_externals()
        for p in spec.get("parts", []):
            t = p["type"]
            if t in EXTERNAL:
                continue
            fn = getattr(self, f"part_{t}", None)
            if fn is None:
                raise ValueError(f"不支援的零件：{t}")
            fn(p)
        for w in spec.get("wires", []):
            a, b = w[0], w[1]
            color = w[2] if len(w) > 2 else "red"
            self.wire(a, b, color)
        for pr in spec.get("probes", []):
            self.probe(pr)
        # 標題與註記
        self.text("top", self.margin, self.margin + 0.4 * P, spec.get("title", ""), 15, anchor="start", weight="bold", color="#111")
        ny = self.height - self.margin - (len(spec.get("notes", [])) - 1) * 1.1 * P
        for i, n in enumerate(spec.get("notes", [])):
            self.text("top", self.margin, ny + i * 1.1 * P, "• " + n, 11, anchor="start", color="#333")
        body = "".join("".join(self.layers[k]) for k in ("board", "part", "wire", "label", "top"))
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.width:.0f} {self.height:.0f}" '
                f'width="{self.width:.0f}" height="{self.height:.0f}" font-family="-apple-system, PingFang TC, Noto Sans TC, Helvetica, Arial, sans-serif">'
                f'<rect width="100%" height="100%" fill="#ffffff"/>{body}</svg>')


EXTERNAL = {
    "motor": (4, Drawing.ext_motor),
    "servo": (5, Drawing.ext_servo),
    "battery9v": (3, Drawing.ext_battery9v),
    "aa4": (5, Drawing.ext_aa4),
    "relay": (5.5, Drawing.ext_relay),
    "coil": (6, Drawing.ext_coil),
    "meter": (4, Drawing.ext_meter),
    "scope": (5.5, Drawing.ext_scope),
    "logic": (5.5, Drawing.ext_logic),
    "usb": (3, Drawing.ext_usb),
}


def build(spec_path, out_path):
    spec = json.loads(Path(spec_path).read_text(encoding="utf-8"))
    svg = Drawing(spec).render()
    Path(out_path).write_text(svg, encoding="utf-8")


def main():
    args = sys.argv[1:]
    if args and args[0] == "--all":
        src, dst = Path(args[1]), Path(args[2])
        dst.mkdir(parents=True, exist_ok=True)
        n = 0
        for f in sorted(src.glob("*.json")):
            try:
                build(f, dst / (f.stem + ".svg"))
                n += 1
            except Exception as e:  # noqa
                print(f"✗ {f.name}: {e}")
        print(f"已產生 {n} 張圖 → {dst}")
    elif len(args) == 2:
        build(args[0], args[1])
        print("ok", args[1])
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
