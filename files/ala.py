def alam() -> None:
    last = 0
    while True:
        sel = vr("dmenu")(
            "Alarm settings",
            [
                "Go back to Main Menu",
                "Configure",
                (
                    "Enabled"
                    if (((not vr("model")) and vr("r").alarm_interrupt) or vr("alarm"))
                    else "Disabled"
                ),
            ],
            preselect=last,
        )
        last = sel
        if sel < 1:
            break
        elif sel == 1:
            hdict = []
            for i in range(0, 10):
                hdict.append("0" + str(i) + ":XX")
            for i in range(10, 24):
                hdict.append(str(i) + ":XX")
            hour = vr("slidemenu")(
                "Set the hour - XX:XX",
                hdict,
            )
            if hour != -1:
                mdict = []
                srh = ("0" + str(hour)) if hour < 10 else str(hour)
                for i in range(0, 10):
                    mdict.append(srh + ":0" + str(i))
                for i in range(10, 60):
                    mdict.append(srh + ":" + str(i))
                minute = vr("slidemenu")(
                    "Set the minute - "
                    + (("0" + str(hour)) if hour < 10 else str(hour))
                    + ":XX",
                    mdict,
                )
                if minute != -1:
                    if not vr("model"):
                        dlsta = ["Any"] + vr("days")
                        day = vr("dmenu")(
                            "Select the day - "
                            + (("0" + str(hour)) if hour < 10 else str(hour))
                            + ":"
                            + (("0" + str(minute)) if minute < 10 else str(minute)),
                            dlsta,
                        )
                        mode = "weekly"
                        if day != -1:
                            vr("ctop")("Calculating..")
                            vr("refr")()
                            if not day:
                                mode = "daily"
                            else:
                                day -= 1
                            ct = vr("r").datetime
                            target = time.mktime(
                                time.struct_time(
                                    (
                                        ct.tm_year,
                                        ct.tm_mon,
                                        ct.tm_mday,
                                        hour,
                                        minute,
                                        0,
                                        ct.tm_wday,
                                        ct.tm_yday,
                                        ct.tm_isdst,
                                    )
                                )
                            )
                            if target < time.time():
                                target += 86400
                            if mode == "daily":
                                while time.localtime(target).tm_wday != day:
                                    target += 86400
                            target = time.localtime(target)
                            vr("j").nwrite(" Done!\nConfiguring..")
                            vr("refr")()
                            vr("r").alarm = (target, mode)
                            vr("force_refr", True)
                            vr("j").write(" Done!")
                            vr("refr")()
                            if not vr("r").alarm_interrupt:
                                vr("j").nwrite("Enabling.. ")
                                vr("refr")()
                                vr("r").alarm_interrupt = True
                                vr("r").alarm_status = False
                                vr("j").nwrite("Done!")
                                vr("refr")()
                            time.sleep(0.4)
                    else:
                        vr("ctop")("Saving..")
                        vr(
                            "alarm",
                            ("0" if hour < 10 else "")
                            + str(hour)
                            + ("0" if minute < 10 else "")
                            + str(minute),
                        )
                        try:
                            remount("/", False)
                            cptoml.put("alarm", vr("alarm"), subtable="TWM")
                            remount("/", True)
                            vr("j").nwrite(" Done!")
                            time.sleep(0.4)
                        except RuntimeError:
                            vr("vibr")(vr("err_seq"))
                            vr("j").nwrite(" FAILED!")
                            vr("player").play(vr("s_no"))
                            vr("refr")()
                            time.sleep(3)

        elif sel == 2:
            if not vr("model"):
                vr("r").alarm_interrupt = not vr("r").alarm_interrupt
            else:
                if vr("alarm"):
                    vr("ctop")("Saving.. ")
                    vr("alarm", None)
                    vr("refr")()
                    try:
                        remount("/", False)
                        cptoml.put("alarm", "0", subtable="TWM")
                        remount("/", True)
                        vr("j").nwrite("Done!")
                        vr("refr")()
                        time.sleep(0.4)
                    except RuntimeError:
                        vr("vibr")(vr("err_seq"))
                        vr("j").nwrite(" FAILED!")
                        vr("player").play(vr("s_no"))
                        vr("refr")()
                        time.sleep(3)
                else:
                    vr("ctop")("No alarm set!")
                    vr("player").play(vr("s_no"))
                    vr("refr")()
                    time.sleep(3)


vr("alam", alam)
del alam
vr("alam")()
vrd("alam")
