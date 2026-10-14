#!/usr/bin/env python3
"""產生電路符號總表 electric/src/images/symbols.svg（每格：名稱、標準符號、本書 ASCII 寫法）。"""
from pathlib import Path

CW, CH = 230, 150          # 每格大小
COLS = 3
S = []                     # 符號繪圖函式清單


def card(name, ascii_, draw, hint=""):
    S.append((name, ascii_, draw, hint))


def wire(x1, y1, x2, y2, sw=2):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#222" stroke-width="{sw}" stroke-linecap="round"/>'


def txt(x, y, s, size=11, anchor="middle", color="#222", weight="normal"):
    return f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="{anchor}" fill="{color}" font-weight="{weight}">{s}</text>'


def dot(x, y):
    return f'<circle cx="{x}" cy="{y}" r="3.5" fill="#222"/>'


# ---- 各符號（以格子中心 (0,0) 為原點，寬約 160） ----
def sym_wire():
    return (wire(-70, -20, 70, -20) + txt(0, -30, "導線", 10) +
            wire(-70, 15, 70, 15) + wire(0, -5, 0, 40) + dot(0, 15) + txt(8, 32, "有點＝相接", 9, "start") +
            wire(-70, 35, -20, 35) + f'<path d="M-20,35 a8,8 0 0 1 16,0" fill="none" stroke="#222" stroke-width="2"/>' + wire(-4, 35, 30, 35) +
            wire(-12, 20, -12, 50) + txt(-72, 55, "跳過＝不相接", 9, "start"))


def sym_resistor():
    z = "M-60,0 L-40,0 L-35,-10 L-25,10 L-15,-10 L-5,10 L5,-10 L15,10 L25,-10 L35,10 L40,0 L60,0"
    return (f'<path d="{z}" fill="none" stroke="#222" stroke-width="2"/>' + txt(0, -22, "美式（鋸齒）", 9) +
            wire(-60, 35, -40, 35) + f'<rect x="-40" y="26" width="80" height="18" fill="none" stroke="#222" stroke-width="2"/>' +
            wire(40, 35, 60, 35) + txt(0, 60, "國際式（長方形）", 9))


def sym_pot():
    return (sym_resistor().split("<text")[0] +
            f'<path d="M0,-40 L0,-14" stroke="#222" stroke-width="2"/><path d="M-6,-14 L0,-4 L6,-14 z" fill="#222"/>' +
            txt(14, -30, "滑動端（中間腳）", 9, "start"))


def sym_ldr():
    z = "M-40,0 L-30,-10 L-20,10 L-10,-10 L0,10 L10,-10 L20,10 L30,-10 L40,0"
    return (wire(-60, 0, -40, 0) + f'<path d="{z}" fill="none" stroke="#222" stroke-width="2"/>' + wire(40, 0, 60, 0) +
            f'<circle cx="0" cy="0" r="38" fill="none" stroke="#222" stroke-width="1.5"/>' +
            f'<path d="M-50,-45 L-30,-28 M-40,-50 L-20,-33" stroke="#222" stroke-width="2"/>'
            f'<path d="M-30,-28 l-8,-1 l6,-6 z M-20,-33 l-8,-1 l6,-6 z" fill="#222"/>' + txt(0, 58, "箭頭＝光照進來", 9))


def sym_cap():
    return (wire(-60, 0, -6, 0) + wire(-6, -22, -6, 22, 3) + wire(6, -22, 6, 22, 3) + wire(6, 0, 60, 0) +
            txt(0, 42, "兩條直線，沒有極性", 9))


def sym_ecap():
    return (wire(-60, 0, -6, 0) + wire(-6, -22, -6, 22, 3) +
            f'<path d="M6,-22 A30,30 0 0 0 6,22" fill="none" stroke="#222" stroke-width="3"/>' + wire(6, 0, 60, 0) +
            txt(-22, -28, "+", 14, weight="bold", color="#d7261e") + txt(0, 42, "直線＝正極、弧線＝負極", 9))


