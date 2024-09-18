vr("d", be.devices["DISPLAY"][0])
vr("d").auto_refresh = False
vr("dm", "text")
vr("c", pv[0]["consoles"]["ttyDISPLAY0"])
vr("c").display = vr("d")
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
vr("j").move(y=12, x=12)
vr("j").nwrite("<|" + (" " * 14) + ">")
vrd("lmid")
vr("refr")()

vr("p", be.devices["AXP2101"][0])
vr("p")._bldo2_voltage_setpoint = 3300
vr("p")._aldo2_voltage_setpoint = 3300
vr("p")._dldo1_voltage_setpoint = 3300
vr("t", be.devices["ftouch"][0])
vr("b", be.devices["bat"][0])
vr("a", be.devices["BMA423"][0])
vr("r", be.devices["rtc"][0])
vr("v", be.devices["vib"][0])
vr("r").alarm_status = False
vr("i2s", be.devices["i2s"][0])
vr("15flag", True)
vr("10flag", True)
vr("05flag", True)
vr("00flag", True)

vr("j").move(y=12, x=14)
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

vr("j").move(y=12, x=14)
vr("j").nwrite("|")
vr("refr")()

vr("mainbri", cptoml.fetch("brightness", subtable="TWM") / 100)
vr("susbri", (cptoml.fetch("suspend_brightness", subtable="TWM")) * 0.001)
vr("reset_standby", False)
vr("chmaxt", None)
vr("p")._aldo4_voltage_setpoint = 0
vr("timer", None)
vr("timer_rem", None)
vr("bcon", vr("p").is_battery_connected)
vr("al_seq", [vr("v").effect(16)])
vr("bop_seq", [vr("v").effect(3)])
vr("bop_bad_seq", [vr("v").effect(1)])
vr("clk_seq", [vr("v").effect(26)])
vr("confirm_bop_seq", [vr("v").effect(13)])
vr("err_seq", [vr("v").effect(47), vr("v").pause(0.3), vr("v").effect(47)])
vr("vibrate", cptoml.fetch("vibration", subtable="TWM") == True)
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

vr("j").move(y=12, x=15)
vr("j").nwrite("|")
vr("refr")()


def rk() -> tuple:
    return vr("p").power_key_was_pressed


def rt() -> list:
    return vr("t").touches


def ra() -> tuple:
    return vr("a").acceleration


def moved() -> tuple:
    tac = vr("ra")()
    oac = vr("last_accel")
    vr("last_accel", tac)
    res = (
        abs(abs(tac[0]) - abs(oac[0])) > 0.2
        or abs(abs(tac[1]) - abs(oac[1])) > 0.2
        or abs(abs(tac[2]) - abs(oac[2])) > 0.2
    )
    return res


def ctop(data: str) -> None:
    vr("j").clear()
    vr("j").nwrite(data)


def waitc() -> None:
    t = vr("rt")()
    k = vr("rk")()
    while t or k[0] or k[1]:
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
        if vr("r").alarm_interrupt:
            vr("j").nwrite("Alarm: ")
            ahr = vr("r").alarm[0].tm_hour
            amin = vr("r").alarm[0].tm_min
            if vr("r").alarm[1] != "daily":
                vr("j").nwrite(vr("days")[vr("r").alarm[0].tm_wday] + " ")
            vr("j").nwrite(
                (("0" + str(ahr)) if ahr < 10 else str(ahr))
                + ":"
                + (("0" + str(amin)) if amin < 10 else str(amin))
            )
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
                " " * 9
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


vr("j").move(y=12, x=16)
vr("j").nwrite("|")
vr("refr")()


def suspend() -> None:
    vr("d").brightness = vr("susbri")
    vr("force_refr", True)
    vr("lowpow", True)
    vr("p")._bldo2_voltage_setpoint = 0
    vr("p")._dldo1_voltage_setpoint = 0
    vr("p")._dldo1_voltage_setpoint = 0
    target = 80_000_000 if be.devices["network"][0].enabled else 40_000_000
    if not vr("susbri"):
        vr("p")._aldo2_voltage_setpoint = 0
        if target == 40_000_000 and not pv[0]["consoles"]["ttyUSB0"].connected:
            target = 20_000_000
    cpu.frequency = target


