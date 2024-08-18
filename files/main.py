rename_process("twm")
vr("opts", be.api.xarg())
if (not be.api.console_connected()) or "f" in vr("opts")["o"]:
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
else:
    term.write("Another console is already connected, rerun with -f to run anyways.")
