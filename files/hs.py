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
                    "   [...]" if (scl != len(data) - vr("c").size[1] + bigl) else None
                )
            vr("refr")()
            t = vr("rt")()
            k = vr("rk")()
            if k[1]:
                vr("quit_twm", True)
            if k[0] or k[1]:
                return -1
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
                    return -1
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
            break
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
        else:
            vr("j").clear()
            vr("j").nwrite("Shutting down.. ")
            vr("refr")()
            be.based.run("shutdown")


def vmain() -> None:
    while not vr("quit_twm"):
        if vr("lm")():
            vr("hs")()
        else:
            break


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
