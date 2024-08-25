vr("snk_quit", False)
vr("dbit").fill(36)  # W95-wallpaper-like lime green as our background

# Tiles (good luck debugging):
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
# 12: Black
# 13: Snake body q2
# 14: Snake body q3
# 15: Snake body q4
# 16: Snake body q1
# 17: Apple
# 18: Heart

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


# Black, starting 192
for pv[get_pid()]["i"] in range(192, 208):
    for pv[get_pid()]["z"] in range(16):
        vr("dbit")[vr("i"), vr("z")] = 0


# Snake body q2, starting 208
for pv[get_pid()]["i"] in range(208, 213):
    for pv[get_pid()]["z"] in range(5, 11):
        vr("dbit")[vr("i"), vr("z")] = 90

for pv[get_pid()]["i"] in range(213, 219):
    for pv[get_pid()]["z"] in range(11):
        vr("dbit")[vr("i"), vr("z")] = 90

vr("dbit")[218, 9] = 36
vr("dbit")[217, 10] = 36
vr("dbit")[218, 10] = 36


# Snake body q3, starting 224
for pv[get_pid()]["i"] in range(224, 229):
    for pv[get_pid()]["z"] in range(5, 11):
        vr("dbit")[vr("i"), vr("z")] = 90

for pv[get_pid()]["i"] in range(229, 235):
    for pv[get_pid()]["z"] in range(5, 16):
        vr("dbit")[vr("i"), vr("z")] = 90

vr("dbit")[233, 5] = 36
vr("dbit")[234, 5] = 36
vr("dbit")[234, 6] = 36


# Snake body q4, starting 0, 16
for pv[get_pid()]["i"] in range(5, 11):
    for pv[get_pid()]["z"] in range(21, 32):
        vr("dbit")[vr("i"), vr("z")] = 90

for pv[get_pid()]["i"] in range(11, 16):
    for pv[get_pid()]["z"] in range(21, 27):
        vr("dbit")[vr("i"), vr("z")] = 90

vr("dbit")[5, 21] = 36
vr("dbit")[6, 21] = 36
vr("dbit")[5, 22] = 36

# Snake body q1, starting 16, 16
for pv[get_pid()]["i"] in range(27, 32):
    for pv[get_pid()]["z"] in range(21, 27):
        vr("dbit")[vr("i"), vr("z")] = 90

for pv[get_pid()]["i"] in range(21, 27):
    for pv[get_pid()]["z"] in range(16, 27):
        vr("dbit")[vr("i"), vr("z")] = 90

vr("dbit")[21, 25] = 36
vr("dbit")[21, 26] = 36
vr("dbit")[22, 26] = 36

# Apple, starting 32, 16
vr("dbit")[41, 17] = 10
vr("dbit")[42, 17] = 10
vr("dbit")[40, 18] = 10
vr("dbit")[41, 18] = 10
vr("dbit")[39, 19] = 10
vr("dbit")[40, 19] = 10
for pv[get_pid()]["i"] in range(20, 28):
    for pv[get_pid()]["z"] in range(34, 46):
        vr("dbit")[vr("z"), vr("i")] = 1

vr("dbit")[34, 20] = 36
vr("dbit")[34, 27] = 36
vr("dbit")[45, 20] = 36
vr("dbit")[45, 27] = 36

# Heart, starting 48, 16
vr("dbit")[52, 20] = 28
vr("dbit")[53, 20] = 28
vr("dbit")[54, 20] = 28
vr("dbit")[57, 20] = 28
vr("dbit")[58, 20] = 28
vr("dbit")[59, 20] = 28
for pv[get_pid()]["i"] in range(51, 61):
    for pv[get_pid()]["z"] in range(21, 24):
        vr("dbit")[vr("i"), vr("z")] = 28

for pv[get_pid()]["i"] in range(52, 60):
    vr("dbit")[vr("i"), 24] = 28

for pv[get_pid()]["i"] in range(53, 59):
    vr("dbit")[vr("i"), 25] = 28

for pv[get_pid()]["i"] in range(54, 58):
    vr("dbit")[vr("i"), 26] = 28

vr("dbit")[55, 27] = 28
vr("dbit")[56, 27] = 28

vrd("i")
vrd("z")


def decode_chain(chain: str):
    # Split the string by "|" and convert each part to an integer
    try:
        integers = [int(num) for num in chain.split("|")]
        return [integers[i : i + 3] for i in range(0, len(integers), 3)]
    except:
        return None