def resume() -> None:
    cpu.frequency = 240_000_000
    vr("d").brightness = vr("mainbri")
    vr("p")._bldo2_voltage_setpoint = 3300
    vr("p")._aldo2_voltage_setpoint = 3300
    vr("p")._dldo1_voltage_setpoint = 3300
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
    if vr("r").alarm_status:
        return True
    if vr("timer") is not None and vr("timer") < time.monotonic():
        return True
    if vr("b").status == "discharging":
        if not vr("b").percentage:
            return True
        elif vr("15flag") and vr("b").percentage < 16:
            return True
        elif vr("10flag") and vr("b").percentage < 11:
            return True
        elif vr("05flag") and vr("b").percentage < 6:
            return True
        elif vr("00flag") and not vr("b").percentage:
            return True

    return False


def treat_timers() -> None:
    if vr("r").alarm_status:
        vr("ring_alarm")()
    if vr("timer") is not None and vr("timer") < time.monotonic():
        vr("ring_timer")()
    if vr("b").status == "discharging":
        if not vr("b").percentage:
            vr("shutdown")()
        else:
            doa = True
            if vr("00flag") and not vr("b").percentage:
                vr("00flag", False)
                if doa:
                    vr("notifycrit")()
                    doa = False
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
    vr("vibr")(vr("err_seq"))
    time.sleep(3)


def notifycrit() -> None:
    if vr("lowpow"):
        vr("resume")()
    vr("ctop")("Battery CRITICAL!")
    vr("refr")()
    vr("player").play(vr("s_no"))
    vr("vibr")(vr("err_seq"))
    time.sleep(3)


def bati() -> None:
    if vr("b").charging_enabled:
        if vr("b").status == "charged":
            if vr("chmaxt") is None:
                vr("chmaxt", None)
            elif time.monotonic() - vr("chmaxt") > 600:
                vr("b").charging_enabled = False
    else:
        if vr("b").percentage < 98:
            vr("b").charging_enabled = True
            vr("chmaxt", None)


def ring_alarm() -> None:
    if vr("lowpow"):
        vr("resume")()
    if not vr("player").playing:
        vr("player").play(vr("s_al"))
    vr("d").brightness = vr("mainbri")
    ahr = vr("r").alarm[0].tm_hour
    amin = vr("r").alarm[0].tm_min
    astr = "ALARM -!- alarm - ALARM -!- alarm -- "
    shf = 0
    sht = time.monotonic()
    nt = False
    rt = -1
    vr("ctop")(
        "ALARM - "
        + (("0" + str(ahr)) if ahr < 10 else str(ahr))
        + ":"
        + (("0" + str(amin)) if amin < 10 else str(amin))
        + "\n"
        + (vr("c").size[0] * "-")
    )
    vr("j").move(y=7, x=19)
    vr("j").nwrite("/\\")
    vr("j").move(y=8, x=18)
    vr("j").nwrite("/  \\")
    vr("j").move(y=9, x=17)
    vr("j").nwrite("/ || \\")
    vr("j").move(y=10, x=16)
    vr("j").nwrite("/  ||  \\")
    vr("j").move(y=11, x=15)
    vr("j").nwrite("/   ..   \\")
    vr("j").move(y=12, x=14)
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
                vr("vibr")(vr("al_seq"))
            k = vr("rk")()
            vr("j").move(y=4, x=2)
            vr("j").nwrite(vr("str_rotate")(astr, shf))
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
    vr("r").alarm_status = False
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
                vr("vibr")(vr("al_seq"))
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


vr("j").move(y=12, x=17)
vr("j").nwrite("|")
vr("refr")()


def pstr() -> str:
    return (str(vr("b").percentage) + "%") if vr("bcon") else "N/A"


