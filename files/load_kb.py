def dr_keys() -> None:
    vr("d").move(y=15)
    vr("d").nwrite("-" * 52)
    kseq = None
    if not vr("caps"):
        kseq = "|  esc  `  1  2  3  4  5  6  7  8  9  0  -  =  bck ||"
    elif vr("caps") == 2:
        kseq = "|  ESC  ~  1  2  3  4  5  6  7  8  9  0  _  +  BCK ||"
    else:
        kseq = "|  ESC  ~  !  @  #  $  %  ^  &  *  (  )  _  +  BCK ||"
    if not vr("caps"):
        kseq += str(
            " " * 2
            + "tab     q  w  e  r  t  y  u  i  o  p  [  ]   \\  ||"
            + " " * 2
            + "caps    a  s  d  f  g  h  j  k  l  ;   '  enter ||"
            + " " * 2
            + "shift   z  x  c  v  b  n  m  ,  .   /   space <<"
        )
    else:
        capsl = "caps"
        if vr("caps") == 2:
            capsl = capsl.upper()
        kseq += str(
            " " * 2
            + "TAB     Q  W  E  R  T  Y  U  I  O  P  {  }   |  ||"
            + " " * 2
            + capsl
            + '    A  S  D  F  G  H  J  K  L  :   "  ENTER ||'
            + " " * 2
            + "SHIFT   Z  X  C  V  B  N  M  <  >   ?   SPACE <<"
        )
    vr("d").nwrite(kseq)


vr("dr_keys", dr_keys)
del dr_keys

vr(
    "vkloc",
    [
        [0, 3, 7],
        [0, 8, 10],
        [0, 11, 13],
        [0, 14, 16],
        [0, 17, 19],
        [0, 20, 22],
        [0, 23, 25],
        [0, 26, 28],
        [0, 29, 31],
        [0, 32, 34],
        [0, 35, 37],
        [0, 38, 40],
        [0, 41, 43],
        [0, 44, 46],
        [0, 47, 51],
        [1, 3, 7],
        [1, 11, 13],
        [1, 14, 16],
        [1, 17, 19],
        [1, 20, 22],
        [1, 23, 25],
        [1, 26, 28],
        [1, 29, 31],
        [1, 32, 34],
        [1, 35, 37],
        [1, 38, 40],
        [1, 41, 43],
        [1, 44, 46],
        [1, 48, 50],
        [2, 3, 8],
        [2, 11, 13],
        [2, 14, 16],
        [2, 17, 19],
        [2, 20, 22],
        [2, 23, 25],
        [2, 26, 28],
        [2, 29, 31],
        [2, 32, 34],
        [2, 35, 37],
        [2, 38, 40],
        [2, 42, 44],
        [2, 45, 51],
        [3, 3, 9],
        [3, 11, 13],
        [3, 14, 16],
        [3, 17, 19],
        [3, 20, 22],
        [3, 23, 25],
        [3, 26, 28],
        [3, 29, 31],
        [3, 32, 34],
        [3, 35, 37],
        [3, 39, 41],
        [3, 43, 49],
    ],
)

vr(
    "keys",
    [
        [-1, -1],
        [96, 126],
        [49, 33],
        [50, 64],
        [51, 35],
        [52, 36],
        [53, 37],
        [54, 94],
        [55, 38],
        [56, 42],
        [57, 40],
        [48, 41],
        [45, 95],
        [61, 43],
        [127, 127],
        [9, 9],
        [113, 81],
        [119, 87],
        [101, 69],
        [114, 82],
        [116, 84],
        [121, 89],
        [117, 85],
        [105, 73],
        [111, 79],
        [112, 80],
        [91, 123],
        [93, 125],
        [92, 124],
        [400, 400],
        [97, 65],
        [115, 83],
        [100, 68],
        [102, 70],
        [103, 71],
        [104, 72],
        [106, 74],
        [107, 75],
        [108, 76],
        [59, 58],
        [39, 34],
        [10, 10],
        [401, 401],
        [122, 90],
        [120, 88],
        [99, 67],
        [118, 86],
        [98, 66],
        [110, 78],
        [109, 77],
        [44, 60],
        [46, 62],
        [47, 63],
        [32, 32],
    ],
)


def vsel(kid: int, chrl="[", chrt="]") -> None:
    ckl = vr("vkloc")[kid]
    vr("d").move(y=ckl[0] + 16, x=ckl[1])
    vr("d").nwrite(chrl)
    vr("d").move(y=ckl[0] + 16, x=ckl[2])
    vr("d").nwrite(chrt)


