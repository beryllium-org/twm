rename_process("twm")
vr("opts", be.api.xarg())
try:
    if be.api.console_connected() and "f" not in vr("opts")["o"]:
        if "s" in vr("opts")["o"]:
            raise KeyboardInterrupt
        term.write(
            "Another console is already connected!\nRerun with -f to run anyways, or disconnect to continue.\nCtrl + C to abort."
        )
        while be.api.console_connected():
            if term.is_interrupted():
                raise KeyboardInterrupt
            time.sleep(1)
    vr("ok", 0)
    be.api.subscript("/bin/twm/init.py")
    if vr("ok") == 1:
        vrd("ok")
        vr("crashes", 0)
        while vr("crashes") < 3:
            try:
                vr("main")()
                vr("b").charging_enabled = True
                vr("p")._aldo4_voltage_setpoint = 3300
                vr("player").deinit()
                if vr("lowpow"):
                    vr("resume")()
                break
            except Exception as err:
                vrp("crashes")
                term.write("TWM crashed. Crash log:")
                term.nwrite(str(format_exception(err)[0]))
                del err
                if vr("crashes") != 3:
                    term.write("Reloading TWM..")
                else:
                    term.write("Too many crashes, exiting TWM!")
    else:
        term.write("Failed to initialize TWM!")
    vr("c").disable()
    be.devices["DISPLAY"][0].auto_refresh = True
except KeyboardInterrupt:
    pass