vr("decode_chain", decode_chain)
del decode_chain


def decode_apples(apples: str):
    try:
        integers = [int(num) for num in apples.split("|")]
        return [integers[i : i + 2] for i in range(0, len(integers), 2)]
    except:
        return None


vr("decode_apples", decode_apples)
del decode_apples


# TTY menu screen
def snk_home() -> None:
    loaded = False

    loaded_hearts = cptoml.fetch("hearts", "SNAKE")
    if loaded_hearts is not None and loaded_hearts > 0:
        loaded_score = cptoml.fetch("score", "SNAKE")
        if loaded_score is not None and loaded_score > -1:
            loaded_level = cptoml.fetch("level", "SNAKE")
            if loaded_level is not None and loaded_level > 0:
                loaded_apple_power = cptoml.fetch("apple_power", "SNAKE")
                if loaded_apple_power is not None and loaded_apple_power > -1:
                    loaded_next_move = cptoml.fetch("next_move", "SNAKE")
                    if (
                        loaded_next_move is not None
                        and loaded_next_move > -1
                        and loaded_next_move < 5
                    ):
                        loaded_prev_move = cptoml.fetch("prev_move", "SNAKE")
                        if (
                            loaded_prev_move is not None
                            and loaded_prev_move > -1
                            and loaded_prev_move < 5
                        ):
                            loaded_chain = cptoml.fetch("chain", "SNAKE")
                            if loaded_chain is not None:
                                vr("chain", vr("decode_chain")(loaded_chain))
                                if vr("chain") is not None:
                                    loaded_apples = cptoml.fetch("apples", "SNAKE")
                                    if loaded_apples is not None:
                                        loaded = True
                                        vr("prev_move", loaded_prev_move)
                                        vr("next_move", loaded_next_move)
                                        vr("apple_power", loaded_apple_power)
                                        vr("level", loaded_level)
                                        vr("score", loaded_score)
                                        vr("hearts", loaded_hearts)
                                        vr("apples", vr("decode_apples")(loaded_apples))
                                        if vr("apples") is None:
                                            vr("apples", [])

    if not loaded:
        # New game
        vr("score", 0)
        vr("level", 1)
        vr("hearts", 3)
        vr("apple_power", 0)
        vr("next_move", 0)
        vr("prev_move", 0)
        vr("chain", [[5, 5, 2], [6, 5, 6], [7, 5, 8]])
        vr("apples", [])

    try:
        while not vr("snk_quit"):
            vr("ctop")("Snake\n" + (vr("c").size[0] * "-"))
            vr("j").move(y=vr("c").size[1] - 1, x=(vr("c").size[0] // 2) - 9)
            vr("j").write("Press power to exit")
            vr("j").nwrite((" " * 7) + "Touch anywhere to start")
            vr("j").move(y=3, x=(vr("c").size[0] // 2) - 5)
            vr("j").nwrite("Highscores")
            hscr = vr("hscore")()
            vr("j").move(y=4, x=(vr("c").size[0] // 2) - 5)
            vr("j").nwrite("1. " + (str(hscr[0]) if hscr[0] else ""))
            vr("j").move(y=5, x=(vr("c").size[0] // 2) - 5)
            vr("j").nwrite("2. " + (str(hscr[1]) if hscr[1] else ""))
            vr("j").move(y=6, x=(vr("c").size[0] // 2) - 5)
            vr("j").nwrite("3. " + (str(hscr[2]) if hscr[2] else ""))
            vr("j").move(y=7, x=(vr("c").size[0] // 2) - 5)
            vr("j").nwrite("4. " + (str(hscr[3]) if hscr[3] else ""))
            vr("j").move(y=8, x=(vr("c").size[0] // 2) - 5)
            vr("j").nwrite("5. " + (str(hscr[4]) if hscr[4] else ""))
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
        vr("textmode")()
        vr("quit_twm", True)


vr("snk_home", snk_home)
del snk_home


def encode_snake(snake: list) -> None:
    vr("chain", [])
    for i in range(len(snake)):
        vra("chain", [snake[i][0], snake[i][1], vr("tg")[snake[i][0], snake[i][1]]])


vr("encode_snake", encode_snake)
del encode_snake


def stringify_chain(chain: list) -> str:
    res = ""
    for i in range(len(chain)):
        res += str(chain[i][0]) + "|" + str(chain[i][1]) + "|" + str(chain[i][2]) + "|"
    return res[:-1]


vr("stringify_chain", stringify_chain)
del stringify_chain


def stringify_apples(apples: list) -> str:
    res = ""
    for i in range(len(apples)):
        res += str(apples[i][0]) + "|" + str(apples[i][1]) + "|"
    return res[:-1]


vr("stringify_apples", stringify_apples)
del stringify_apples


from os import urandom

vr("urandom", urandom)
del urandom


def get_rand_empty() -> list:
    while True:
        # Generate a random value for index 0 (0-14)
        x = int.from_bytes(vr("urandom")(1), "little") % 15

        # Generate a random value for index 1 (2-14)
        y = (int.from_bytes(vr("urandom")(1), "little") % 13) + 2

        if vr("tg")[x, y] == 0:
            return [x, y]


vr("get_rand_empty", get_rand_empty)
del get_rand_empty


def spawn(item: bool) -> list:
    # False apple
    # True heart
    randm = vr("get_rand_empty")()
    vr("tg")[randm[0], randm[1]] = 18 if item else 17
    return randm


vr("spawn", spawn)
del spawn


def hscore(nscore: int = None) -> None:
    hstr = cptoml.fetch("hscores", "SNAKE")
    if hstr is None:
        hstr = ""
    intr = []
    try:
        intr = [int(num) for num in hstr.split("|")]
    except:
        pass
    h = [0] * 5
    try:
        for i in range(5):
            h[i] = intr[i]
    except IndexError:
        pass
    if nscore is None:
        return h
    h.append(nscore)
    h.sort()
    h.reverse()
    hstr = ""
    for i in range(5):
        hstr += str(h[i]) + "|"
    print(hstr)
    try:
        remount("/", False)
        cptoml.put("hscores", hstr, "SNAKE")
        remount("/", True)
    except RuntimeError:
        pass


vr("hscore", hscore)
del hscore


def snk_start() -> list:
    # Initial / Loaded snake array
    snake = []
    apples = vr("apples")
    hearts_dropped = []
    next_move = vr("next_move")  # 0 left, 1 right, 2 up, 3 down
    prev_move = vr("prev_move")
    apple_power = vr("apple_power")
    hearts = vr("hearts")
    score = vr("score")
    level = vr("level")

    vr("waitc")()
    vr("ctop")(
        "Score: "
        + (" " * (5 - len(str(score))))
        + str(score)
        + " |\nLevel: "
        + (" " * (5 - len(str(level))))
        + str(level)
        + " | HP: "
        + str(hearts)
        + " |"
    )
    # We will now switch to dual graphics / tty mode only using the first
    # two lines of tty for scorekeeping stuff
    vr("dualmode")(16, 16, 16, 16)
    # Reset all tgs
    for i in range(16):
        vr("tg")[i, 0] = 12
        vr("tg")[i, 1] = 12
    for i in range(2, 16):
        for z in range(15):
            vr("tg")[z, i] = 0

    # Load active snake chain
    for i in range(len(vr("chain"))):
        snake.append([vr("chain")[i][0], vr("chain")[i][1]])
        vr("tg")[snake[i][0], snake[i][1]] = vr("chain")[i][2]

    # Spawn apples as needed
    while len(vr("apples")) < min(25 - score % 25, 3):
        vra("apples", vr("spawn")(False))

    # Redraw all apples
    for i in range(len(apples)):
        vr("tg")[apples[i][0], apples[i][1]] = 17

    direct = next_move in [2, 3]  # False up/down, True left right
    vr("refr")()
    game_ok = True
    pause = False
    while game_ok:
        while pause:
            k = vr("rk")()
            if k[0]:
                pause = False
                vr("j").move(y=1, x=16)
                vr("j").nwrite(" " * 12)
                vr("j").move(y=2, x=24)
                vr("j").nwrite(" " * 6)
                vr("refr")()
            elif k[1]:
                game_ok = False
                vr("hearts", hearts)
                vr("apple_power", apple_power)
                vr("apples", apples)
                vr("encode_snake")(snake)
                vr("next_move", next_move)
                vr("prev_move", prev_move)
                vr("score", score)
                vr("level", level)
                break
        tickt = time.monotonic() + 1 - ((level - 1) * 0.005)  # Time till next move
        dswap = True  # Swapped directions register
        while game_ok:
            t = vr("rt")()
            k = vr("rk")()
            if t:
                if dswap:
                    direct = not direct
                    dswap = False  # Only allow swapping directions once
                if direct:
                    next_move = 2 if t[0]["y"] < 130 else 3
                    # Do consider the top of the screen is black
                    # The user will be clicking a bit off center
                else:
                    next_move = 0 if t[0]["x"] < 120 else 1
            elif k[0]:
                pause = True
                vr("j").move(y=1, x=16)
                vr("j").nwrite("Hold to quit")
                vr("j").move(y=2, x=24)
                vr("j").nwrite("PAUSED")
                vr("refr")()
                break
            elif k[1]:
                game_ok = False
                vr("snk_quit", True)
                vr("hearts", hearts)
                vr("apple_power", apple_power)
                vr("apples", apples)
                vr("encode_snake")(snake)
                vr("next_move", next_move)
                vr("prev_move", prev_move)
                vr("score", score)
                vr("level", level)
                break
            if time.monotonic() >= tickt:
                # Tail
                if apple_power:
                    apple_power -= 1
                else:
                    vr("tg")[snake[-1][0], snake[-1][1]] = 0  # Clear the tile we left
                    snake.pop()  # Remove tile from snake

                    # Update the tail's tile based on the direction of the snake,
                    # considering wrapping
                    tail_x, tail_y = snake[-1]  # Current tail position
                    prev_x, prev_y = snake[
                        -2
                    ]  # Position of the segment before the tail

                    # Adjust the positions to account for wrapping around the grid
                    if tail_x == 0 and prev_x == 14:
                        prev_x = -1
                    elif tail_x == 14 and prev_x == 0:
                        prev_x = 15
                    if tail_y == 2 and prev_y == 14:
                        prev_y = 1
                    elif tail_y == 14 and prev_y == 2:
                        prev_y = 15

                    # Determine the new tail tile based on adjusted positions
                    if vr("tg")[tail_x, tail_y] == 5:  # Snake body vertical
                        nt = 10 if prev_y > tail_y else 7  # Tail up or down
                    elif vr("tg")[tail_x, tail_y] == 6:  # Snake body horizontal
                        nt = 9 if prev_x > tail_x else 8  # Tail right or left
                    elif vr("tg")[tail_x, tail_y] == 16:  # q1
                        nt = 7 if prev_y < tail_y else 9  # Tail down or left
                    elif vr("tg")[tail_x, tail_y] == 15:  # q4
                        nt = 9 if prev_x > tail_x else 10  # Tail left or up
                    elif vr("tg")[tail_x, tail_y] == 14:  # q3
                        nt = 10 if prev_y > tail_y else 8  # Tail up or right
                    else:  # q2
                        nt = 8 if prev_x < tail_x else 7  # Tail right or down

                    # Update tail tile
                    vr("tg")[tail_x, tail_y] = nt

                # Head
                next_box = snake[0].copy()
                if not next_move:  # Going left
                    next_box[0] -= 1
                    if next_box[0] < 0:
                        next_box[0] = 14
                    if vr("tg")[next_box[0], next_box[1]] == 18:
                        vrp("hearts")
                    vr("tg")[next_box[0], next_box[1]] = 2
                    if dswap:
                        vr("tg")[snake[0][0], snake[0][1]] = 6
                    else:
                        vr("tg")[snake[0][0], snake[0][1]] = (
                            14 if prev_move == 2 else 13
                        )
                elif next_move == 1:  # Going right
                    next_box[0] += 1
                    if next_box[0] > 14:
                        next_box[0] = 0
                    if vr("tg")[next_box[0], next_box[1]] == 18:
                        vrp("hearts")
                    vr("tg")[next_box[0], next_box[1]] = 3
                    if dswap:
                        vr("tg")[snake[0][0], snake[0][1]] = 6
                    else:
                        vr("tg")[snake[0][0], snake[0][1]] = (
                            15 if prev_move == 2 else 16
                        )
                elif next_move == 2:  # Going up
                    next_box[1] -= 1
                    if next_box[1] < 2:
                        next_box[1] = 14
                    if vr("tg")[next_box[0], next_box[1]] == 18:
                        vrp("hearts")
                    vr("tg")[next_box[0], next_box[1]] = 1
                    if dswap:
                        vr("tg")[snake[0][0], snake[0][1]] = 5
                    else:
                        vr("tg")[snake[0][0], snake[0][1]] = 16 if not prev_move else 13
                else:  # Going down
                    next_box[1] += 1
                    if next_box[1] > 14:
                        next_box[1] = 2
                    if vr("tg")[next_box[0], next_box[1]] == 18:
                        vrp("hearts")
                    vr("tg")[next_box[0], next_box[1]] = 4
                    if dswap:
                        vr("tg")[snake[0][0], snake[0][1]] = 5
                    else:
                        vr("tg")[snake[0][0], snake[0][1]] = 15 if not prev_move else 14

                snake.insert(0, next_box.copy())  # Add the new head
                prev_move = next_move  # Record directions

                # Check collision
                if snake[0] in snake[1:] or vr("tg")[snake[0][0], snake[0][1]] == 11:
                    # Game over
                    game_ok = False
                    hearts -= 1
                    vr("hearts", hearts)
                    # Default snake
                    if hearts:
                        vr("apple_power", 0)
                        vr("chain", [[5, 5, 2], [6, 5, 6], [7, 5, 8]])
                        vr("next_move", 0)
                        vr("prev_move", 0)
                    break
                elif snake[0] in apples:
                    apples.remove(snake[0])
                    apple_power += 3
                    score += 1
                    vr("j").move(y=1, x=8)
                    vr("j").nwrite((" " * (5 - len(str(score)))) + str(score))
                    if (25 - score % 25 > 2) and score % 25:
                        vra("apples", vr("spawn")(False))
                    if hearts < 7:
                        if int.from_bytes(vr("urandom")(1), "little") < 13:
                            hearts_dropped.append(
                                [vr("spawn")(True), time.monotonic() + 15]
                            )
                else:
                    for i in range(len(hearts_dropped)):
                        if snake[0] == hearts_dropped[i][0]:
                            hearts += 1
                            vr("j").move(y=2, x=20)
                            vr("j").nwrite(str(hearts))
                            hearts_dropped.remove(hearts_dropped[i])
                            break

                for i in range(len(hearts_dropped) - 1, -1, -1):
                    if hearts_dropped[i][1] < time.monotonic():
                        # visual pop
                        vr("tg")[hearts_dropped[i][0][0], hearts_dropped[i][0][1]] = 0
                        hearts_dropped.remove(hearts_dropped[i])

                if not apples:
                    game_ok = False
                    level += 1
                    vr("hearts", hearts)
                    vr("level", level)
                    vr("score", score)
                    vr("apple_power", 0)
                    vr("apples", [])
                    vr("chain", [[5, 5, 2], [6, 5, 6], [7, 5, 8]])
                    vr("next_move", 0)
                    vr("prev_move", 0)
                    break

                vr("refr")()  # Show the user
                break


vr("snk_start", snk_start)
del snk_start


def snk_end() -> None:
    vr("textmode")()
    if not vr("hearts"):
        # Reset to new game
        vr("apple_power", 0)
        vr("chain", [[5, 5, 2], [6, 5, 6], [7, 5, 8]])
        vr("next_move", 0)
        vr("prev_move", 0)
        vr("hearts", 3)
        vr("hscore")(vr("score"))
        vr("score", 0)
        vr("level", 1)
    vr("save_all")()


vr("snk_end", snk_end)
del snk_end


def save_all() -> None:
    try:
        remount("/", False)
        cht = vr("chain")
        apt = vr("apples")
        vr("j").clear()
        vr("j").nwrite("Saving.")
        vr("refr")()
        vr("chain", vr("stringify_chain")(vr("chain")))
        vr("apples", vr("stringify_apples")(vr("apples")))
        for i in [
            "apples",
            "hearts",
            "apple_power",
            "chain",
            "next_move",
            "prev_move",
            "score",
            "level",
        ]:
            cptoml.put(i, vr(i), "SNAKE")
            vr("j").nwrite(".")
            vr("refr")()
        vr("chain", cht)
        vr("apples", apt)
        remount("/", True)
    except RuntimeError:
        dm = vr("dm")
        if dm == "dual":
            vr("textmode")()
        vr("vibr")(vr("err_seq"))
        vr("j").clear()
        vr("j").nwrite("Could not store game state!")
        vr("player").play(vr("s_no"))
        vr("refr")()
        time.sleep(3)
        if dm == "dual":
            vr("dualmode")(16, 16, 16, 16)


vr("save_all", save_all)
del save_all


vr("snk_home")()

vrd("snk_quit")
vrd("snk_home")
vrd("snk_start")
vrd("snk_end")
