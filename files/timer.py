vr(
    "hourg",
    [
        "+8-=-=-=-=-=-8+",
        " | ,.-'\"'-., |",
        " |/:::::::::\\|",
        " |\\:::::::::/|",
        " | \\:::::::/ |",
        " |  \\:::::/  |",
        " |   \\:::/   |",
        " |    ):(    |",
        " |   /   \\   |",
        " |  /     \\  |",
        " | /       \\ |",
        " |/         \\|",
        " |\\         /|",
        " | '--___--' |",
        "+8-=-=-=-=-=-8+",
    ],
)


def remt() -> None:
    if vr("timer_rem") is not None:
        if vr("timer") is not None:
            rem = int(vr("timer") - time.monotonic())
        else:
            rem = vr("timer_rem")
        if vr("sht") != rem:
            vr("j").move(y=8, x=20)
            vr("j").nwrite("Remaining time:")
            vr("j").move(y=9, x=20)
            vr("j").nwrite(" " * 15)
            vr("j").move(y=9, x=20)
            hours, minutes = divmod(rem, 3600)
            minutes /= 60
            hours = int(hours)
            minutes = int(minutes)
            if hours or (minutes > 10):
                vr("j").nwrite(
                    (str(hours) if hours > 9 else ("0" + str(hours)))
                    + ":"
                    + (str(minutes) if minutes > 9 else ("0" + str(minutes)))
                )
            else:
                vr("j").nwrite(str(rem) + " seconds")
            vr("sht", rem)
    elif vr("sht") is not None:
        vr("j").move(y=8, x=20)
        vr("j").nwrite(" " * 15)
        vr("j").move(y=9, x=20)
        vr("j").nwrite(" " * 15)
        vr("sht", None)


