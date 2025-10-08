import curses
import random
import time

# ASCII Art for "R I A L O"
RIALO = [
"RRRR    III   AAAAA   L       OOOOO",
"R   R    I    A   A  L      O     O",
"RRRR     I    AAAAA  L      O     O",
"R  R     I    A   A  L      O     O",
"R   R   III   A   A  LLLLL   OOOOO"
]

# Rainbow color sequence
RAINBOW_COLORS = [
    curses.COLOR_RED,
    curses.COLOR_YELLOW,
    curses.COLOR_GREEN,
    curses.COLOR_CYAN,
    curses.COLOR_BLUE,
    curses.COLOR_MAGENTA
]

def draw_rialo_rainbow(win):
    sh, sw = win.getmaxyx()
    start_y = 2
    start_x = sw // 2 - len(RIALO[0]) // 2
    for i, line in enumerate(RIALO):
        for j, char in enumerate(line):
            if char != ' ':
                color_index = j % len(RAINBOW_COLORS) + 1
                try:
                    win.addch(start_y + i, start_x + j, char, curses.color_pair(color_index) | curses.A_BOLD)
                except curses.error:
                    pass

def main(stdscr):
    curses.curs_set(0)
    curses.start_color()

    # Initialize rainbow colors
    for i, color in enumerate(RAINBOW_COLORS):
        curses.init_pair(i + 1, color, curses.COLOR_BLACK)

    curses.init_pair(8, curses.COLOR_RED, curses.COLOR_BLACK)    # Food
    curses.init_pair(9, curses.COLOR_GREEN, curses.COLOR_BLACK)  # Snake

    sh, sw = stdscr.getmaxyx()
    w = curses.newwin(sh, sw, 0, 0)
    w.timeout(100)
    w.keypad(1)

    # Snake setup
    snake = [[sh // 2 + 8, sw // 2 + i] for i in range(7)]
    snake_length = 7
    key = curses.KEY_RIGHT

    # Food
    food = [random.randint(10, sh - 2), random.randint(1, sw - 2)]
    w.addch(food[0], food[1], 'O', curses.color_pair(8))

    # Score
    score = 0

    while True:
        # Display score
        try:
            w.addstr(0, 2, f"Score: {score}", curses.A_BOLD | curses.color_pair(8))
        except curses.error:
            pass

        next_key = w.getch()
        if next_key in [curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT]:
            if (key == curses.KEY_UP and next_key != curses.KEY_DOWN) or \
               (key == curses.KEY_DOWN and next_key != curses.KEY_UP) or \
               (key == curses.KEY_LEFT and next_key != curses.KEY_RIGHT) or \
               (key == curses.KEY_RIGHT and next_key != curses.KEY_LEFT):
                key = next_key

        # Move head
        head = snake[0].copy()
        if key == curses.KEY_DOWN: head[0] += 1
        elif key == curses.KEY_UP: head[0] -= 1
        elif key == curses.KEY_LEFT: head[1] -= 1
        elif key == curses.KEY_RIGHT: head[1] += 1

        # Wrap edges
        head[0] %= sh
        head[1] %= sw
        snake.insert(0, head)

        # Eat food
        if head == food:
            food = None
            while food is None:
                nf = [random.randint(10, sh - 2), random.randint(1, sw - 2)]
                if nf not in snake:
                    food = nf
            w.addch(food[0], food[1], 'O', curses.color_pair(8))
            snake_length += 1
            score += 1  # increase score
        else:
            if len(snake) > snake_length:
                tail = snake.pop()
                w.addch(tail[0], tail[1], ' ')

        # Draw rainbow RIALO
        draw_rialo_rainbow(w)

        # Draw food
        w.addch(food[0], food[1], 'O', curses.color_pair(8))

        # Draw snake rainbow
        for index, seg in enumerate(snake):
            try:
                color_index = (index % len(RAINBOW_COLORS)) + 1
                w.addch(seg[0], seg[1], '*', curses.color_pair(color_index) | curses.A_BOLD)
            except curses.error:
                pass

        time.sleep(0.15)  # slower snake speed

curses.wrapper(main)
