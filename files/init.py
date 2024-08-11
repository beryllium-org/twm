vr("j", jcurses())
vr("c", pv[0]["consoles"]["ttyDISPLAY0"])
vr("j").console = vr("c")
vr("j").clear()
vr("p", be.devices["AXP2101"][0])
vr("t", be.devices["ftouch"][0])
vr("d", be.devices["DISPLAY"][0])
vr("b", be.devices["bat"][0])
vr("a", be.devices["BMA423"][0])
vr("d").auto_refresh = False
vr("quit_twm", False)
vr("last_shown", [0, 0, 0, 0, 0, 0])
vr("force_refr", False)
vr("cached_ip", "")
vr("chm", None)
vr("ind", False)
vr("batc", -70)
vr("lowpow", False)
vr("susbri", 0.004)


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
        vr("j").nwrite(vr("days")[wd] + " " + str(d) + "/" + str(o) + "/" + str(y))
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
    vr("p")._aldo4_voltage_setpoint = 0
    cpu.frequency = 80_000_000 if be.devices["network"][0].enabled else 40_000_000


def resume() -> None:
    cpu.frequency = 240_000_000
    vr("d").brightness = 1
    vr("p")._bldo2_voltage_setpoint = 3300
    vr("p")._aldo4_voltage_setpoint = 3300
    if not vr("p")._aldo2_voltage_setpoint:
        vr("p")._aldo2_voltage_setpoint = 3300
    vr("lowpow", False)
    vr("force_refr", True)
    vr("updi")(True)


def bati() -> None:
    if vr("b").charging_enabled:
        if vr("b").status == "charged":
            vr("b").charging_enabled = False
    else:
        if vr("b").percentage < 98:
            vr("b").charging_enabled = True


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


def lm(start_locked: bool = False) -> None:
    if start_locked:
        vr("d").brightness = 0
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
            if not vr("lowpow"):
                if vr("rt")():
                    lp = time.monotonic()
                    if vr("d").brightness < 1:
                        vr("d").brightness = 1
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
                    time.sleep(0.15)
                elif vr("moved")() or vr("rt")():
                    vr("d").brightness = vr("susbri")
                    if not vr("p")._aldo2_voltage_setpoint:
                        vr("p")._aldo2_voltage_setpoint = 3300
                    lm = time.monotonic()
                else:
                    time.sleep(0.3)
            vr("clocker")()
            vr("updi")()
            t = vr("rk")()
            if t[1] and not vr("lowpow"):
                vr("b").charging_enabled = True
                vr("quit_twm", True)
                return
            elif t[0] or start_locked:
                if vr("lowpow"):
                    vr("resume")()
                    if time.monotonic() - press < 1.1:
                        vr("b").charging_enabled = True
                        return
                    lp = time.monotonic()
                else:
                    start_locked = False
                    if time.monotonic() - press < 0.55:
                        vr("b").charging_enabled = True
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
        vr("b").charging_enabled = True
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
        retry = False
        vr("waitc")()
        vr("ctop")(title + "\n" + (vr("c").size[0] * "-"))
        sel = preselect
        scl = 0
        while sel - scl > vr("c").size[1] - 6:
            scl += 1
        vr("j").move(y=vr("c").size[1] - 2)
        sz = vr("c").size[0] // 4
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
        vr("j").move(y=vr("c").size[1] - 1, x=5)
        vr("j").nwrite("UP")
        vr("j").move(y=vr("c").size[1] - 1, x=13)
        vr("j").nwrite("DOWN")
        vr("j").move(y=vr("c").size[1] - 1, x=23)
        vr("j").nwrite("ABORT")
        vr("j").move(y=vr("c").size[1] - 1, x=34)
        vr("j").nwrite("OK")
        try:
            while not vr("quit_twm"):
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
                    for i in range(vr("c").size[1] - bigl):
                        vr("ditem")(data[i + scl], sel - scl == i)
                    vr("lc")()
                    vr("j").write(
                        "   [...]"
                        if (scl != len(data) - vr("c").size[1] + bigl)
                        else None
                    )
                vr("refr")()
                t = vr("rt")()
                k = vr("rk")()
                if k[1]:
                    vr("quit_twm", True)
                elif k[0]:
                    vr("lm")()
                    retry = True
                    break
                elif t and t[0]["y"] > 190:
                    if t[0]["x"] < 61:  # up
                        if sel:
                            sel -= 1
                            if scl and (sel - scl < 0):
                                scl -= 1
                    elif t[0]["x"] < 121:  # down
                        if sel < len(data) - 1:
                            sel += 1
                            if big and (sel - scl > vr("c").size[1] - bigl - 1):
                                scl += 1
                    elif t[0]["x"] < 181:  # cancel
                        break
                    else:  # confirm
                        return sel
                    time.sleep(0.05)
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
            vr("j").clear()
            vr("j").nwrite("Rebooting.. ")
            vr("refr")()
            be.based.run("reboot")
            vr("quit_twm", True)
        elif sel == 8:
            vr("j").clear()
            vr("j").nwrite("Shutting down.. ")
            vr("refr")()
            be.based.run("shutdown")
        else:
            raise RuntimeError("Unknown value!")


def vmain() -> None:
    while not vr("quit_twm"):
        vr("hs")()


vr("rk", rk)
del rk
vr("rt", rt)
del rt
vr("ra", ra)
vr("last_accel", ra())
del ra
vr("moved", moved)
del moved
vr("ctop", ctop)
del ctop
vr("waitc", waitc)
del waitc
vr("lc", lc)
del lc
vr("refr", refr)
del refr
vr("tix", 0)
vr("bati", bati)
del bati
vr("updi", updi)
del updi
vr("clocker", clocker)
del clocker
vr("suspend", suspend)
del suspend
vr("resume", resume)
del resume
vr("lm", lm)
del lm
vr("ditem", ditem)
del ditem
vr("dmenu", dmenu)
del dmenu
vr("appm", appm)
del appm
vr("quit_twm", False)
vr("hs", hs)
del hs
vr("main", vmain)
del vmain

vrp("ok")
