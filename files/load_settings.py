def setm() -> None:
    while True:
        sel = vr("dmenu")(
            "Settings",
            [
                "Go back to Main Menu",
                "Reboot",
                "Reload",
                "Enable developer mode (once)",
                "Enable developer mode (permenantly)",
            ],
            hint="Press top left to close. Press Enter to select.",
        )
        if sel > 0:
            vr("quit_womp", True)
        if sel == 1:
            be.based.run("reboot")
        elif sel == 2:
            be.based.run("reload")
        elif sel == 3:
            be.based.run("devmode -q")
        else:
            be.based.run("devmode -q -p")
        break


vr("setm", setm)
del setm
