vr("tix", 0)


def ticker() -> None:
    if not vr("tix"):
        vr("d").nwrite("[|||||||]")
    elif vr("tix") == 1:
        vr("d").nwrite("[ ||||| ]")
    elif vr("tix") == 2:
        vr("d").nwrite("[  |||  ]")
    elif vr("tix") == 3:
        vr("d").nwrite("[   |   ]")
    elif vr("tix") == 4:
        vr("d").nwrite("[  |||  ]")
    elif vr("tix") == 5:
        vr("d").nwrite("[ ||||| ]")
    vrp("tix")
    if vr("tix") == 6:
        vr("tix", 0)


vr("ticker", ticker)
del ticker


def drinfo() -> None:
    vr("d").move(x=23, y=6)
    vr("d").nwrite(str(len(pid_act)) + " Active processes   ")
    vr("d").move(x=23, y=7)
    vr("d").nwrite(str(len(be.scheduler)) + " Running in background   ")
    vr("d").move(x=23, y=8)
    gc.collect()
    gc.collect()
    gc.collect()
    vr("d").nwrite(str(gc.mem_free()) + " Bytes free     ")
    vr("d").move(x=37, y=9)
    vr("ticker")()
    vr("refr")()


vr("drinfo", drinfo)
del drinfo


def lm() -> bool:
    vr("d").clear()
    vr("ctop")(
        "T-Watch Manager (T. W. M.)"
        + " " * 8
        + "v1.0"
        + (vr("c").size[0] * "-")
    )
    vr("d").move(y=vr("c").size[1])
    vr("d").nwrite("Hold top left to quit. To unlock, hold enter.")
    vr("d").move(y=4)
    sps = " "
    vr("d").write(sps + ".------------.")
    vr("d").write(sps + "| 4   9.0122 |")
    vr("d").write(sps + "|    _  _    |")
    vr("d").write(sps + "|   |_)|_    |")
    vr("d").write(sps + "|   |_)|_    |")
    vr("d").write(sps + "|            |    System active")
    vr("d").write(sps + "| Beryllium  |")
    vr("d").write(sps + "'------------'")
    del sps
    time.sleep(1)
    be.io.ledset(1)
    last_r = 0
    try:
        while True:
            if float(time.monotonic() - last_r) > 0.4:
                vr("drinfo")()
                last_r = time.monotonic()
            vr("d").focus = 0
            vr("d").buf[1] = ""
            vr("d").buf[0] = 9
            gc.collect()
            vr("d").program_non_blocking()
            v = vr("d").buf[0]
            if v == -1:
                return False
            elif v in [4, 7]:
                be.io.ledset(3)
                ct = time.monotonic()
                good = True
                if v == 7:
                    vr("d").move(y=vr("c").size[1], x=35)
                    vr("d").nwrite("keep holding.")
                else:
                    vr("d").move(y=vr("c").size[1])
                    vr("d").nwrite(" Keep holding to quit.")
                vr("refr")()
                while time.monotonic() - ct < 0.5:
                    if not pv[0]["consoles"]["ttyDISPLAY0"].in_waiting:
                        good = False
                        be.io.ledset(1)
                        break
                if good:
                    vr("d").move(y=vr("c").size[1])
                    vr("lc")()
                    vr("d").nwrite("To continue, release.")
                    vr("refr")()
                    vr("waitc")()
                    return v == 7
                else:
                    vr("d").move(y=vr("c").size[1])
                    vr("d").nwrite("Hold top left to quit. To unlock, hold enter.  ")
                    vr("refr")()
            elif v == 9:
                be.api.tasks.run()
    except KeyboardInterrupt:
        return False


vr("lm", lm)
del lm
