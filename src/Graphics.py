import pygame
import pygame_gui
import pygame_menu

def calculateSquare(pos, board, size):
    if 8 - pos[1]/size < 0: return (-1, -1)
    x, y = int(pos[0]/size), int(8 - pos[1]/size)
    if (not board.flipped):
        return (x, y)
    return (7 - x, 7 - y)

def inBounds(pos, size):
    for i in range(2):
        if pos[i] > size * 7.56:
            pos[i] = size * 7.56
        elif pos[i] < 0:
            pos[i] = 0

def loadAssets(size):
    o = [None for i in range(17)]
    team = ['l', 'd']
    pieces = [None, 'p', 'r', 'n', 'b', 'q', 'k']

    for i in range(1, 7):
        for j in range(2):
            o[i + 10*j] = pygame.transform.scale(pygame.image.load("src/assets/pieces/Chess_{0}{1}t60.png".format(pieces[i], team[j])), (size, size))

    whiteSquare = pygame.image.load("src/assets/pieces/whiteSq.png")
    whiteSquare = pygame.transform.scale(whiteSquare, (size, size))
    blackSquare = pygame.image.load("src/assets/pieces/blackSq.png")
    blackSquare = pygame.transform.scale(blackSquare, (size, size))

    o[7] = whiteSquare
    o[8] = blackSquare

    return o

def printBoard(screen, assets, board, size):
    screen.fill((255, 255, 255), (0, 0, size*8, size*8))
    for i in range(7, -1, -1):
        for j in range(8):
            x = j
            y = 7 - i
            if board.flipped:
                x = 7-x
                y = 7-y
            if (x + y)%2 == 0:
                screen.blit(assets[7], (x*size, y*size))
            else:
                screen.blit(assets[8], (x*size, y*size))
            if board.heldPiece and j == board.heldPiece[0] and i == board.heldPiece[1]:
                continue
            if board.board[j][i]:
                screen.blit(assets[board.board[j][i]], (x*size, y*size))

def loadGuiButtons(manager):
    flipButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((520, 500), (90, 40)), text='flip', manager=manager)
    newGameButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((520, 550), (90, 40)), text='new game', manager=manager)
    forwardButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((250, 500), (40, 40)), text='>', manager=manager, object_id="arrows")
    backButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((190, 500), (40, 40)), text='<', manager=manager, object_id="arrows")
    newGameButton.disable()
    forwardButton.disable()
    backButton.disable()
    return [flipButton, newGameButton, forwardButton, backButton]

def createMenu():
    defaultFont = pygame.font.Font("src/assets/fonts/Cascadia.ttf", 16)
    tableTheme = pygame_menu.Theme(background_color=(48,48,48), title_font_size=(16),
        title_font_color=(200, 200, 200), title_bar_style=1001, title_font=defaultFont,
        widget_font=defaultFont, widget_background_color=(35,35,35))
    m = pygame_menu.Menu("moves", 220, 480, position=(100, 0), theme=tableTheme, center_content=False)
    m.get_menubar().set_background_color((0, 0, 0, 175))
    return m

def updateTable(menu, storage, turn, moveNumber):
    t = [storage.game.pop()]
    p = storage.game.variation_san(t)
    storage.game.push(t[0])
    menu.select_widget(None)
    if turn:
        for i, v in enumerate(p):
            if not v.isdigit(): break
        menu.add.button(p[i:], margin=(0,0), align=pygame_menu.locals.ALIGN_RIGHT, float=True, button_id=str(moveNumber))
    else:
        menu.add.vertical_margin(1)
        menu.add.button(p, margin=(18,0), align=pygame_menu.locals.ALIGN_LEFT, button_id=str(moveNumber))
    r = menu.get_widgets()[-1]
    r.select()
    r.set_onselect(functionTest)
    menu.scroll_to_widget(r)

def functionTest(a, b, c):
    if a:
        print(a, b, c)
        print(b.get_id())

def generateButtons(manager, board, coords, size):
    out = []

    x = coords[0]
    y = 7 - coords[1]
    if board.flipped:
        x = 7 - x
        y = 7 - y

    direction = 1
    if y:
        direction = -1

    base = 0
    if not board.turn: base = 4
    for i in range(4):
        out.append(pygame_gui.elements.UIButton(relative_rect=pygame.Rect((x*size, (y + direction * i)*size), (size, size)), text='', manager=manager, object_id="promote_" + str(i + base)))

    return out
