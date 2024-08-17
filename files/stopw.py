def split_time(val: int) -> tuple:
    days, remainder = divmod(val, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, remainder = divmod(remainder, 60)
    seconds = int(remainder)
    milliseconds = int((remainder - seconds) * 1000)
    days = int(days)
    hours = int(hours)
    minutes = int(minutes)
    return (days, hours, minutes, seconds, milliseconds)


def rendt(val: int, rend_ms: bool) -> None:
    days, hours, minutes, seconds, milliseconds = vr("split_time")(val)

    for i in range(3):
        vr("j").move(y=4 + i)
        vr("lc")()
        vr("j").nwrite(">" + " " * 2)
        if days:
            if days < 10:
                vr("j").nwrite(vr("bigs")[days][i])
            elif days < 99:
                dstr = str(days)
                ld = int(dstr[1])
                hd = int(dstr[0])
                vr("j").nwrite(vr("bigs")[hd][i] + vr("bigs")[ld][i])
            else:
                if days > 999:
                    days = 999
                dstr = str(days)
                ld = int(dstr[2])
                md = int(dstr[1])
                hd = int(dstr[0])
                vr("j").nwrite(
                    vr("bigs")[hd][i] + vr("bigs")[md][i] + vr("bigs")[ld][i]
                )
            vr("j").nwrite(vr("bigs")[12][i])
        if hours or days:
            if hours < 10:
                if days:
                    vr("j").nwrite(vr("bigs")[0][i])
                vr("j").nwrite(vr("bigs")[hours][i])
            else:
                hstr = str(hours)
                lh = int(hstr[1])
                hh = int(hstr[0])
                vr("j").nwrite(vr("bigs")[hh][i] + vr("bigs")[lh][i])
            vr("j").nwrite(vr("bigs")[12][i])
        if minutes or hours or days:
            if minutes < 10:
                if hours or days:
                    vr("j").nwrite(vr("bigs")[0][i])
                vr("j").nwrite(vr("bigs")[minutes][i])
            else:
                mstr = str(minutes)
                lm = int(mstr[1])
                hm = int(mstr[0])
                vr("j").nwrite(vr("bigs")[hm][i] + vr("bigs")[lm][i])
            vr("j").nwrite(vr("bigs")[12][i])
        if seconds < 10:
            if minutes or hours or days:
                vr("j").nwrite(vr("bigs")[0][i])
            vr("j").nwrite(vr("bigs")[seconds][i])
        else:
            sstr = str(seconds)
            ls = int(sstr[1])
            hs = int(sstr[0])
            vr("j").nwrite(vr("bigs")[hs][i] + vr("bigs")[ls][i])
        vr("j").nwrite(vr("bigs")[13][i])
        if rend_ms:
            msstr = str(milliseconds)
            mslen = len(msstr)
            msh = 0 if mslen != 3 else msstr[0]
            msh = int(msh)
            msm = 0
            if mslen > 1:
                msm = msstr[1] if msh else msstr[0]
            msm = int(msm)
            msl = int(msstr[-1:])
            vr("j").nwrite(vr("bigs")[msh][i])
            if days < 100:
                vr("j").nwrite(vr("bigs")[msm][i])
            if days < 10:
                vr("j").nwrite(vr("bigs")[msl][i])
        else:
            vr("j").nwrite(vr("bigs")[10][i])
            if days < 100:
                vr("j").nwrite(vr("bigs")[10][i])
            if days < 10:
                vr("j").nwrite(vr("bigs")[10][i])
        vr("refr")()


def stopw() -> None:
    rt = None
    st = 0
    retry = True
    lapc = 0
    laps = []
    while retry and not vr("quit_twm"):
        retry = False
        vr("j").clear()
        vr("j").nwrite("Loading..")
        vr("refr")()
        lt = time.monotonic()
        vr("waitc")()
        vr("ctop")("Stopwatch\n" + (vr("c").size[0] * "-"))
        ct = time.monotonic()
        lk = 0
        sh = -1
        vr("drawbox")()
        ysize = vr("c").size[1] - 1
        vr("j").move(y=ysize, x=5)
        vr("j").nwrite("LAP")
        vr("j").move(y=ysize, x=13)
        vr("j").nwrite("RESET")
        if not st == 2:
            vr("j").move(y=ysize, x=24)
            vr("j").nwrite("EXIT")
        vr("j").move(y=ysize, x=32)
        vr("j").nwrite("TOGGLE")
        vr("j").move(y=7)
        vr("j").nwrite(">")
        timeout = time.monotonic()
        try:
            while True:
                if vr("check_timers")():
                    retry = True
                    break
                t = vr("rt")()
                k = vr("rk")()
                lt = time.monotonic()
                dt = (lt - rt) if st == 2 else (rt if rt is not None else 0)
                if st == 2 or (st and vr("ldt") != dt):
                    vr("rendt")(dt, vr("d").brightness > 0.05)
                    if st != 2:
                        vr("ldt", dt)
                if st != 2:
                    if sh != st:
                        sh = st
                    if lt - ct > 1:
                        ct = time.monotonic()
                        st = int(not st)
                if t:
                    timeout = lt
                    if vr("d").brightness < vr("mainbri"):
                        vr("d").brightness = vr("mainbri")
                    elif t[0]["y"] > 190 and lt - lk > 0.3:
                        lk = lt
                        x = t[0]["x"]
                        if x < 61:  # lap
                            if st == 2:
                                vr("j").move(y=9)
                                lapc += 1
                                laps.append(dt)
                                for i in range(lapc, max(1, lapc - 4) - 1, -1):
                                    vr("lc")()
                                    vr("j").nwrite("Lap #" + str(i) + ": ")
                                    days, hours, minutes, seconds, milliseconds = vr(
                                        "split_time"
                                    )(laps[i - 1])
                                    if days:
                                        vr("j").nwrite(str(days) + ":")
                                    if hours or days:
                                        vr("j").nwrite(
                                            ("0" if (days and hours < 10) else "")
                                            + str(hours)
                                            + ":"
                                        )
                                    if minutes or hours or days:
                                        vr("j").nwrite(
                                            (
                                                "0"
                                                if ((days or hours) and minutes < 10)
                                                else ""
                                            )
                                            + str(minutes)
                                            + ":"
                                        )
                                    vr("j").nwrite(
                                        (
                                            "0"
                                            if (
                                                (days or hours or minutes)
                                                and seconds < 10
                                            )
                                            else ""
                                        )
                                        + str(seconds)
                                        + "."
                                    )
                                    vr("j").write(str(milliseconds))
                                vr("vibr")(vr("bop_seq"))
                        elif x < 121:  # reset
                            rt = lt if st == 2 else None
                            for i in range(9, 14):
                                vr("j").move(y=i)
                                vr("lc")()
                            laps = []
                            lapc = 0
                            vr("vibr")(vr("bop_seq"))
                        elif x < 181:  # exit
                            if st != 2:
                                vr("vibr")(vr("confirm_bop_seq"))
                                break
                        else:  # toggle
                            st = 2 if st != 2 else 0
                            if st == 2:
                                if rt is None:
                                    rt = lt
                                else:
                                    rt = lt - rt
                                vr("j").move(y=ysize, x=24)
                                vr("j").nwrite(" " * 4)
                            else:
                                rt = lt - rt
                                vr("j").move(y=ysize, x=24)
                                vr("j").nwrite("EXIT")
                            vr("vibr")(vr("bop_seq"))
                elif k[0]:
                    timeout = lt
                    if vr("d").brightness < vr("mainbri"):
                        vr("d").brightness = vr("mainbri")
                    st = 2 if st != 2 else 0
                    if st == 2:
                        if rt is None:
                            rt = lt
                        else:
                            rt = lt - rt
                        vr("j").move(y=ysize, x=24)
                        vr("j").nwrite(" " * 4)
                    else:
                        rt = lt - rt
                        vr("j").move(y=ysize, x=24)
                        vr("j").nwrite("EXIT")
                elif lt - timeout > 10:
                    if vr("d").brightness > 0.05:
                        vr("d").brightness -= 0.01
                        time.sleep(0.01)

        except KeyboardInterrupt:
            vr("quit_twm", True)


vr("split_time", split_time)
del split_time
vr("ldt", -1)
vr("rendt", rendt)
del rendt
vr("stopw", stopw)
del stopw
vr("stopw")()
vrd("stopw")
