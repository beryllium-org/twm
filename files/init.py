vr("j", jcurses())
vr("c", pv[0]["consoles"]["ttyDISPLAY0"])
vr("j").console = vr("c")
vr("j").clear()
vr("p", be.devices["AXP2101"][0])
vr("t", be.devices["ftouch"][0])
vr("d", be.devices["DISPLAY"][0])
vr("b", be.devices["bat"][0])
vr("a", be.devices["BMA423"][0])
vr("r", be.devices["rtc"][0])
vr("v", be.devices["vib"][0])
vr("r").alarm_status = False
vr("d").auto_refresh = False
vr("quit_twm", False)
vr("last_shown", [0, 0, 0, 0, 0, 0])
vr("force_refr", False)
vr("cached_ip", "")
vr("ind", False)
vr("batc", -70)
vr("lowpow", False)
vr("mainbri", cptoml.fetch("brightness", subtable="TWM") / 100)
vr("susbri", (cptoml.fetch("suspend_brightness", subtable="TWM") + 1) * 0.001)
vr("chmaxt", None)
vr("p")._aldo4_voltage_setpoint = 0
vr("timer", None)
vr("timer_rem", None)
vr("al_seq", [vr("v").effect(16)])
vr("bop_seq", [vr("v").effect(3)])
vr("bop_bad_seq", [vr("v").effect(1)])
vr("clk_seq", [vr("v").effect(26)])
vr("confirm_bop_seq", [vr("v").effect(13)])
vr("err_seq", [vr("v").effect(47), vr("v").pause(0.3), vr("v").effect(47)])
vr("vibrate", cptoml.fetch("vibration", subtable="TWM") == True)

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
vr("c").enable()


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
    return (
        abs(tac[0] - oac[0]) > 0.1
        or abs(tac[1] - oac[1]) > 0.1
        or abs(tac[2] - oac[2]) > 0.1
    )


def ctop(data: str) -> None:
    vr("j").clear()
    vr("j").write(data)


def waitc() -> None:
    t = vr("rt")()
    k = vr("rk")()
    while t or k[0] or k[1]:
        t = vr("rt")()
        k = vr("rk")()
        time.sleep(0.02)


def lc() -> None:
    vr("j").nwrite("\r\033[K")


def refr() -> None:
    vr("d").refresh()


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


def suspend() -> None:
    vr("d").brightness = vr("susbri")
    vr("force_refr", True)
    vr("lowpow", True)
    vr("p")._bldo2_voltage_setpoint = 0
    cpu.frequency = 80_000_000 if be.devices["network"][0].enabled else 40_000_000


def resume() -> None:
    cpu.frequency = 240_000_000
    vr("d").brightness = vr("mainbri")
    vr("p")._bldo2_voltage_setpoint = 3300
    if not vr("p")._aldo2_voltage_setpoint:
        vr("p")._aldo2_voltage_setpoint = 3300
    vr("lowpow", False)
    vr("force_refr", True)
    vr("updi")(True)


def check_timers() -> bool:
    if vr("r").alarm_status:
        vr("ring_alarm")()
        return True
    if vr("timer") is not None and vr("timer") < time.monotonic():
        vr("ring_timer")()
        return True
    return False


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


def ring_timer() -> None:
    if vr("lowpow"):
        vr("resume")()
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


