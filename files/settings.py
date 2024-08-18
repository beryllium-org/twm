def setm() -> None:
    last = 0
    while True:
        sel = vr("dmenu")(
            "Settings",
            [
                "Go back to Main Menu",
                "Wi-Fi [" + ("ON" if be.devices["network"][0].enabled else "OFF") + "]",
                "Brightness",
                "Idle brightness",
                "Vibration [" + ("ON" if vr("vibrate") else "OFF") + "]",
                "Sounds [" + ("ON" if vr("sounds") else "OFF") + "]",
                "Alarm sound",
                "Timer sound",
                "Notification sound",
                "Set the time",
                "Reload",
                "Enable devmode (once)",
                "Enable devmode (permenantly)",
                "About",
            ],
            preselect=last,
        )
        last = sel
        if sel < 1:
            break
        elif sel == 1:
            vr("j").clear()
            if be.devices["network"][0].enabled:
                vr("j").nwrite("Disabling Wi-Fi..")
                vr("refr")()
                be.based.run("rfkill block wlan")
            else:
                vr("j").nwrite("Enabling Wi-Fi..")
                vr("refr")()
                be.based.run("rfkill unblock wlan")
            vr("j").nwrite(" Done!")
            vr("refr")()
            time.sleep(0.4)
        elif sel == 2:
            plist = []
            for i in range(100):
                plist.append(str(i + 1) + "%")
            sel = vr("slidemenu")(
                "Brightness", plist, preselect=int(vr("mainbri") / 0.01) - 1
            )
            if sel != -1:
                newbri = (sel + 1) / 100
                vr("mainbri", newbri)
                vr("d").brightness = newbri
                try:
                    remount("/", False)
                    cptoml.put("brightness", sel + 1, subtable="TWM")
                    remount("/", True)
                except RuntimeError:
                    vr("vibr")(vr("err_seq"))
                    vr("j").clear()
                    vr("j").nwrite("Could not write to storage!")
                    vr("player").play(vr("s_no"))
                    vr("refr")()
                    time.sleep(3)
        elif sel == 3:
            plist = []
            start = 0.001
            stop = 0.021
            for i in [start + 0.001 * x for x in range(int((stop - start) / 0.001))]:
                plist.append(str(i))
            sel = vr("slidemenu")(
                "Brightness", plist, preselect=int(vr("susbri") / 0.001) - 1
            )
            if sel != -1:
                newbri = (sel + 1) * 0.001
                vr("susbri", newbri)
                try:
                    remount("/", False)
                    cptoml.put("suspend_brightness", sel, subtable="TWM")
                    remount("/", True)
                except RuntimeError:
                    vr("vibr")(vr("err_seq"))
                    vr("j").clear()
                    vr("j").nwrite("Could not write to storage!")
                    vr("player").play(vr("s_no"))
                    vr("refr")()
                    time.sleep(3)
        elif sel == 4:
            vr("vibrate", not vr("vibrate"))
            try:
                remount("/", False)
                cptoml.put("vibration", vr("vibrate"), subtable="TWM")
                remount("/", True)
            except RuntimeError:
                vr("vibr")(vr("err_seq"))
                vr("j").clear()
                vr("j").nwrite("Could not write to storage!")
                vr("player").play(vr("s_no"))
                vr("refr")()
                time.sleep(3)
        elif sel == 5:
            vr("sounds", not vr("sounds"))
            try:
                remount("/", False)
                cptoml.put("sounds", vr("sounds"), subtable="TWM")
                remount("/", True)
            except RuntimeError:
                vr("vibr")(vr("err_seq"))
                vr("j").clear()
                vr("j").nwrite("Could not write to storage!")
                vr("player").play(vr("s_no"))
                vr("refr")()
                time.sleep(3)
        elif sel == 6:
            fsel = vr("fselect")("/usr/share/sounds")
            if fsel is not None:
                vr("s_al", fsel)
                if fsel == "/usr/share/sounds/twm_alarm.wav":
                    fsel = False
                try:
                    remount("/", False)
                    cptoml.put("alarm_sound", vr("s_al"), subtable="TWM")
                    remount("/", True)
                except RuntimeError:
                    vr("vibr")(vr("err_seq"))
                    vr("j").clear()
                    vr("j").nwrite("Could not write to storage!")
                    vr("player").play(vr("s_no"))
                    vr("refr")()
                    time.sleep(3)
        elif sel == 7:
            fsel = vr("fselect")("/usr/share/sounds")
            if fsel is not None:
                vr("s_tm", fsel)
                if fsel == "/usr/share/sounds/twm_timer.wav":
                    fsel = False
                try:
                    remount("/", False)
                    cptoml.put("timer_sound", vr("s_tm"), subtable="TWM")
                    remount("/", True)
                except RuntimeError:
                    vr("vibr")(vr("err_seq"))
                    vr("j").clear()
                    vr("j").nwrite("Could not write to storage!")
                    vr("player").play(vr("s_no"))
                    vr("refr")()
                    time.sleep(3)
        elif sel == 8:
            fsel = vr("fselect")("/usr/share/sounds")
            if fsel is not None:
                vr("s_no", fsel)
                if fsel == "/usr/share/sounds/twm_notification.wav":
                    fsel = False
                try:
                    remount("/", False)
                    cptoml.put("notification_sound", vr("s_no"), subtable="TWM")
                    remount("/", True)
                except RuntimeError:
                    vr("vibr")(vr("err_seq"))
                    vr("j").clear()
                    vr("j").nwrite("Could not write to storage!")
                    vr("player").play(vr("s_no"))
                    vr("refr")()
                    time.sleep(3)
        elif sel == 9:
            vr("vibr")(vr("err_seq"))
            vr("j").clear()
            vr("j").nwrite("Not yet implemented!")
            vr("player").play(vr("s_no"))
            vr("refr")()
            time.sleep(1.8)
        elif sel == 10:
            be.based.run("reload")
            vr("quit_twm", True)
        elif sel == 11:
            vr("j").clear()
            vr("j").nwrite("Enabling.. ")
            vr("refr")()
            be.based.run("devmode -q")
            vr("quit_twm", True)
        elif sel == 12:
            vr("j").clear()
            vr("j").nwrite("Enabling (permenantly).. ")
            vr("refr")()
            be.based.run("devmode -q -p")
            vr("quit_twm", True)
        else:
            vr("j").clear()
            vr("j").write("Beryllium OS T-Watch Manager")
            vr("j").write("\nAuthor: Bill Sideris\n\n")
            ot = term.console
            term.console = vr("c")
            be.based.run("neofetch")
            term.console = ot
            del ot
            vr("refr")()
            k = vr("rk")()
            t = vr("rt")()
            while not (k[0] or k[1] or t):
                k = vr("rk")()
                t = vr("rt")()
                time.sleep(0.05)


vr("setm", setm)
del setm
vr("setm")()
vrd("setm")
