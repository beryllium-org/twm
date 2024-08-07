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
            if be.devices["network"][0].enabled:
                be.devices["network"][0].stop()
            else:
                be.devices["network"][0].start()
        elif sel == 2:
            be.based.run("reload")
        elif sel == 3:
            be.based.run("devmode -q")
        else:
            be.based.run("devmode -q -p")


vr("setm", setm)
del setm
vr("setm")()
vrd("setm")