def updi(force=False) -> None:
    need_refr = False
    tst = vr("b").status
    if tst != "discharging":
        if vr("chm") != tst:
            vr("chm", tst)
            vr("j").move(y=11)
            vr("lc")()
            vr("j").move(y=11, x=(vr("c").size[0] // 2) - (len(tst) // 2))
            vr("j").nwrite(tst)
            force = True
    elif vr("chm"):
        vr("j").move(y=11)
        vr("lc")()
        force = True

    if force or time.monotonic() - vr("batc") > 60:
        vr("j").move(y=17, x=30)
        vr("j").nwrite(str(vr("b").percentage) + "%" + " " * 3)
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

    if need_refr:
        vr("refr")()


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
    return ll > 7


def vibr(pattern: list) -> None:
    if vr("vibrate"):
        for i in range(len(pattern)):
            vr("v").sequence[i] = pattern[i]
        for i in range(len(pattern), 8):
            vr("v").sequence[i] = vr("v").effect(0)
        vr("v").play()


def stv() -> None:
    vr("v").stop()


def lm(start_locked: bool = False) -> None:
    vr("chm", None)
    if start_locked:
        vr("d").brightness = vr("susbri")
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
                    retry = True
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
                        if vr("moved")():
                            lm = time.monotonic()
                        elif time.monotonic() - lm > 30:
                            if vr("d").brightness > 0.001:
                                vr("d").brightness -= 0.001
                            else:
                                vr("d").brightness = 0
                                vr("p")._aldo2_voltage_setpoint = 0
                        time.sleep(0.2)
                    elif vr("moved")() or vr("rt")():
                        vr("d").brightness = vr("susbri")
                        if not vr("p")._aldo2_voltage_setpoint:
                            vr("p")._aldo2_voltage_setpoint = 3300
                        lm = time.monotonic()
                        time.sleep(0.2)
                    else:
                        time.sleep(0.5)
                if vr("d").brightness:
                    vr("clocker")()
                    vr("updi")()
                else:
                    vr("bati")()
                t = vr("rk")()
                if t[1] and not vr("lowpow"):
                    vr("quit_twm", True)
                    return
                elif t[0] or start_locked:
                    if vr("lowpow"):
                        vr("resume")()
                        if time.monotonic() - press < 1.1:
                            return
                        lp = time.monotonic()
                    else:
                        start_locked = False
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


def dmenu(title: str, data: list, preselect=0) -> int:
    retry = True
    while retry and not vr("quit_twm"):
        timeout = time.monotonic()
        retry = False
        vr("waitc")()
        vr("ctop")(title + "\n" + (vr("c").size[0] * "-"))
        sel = preselect
        scl = 0
        while sel - scl > vr("c").size[1] - 6:
            scl += 1
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
        try:
            while not vr("quit_twm"):
                if vr("check_timers")():
                    retry = True
                    break
                vr("j").move(y=3)
                bigl = 7
                big = len(data) > vr("c").size[1] - bigl
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
                    vr("j").write(
                        "   [...]" if (scl != len(data) - ysize + 1 + bigl) else None
                    )
                vr("refr")()
                if db:
                    vr("vibr")(vr("bop_seq") if db == 1 else vr("bop_bad_seq"))
                    db = 0
                t = vr("rt")()
                k = vr("rk")()
                if k[1]:
                    vr("quit_twm", True)
                elif k[0]:
                    vr("lm")()
                    retry = True
                    break
                elif t:
                    timeout = time.monotonic()
                    if vr("d").brightness < vr("mainbri"):
                        vr("d").brightness = vr("mainbri")
                    elif t[0]["y"] > 190:
                        db = 1
                        x = t[0]["x"]
                        if x < 61:  # up
                            if sel:
                                sel -= 1
                                if scl and (sel - scl < 0):
                                    scl -= 1
                            else:
                                db += 1
                        elif x < 121:  # down
                            if sel < len(data) - 1:
                                sel += 1
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
                        time.sleep(0.05)
                elif time.monotonic() - timeout > 10:
                    if vr("d").brightness > 0.1:
                        vr("d").brightness -= 0.05
                        time.sleep(0.12)
                    else:
                        vr("lm")(True)
                        retry = True
                        break
        except KeyboardInterrupt:
            vr("quit_twm", True)
    return -1


def slidemenu(title: str, data: list, preselect=0) -> int:
    retry = True
    sel = preselect
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
        try:
            while not vr("quit_twm"):
                if vr("check_timers")():
                    retry = True
                    break
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
                    vr("refr")()
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
                    vr("quit_twm", True)
                elif k[0]:
                    vr("lm")()
                    retry = True
                    break
                elif t:
                    timeout = time.monotonic()
                    if vr("d").brightness < vr("mainbri"):
                        vr("d").brightness = vr("mainbri")
                    elif t[0]["y"] > 190:
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
                elif time.monotonic() - timeout > 10:
                    if vr("d").brightness > 0.1:
                        vr("d").brightness -= 0.05
                        time.sleep(0.12)
                    else:
                        vr("lm")(True)
                        retry = True
                        break
        except KeyboardInterrupt:
            vr("quit_twm", True)
    return -1


def appm() -> None:
    apps_lst = be.api.fs.listdir("/usr/share/applications")
    apps_k = ["Main menu"]
    for i in range(len(apps_lst)):
        apps_k.append(apps_lst[i][0])
    while True:
        sel = vr("dmenu")(
            "Apps",
            apps_k,
        )
        if sel in [-1, 0]:
            break
        else:
            pass  # not yet implemented
            # be.based.command.fpexec("/usr/share/applications/")


def hs() -> None:
    vr("lm")(True)
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
                "Quit",
                "Restart",
                "Shutdown",
            ],
        )
        if sel == -1:
            if not vr("quit_twm"):
                vr("lm")()
        elif sel == 0:
            vr("appm")()
        elif sel == 1:
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
            vr("quit_twm", True)
        elif sel == 7:
            sel = vr("dmenu")(
                "Reboot",
                [
                    "Reboot",
                    "Reboot safemode",
                    "Reboot to TinyUF2",
                    "Reboot to bootloader",
                ],
            )
            if sel == 0:
                vr("j").clear()
                vr("j").nwrite("Rebooting.. ")
                vr("refr")()
                be.based.run("reboot")
                vr("quit_twm", True)
            elif sel == 1:
                vr("j").clear()
                vr("j").nwrite("Rebooting to safemode.. ")
                vr("refr")()
                be.based.run("reboot safemode")
                vr("quit_twm", True)
            elif sel == 2:
                vr("j").clear()
                vr("j").nwrite("Rebooting to TinyUF2.. ")
                vr("refr")()
                be.based.run("reboot uf2")
                vr("quit_twm", True)
            elif sel == 3:
                vr("j").clear()
                vr("j").nwrite("Rebooting to bootloader.. ")
                vr("refr")()
                be.based.run("reboot bootloader")
                vr("quit_twm", True)
        elif sel == 8:
            vr("j").clear()
            vr("j").nwrite("Shutting down.. ")
            vr("refr")()
            be.based.run("shutdown")
            vr("j").nwrite("Bye!")
            vr("refr")()
        else:
            raise RuntimeError("Unknown value!")


def vmain() -> None:
    while not vr("quit_twm"):
        # vr("ring_alarm")()
        # vr("ring_timer")()
        vr("hs")()


vr("rk", rk)
vr("rt", rt)
vr("ra", ra)
vr("last_accel", ra())
vr("moved", moved)
vr("ctop", ctop)
vr("waitc", waitc)
vr("lc", lc)
vr("refr", refr)
vr("tix", 0)
vr("bati", bati)
vr("ring_alarm", ring_alarm)
vr("ring_timer", ring_timer)
vr("check_timers", check_timers)
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
    lc,
    refr,
    bati,
    ring_alarm,
    ring_timer,
    check_timers,
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

vrp("ok")