def ftimer() -> None:
    retry = True
    htick = -1
    slist = []
    vr("j").clear()
    vr("j").nwrite("Loading..")
    vr("refr")()
    for i in range(59):
        slist.append(str(i + 1) + " minutes")
    for i in range(23):
        slist.append(str(i + 1) + " hours")
        for j in range(59):
            slist.append(str(i + 1) + " hours " + str(j + 1) + " minutes")
    try:
        while retry and not vr("quit_twm"):
            retry = False
            htick = -1
            vr("waitc")()
            vr("j").clear()
            vr("j").move(y=1, x=18)
            vr("j").nwrite("| Timer")
            vr("j").move(y=2, x=18)
            vr("j").nwrite("'" + ("-" * (vr("c").size[0] - 18)))
            sz = vr("c").size[0] // 4
            ysize = vr("c").size[1]
            vr("j").move(y=ysize - 2)
            vr("j").nwrite(
                " /"
                + "-" * (sz - 2)
                + "-"
                + ("-" * (sz) + "v") * 2
                + "-" * (sz - 1)
                + "."
                + "/"
                + " " * sz
                + (sz * " " + "|") * 2
                + (sz - 1) * " "
                + "/"
                + "'"
                + "-" * sz
                + ("-" * (sz) + "^") * 2
                + "-" * (sz - 2)
                + "/"
            )
            vr("j").move(y=ysize - 1, x=7)
            vr("j").nwrite("CONFIGURE")
            vr("j").move(y=ysize - 1, x=24)
            vr("j").nwrite("EXIT")
            vr("j").move(y=ysize - 1, x=32)
            vr("j").nwrite("TOGGLE")
            need_refr = True
            lk = time.monotonic()
            ht = -1
            vr("remt")()
            while not vr("quit_twm"):
                if vr("check_timers")():
                    retry = True
                    break
                lt = time.monotonic()
                vr("remt")()
                if vr("timer") is None:
                    if htick != 0:
                        htick = 0
                        for i in range(len(vr("hourg"))):
                            vr("j").move(y=i + 1)
                            vr("j").nwrite(vr("hourg")[i])
                        need_refr = True
                else:
                    if lt - ht > 0.45:
                        ht = lt
                        htick += 1
                        if htick == 1:
                            vr("j").move(y=3, x=7)
                            vr("j").nwrite("." * 3)
                            for i in range(4):
                                vr("j").move(y=9 + i, x=8)
                                vr("j").nwrite(".")
                            vr("j").move(y=13, x=7)
                            vr("j").nwrite("." * 3)
                        elif htick == 2:
                            vr("j").move(y=3, x=6)
                            vr("j").nwrite("." * 5)
                            vr("j").move(y=13, x=6)
                            vr("j").nwrite("." * 5)
                        elif htick == 3:
                            vr("j").move(y=3, x=4)
                            vr("j").nwrite("." * 9)
                            vr("j").move(y=13, x=4)
                            vr("j").nwrite("." * 9)
                        elif htick == 4:
                            vr("j").move(y=3, x=7)
                            vr("j").nwrite(" " * 3)
                            vr("j").move(y=13, x=6)
                            vr("j").nwrite(":" * 3)
                        elif htick == 5:
                            vr("j").move(y=3, x=5)
                            vr("j").nwrite(" " * 6)
                            vr("j").move(y=13, x=5)
                            vr("j").nwrite(":" * 5)
                        elif htick == 6:
                            vr("j").move(y=3, x=4)
                            vr("j").nwrite(" " * 9)
                            vr("j").move(y=13, x=4)
                            vr("j").nwrite(":" * 9)
                            vr("j").move(y=4, x=7)
                            vr("j").nwrite("." * 3)
                            vr("j").move(y=12, x=7)
                            vr("j").nwrite("." * 3)
                        elif htick == 7:
                            vr("j").move(y=4, x=5)
                            vr("j").nwrite("." * 6)
                            vr("j").move(y=12, x=4)
                            vr("j").nwrite("....:....")
                        elif htick == 8:
                            vr("j").move(y=4, x=4)
                            vr("j").nwrite(" " * 9)
                            vr("j").move(y=12, x=4)
                            vr("j").nwrite(":" * 9)
                        elif htick == 9:
                            vr("j").move(y=5, x=7)
                            vr("j").nwrite("..")
                            vr("j").move(y=11, x=8)
                            vr("j").nwrite(":.")
                        elif htick == 10:
                            vr("j").move(y=5, x=5)
                            vr("j").nwrite("... ...")
                            vr("j").move(y=11, x=7)
                            vr("j").nwrite(":" * 4)
                        elif htick == 11:
                            vr("j").move(y=5, x=5)
                            vr("j").nwrite(" " * 7)
                            vr("j").move(y=11, x=5)
                            vr("j").nwrite(":" * 7)
                        elif htick == 12:
                            vr("j").move(y=6, x=8)
                            vr("j").nwrite("..")
                            vr("j").move(y=10, x=7)
                            vr("j").nwrite(".:.")
                        elif htick == 13:
                            vr("j").move(y=6, x=6)
                            vr("j").nwrite("..:. ")
                            vr("j").move(y=10, x=6)
                            vr("j").nwrite(".:::.")
                        elif htick == 14:
                            vr("j").move(y=6, x=6)
                            vr("j").nwrite("  ..")
                            vr("j").move(y=10, x=6)
                            vr("j").nwrite("::::.")
                        elif htick == 15:
                            vr("j").move(y=6, x=8)
                            vr("j").nwrite("  ")
                            vr("j").move(y=7, x=8)
                            vr("j").nwrite(".")
                            vr("j").move(y=10, x=10)
                            vr("j").nwrite(":")
                            vr("j").move(y=9, x=7)
                            vr("j").nwrite(".")
                        elif htick == 16:
                            vr("j").move(y=7, x=7)
                            vr("j").nwrite("   ")
                            vr("j").move(y=9, x=7)
                            vr("j").nwrite(":::")
                            vr("j").move(y=8, x=8)
                            vr("j").nwrite(" ")
                        else:
                            htick = 0
                            for i in range(len(vr("hourg"))):
                                vr("j").move(y=i + 1)
                                vr("j").nwrite(vr("hourg")[i])
                        need_refr = True
                if need_refr or vr("timer") is not None:
                    vr("refr")()
                    need_refr = False
                t = vr("rt")()
                k = vr("rk")()
                if t:
                    if t[0]["y"] > 190 and lt - lk > 0.3:
                        x = t[0]["x"]
                        lk = lt
                        if x < 121:  # conigure
                            sel = vr("slidemenu")(
                                "Configure timer",
                                slist,
                            )
                            if sel != -1:
                                vr("timer_rem", (sel + 1) * 60)
                            else:
                                vr("timer_rem", None)
                            retry = True
                            break
                        elif x < 181:  # exit
                            return
                        else:  # toggle
                            if vr("timer_rem") is not None:
                                if vr("timer") is None:
                                    vr("timer", lt + vr("timer_rem"))
                                else:
                                    vr("timer", None)
                            else:
                                vr("j").clear()
                                vr("j").nwrite("No timer configured!")
                                vr("refr")()
                                time.sleep(3)
                                retry = True
                                break
                if k[0]:
                    vr("lm")(True)
                    retry = True
                    break
    except KeyboardInterrupt:
        vr("quit_twm", True)


vr("sht", None)
vr("remt", remt)
del remt
vr("ftimer", ftimer)
del ftimer
vr("ftimer")()
vrd("ftimer")
