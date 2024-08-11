def setm() -> None:
    last = 0
    while True:
        sel = vr("dmenu")(
            "Settings",
            [
                "Go back to Main Menu",
                "Wi-Fi [" + ("ON" if be.devices["network"][0].enabled else "OFF") + "]",
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
            be.based.run("reload")
            vr("quit_twm", True)
        elif sel == 3:
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
