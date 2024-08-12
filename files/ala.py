def alam() -> None:
    last = 0
    enstate = False
    while True:
        sel = vr("dmenu")(
            "Alarm settings",
            [
                "Go back to Main Menu",
                "Set the time",
                "Enable" if not enstate else "Disable",
            ],
            preselect=last,
        )
        last = sel
        if sel < 1:
            break
        elif sel == 1:
            vr("j").clear()
            vr("j").nwrite("Configuring..")
            vr("refr")()
            vr("j").nwrite(" Done!")
            vr("refr")()
            time.sleep(0.4)
        elif sel == 2:
            enstate = not enstate


vr("alam", alam)
del alam
vr("alam")()
vrd("alam")