def updi(force=False) -> None:
    need_refr = False
    res = False
    tst = vr("b").status
    if tst != "discharging":
        if vr("chm") != tst:
            vr("15flag", True)
            vr("10flag", True)
            vr("05flag", True)
            vr("00flag", True)
            if tst != "charged" and vr("chm") not in ["charged", None]:
                res = True
            vr("chm", tst)
            vr("j").move(y=11)
            vr("lc")()
            vr("j").move(y=11, x=(vr("c").size[0] // 2) - (len(tst) // 2))
            vr("j").nwrite(tst)
            force = True
    elif vr("chm") not in [None, "discharging"]:
        vr("j").move(y=11)
        vr("lc")()
        res = True
        vr("chm", "discharging")
        force = True
    elif vr("chm") is None:
        vr("chm", "discharging")

    if force or time.monotonic() - vr("batc") > 60:
        vr("j").move(y=17, x=30)
        vr("j").nwrite(vr("pstr")() + " " * 3)
        need_refr = True
        vr("batc", time.monotonic())
        vr("bati")()

    tmpip = str(be.devices["network"][0].get_ipconf()["ip"])
    if vr("cached_ip") != tmpip:
        vr("j").move(y=16, x=23)
        vr("j").nwrite(" " * 16)
        vr("j").move(y=16, x=23)
        vr("j").nwrite(tmpip)
        need_refr = True

    if need_refr and vr("d").brightness:
        vr("refr")()

    if res:
        vr("reset_standby", True)
        if vr("lowpow"):
            vr("resume")()
        vr("vibr")(vr("confirm_bop_seq"))


def str_rotate(string: str, n: int) -> str:
    return string[n:] + string[:n]


def swipe_unlock() -> bool:
    vr("j").clear()
    ct = vr("rt")()
    ll = 1
    rot = 0
    lstr = "--^^^^-^-Swipe-up-to-unlock-^^--^^^^-"
    checkt = time.monotonic()
    while ct:
        vr("lc")()
        y = ct[0]["y"]
        ll = int((y * (vr("c").size[1]) / 240) + 1)
        vr("j").move(y=ll, x=2)
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
    if vr("vibrate"):
        vr("stv")()
        for i in range(len(pattern)):
            vr("v").sequence[i] = pattern[i]
        for i in range(len(pattern), 8):
            vr("v").sequence[i] = vr("v").effect(0)
        vr("v").play()


def stv() -> None:
    vr("v").stop()


vr("j").move(y=12, x=18)
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
            "T-Watch Manager (T. W. M.)" + " " * 9 + "v1.0" + (vr("c").size[0] * "-")
        )
        vr("j").move(y=13)
        vr("j").nwrite(vr("c").size[0] * "-")
        vr("j").nwrite(" " * 2 + "\n  ".join(vr("logo")))
        vr("j").move(y=15, x=19)
        vr("j").nwrite("| IP Address:")
        vr("j").move(y=16, x=19)
        vr("j").nwrite("| - " + str(be.devices["network"][0].get_ipconf()["ip"]))
        vr("j").move(y=17, x=19)
        vr("j").nwrite("| Battery: ")
        vr("j").move(y=18, x=19)
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
                if not vr("lowpow"):
                    tou = vr("rt")()
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
                            vr("d").brightness -= 0.05
                            time.sleep(0.05)
                        else:
                            vr("suspend")()
                            lm = time.monotonic()
                    gc.collect()
                else:
                    if vr("d").brightness:
                        if vr("moved")() or vr("rt")():
                            lm = time.monotonic()
                        elif time.monotonic() - lm > 60:
                            if vr("d").brightness > 0.001:
                                vr("d").brightness -= 0.001
                            else:
                                vr("d").brightness = 0
                                vr("p")._aldo2_voltage_setpoint = 0
                                if not (
                                    be.devices["network"][0].enabled
                                    or pv[0]["consoles"]["ttyUSB0"].connected
                                ):
                                    cpu.frequency = 20_000_000
                        time.sleep(0.2)
                    elif vr("susbri") and (vr("moved")() or vr("rt")()):
                        vr("d").brightness = vr("susbri")
                        if not vr("p")._aldo2_voltage_setpoint:
                            vr("p")._aldo2_voltage_setpoint = 3300
                        lm = time.monotonic()
                        time.sleep(0.2)
                    else:
                        time.sleep(0.8)
                if vr("d").brightness:
                    vr("clocker")()
                vr("updi")()
                if vr("reset_standby"):
                    vr("reset_standby", False)
                    lm = time.monotonic()
                    lp = lm
                t = vr("rk")()
                if t[1]:
                    vr("shutdown")()
                elif t[0]:
                    if vr("lowpow"):
                        vr("resume")()
                        if time.monotonic() - press < 1.1:
                            return
                        lp = time.monotonic()
                    else:
                        if time.monotonic() - press < 0.55:
                            return
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


vr("j").move(y=12, x=19)
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


vr("j").move(y=12, x=20)
vr("j").nwrite("|")
vr("refr")()


def drawbox() -> None:
    sz = vr("c").size[0] // 4
    vr("j").move(y=vr("c").size[1] - 2)
    vr("j").nwrite(
        " /"
        + "-" * (sz - 2)
        + "v"
        + ("-" * (sz) + "v") * 2
        + "-" * (sz - 1)
        + "."
        + "/"
        + " " * (sz - 1)
        + "|"
        + (sz * " " + "|") * 2
        + (sz - 1) * " "
        + "/"
        + "'"
        + "-" * (sz - 1)
        + "^"
        + ("-" * (sz) + "^") * 2
        + "-" * (sz - 2)
        + "/"
    )


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
        timeout_c = time.monotonic()
        if reset_sel and not remember:
            sel = 0
            scl = 0
            reset_sel = False
        retry = False
        vr("waitc")()
        vr("ctop")(title + "\n" + (vr("c").size[0] * "-"))
        vr("drawbox")()
        ysize = vr("c").size[1] - 1
        vr("j").move(y=ysize, x=5)
        vr("j").nwrite("UP")
        vr("j").move(y=ysize, x=13)
        vr("j").nwrite("DOWN")
        vr("j").move(y=ysize, x=23)
        vr("j").nwrite("ABORT")
        vr("j").move(y=ysize, x=34)
        vr("j").nwrite("OK")
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
                    vr("vibr")(vr("bop_seq") if db == 1 else vr("bop_bad_seq"))
                    db = 0
                t = vr("rt")()
                k = vr("rk")()
                if k[1]:
                    vr("shutdown")()
                elif k[0]:
                    vr("lm")()
                    retry = True
                    reset_sel = True
                    break
                elif t:
                    timeout_c = time.monotonic()
                    if vr("d").brightness < vr("mainbri"):
                        vr("d").brightness = vr("mainbri")
                    elif t[0]["y"] > 190 and timeout_c - tm > 0.145:
                        db = 1
                        x = t[0]["x"]
                        tm = timeout_c
                        if x < 61:  # up
                            if sel:
                                sel -= 1
                                u = True
                                if scl and (sel - scl < 0):
                                    scl -= 1
                            else:
                                db += 1
                        elif x < 121:  # down
                            if sel < len(data) - 1:
                                sel += 1
                                u = True
                                if big and (sel - scl > ysize - bigl):
                                    scl += 1
                            else:
                                db += 1
                        elif x < 181:  # cancel
                            vr("vibr")(vr("confirm_bop_seq"))
                            break
                        else:  # confirm
                            vr("vibr")(vr("confirm_bop_seq"))
                            return sel
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


vr("j").move(y=12, x=21)
vr("j").nwrite("|")
vr("refr")()


def slidemenu(title: str, data: list, preselect=0) -> int:
    retry = True
    sel = preselect
    need_refr = True
    while retry and not vr("quit_twm"):
        timeout = time.monotonic()
        retry = False
        vr("waitc")()
        vr("ctop")(title + "\n" + (vr("c").size[0] * "-"))
        vr("drawbox")()
        oldselp = -1
        oldsel = -1
        iteml = len(data)
        dashes = vr("c").size[0] - 2
        vr("j").move(y=vr("c").size[1] - 1, x=4)
        vr("j").nwrite("MINUS")
        vr("j").move(y=vr("c").size[1] - 1, x=13)
        vr("j").nwrite("PLUS")
        vr("j").move(y=vr("c").size[1] - 1, x=23)
        vr("j").nwrite("ABORT")
        vr("j").move(y=vr("c").size[1] - 1, x=34)
        vr("j").nwrite("OK")
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
                    vr("vibr")(seq)
                    db = 0
                t = vr("rt")()
                k = vr("rk")()
                if k[1]:
                    vr("shutdown")()
                elif k[0]:
                    vr("lm")()
                    retry = True
                    break
                elif t:
                    timeout = time.monotonic()
                    if vr("d").brightness < vr("mainbri"):
                        vr("d").brightness = vr("mainbri")
                    elif t[0]["y"] > 190:
                        if timeout - tm > 0.145:
                            tm = timeout
                            db = 1
                            if t[0]["x"] < 61:  # minus
                                if sel:
                                    sel -= 1
                                else:
                                    db += 1
                            elif t[0]["x"] < 121:  # plus
                                if sel < len(data) - 1:
                                    sel += 1
                                else:
                                    db += 1
                            elif t[0]["x"] < 181:  # cancel
                                vr("vibr")(vr("confirm_bop_seq"))
                                break
                            else:  # confirm
                                vr("vibr")(vr("confirm_bop_seq"))
                                return sel
                            time.sleep(0.1)
                    else:
                        x = t[0]["x"]
                        if x > 5 and x < 235:
                            sel = ((x - 5) * iteml) // 230
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
                vr("vibr")(vr("err_seq"))
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
                    vr("vibr")(vr("err_seq"))
                    vr("j").nwrite("Unknown execution mode!")
                    vr("refr")()
                    time.sleep(3)
    vrd("apps")


vr("j").move(y=12, x=22)
vr("j").nwrite("|")
vr("refr")()


def hs() -> None:
    vr("d").brightness = vr("mainbri")
    vr("lm")()
    prev = 0
    while not vr("quit_twm"):
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
                    "Shutdown",
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
                vr("j").clear()
                vr("j").nwrite("Bye!")
                vr("refr")()
            elif sel == 2:
                be.based.run("reload")
            elif sel == 3:
                vr("j").clear()
                vr("j").nwrite("Rebooting.. ")
                vr("refr")()
                be.based.run("reboot")
            elif sel == 4:
                vr("j").clear()
                vr("j").nwrite("Rebooting to safemode.. ")
                vr("refr")()
                be.based.run("reboot safemode")
            elif sel == 5:
                vr("j").clear()
                vr("j").nwrite("Rebooting to TinyUF2.. ")
                vr("refr")()
                be.based.run("reboot uf2")
            elif sel == 6:
                vr("j").clear()
                vr("j").nwrite("Rebooting to bootloader.. ")
                vr("refr")()
                be.based.run("reboot bootloader")
            elif sel == 7:
                vr("j").clear()
                vr("j").nwrite("Enabling.. ")
                vr("refr")()
                be.based.run("devmode -q")
            elif sel == 8:
                vr("j").clear()
                vr("j").nwrite("Enabling (permenantly).. ")
                vr("refr")()
                be.based.run("devmode -q -p")
            if sel != -1:
                vr("quit_twm", True)


def vmain() -> None:
    while not vr("quit_twm"):
        vr("hs")()


vr("j").move(y=12, x=23)
vr("j").nwrite("|")
vr("refr")()


vr("rk", rk)
vr("rt", rt)
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
vr("notifycrit", notifycrit)
vr("bati", bati)
vr("ring_alarm", ring_alarm)
vr("ring_timer", ring_timer)
vr("fselect", fselect)
vr("check_timers", check_timers)
vr("treat_timers", treat_timers)
vr("updi", updi)
vr("clocker", clocker)
vr("suspend", suspend)
vr("resume", resume)
vr("str_rotate", str_rotate)
vr("swipe_unlock", swipe_unlock)
vr("lm", lm)
vr("vibr", vibr)
vr("stv", stv)
vr("drawbox", drawbox)
vr("ditem", ditem)
vr("dmenu", dmenu)
vr("slidemenu", slidemenu)
vr("appm", appm)
vr("hs", hs)
vr("main", vmain)
del (
    rk,
    rt,
    ra,
    moved,
    ctop,
    waitc,
    wany,
    lc,
    pstr,
    notifylow,
    notifycrit,
    bati,
    ring_alarm,
    ring_timer,
    fselect,
    check_timers,
    treat_timers,
    updi,
    clocker,
    suspend,
    resume,
    str_rotate,
    swipe_unlock,
    lm,
    vibr,
    stv,
    drawbox,
    ditem,
    dmenu,
    slidemenu,
    appm,
    hs,
    vmain,
)

vr("j").move(y=12, x=24)
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

vr("j").move(y=12, x=25)
vr("j").nwrite("|")
vr("refr")()

vr("tg", None)
vr("draw_group", None)


def shutdown(instant=False) -> None:
    if vr("lowpow"):
        vr("resume")()
    if not instant:
        vr("ctop")("Shutting down.. ")
        vr("refr")()
        vr("d").brightness = vr("mainbri")
        vr("vibr")(vr("al_seq"))
        time.sleep(1)
        while vr("d").brightness > 0.01:
            vr("d").brightness -= 0.01
            time.sleep(0.1)
        vr("j").nwrite("Bye!")
        vr("refr")()
    be.based.run("shutdown")


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

vr("j").move(y=12, x=26)
vr("j").nwrite("||")
vr("refr")()

vrp("ok")