def sym_inductor():
    p = "M-60,0 L-40,0 " + " ".join(f"a10,10 0 0 1 20,0" for _ in range(4)) + " L60,0"
    return f'<path d="{p}" fill="none" stroke="#222" stroke-width="2"/>' + txt(0, 36, "一串圈圈＝線圈", 9)


def sym_diode():
    return (wire(-60, 0, -18, 0) + f'<path d="M-18,-16 L18,0 L-18,16 z" fill="#222"/>' + wire(18, -16, 18, 16, 3) + wire(18, 0, 60, 0) +
            txt(-36, -24, "陽極 +", 9) + txt(36, -24, "陰極 −（色環端）", 9) + txt(0, 42, "電流只能順著三角形方向流", 9))


def sym_led():
    return (sym_diode().split("<text")[0] +
            f'<path d="M4,-22 L18,-38 M14,-20 L28,-36" stroke="#222" stroke-width="2"/>'
            f'<path d="M18,-38 l-8,1 l6,6 z M28,-36 l-8,1 l6,6 z" fill="#222"/>' +
            txt(-40, 42, "長腳 +", 9) + txt(40, 42, "短腳 −", 9))


def sym_npn():
    return (f'<circle cx="0" cy="0" r="34" fill="none" stroke="#222" stroke-width="1.5"/>' +
            wire(-60, 0, -14, 0) + wire(-14, -22, -14, 22, 4) +
            wire(-14, -8, 18, -30) + wire(18, -30, 18, -55) +
            wire(-14, 8, 18, 30) + wire(18, 30, 18, 55) +
            f'<path d="M18,30 l-12,-4 l4,-9 z" fill="#222"/>' +
            txt(-50, -10, "B", 11, weight="bold") + txt(30, -45, "C", 11, weight="bold") + txt(30, 50, "E（箭頭朝外）", 10, "start", weight="bold"))


def sym_mosfet():
    return (f'<circle cx="0" cy="0" r="34" fill="none" stroke="#222" stroke-width="1.5"/>' +
            wire(-60, 0, -20, 0) + wire(-20, -22, -20, 22, 3) +
            wire(-8, -24, -8, -12, 4) + wire(-8, -6, -8, 6, 4) + wire(-8, 12, -8, 24, 4) +
            wire(-8, -18, 18, -18) + wire(18, -18, 18, -55) +
            wire(-8, 18, 18, 18) + wire(18, 18, 18, 55) + wire(-8, 0, 18, 0) + wire(18, 0, 18, 18) +
            f'<path d="M-8,0 l10,-5 l0,10 z" fill="#222"/>' +
            txt(-50, -10, "G", 11, weight="bold") + txt(30, -45, "D", 11, weight="bold") + txt(30, 52, "S", 11, weight="bold"))


def sym_battery():
    return (wire(-60, 0, -22, 0) + wire(-22, -20, -22, 20, 3) + wire(-10, -10, -10, 10, 3) +
            wire(2, -20, 2, 20, 3) + wire(14, -10, 14, 10, 3) + wire(14, 0, 60, 0) +
            txt(-30, -30, "+（長線）", 9) + txt(22, -30, "−（短線）", 9) + txt(0, 42, "電池／直流電源", 9))


def sym_gnd():
    return (wire(0, -40, 0, 0) + wire(-24, 0, 24, 0, 3) + wire(-15, 10, 15, 10, 3) + wire(-6, 20, 6, 20, 3) +
            txt(0, 45, "GND 接地：電路的 0V", 9) + txt(0, 60, "所有 GND 都接在一起", 9))


def sym_switch():
    return (wire(-60, -22, -20, -22) + dot(-20, -22) + wire(-20, -22, 20, -42) + dot(20, -22) + wire(20, -22, 60, -22) +
            txt(0, -4, "開關（畫的是斷開狀態）", 9) +
            wire(-60, 34, -20, 34) + dot(-20, 34) + dot(20, 34) + wire(-20, 20, 20, 20) + wire(0, 20, 0, 8) + wire(20, 34, 60, 34) +
            txt(0, 52, "按鈕（按下才接通）", 9))


