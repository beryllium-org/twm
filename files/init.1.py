vr("d", be.devices["DISPLAY"][0])
vr("d").auto_refresh = False
vr("dm", "text")
vr("c", pv[0]["consoles"]["tty1"])
vr("j", jcurses())
vr("j").console = vr("c")
vr("c").enable()
vr("j").clear()
vr("j").trigger_dict = {
    "ctrlC": -1,
    "overflow": 8,
    "rest": "ignore",
    "rest_a": "common",
    "echo": "none",
    "prefix": "",
    "permit_pos": False,
    "idle": 9,
}
vr(
    "logo",
    [
        ",-----------,",
        "| 4    9.01 |",
        "|           |",
        "|           |",
        "| BERYLLIUM |",
        "'-----------'",
    ],
)


def refr() -> None:
    vr("d").refresh()


vr("refr", refr)
del refr

vr("lmid", (vr("c").size[0] // 2) - (len(vr("logo")[0]) // 2))
vr("j").move(y=5)
vr("j").nwrite(
    vr("j").nwrite(" " * vr("lmid") + ("\n" + (" " * vr("lmid"))).join(vr("logo")))
)
vr("j").move(y=12, x=19)
vr("j").nwrite("<|" + (" " * 14) + ">")
vrd("lmid")
vr("refr")()

vr("b", be.devices["bat"][0])
vr("blast", vr("b").percentage)
vr("i2s", be.devices["i2s"][0])
vr("t", be.devices["gtouch"][0])
vr("15flag", True)
vr("10flag", True)
vr("05flag", True)

vr("j").move(y=12, x=20)
vr("j").nwrite("|")
vr("refr")()


class player:
    def __init__(self, dev, cl):
        self._dev = dev
        self._aud = cl
        self._f = None
        self._b = None
        self._fnc = "    "

    def play(self, filen=None) -> None:
        if vr("sounds"):
            if filen is None or filen == self._fnc:
                if self._b is not None:
                    if self._dev.playing:
                        self.stop()
                    self._dev.play(self._b)
                else:
                    raise ValueError("No file provided!")
            else:
                self.stop()
                if self._b is not None:
                    self._b.deinit()
                    self._b = None
                    self._f.close()
                    self._f = None
                res = be.api.fs.resolve(filen)
                if res is not None:
                    try:
                        self._f = open(res, "rb")
                        self._b = self._aud(self._f)
                        self._fnc = filen
                        self._dev.play(self._b)
                    except:
                        raise OSError("Could not open media file!")

    def stop(self) -> None:
        self._dev.stop()

    def deinit(self) -> None:
        self._dev.stop()
        if self._b is not None:
            self._b.deinit()
            self._b = None
        if self._f is not None:
            self._f.close()
            self._f = None
        del self._aud, self._dev

    @property
    def playing(self) -> bool:
        return self._dev.playing


from audiocore import WaveFile

vr("player", player(vr("i2s"), WaveFile))
del WaveFile, player
vr("quit_twm", False)
vr("last_shown", [0, 0, 0, 0, 0, 0])
vr("force_refr", False)
vr("cached_ip", "")
vr("ind", False)
vr("batc", -70)
vr("lowpow", False)
vr("pkst", vr("c").alt_mode)
vr("lasttt", 0)
vr("lastth", [])
vr("stkey", None)

vr("j").move(y=12, x=21)
vr("j").nwrite("|")
vr("refr")()

vr("mainbri", cptoml.fetch("brightness", subtable="TWM") / 100)
vr("susbri", (cptoml.fetch("suspend_brightness", subtable="TWM")) * 0.01)
vr("reset_standby", False)
vr("alarm", (cptoml.fetch("alarm", subtable="TWM")))
if vr("alarm") and len(vr("alarm")) != 4:
    vr("alarm", None)
vr("timer", None)
vr("timer_rem", None)

vr("al_seq", None)
vr("bop_seq", None)
vr("bop_bad_seq", None)
vr("clk_seq", None)
vr("confirm_bop_seq", None)
vr("err_seq", None)
vr("vibrate", False)
vr("sounds", cptoml.fetch("sounds", subtable="TWM") == True)

vr("s_al", cptoml.fetch("alarm_sound", subtable="TWM"))
if not isinstance(vr("s_al"), str):
    vr("s_al", "/usr/share/sounds/twm_alarm.wav")

vr("s_tm", cptoml.fetch("timer_sound", subtable="TWM"))
if not isinstance(vr("s_tm"), str):
    vr("s_tm", "/usr/share/sounds/twm_timer.wav")

vr("s_no", cptoml.fetch("notification_sound", subtable="TWM"))
if not isinstance(vr("s_no"), str):
    vr("s_no", "/usr/share/sounds/twm_notification.wav")

vr("j").move(y=12, x=22)
vr("j").nwrite("|")
vr("refr")()


def rk(only_power: bool = False) -> tuple:
    nub = vr("c").alt_mode != vr("pkst")
    if nub:
        vr("pkst", not vr("pkst"))
    if only_power:
        return [False, nub]
    key = ""
    if vr("stkey") == 10:
        vr("stkey", None)
        return [True, nub]
    if vr("c").in_waiting:
        key = vr("c").read(1)
        vr("c").reset_input_buffer()
    isent = key == "\n"
    if not isent:
        vr("stkey", key)
    return [isent, nub]


def rt() -> list:
    res = []
    if time.monotonic() - vr("lasttt") > 0.02:
        for i in vr("t").touches:
            res.append({"x": i[1], "y": 240 - i[0], "z": i[2]})
        vr("lastth", res)
        vr("lasttt", time.monotonic())
    else:
        return vr("lastth")
    return res


vr(
    "rj_map",
    {
        23: "w",
        72: "w",
        19: "s",
        70: "s",
        1: "a",
        68: "a",
        4: "d",
        9: "d",
        17: "q",
        5: "e",
        3: "c",
        32: " ",
    },
)


def rj() -> str:
    stkey = vr("stkey")
    if stkey or vr("c").in_waiting:
        k = stkey or vr("c").read(1)[0]
        vr("stkey", None)

        if k in (27, 91):
            return vr("rj")()

        if k == 10:
            vr("stkey", 10)

        return vr("rj_map").get(k, "")
    return ""


def ra() -> tuple:
    return (0, 0, 0)


def moved() -> tuple:
    return True


def ctop(data: str) -> None:
    vr("j").clear()
    vr("j").nwrite(data)


def waitc() -> None:
    t = vr("rt")()
    k = vr("rk")()
    while t or k[0]:
        t = vr("rt")()
        k = vr("rk")()
        time.sleep(0.02)


def wany() -> None:
    k = vr("rk")()
    t = vr("rt")()
    while not (k[0] or k[1] or t):
        k = vr("rk")()
        t = vr("rt")()
        time.sleep(0.05)
    if k[1]:
        vr("shutdown")()


def lc() -> None:
    vr("j").nwrite("\r\033[K")


def compare_time(target_time: str) -> int:
    now = time.localtime()
    current_minutes = now.tm_hour * 60 + now.tm_min
    target_minutes = int(target_time[:2]) * 60 + int(target_time[2:])

    return (current_minutes > target_minutes) - (current_minutes < target_minutes)


def clocker() -> None:
    need_refr = False
    ct = time.localtime()
    d = ct.tm_mday
    o = ct.tm_mon
    y = ct.tm_year
    h = ct.tm_hour
    m = ct.tm_min
    s = ct.tm_sec
    wd = ct.tm_wday
    darr = [d, o, y]
    harr = [h, m, s]
    if darr != vr("last_shown")[:3]:
        need_refr = True
        vr("last_shown", darr + vr("last_shown")[3:])
    if vr("lowpow"):
        if m != vr("last_shown")[4]:
            vr("last_shown", vr("last_shown")[:3] + harr)
            need_refr = True
    else:
        if s != vr("last_shown")[5]:
            vr("last_shown", vr("last_shown")[:3] + harr)
            need_refr = True

    if vr("force_refr"):
        need_refr = True
        vr("force_refr", False)
    if need_refr:
        vr("j").move(y=3)
        vr("lc")()
        d = str(d) if d > 9 else "0" + str(d)
        o = vr("months")[o - 1]
        vr("j").write(vr("days")[wd] + " " + str(d) + "/" + str(o) + "/" + str(y))
        vr("lc")()
        if vr("alarm"):
            vr("j").nwrite("Alarm: ")
            vr("j").nwrite(vr("alarm")[:2] + ":" + vr("alarm")[2:])
        hl = h
        hh = 0
        if hl > 9:
            hl = int(str(h)[1])
            hh = int(str(h)[0])
        ml = m
        mh = 0
        if ml > 9:
            ml = int(str(m)[1])
            mh = int(str(m)[0])
        sl = s
        sh = 0
        if vr("lowpow"):
            sl = 10
            sh = 10
        else:
            if sl > 9:
                sl = int(str(s)[1])
                sh = int(str(s)[0])
        ind = True
        if vr("lowpow"):
            ind = True
        elif not vr("ind"):
            ind = False
            vr("ind", True)
        else:
            vr("ind", False)

        ind = 12 if ind else 11
        for i in range(3):
            vr("j").move(y=6 + i)
            vr("lc")()
            vr("j").nwrite(
                " " * 16
                + vr("bigs")[hh][i]
                + vr("bigs")[hl][i]
                + vr("bigs")[ind][i]
                + vr("bigs")[mh][i]
                + vr("bigs")[ml][i]
                + vr("bigs")[ind][i]
                + vr("bigs")[sh][i]
                + vr("bigs")[sl][i]
            )
        vr("updi")(True)
    elif vr("lowpow"):
        time.sleep(0.15)


vr("j").move(y=12, x=23)
vr("j").nwrite("|")
vr("refr")()


def suspend() -> None:
    vr("d").brightness = vr("susbri")
    vr("force_refr", True)
    vr("lowpow", True)
    cpu.frequency = 80_000_000


def resume() -> None:
    cpu.frequency = 240_000_000
    vr("d").brightness = vr("mainbri")
    vr("lowpow", False)
    vr("force_refr", True)
    vr("updi")(True)


def fselect(frompath: str = "/home/board"):
    vr("selector", frompath)
    vr("selected", False)
    be.api.subscript("/bin/twm/fm.py")
    res = None
    if vr("selected") == True:
        res = vr("selector")
    vr("selector", None)
    return res


def check_timers() -> bool:
    ct = time.localtime()
    ft = (
        ("0" if ct.tm_hour < 10 else "")
        + str(ct.tm_hour)
        + ("0" if ct.tm_min < 10 else "")
        + str(ct.tm_min)
    )
    if vr("alarm") is not None and vr("alarm") == ft:
        return True
    if vr("timer") is not None and vr("timer") < time.monotonic():
        return True
    perc = vr("b").percentage
    if not perc:
        return True
    elif vr("15flag") and perc < 16:
        return True
    elif vr("10flag") and perc < 11:
        return True
    elif vr("05flag") and perc < 6:
        return True
    return False


def treat_timers() -> None:
    ct = time.localtime()
    ft = (
        ("0" if ct.tm_hour < 10 else "")
        + str(ct.tm_hour)
        + ("0" if ct.tm_min < 10 else "")
        + str(ct.tm_min)
    )
    if vr("alarm") is not None and vr("alarm") == ft:
        vr("ring_alarm")()
    if vr("timer") is not None and vr("timer") < time.monotonic():
        vr("ring_timer")()
    doa = True
    if not vr("b").percentage:
        vr("shutdown")()
    if vr("05flag") and vr("b").percentage < 6:
        vr("05flag", False)
        if doa:
            vr("notifylow")()
            doa = False
    if vr("10flag") and vr("b").percentage < 11:
        vr("10flag", False)
        if doa:
            vr("notifylow")()
            doa = False
    if vr("15flag") and vr("b").percentage < 16:
        vr("15flag", False)
        if doa:
            vr("notifylow")()
            doa = False


def notifylow() -> None:
    if vr("lowpow"):
        vr("resume")()
    vr("ctop")("Low battery!")
    vr("refr")()
    vr("player").play(vr("s_no"))
    time.sleep(3)


def ring_alarm() -> None:
    if vr("lowpow"):
        vr("resume")()
    if not vr("player").playing:
        vr("player").play(vr("s_al"))
    vr("d").brightness = vr("mainbri")
    ahr = vr("alarm")[:2]
    amin = vr("alarm")[2:]
    astr = "ALARM -- alarm - ALARM -!- alarm -- ALARM -- alarm -"
    shf = 0
    sht = time.monotonic()
    nt = False
    rt = -1
    vr("ctop")(f"ALARM - {ahr}:{amin}\n" + (vr("c").size[0] * "-"))
    vr("j").move(y=7, x=26)
    vr("j").nwrite("/\\")
    vr("j").move(y=8, x=25)
    vr("j").nwrite("/  \\")
    vr("j").move(y=9, x=24)
    vr("j").nwrite("/ || \\")
    vr("j").move(y=10, x=23)
    vr("j").nwrite("/  ||  \\")
    vr("j").move(y=11, x=22)
    vr("j").nwrite("/   ..   \\")
    vr("j").move(y=12, x=21)
    vr("j").nwrite("/__________\\")
    vr("refr")()
    k = vr("rk")()
    try:
        while not k[0]:
            if not vr("player").playing:
                vr("player").play(vr("s_al"))
            lt = time.monotonic()
            if lt - rt > 2:
                rt = lt
            k = vr("rk")()
            vr("j").move(y=4, x=1)
            vr("j").nwrite(vr("str_rotate")(astr, shf))
            vr("j").move(y=18, x=1)
            vr("j").nwrite(vr("str_rotate")(astr, shf))
            vr("j").move(y=15)
            vr("lc")()
            if nt < 0:
                vr("j").nwrite((" " * 13) + "Press Power button to exit")
            nt += 1
            if nt > 6:
                nt = -6
            shf += 1
            sht = lt
            if shf > len(astr):
                shf = 0
            vr("refr")()
    except KeyboardInterrupt:
        vr("quit_twm", True)
    vr("player").stop()


def ring_timer() -> None:
    if vr("lowpow"):
        vr("resume")()
    if not vr("player").playing:
        vr("player").play(vr("s_tm"))
    vr("d").brightness = vr("mainbri")
    astr = " TIME IS UP -!- TIMER RAN OUT --!!-- "
    nt = False
    vr("ctop")("TIMER\n" + (vr("c").size[0] * "-"))
    vr("j").move(y=5, x=14)
    vr("j").nwrite("TIME IS UP!")
    vr("refr")()
    k = vr("rk")()
    shf = 0
    rt = -1
    try:
        while not k[0]:
            if not vr("player").playing:
                vr("player").play(vr("s_tm"))
            lt = time.monotonic()
            if lt - rt > 3:
                rt = lt
            k = vr("rk")()
            vr("j").move(y=18, x=2)
            vr("j").nwrite(vr("str_rotate")(astr, shf))
            vr("j").move(y=15)
            vr("lc")()
            if nt < 0:
                vr("j").nwrite((" " * 6) + "Press Power button to exit")
            nt += 1
            if nt > 6:
                nt = -6
            shf += 1
            sht = lt
            if shf > len(astr):
                shf = 0
            vr("refr")()
    except KeyboardInterrupt:
        vr("quit_twm", True)
    vr("timer", None)
    vr("player").stop()


vr("j").move(y=12, x=24)
vr("j").nwrite("|")
vr("refr")()


def pstr() -> str:
    return (str(vr("b").percentage) + "%") if vr("b") else "N/A"


def updi(force=False) -> None:
    need_refr = False
    res = False
    if vr("b").percentage > 20:
        vr("15flag", True)
        vr("10flag", True)
        vr("05flag", True)

    if force or time.monotonic() - vr("batc") > 60:
        vr("j").move(y=17, x=45)
        vr("j").nwrite(vr("pstr")() + " " * 3)
        need_refr = True
        vr("batc", time.monotonic())

    tmpip = str(be.devices["network"][0].get_ipconf()["ip"])
    if vr("cached_ip") != tmpip:
        vr("j").move(y=16, x=36)
        vr("j").nwrite(" " * 16)
        vr("j").move(y=16, x=36)
        vr("j").nwrite(tmpip)
        need_refr = True

    if need_refr and vr("d").brightness:
        vr("refr")()

    if res:
        vr("reset_standby", True)


def str_rotate(string: str, n: int) -> str:
    return string[n:] + string[:n]


def swipe_unlock() -> bool:
    vr("j").clear()
    ct = vr("rt")()
    ll = 1
    rot = 0
    lstr = "-^^-Swipe-up-to-unlock-^-^^-^-^-Swipe-up-to-unlock-"
    checkt = time.monotonic()
    while ct:
        vr("lc")()
        y = ct[0]["y"]
        ll = int((y * (vr("c").size[1]) / 240) + 1)
        vr("j").move(y=ll, x=1)
        vr("j").nwrite(vr("str_rotate")(lstr, rot))
        if time.monotonic() - checkt > 0.12:
            rot += 1
            if rot > len(lstr):
                rot = 0
            checkt = time.monotonic()
        vr("refr")()
        ct = vr("rt")()
    vr("chm", None)
    return ll > 7


def vibr(pattern: list) -> None:
    pass  # No vibration


def stv() -> None:
    pass  # No vibration


vr("j").move(y=12, x=25)
vr("j").nwrite("|")
vr("refr")()


def lm(start_locked: bool = False) -> None:
    vr("chm", None)
    if start_locked:
        vr("d").brightness = vr("susbri")
        vr("suspend")()
    retry = True
    while retry and not vr("quit_twm"):
        retry = False
        vr("j").clear()
        vr("ctop")(
            "T-Deck Manager (T. W. M.)" + " " * 23 + "v1.1" + (vr("c").size[0] * "-")
        )
        vr("j").move(y=13)
        vr("j").nwrite(vr("c").size[0] * "-")
        vr("j").nwrite(" " * 2 + "\n  ".join(vr("logo")))
        vr("j").move(y=15, x=34)
        vr("j").nwrite("| IP Address:")
        vr("j").move(y=16, x=34)
        vr("j").nwrite("| - " + str(be.devices["network"][0].get_ipconf()["ip"]))
        vr("j").move(y=17, x=34)
        vr("j").nwrite("| Battery: ")
        vr("j").move(y=18, x=34)
        gc.collect()
        gc.collect()
        freeb = gc.mem_free()
        if freeb > 1024:
            freeb = str(freeb // 1024) + "k"
        else:
            freeb = str(freeb)
        vr("j").nwrite("| " + freeb + " bytes free")
        lp = time.monotonic()
        lm = time.monotonic()
        press = 0
        vr("waitc")()
        try:
            while True:
                if vr("check_timers")():
                    vr("treat_timers")()
                    retry = True
                    vr("chm", None)
                    break
                m = vr("rj")()
                if not vr("lowpow"):
                    tou = vr("rt")()
                    if m == "q":
                        vr("shutdown")()
                        retry = True
                        break
                    elif m == " ":
                        return
                    if tou:
                        lp = time.monotonic()
                        if vr("d").brightness < vr("mainbri"):
                            vr("d").brightness = vr("mainbri")
                        elif tou[0]["y"] > 160:
                            retry = vr("swipe_unlock")()
                            vr("force_refr", True)
                            break
                    if time.monotonic() - lp > 8:
                        if vr("d").brightness > 0.1:
                            vr("d").brightness -= 0.01
                            time.sleep(0.05)
                        else:
                            vr("suspend")()
                            lm = time.monotonic()
                    gc.collect()
                else:
                    vr("c").alt_mode = False
                    time.sleep(0.1)
                if vr("d").brightness:
                    vr("clocker")()
                vr("updi")()
                if vr("reset_standby"):
                    vr("reset_standby", False)
                    lm = time.monotonic()
                    lp = lm
                t = [False, False] if not m else vr("rk")(True)
                if (not vr("lowpow")) and m == " ":
                    return
                if t[1]:
                    if not vr("lowpow"):
                        vr("shutdown")()
                        retry = True
                        break
                elif vr("stkey") == 10:
                    vr("stkey", None)
                    if vr("lowpow"):
                        vr("resume")()
                        lp = time.monotonic()
                        vr("waitc")()
                    else:
                        vr("suspend")()
                        lm = time.monotonic()
                    press = time.monotonic()
                elif vr("lowpow"):
                    be.api.tasks.run()
        except KeyboardInterrupt:
            if vr("lowpow"):
                vr("resume")()
            vr("quit_twm", True)
            return


vr("j").move(y=12, x=26)
vr("j").nwrite("|")
vr("refr")()
vr(
    "bigs",
    [
        [" _ ", "| |", "|_|"],  # 0 | 0
        ["   ", "  |", "  |"],  # 1 | 1
        [" _ ", " _|", "|_ "],  # 2 | 2
        [" _ ", " _|", " _|"],  # 3 | 3
        ["   ", "|_|", "  |"],  # 4 | 4
        [" _ ", "|_ ", " _|"],  # 5 | 5
        [" _ ", "|_ ", "|_|"],  # 6 | 6
        [" _ ", "  |", "  |"],  # 7 | 7
        [" _ ", "|_|", "|_|"],  # 8 | 8
        [" _ ", "|_|", " _|"],  # 9 | 9
        ["   ", " _ ", "   "],  # - | 10
        [" ", " ", " "],  #   | 11
        [" ", ".", "."],  # : | 12
        [" ", " ", "."],  # . | 13
    ],
)
vr(
    "months",
    [
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec",
    ],
)
vr(
    "days",
    [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ],
)


vr("j").move(y=12, x=27)
vr("j").nwrite("|")
vr("refr")()


def ditem(item: str, sel: bool) -> None:
    vr("lc")()
    ldat = " - "
    if sel:
        ldat += "[ "
    ldat += item
    if sel:
        ldat += " ]"
    vr("j").write(ldat)


def dmenu(
    title: str, data: list, preselect: int = 0, timeout: int = 10, remember: bool = True
) -> int:
    retry = True
    sel = preselect
    scl = 0
    while sel - scl > vr("c").size[1] - 8:
        scl += 1
    reset_sel = False
    while retry and not vr("quit_twm"):
        vr("c").alt_mode = True
        timeout_c = time.monotonic()
        if reset_sel and not remember:
            sel = 0
            scl = 0
            reset_sel = False
        retry = False
        vr("waitc")()
        vr("ctop")(title + "\n" + (vr("c").size[0] * "-"))
        ysize = vr("c").size[1]
        db = 0
        tm = -1
        u = True
        try:
            while not vr("quit_twm"):
                if vr("check_timers")():
                    vr("treat_timers")()
                    retry = True
                    break
                vr("j").move(y=1, x=vr("c").size[0] - 4)
                vr("j").nwrite(" " * 4)
                cpstr = vr("pstr")()
                vr("j").move(y=1, x=vr("c").size[0] - len(cpstr))
                vr("j").nwrite(cpstr)
                if u:
                    u = False
                    vr("j").move(y=3)
                    bigl = 7
                    big = len(data) > vr("c").size[1] - bigl + 1
                    if not big:
                        vr("j").write()
                        for i in range(len(data)):
                            vr("ditem")(data[i], sel == i)
                    else:
                        vr("lc")()
                        vr("j").write("   [...]" if scl else None)
                        for i in range(ysize + 1 - bigl):
                            vr("ditem")(data[i + scl], sel - scl == i)
                        vr("lc")()
                        if scl != len(data) - (ysize + 1 - bigl):
                            vr("j").write("   [...]")
                    vr("refr")()
                if db:
                    db = 0
                m = vr("rj")()
                k = vr("rk")()
                t = vr("rt")()
                if t:
                    timeout_c = time.monotonic()
                    if vr("d").brightness < vr("mainbri"):
                        vr("d").brightness = vr("mainbri")
                if k[1]:
                    break
                elif k[0]:
                    return sel
                elif m:
                    timeout_c = time.monotonic()
                    if vr("d").brightness < vr("mainbri"):
                        vr("d").brightness = vr("mainbri")
                    else:
                        db = 1
                        tm = timeout_c
                        if m == "w":  # up
                            if sel:
                                sel -= 1
                                u = True
                                if scl and (sel - scl < 0):
                                    scl -= 1
                            else:
                                db += 1
                        elif m == "s":  # down
                            if sel < len(data) - 1:
                                sel += 1
                                u = True
                                if big and (sel - scl > ysize - bigl):
                                    scl += 1
                            else:
                                db += 1
                        elif m == "q":  # cancel
                            break
                elif timeout is not None and time.monotonic() - timeout_c > timeout:
                    if vr("d").brightness > 0.1:
                        vr("d").brightness -= 0.05
                        time.sleep(0.145)
                    else:
                        vr("lm")(True)
                        retry = True
                        reset_sel = True
                        break
        except KeyboardInterrupt:
            vr("quit_twm", True)
    return -1


vr("j").move(y=12, x=28)
vr("j").nwrite("|")
vr("refr")()


def slidemenu(title: str, data: list, preselect=0) -> int:
    retry = True
    sel = preselect
    need_refr = True
    while retry and not vr("quit_twm"):
        vr("c").alt_mode = True
        timeout = time.monotonic()
        retry = False
        vr("waitc")()
        vr("ctop")(title + "\n" + (vr("c").size[0] * "-"))
        oldselp = -1
        oldsel = -1
        iteml = len(data)
        dashes = vr("c").size[0] - 2
        db = 0
        tm = -1
        try:
            while not vr("quit_twm"):
                if vr("check_timers")():
                    vr("treat_timers")()
                    retry = True
                    break
                vr("j").move(y=1, x=vr("c").size[0] - 4)
                vr("j").nwrite(" " * 4)
                cpstr = vr("pstr")()
                vr("j").move(y=1, x=vr("c").size[0] - len(cpstr))
                vr("j").nwrite(cpstr)
                if sel != oldsel:
                    selp = (sel * dashes) // (iteml - 1)
                    oldsel = sel
                    if selp != oldselp:
                        vr("j").move(y=4)
                        vr("j").nwrite(" " + ("-" * dashes))
                        oldselp = selp
                        vr("j").move(y=3)
                        vr("lc")()
                        newp = selp + (2 if selp < dashes else 1)
                        vr("j").move(y=3, x=newp)
                        vr("j").nwrite("v")
                        vr("j").move(y=4, x=newp)
                        vr("j").nwrite("|")
                        vr("j").move(y=5)
                        vr("lc")()
                        vr("j").move(y=5, x=newp)
                        vr("j").nwrite("^")
                    vr("j").move(y=6)
                    vr("lc")()
                    vr("j").move(
                        y=6, x=(vr("c").size[0] // 2 - len(data[sel]) // 2 + 1)
                    )
                    vr("j").nwrite(data[sel])
                    need_refr = True
                if db:
                    seq = vr("bop_seq")
                    if db == 2:
                        seq = vr("bop_bad_seq")
                    elif db == 3:
                        seq = vr("clk_seq")
                    db = 0
                t = vr("rt")()
                m = vr("rj")()
                k = vr("rk")()
                if k[1]:
                    break
                elif k[0]:
                    return sel
                elif t or m:
                    timeout = time.monotonic()
                    if vr("d").brightness < vr("mainbri"):
                        vr("d").brightness = vr("mainbri")
                    if m:
                        db = 1
                        if m == "a":  # minus
                            if sel:
                                sel -= 1
                            else:
                                db += 1
                        elif m == "d":  # plus
                            if sel < len(data) - 1:
                                sel += 1
                            else:
                                db += 1
                        elif m == "q":  # cancel
                            break
                        time.sleep(0.1)
                    else:
                        x = t[0]["x"]
                        if x > 5 and x < 320:
                            sel = ((x - 5) * iteml) // 320
                            if sel != oldsel:
                                db = 3
                                need_refr = True
                elif time.monotonic() - timeout > 10:
                    if vr("d").brightness > 0.1:
                        vr("d").brightness -= 0.05
                        time.sleep(0.12)
                    else:
                        vr("lm")(True)
                        retry = True
                        break

                if need_refr:
                    need_refr = False
                    vr("refr")()
        except KeyboardInterrupt:
            vr("quit_twm", True)
    return -1


def appm() -> None:
    vr("ok", 0)
    be.api.subscript("/bin/stringproccessing/appmenul.py")
    if not vr("ok"):
        raise OSError("COULD NOT PARSE APPLICATIONS")
    apps_k = list(vr("apps").keys())
    apps_k.sort()
    apps_k.insert(0, "Main menu")
    prev = 0
    while True:
        sel = vr("dmenu")("Apps", apps_k, preselect=prev)
        if sel in [-1, 0]:
            break
        else:
            prev = sel
            desc = vr("apps")[apps_k[sel]][0]
            exef = vr("apps")[apps_k[sel]][1]
            mode = vr("apps")[apps_k[sel]][2]
            if exef is None or mode is None:
                vr("j").clear()
                vr("player").play(vr("s_no"))
                vr("j").nwrite("Invalid application!")
                vr("refr")()
                time.sleep(3)
            else:
                if mode == "python":
                    vr("j").clear()
                    vr("j").nwrite("Running python application..")
                    vr("refr")()
                    be.based.command.fpexec(exef)
                elif mode == "wm":
                    vr("j").clear()
                    vr("refr")()
                    be.api.subscript(exef)
                elif mode == "shell":
                    vr("j").clear()
                    vr("j").nwrite("Running shell application..")
                    vr("refr")()
                    be.based.run(exef)
                else:
                    vr("j").clear()
                    vr("player").play(vr("s_no"))
                    vr("j").nwrite("Unknown execution mode!")
                    vr("refr")()
                    time.sleep(3)
    vrd("apps")


vr("j").move(y=12, x=29)
vr("j").nwrite("|")
vr("refr")()


def hs() -> None:
    vr("d").brightness = vr("mainbri")
    vr("lm")()
    prev = 0
    while not vr("quit_twm"):
        vr("waitc")()
        sel = vr("dmenu")(
            "Home",
            [
                "Apps",
                "Files",
                "Alarms",
                "Stopwatch",
                "Timer",
                "Settings",
                "Power",
            ],
            preselect=prev,
            remember=False,
        )
        prev = sel if sel != -1 else 0
        if sel == -1:
            if not vr("quit_twm"):
                vr("lm")()
        elif sel == 0:
            vr("appm")()
        elif sel == 1:
            vr("selector", None)
            be.api.subscript("/bin/twm/fm.py")
        elif sel == 2:
            be.api.subscript("/bin/twm/ala.py")
        elif sel == 3:
            be.api.subscript("/bin/twm/stopw.py")
        elif sel == 4:
            be.api.subscript("/bin/twm/timer.py")
        elif sel == 5:
            be.api.subscript("/bin/twm/settings.py")
        elif sel == 6:
            sel = vr("dmenu")(
                "Power menu",
                [
                    "Exit to shell",
                    "Reload",
                    "Reboot",
                    "Reboot safemode",
                    "Reboot to TinyUF2",
                    "Reboot to bootloader",
                    "Developer mode (once)",
                    "Developer mode (permenantly)",
                ],
            )
            if not sel:
                vr("shutdown")()
            elif sel == 1:
                be.based.run("reload")
            elif sel == 2:
                vr("j").clear()
                vr("j").nwrite("Rebooting.. ")
                vr("refr")()
                be.based.run("reboot")
            elif sel == 3:
                vr("j").clear()
                vr("j").nwrite("Rebooting to safemode.. ")
                vr("refr")()
                be.based.run("reboot safemode")
            elif sel == 4:
                vr("j").clear()
                vr("j").nwrite("Rebooting to TinyUF2.. ")
                vr("refr")()
                be.based.run("reboot uf2")
            elif sel == 5:
                vr("j").clear()
                vr("j").nwrite("Rebooting to bootloader.. ")
                vr("refr")()
                be.based.run("reboot bootloader")
            elif sel == 6:
                vr("j").clear()
                vr("j").nwrite("Enabling.. ")
                vr("refr")()
                be.based.run("devmode -q")
            elif sel == 7:
                vr("j").clear()
                vr("j").nwrite("Enabling (permenantly).. ")
                vr("refr")()
                be.based.run("devmode -q -p")
            if sel != -1:
                vr("quit_twm", True)


def vmain() -> None:
    while not vr("quit_twm"):
        vr("hs")()


vr("j").move(y=12, x=30)
vr("j").nwrite("|")
vr("refr")()


vr("rk", rk)
vr("rt", rt)
vr("rj", rj)
vr("ra", ra)
vr("last_accel", ra())
vr("moved", moved)
vr("ctop", ctop)
vr("waitc", waitc)
vr("wany", wany)
vr("lc", lc)
vr("tix", 0)
vr("pstr", pstr)
vr("notifylow", notifylow)
vr("ring_alarm", ring_alarm)
vr("ring_timer", ring_timer)
vr("fselect", fselect)
vr("check_timers", check_timers)
vr("treat_timers", treat_timers)
vr("updi", updi)
vr("compare_time", compare_time)
vr("clocker", clocker)
vr("suspend", suspend)
vr("resume", resume)
vr("str_rotate", str_rotate)
vr("swipe_unlock", swipe_unlock)
vr("lm", lm)
vr("vibr", vibr)
vr("stv", stv)
vr("ditem", ditem)
vr("dmenu", dmenu)
vr("slidemenu", slidemenu)
vr("appm", appm)
vr("hs", hs)
vr("main", vmain)
del (
    rk,
    rt,
    rj,
    ra,
    moved,
    ctop,
    waitc,
    wany,
    lc,
    pstr,
    notifylow,
    ring_alarm,
    ring_timer,
    fselect,
    check_timers,
    treat_timers,
    updi,
    compare_time,
    clocker,
    suspend,
    resume,
    str_rotate,
    swipe_unlock,
    lm,
    vibr,
    stv,
    ditem,
    dmenu,
    slidemenu,
    appm,
    hs,
    vmain,
)

vr("j").move(y=12, x=31)
vr("j").nwrite("|")
vr("refr")()

import displayio

vr("displayio", displayio)
del displayio

vr("dbit", vr("displayio").Bitmap(vr("d").width, vr("d").height, 256))
vr("pal", vr("displayio").Palette(256))

# Populate the palette with ANSI colors
for pv[get_pid()]["i"] in range(256):
    if vr("i") < 16:
        # Standard colors (0-15)
        if vr("i") == 0:
            vr("red", 0x00)
            vr("green", 0x00)
            vr("blue", 0x00)
        elif vr("i") == 1:
            vr("red", 0x80)
            vr("green", 0x00)
            vr("blue", 0x00)
        elif vr("i") == 2:
            vr("red", 0x00)
            vr("green", 0x80)
            vr("blue", 0x00)
        elif vr("i") == 3:
            vr("red", 0x80)
            vr("green", 0x80)
            vr("blue", 0x00)
        elif vr("i") == 4:
            vr("red", 0x00)
            vr("green", 0x00)
            vr("blue", 0x80)
        elif vr("i") == 5:
            vr("red", 0x80)
            vr("green", 0x00)
            vr("blue", 0x80)
        elif vr("i") == 6:
            vr("red", 0x00)
            vr("green", 0x80)
            vr("blue", 0x80)
        elif vr("i") == 7:
            vr("red", 0xC0)
            vr("green", 0xC0)
            vr("blue", 0xC0)
        elif vr("i") == 8:
            vr("red", 0x80)
            vr("green", 0x80)
            vr("blue", 0x80)
        elif vr("i") == 9:
            vr("red", 0xFF)
            vr("green", 0x00)
            vr("blue", 0x00)
        elif vr("i") == 10:
            vr("red", 0x00)
            vr("green", 0xFF)
            vr("blue", 0x00)
        elif vr("i") == 11:
            vr("red", 0xFF)
            vr("green", 0xFF)
            vr("blue", 0x00)
        elif vr("i") == 12:
            vr("red", 0x00)
            vr("green", 0x00)
            vr("blue", 0xFF)
        elif vr("i") == 13:
            vr("red", 0xFF)
            vr("green", 0x00)
            vr("blue", 0xFF)
        elif vr("i") == 14:
            vr("red", 0x00)
            vr("green", 0xFF)
            vr("blue", 0xFF)
        elif vr("i") == 15:
            vr("red", 0xFF)
            vr("green", 0xFF)
            vr("blue", 0xFF)
    elif vr("i") < 232:
        # 6x6x6 color cube (16-231)
        vr("code", vr("i") - 16)
        vr("red", (vr("code") // 36) * 51)
        vr("green", ((vr("code") // 6) % 6) * 51)
        vr("blue", (vr("code") % 6) * 51)
    else:
        # Grayscale colors (232-255)
        vr("gray", (vr("i") - 232) * 10 + 8)
        vr("blue", vr("gray"))
        vr("green", vr("blue"))
        vr("red", vr("green"))
    vr("pal")[vr("i")] = (vr("red") << 16) | (vr("green") << 8) | vr("blue")

vrd("red")
vrd("green")
vrd("blue")
vrd("code")
vrd("gray")
vrd("i")

vr("j").move(y=12, x=32)
vr("j").nwrite("|")
vr("refr")()

vr("tg", None)
vr("draw_group", None)


def shutdown(instant=False) -> None:
    if vr("lowpow"):
        vr("resume")()
    if not instant:
        res = vr("dmenu")("Exit to shell?", ["No", "Yes"])
        if res == 1:
            vr("ctop")("Exiting to shell.. ")
            vr("refr")()
            vr("d").brightness = vr("mainbri")
            vr("refr")()
            vr("exit_tty", True)
            vr("quit_twm", True)
            raise KeyboardInterrupt


def drawmode(width=1, height=1, tile_width=240, tile_height=240) -> None:
    if vr("dm") in ["text", "dual"]:
        vr("c").disable()
    vr("d").brightness = vr("mainbri") if not vr("lowpow") else vr("susbri")
    vr(
        "tg",
        vr("displayio").TileGrid(
            vr("dbit"),
            pixel_shader=vr("pal"),
            width=width,
            height=height,
            tile_width=tile_width,
            tile_height=tile_height,
        ),
    )
    # vr("draw_group", vr("displayio").Group(scale=2))
    vr("draw_group", vr("displayio").Group())
    vra("draw_group", vr("tg"))
    vr("d").root_group = vr("draw_group")
    vr("dm", "draw")


def textmode() -> None:
    if vr("dm") == "dual":
        vr("c").disable()
        vr("c").display = vr("d")
    if vr("dm") in ["draw", "dual"]:
        if vr("tg") is not None:
            vr("tg", None)
            vr("draw_group", None)
        vr("d").root_group = None
        vr("c").enable()
        vr("d").brightness = vr("mainbri") if not vr("lowpow") else vr("susbri")
    vr("dm", "text")


def dualmode(width=1, height=1, tile_width=240, tile_height=240) -> None:
    if vr("dm") == "draw":
        vr("textmode")()
    if vr("dm") == "text":
        vr("d").brightness = vr("mainbri") if not vr("lowpow") else vr("susbri")
        vr(
            "tg",
            vr("displayio").TileGrid(
                vr("dbit"),
                pixel_shader=vr("pal"),
                width=width,
                height=height,
                tile_width=tile_width,
                tile_height=tile_height,
            ),
        )
        vr("draw_group", vr("displayio").Group())
        vra("draw_group", vr("tg"))
        vra("draw_group", vr("d").root_group.pop())
        vr("d").root_group = vr("draw_group")
    vr("dm", "dual")


vr("shutdown", shutdown)
vr("drawmode", drawmode)
vr("textmode", textmode)
vr("dualmode", dualmode)
del drawmode, textmode, dualmode, shutdown

be.code_cache.clear()

vr("j").move(y=12, x=33)
vr("j").nwrite("||")
vr("refr")()

vrp("ok")
