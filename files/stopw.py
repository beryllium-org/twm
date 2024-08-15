def stopw() -> None:
    lt = time.monotonic()
    vr("waitc")()
    vr("ctop")("Stopwatch\n" + (vr("c").size[0] * "-"))
    vr("j").move(y=4)


vr("stopw", stopw)
del stopw
vr("stopw")()
vrd("stopw")