def sym_motor():
    return (wire(-60, 0, -26, 0) + f'<circle cx="0" cy="0" r="26" fill="none" stroke="#222" stroke-width="2"/>' +
            txt(0, 7, "M", 20, weight="bold") + wire(26, 0, 60, 0) + txt(0, 44, "直流馬達", 9))


def sym_buzzer():
    return (wire(-60, 0, -26, 0) + f'<path d="M-26,-14 L-26,14 L10,14 A26,26 0 0 0 10,-14 z" fill="none" stroke="#222" stroke-width="2"/>' +
            wire(10, -14, 60, -14) + wire(10, 14, 60, 14) + txt(-20, -24, "+", 12, weight="bold", color="#d7261e") + txt(0, 44, "蜂鳴器", 9))


def sym_pin():
    return (f'<rect x="-60" y="-22" width="70" height="44" rx="4" fill="#1f6fb2"/>' + txt(-25, 4, "Arduino", 11, color="#fff", weight="bold") +
            wire(10, 0, 60, 0) + dot(10, 0) + txt(36, -8, "D9", 10, weight="bold") + txt(0, 44, "板子的某一隻腳位", 9))


def sym_probe():
    return (wire(-60, 0, 60, 0) + dot(0, 0) + f'<path d="M0,0 l14,-30 l8,4 l-12,28 z" fill="#777" stroke="#333"/>' +
            f'<path d="M14,-30 l8,4 l10,-22 l-8,-4 z" fill="#e8c21a" stroke="#333"/>' +
            txt(0, 44, "示波器／電表的量測點", 9))


card("導線、接點", "──┬──  ──┼──", sym_wire)
card("電阻", "[ 220Ω ]", sym_resistor)
card("可變電阻", "[ 可變電阻 ]", sym_pot)
card("光敏電阻 LDR", "[ LDR ]", sym_ldr)
card("電容（陶瓷）", "══╧══  100nF", sym_cap)
card("電解電容", "+ ══╧══ −", sym_ecap)
card("電感、線圈", "線圈 / [ 1mH ]", sym_inductor)
card("二極體", "──►|──  1N4007", sym_diode)
card("LED 發光二極體", "──►|──  LED", sym_led)
card("NPN 電晶體", "B ──┤  C / E", sym_npn)
card("N 通道 MOSFET", "G ──┤  D / S", sym_mosfet)
card("電池、直流電源", "9V + / 9V −", sym_battery)
card("GND 接地", "── GND", sym_gnd)
card("開關、按鈕", "[ 按鈕 ]", sym_switch)
card("直流馬達", "┌ 馬達 ┐", sym_motor)
card("蜂鳴器", "蜂鳴器 +/−", sym_buzzer)
card("板子腳位", "Arduino D9 ──", sym_pin)
card("量測點／探棒", "CH1 探棒接這裡 ──►", sym_probe)

rows = (len(S) + COLS - 1) // COLS
W, H = COLS * CW + 20, rows * CH + 20
out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
       f'font-family="-apple-system, PingFang TC, Noto Sans TC, Helvetica, Arial, sans-serif">',
       '<rect width="100%" height="100%" fill="#fff"/>']
for i, (name, ascii_, draw, hint) in enumerate(S):
    cx = 10 + (i % COLS) * CW
    cy = 10 + (i // COLS) * CH
    out.append(f'<rect x="{cx}" y="{cy}" width="{CW-6}" height="{CH-6}" rx="8" fill="#fafaf7" stroke="#ddd"/>')
    out.append(txt(cx + 10, cy + 20, name, 13, "start", weight="bold"))
    out.append(f'<text x="{cx + CW - 16}" y="{cy + 20}" font-size="10" text-anchor="end" fill="#666" font-family="Menlo, monospace">{ascii_}</text>')
    out.append(f'<g transform="translate({cx + (CW-6)/2} {cy + 82})">{draw()}</g>')
out.append("</svg>")
Path("electric/src/images/symbols.svg").write_text("\n".join(out), encoding="utf-8")
print("ok electric/src/images/symbols.svg")
