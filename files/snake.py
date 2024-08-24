vr("snk_quit", False)

vr("j").write("Loading..")
vr("refr")()

vr("dbit").fill(36)  # W95-wallpaper-like lime green as our background

# Tiles:
# 0:  Background
# 1:  Snake head up
# 2:  Snake head left
# 3:  Snake head right
# 4:  Snake head down
# 5:  Snake body vertical
# 6:  Snake body horizontal
# 7:  Snake tail down
# 8:  Snake tail right
# 9:  Snake tail left
# 10: Snake tail up
# 11: Spike

# Snake head looking up, starting 16
for pv[get_pid()]["i"] in range(21, 27):
    vr("dbit")[vr("i"), 2] = 90

for pv[get_pid()]["i"] in range(20, 28):
    vr("dbit")[vr("i"), 3] = 90
    vr("dbit")[vr("i"), 4] = 90

for pv[get_pid()]["i"] in range(20, 28):
    vr("dbit")[vr("i"), 9] = 90

for pv[get_pid()]["i"] in range(19, 29):
    vr("dbit")[vr("i"), 7] = 90
    vr("dbit")[vr("i"), 8] = 90

for pv[get_pid()]["i"] in range(5, 7):
    vr("dbit")[19, vr("i")] = 90
    vr("dbit")[20, vr("i")] = 90
    vr("dbit")[21, vr("i")] = 38
    vr("dbit")[22, vr("i")] = 39
    vr("dbit")[23, vr("i")] = 90
    vr("dbit")[24, vr("i")] = 90
    vr("dbit")[25, vr("i")] = 39
    vr("dbit")[26, vr("i")] = 39
    vr("dbit")[27, vr("i")] = 90
    vr("dbit")[28, vr("i")] = 90

for pv[get_pid()]["i"] in range(10, 16):
    for pv[get_pid()]["z"] in range(21, 27):
        vr("dbit")[vr("z"), vr("i")] = 90


# Snake head looking left, starting 32
for pv[get_pid()]["i"] in range(36, 42):
    vr("dbit")[vr("i"), 3] = 90
    vr("dbit")[vr("i"), 12] = 90

for pv[get_pid()]["i"] in range(35, 43):
    vr("dbit")[vr("i"), 4] = 90
    vr("dbit")[vr("i"), 11] = 90

for pv[get_pid()]["i"] in [5, 6, 9, 10]:
    vr("dbit")[34, vr("i")] = 90
    vr("dbit")[35, vr("i")] = 90
    vr("dbit")[36, vr("i")] = 90
    vr("dbit")[37, vr("i")] = 39
    vr("dbit")[38, vr("i")] = 39
    for pv[get_pid()]["z"] in range(39, 48):
        vr("dbit")[vr("z"), vr("i")] = 90

for pv[get_pid()]["i"] in range(7, 9):
    for pv[get_pid()]["z"] in range(34, 48):
        vr("dbit")[vr("z"), vr("i")] = 90


# Snake head looking right, starting 48
for pv[get_pid()]["i"] in range(55, 60):
    vr("dbit")[vr("i"), 3] = 90
    vr("dbit")[vr("i"), 12] = 90

for pv[get_pid()]["i"] in range(54, 61):
    vr("dbit")[vr("i"), 4] = 90
    vr("dbit")[vr("i"), 11] = 90

for pv[get_pid()]["i"] in [5, 6, 9, 10]:
    for pv[get_pid()]["z"] in range(48, 57):
        vr("dbit")[vr("z"), vr("i")] = 90
    vr("dbit")[57, vr("i")] = 39
    vr("dbit")[58, vr("i")] = 39
    vr("dbit")[59, vr("i")] = 90
    vr("dbit")[60, vr("i")] = 90
    vr("dbit")[61, vr("i")] = 90

for pv[get_pid()]["i"] in range(7, 9):
    for pv[get_pid()]["z"] in range(48, 62):
        vr("dbit")[vr("z"), vr("i")] = 90


# Snake head looking down, starting 64
for pv[get_pid()]["i"] in range(14):
    for pv[get_pid()]["z"] in range(69, 75):
        vr("dbit")[vr("z"), vr("i")] = 90

for pv[get_pid()]["i"] in range(7, 12):
    vr("dbit")[67, vr("i")] = 90
    vr("dbit")[76, vr("i")] = 90

for pv[get_pid()]["i"] in range(6, 13):
    vr("dbit")[68, vr("i")] = 90
    vr("dbit")[75, vr("i")] = 90

vr("dbit")[69, 9] = 39
vr("dbit")[70, 9] = 39
vr("dbit")[69, 10] = 39
vr("dbit")[70, 10] = 39
vr("dbit")[73, 9] = 39
vr("dbit")[74, 9] = 39
vr("dbit")[73, 10] = 39
vr("dbit")[74, 10] = 39


# Snake body vertical, starting 80
for pv[get_pid()]["i"] in range(16):
    for pv[get_pid()]["z"] in range(85, 91):
        vr("dbit")[vr("z"), vr("i")] = 90

# Snake body horizontal, starting 96
for pv[get_pid()]["i"] in range(5, 11):
    for pv[get_pid()]["z"] in range(96, 112):
        vr("dbit")[vr("z"), vr("i")] = 90

