import os
import pygame as pg
import random
import sys
import time

WIDTH, HEIGHT = 1600, 900
key_dct = {pg.K_UP:(0, -5),
           pg.K_DOWN:(0, +5),
           pg.K_LEFT:(-5, 0),
           pg.K_RIGHT:(+5, 0)
           }

# 演習1
# 移動した大きさ:xの角度???
kk_dct = {(0, -5): 90,
          (+5, -5): 45,
          (+5, 0): 0,
          (+5, +5):-45,
          (0, +5):-90,
          (-5, +5): -45,
          (-5, 0): 0,
          (-5, -5): 45
          }


os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(obj_rct:pg.Rect) -> tuple[bool, bool]: # boolはTrueFalseをあらわす
    """
    引数：こうかとんRectかばくだんRect
    戻り値：タプル（横方向判定結果、縦方向判定結果）
    画面内ならTrue、画面外ならFalse
    """
    yoko, tate = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right:
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:
        tate = False
    return yoko, tate


def main():
    x = 0
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), x, 2.0)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 900, 400
    enn = pg.Surface((20, 20)) #　一辺が20のからのサーフェイスを作る
    enn.set_colorkey((0, 0, 0))
    pg.draw.circle(enn, (255, 0, 0), (10, 10), 10)
    enn_rct = enn.get_rect()
    enn_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    vx, vy = +5, +5

# 演習1
    kk_img1 = pg.transform.flip(pg.image.load("fig/3.png"),True, False)
    kk_img1 = pg.transform.rotozoom(kk_img1, x, 2.0)
    kk_rct1 = kk_img1.get_rect()
    kk_rct1.center = 900, 400

# 演習3
    big_r = pg.Surface((WIDTH,HEIGHT))
    pg.draw.rect(big_r, (0, 0, 0), pg.Rect(0, 0, WIDTH, HEIGHT))
    big_r.set_alpha(127)
    big_rct = big_r.get_rect()
    big_rct.center = WIDTH / 2, HEIGHT / 2
    gg = pg.font.Font(None, 100)
    txt = gg.render("GAME OVER", True, (255, 255, 255))
    txt_rct = txt.get_rect()
    txt_rct.center = WIDTH / 2, HEIGHT / 2
    kk_cry = pg.image.load("fig/8.png")
    kk_crct = kk_cry.get_rect()
    kk_crct.center = 300, HEIGHT / 2

    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return # もし×ボタン押されたらmainからでていく
            
        if kk_rct.colliderect(enn_rct): # こうかとんに爆弾が当たる
            # 演習3
            screen.blit(big_r ,big_rct)
            screen.blit(txt, txt_rct)
            screen.blit(kk_cry, kk_crct)
            pg.display.update()
            time.sleep(5)
            return    
            
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for k,v in key_dct.items():
            if key_lst[k]:
                sum_mv[0] += v[0]
                sum_mv[1] += v[1]
        kk_rct.move_ip(sum_mv) # 重要      

        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)
        # screen.blit(kk_img1, kk_rct1)
        enn_rct.move_ip(vx, vy)
        yoko, tate = check_bound(enn_rct)
        if not yoko: # 横にはみ出したら
            vx*= -1
        if not tate: # 縦にはみ出したら
            vy *= -1
        screen.blit(enn, enn_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
