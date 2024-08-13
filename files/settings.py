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
                "Reload",
                "Enable devmode (once)",
                "Enable devmode (permenantly)",
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
                be.devices["network"][0].stop()
            else:
                be.devices["network"][0].start()
                vr("j").nwrite("Enabling Wi-Fi..")
                vr("refr")()
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
                    term.write("Could not write brightness value to storage!")
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
                    term.write("Could not write brightness value to storage!")
        elif sel == 4:
            be.based.run("reload")
            vr("quit_twm", True)
        elif sel == 5:
            vr("j").clear()
            vr("j").nwrite("Enabling.. ")
            vr("refr")()
            be.based.run("devmode -q")
            vr("quit_twm", True)
        else:
            vr("j").clear()
            vr("j").nwrite("Enabling (permenantly).. ")
            vr("refr")()
            be.based.run("devmode -q -p")
            vr("quit_twm", True)


vr("setm", setm)
del setm
vr("setm")()
vrd("setm")