vr("vsel", vsel)
del vsel


def usel(kid: int) -> None:
    vr("vsel")(kid, " ", " ")


vr("usel", usel)
del usel

vr("caps", None)


def kb(title: str = "Input text", prompt: str = "", start: str = None) -> bytes:
    sel = 21
    vr("caps", 0)
    vr("dr_keys")()
    vr("d").move(y=0, x=0)
    sps = int((52 - len(title)) / 2) - 2
    vr("d").nwrite(sps * " " + "| " + title + " |" + sps * " ")
    del sps
    vr("d").nwrite("-" * 52)
    vr("d").nwrite(prompt + "_")
    sty = 3
    stx = len(prompt)
    res = []
    if start is not None:
        res += list(bytes(start, "UTF-8"))
    repeat_mode = False
    last_key_time = 0
    while True:
        vr("vsel")(sel)
        vr("refr")()
        be.io.ledset(1)
        vr("d").buf[1] = ""
        vr("d").program()
        if repeat_mode:
            if time.monotonic() - last_key_time > 0.1:
                repeat_mode = False
            else:
                last_key_time = time.monotonic()
        be.io.ledset(3)
        k = vr("d").buf[0]
        if k in [-1, 4]:
            res.clear()
            break
        elif not k:
            vr("usel")(sel)
            if sel < 2:
                sel = 42
            elif sel < 12:
                sel = 41 + sel
            elif sel < 15:
                sel = 53
            elif sel == 15:
                sel = 0
            elif sel < 29:
                sel -= 14
            elif sel == 41:
                sel = 28
            elif sel < 42:
                sel -= 14
            elif sel < 53:
                sel -= 13
            else:
                sel = 41
            vr("vsel")(sel)
        elif k == 1:
            vr("usel")(sel)
            if not sel:
                sel = 14
            elif sel == 15:
                sel = 28
            elif sel == 29:
                sel = 41
            elif sel == 42:
                sel = 53
            else:
                sel -= 1
            vr("vsel")(sel)
        elif k == 2:
            vr("usel")(sel)
            if sel < 2:
                sel = 15
            elif sel < 28:
                sel += 14
            elif sel == 28:
                sel = 41
            elif sel < 41:
                sel += 13
            elif sel == 41:
                sel = 53
            elif sel == 42:
                sel = 0
            elif sel == 53:
                sel = 14
            else:
                sel -= 41
            vr("vsel")(sel)
        elif k == 3:
            vr("usel")(sel)
            if sel == 14:
                sel = 0
            elif sel == 28:
                sel = 15
            elif sel == 41:
                sel = 29
            elif sel == 53:
                sel = 42
            else:
                sel += 1
            vr("vsel")(sel)
        elif k == 7:
            usecaps = bool(vr("caps"))
            if vr("caps") == 2 and sel < 12 and sel != 1:
                usecaps = False
            keysel = vr("keys")[sel][usecaps]
            if vr("caps") == 1 and keysel != 401:
                vr("caps", 0)
                vr("dr_keys")()
            if keysel == 10:
                break
            elif keysel == -1:
                res.clear()
                break
            elif keysel == 401:
                vr("caps", int(not vr("caps")))
                vr("dr_keys")()
            elif keysel == 400:
                if vr("caps") != 2:
                    vr("caps", 2)
                else:
                    vr("caps", 0)
                vr("dr_keys")()
            elif keysel == 127:
                if res:
                    vr("d").move(y=sty, x=stx + len(res))
                    vr("d").nwrite("  \010\010 \010_")
                    res.pop()
                    vr("refr")()
            else:
                res.append(keysel)
                vr("d").move(y=sty, x=stx + len(res))
                vr("d").nwrite(chr(keysel) + "_")
                vr("refr")()
        mkeys = vr("c").in_waiting
        krep = time.monotonic()
        if not repeat_mode:
            if mkeys:
                repeat_mode = True
                while time.monotonic() - krep < 0.5:
                    if not vr("c").in_waiting:
                        repeat_mode = False
                        break
                last_key_time = time.monotonic()
        else:
            while (time.monotonic() - krep < 0.08) and vr("c").in_waiting:
                pass
            last_key_time = time.monotonic()
    return str(bytes(res), "UTF-8")


vr("kb", kb)
del kb