# Snake tail down, starting 112
for pv[get_pid()]["i"] in range(14):
    for pv[get_pid()]["z"] in range(117, 123):
        vr("dbit")[vr("z"), vr("i")] = 90
for pv[get_pid()]["i"] in range(118, 122):
    vr("dbit")[vr("i"), 14] = 90


# Snake tail right, starting 128
for pv[get_pid()]["i"] in range(5, 11):
    for pv[get_pid()]["z"] in range(128, 141):
        vr("dbit")[vr("z"), vr("i")] = 90
for pv[get_pid()]["i"] in range(6, 10):
    vr("dbit")[141, vr("i")] = 90


# Snake tail left, starting 144
for pv[get_pid()]["i"] in range(6, 10):
    vr("dbit")[146, vr("i")] = 90

for pv[get_pid()]["i"] in range(5, 11):
    for pv[get_pid()]["z"] in range(147, 160):
        vr("dbit")[vr("z"), vr("i")] = 90


# Snake tail up, starting 160
for pv[get_pid()]["i"] in range(166, 170):
    vr("dbit")[vr("i"), 2] = 90

for pv[get_pid()]["i"] in range(3, 16):
    for pv[get_pid()]["z"] in range(165, 171):
        vr("dbit")[vr("z"), vr("i")] = 90


# Spike, starting 176
for pv[get_pid()]["i"] in [0, 1, 2, 3, 4, 5, 10, 11, 12, 13, 14, 15]:
    vr("dbit")[183, vr("i")] = 7
    vr("dbit")[184, vr("i")] = 7
for pv[get_pid()]["i"] in [176, 177, 178, 179, 180, 181, 186, 187, 188, 189, 190, 191]:
    vr("dbit")[vr("i"), 7] = 7
    vr("dbit")[vr("i"), 8] = 7
for pv[get_pid()]["i"] in range(3, 7):
    vr("dbit")[182, vr("i")] = 7
    vr("dbit")[185, vr("i")] = 7
    vr("dbit")[182, 7 + vr("i")] = 7
    vr("dbit")[185, 7 + vr("i")] = 7
for pv[get_pid()]["i"] in range(179, 183):
    vr("dbit")[vr("i"), 6] = 7
    vr("dbit")[vr("i"), 9] = 7
    vr("dbit")[vr("i") + 6, 6] = 7
    vr("dbit")[vr("i") + 6, 9] = 7
vr("dbit")[181, 4] = 7
vr("dbit")[180, 5] = 7
vr("dbit")[181, 5] = 7
vr("dbit")[180, 10] = 7
vr("dbit")[181, 10] = 7
vr("dbit")[181, 11] = 7
vr("dbit")[186, 4] = 7
vr("dbit")[186, 5] = 7
vr("dbit")[187, 5] = 7
vr("dbit")[186, 10] = 7
vr("dbit")[187, 10] = 7
vr("dbit")[186, 11] = 7


vrd("z")
vrd("i")


def snk_home() -> None:
    try:
        while not vr("snk_quit"):
            vr("ctop")("Snake\n" + (vr("c").size[0] * "-"))
            vr("j").move(y=vr("c").size[1] - 1, x=10)
            vr("j").write("Press power to exit")
            vr("j").nwrite((" " * 5) + "Touch anywhere to start")
            vr("refr")()
            vr("waitc")()
            while True:
                t = vr("rt")()
                k = vr("rk")()
                if t:
                    vr("snk_start")()
                    vr("snk_end")()
                    break
                elif k[0]:
                    vr("snk_quit", True)
                    break
                elif k[1]:
                    vr("snk_quit", True)
                    vr("quit_twm", True)
                    break
    except KeyboardInterrupt:
        vr("quit_twm", True)


vr("snk_home", snk_home)
del snk_home


def snk_start() -> None:
    vr("drawmode")(16, 16, 16, 16)
    vr("tg")[0, 0] = 1
    vr("tg")[0, 1] = 5
    vr("tg")[0, 2] = 7

    vr("tg")[1, 0] = 10
    vr("tg")[1, 1] = 5
    vr("tg")[1, 2] = 4

    vr("tg")[0, 3] = 2
    vr("tg")[1, 3] = 6
    vr("tg")[2, 3] = 8

    vr("tg")[0, 4] = 9
    vr("tg")[1, 4] = 6
    vr("tg")[2, 4] = 3

    vr("tg")[4, 0] = 11
    vr("tg")[4, 1] = 11
    vr("tg")[4, 2] = 11
    vr("tg")[4, 3] = 11
    vr("tg")[4, 4] = 11
    vr("tg")[4, 5] = 11
    vr("tg")[3, 5] = 11
    vr("tg")[2, 5] = 11
    vr("tg")[1, 5] = 11
    vr("tg")[0, 5] = 11

    vr("refr")()
    vr("waitc")()
    vr("wany")()


vr("snk_start", snk_start)
del snk_start


def snk_end() -> None:
    vr("textmode")()


vr("snk_end", snk_end)
del snk_end


vr("snk_home")()

vrd("snk_quit")
vrd("snk_home")
vrd("snk_start")
vrd("snk_end")
