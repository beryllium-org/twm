vr("d", jcurses())
vr("c", pv[0]["consoles"]["ttyDISPLAY0"])
vr("d").console = vr("c")
vr("d").clear()
vr("p", be.devices["AXP2101"][0])
be.devices["DISPLAY"][0].auto_refresh = False

vr("d").trigger_dict = {
    "ctrlC": -1,
    "overflow": 8,
    "rest": "ignore",
    "rest_a": "common",
    "echo": "none",
    "prefix": "",
    "permit_pos": False,
    "idle": 9,
}
vr("c").enable()
vrp("ok")
