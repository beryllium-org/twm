vr("dcharge", True)


def fc_main() -> None:
    while vr("dcharge"):
        if vr("b").status in ["charged", "charging"]:
            vr("ctop")("Disconnect the charger to continue.\nPress power to abort.")
            vr("refr")()
            while vr("b").status in ["charged", "charging"]:
                k = vr("rk")()
                if k[0]:
                    vr("dcharge", False)
                    break
                time.sleep(0.1)
        if not vr("dcharge"):
            break
        vr("ctop")("Full charge\n" + (vr("c").size[0] * "-") + "\n")
        vr("j").nwrite(
            "\nThis utillity will fully charge\nthe battery to exactly 4.20V.\n\nThis process takes hours.\nTo continue plug the charger.\nTo abort, press the power button."
        )
        vr("refr")()
        vr("waitc")()
        vr("b").charging_enabled = False
        vr("p")._write_register8(0x63, 0x10)
        vr("b").charging_enabled = True
        while vr("dcharge"):
            if vr("check_timers")():
                vr("treat_timers")()
            k = vr("rk")()
            t = vr("rt")()
            if k[0] or k[1]:
                vr("dcharge", False)
            elif vr("b").status in ["charged", "charging"]:
                fctm = time.monotonic()
                while vr("dcharge"):
                    vr("ctop")("Charging fully..\nDisconnect to stop.")
                    vr("refr")()
                    while vr("dcharge"):
                        if vr("check_timers")():
                            vr("treat_timers")()
                            break
                        if vr("b").status == "charged":
                            vr("dcharge", False)
                            vr("ctop", "Charging finished!")
                            vr("d").brightness = vr("mainbri")
                            vr("refr")()
                            time.sleep(3)
                            break
                        elif vr("b").status == "discharging":
                            vr("dcharge", False)
                            vr("d").brightness = vr("mainbri")
                            break
                        k = vr("rk")()
                        t = vr("rt")()
                        if k[0]:
                            vr("dcharge", False)
                        if t:
                            vr("d").brightness = vr("mainbri")
                            fctm = time.monotonic()
                        elif (
                            vr("d").brightness > vr("susbri")
                            and time.monotonic() - fctm > 5
                        ):
                            vr("d").brightness = vr("susbri")
                        else:
                            time.sleep(0.05)
            else:
                time.sleep(0.08)
        vr("b").charging_enabled = False
        vr("p")._write_register8(0x63, 0x11)
        vr("b").charging_enabled = True


vr("fc_main", fc_main)
del fc_main
vr("fc_main")()
vrd("fc_main")
vrd("dcharge")
