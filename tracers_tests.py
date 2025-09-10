import pyMeow as pm
from typing import Optional, Tuple


# 0x312495F0

# F0



VIEW_MATRIX_OFFSET = 0x2BC43950         # На эти два оффсета я не успел найти указаиели :( 
PROJECTION_MATRIX_OFFSET = 0x2BC43EF0   #

STASH_BASE = 0x5C8000000
STASH_REGION = 0xB6895140



# 55DB7730

rr = pm.open_process("javaw.exe")
game_module = pm.get_module(rr, 'jvm.dll')["base"]

def multiply_matrix_vector(matrix: list, vec: list) -> list:
    return [
        matrix[0] * vec[0] + matrix[4] * vec[1] + matrix[8] * vec[2] + matrix[12] * 1.0,
        matrix[1] * vec[0] + matrix[5] * vec[1] + matrix[9] * vec[2] + matrix[13] * 1.0,
        matrix[2] * vec[0] + matrix[6] * vec[1] + matrix[10] * vec[2] + matrix[14] * 1.0,
        matrix[3] * vec[0] + matrix[7] * vec[1] + matrix[11] * vec[2] + matrix[15] * 1.0
    ]





# кривое но рабочее
def world2screen(world_pos: Tuple[float, float, float]) -> Optional[Tuple[float, float]]:
    
    
    player_x = pm.r_float64(rr, pm.pointer_chain_64(rr, game_module+0x007F9080, [0x0, 0x2A0, 0x4A8, 0x430, 0x340, 0x340, 0x70]))
    player_y = pm.r_float64(rr, pm.pointer_chain_64(rr, game_module+0x007F9080, [0x0, 0x2A0, 0x4A8, 0x430, 0x340, 0x340, 0x78]))
    player_z = pm.r_float64(rr, pm.pointer_chain_64(rr, game_module+0x007F9080, [0x0, 0x2A0, 0x4A8, 0x430, 0x340, 0x340, 0x80]))
    view_matrix = pm.r_floats(rr, VIEW_MATRIX_OFFSET, 16)
    proj_matrix = pm.r_floats(rr, PROJECTION_MATRIX_OFFSET, 16)
    screen_width = 1920
    screen_height = 1080

    camera_space = [
        world_pos[0] - player_x,
        world_pos[1] - player_y,
        world_pos[2] - player_z
    ]
    
    view_space = multiply_matrix_vector(view_matrix, camera_space)
    clip_space = multiply_matrix_vector(proj_matrix, view_space)
    
    if clip_space[3] < 1e-5:
        return None  
    
    ndc = [
        clip_space[0] / clip_space[3],
        clip_space[1] / clip_space[3],
        clip_space[2] / clip_space[3]
    ]
    
    screen_x = (ndc[0] * 0.5 + 0.5) * screen_width 
    screen_y = (0.5 - ndc[1] * 0.5) * screen_height  
    
    if not (-1 <= ndc[0] <= 1 and -1 <= ndc[1] <= 1):
        return None
    
    return (screen_x, screen_y)


def main():
            byteBuffer = pm.r_bytes(rr, STASH_BASE, STASH_REGION)
            results = pm.aob_scan_bytes("9F DD 00 F8 01 01 00 00", byteBuffer, False)

            try:
                playerX = pm.r_float64(rr, pm.pointer_chain_64(rr, game_module + 0x007F9080, [0x0, 0x2A0, 0x4A8, 0x430, 0x340, 0x340, 0x70]))
                playerZ = pm.r_float64(rr , pm.pointer_chain_64(rr, game_module + 0x007F9080, [0x0, 0x2A0, 0x4A8, 0x430, 0x340, 0x340, 0x80]))
            except Exception as e:
                print(f"Player coord error: {e}")

            found_stashes = []
            scaned_coords = set()
            round_p = 3
            print(results)
            for addr in results:
                try:

                    y = pm.r_float64(rr, (STASH_BASE + addr) + 192)
                    x = pm.r_float64(rr, (STASH_BASE + addr) + 184)
                    z = pm.r_float64(rr, (STASH_BASE + addr) + 200)
                
                    if 1 < y < 200 and (y - int(y)) == 0.0:
                        x_r = round(x, round_p)
                        z_r = round(z, round_p)
                        y_r = round(y, 1)
                        
                        coord = (x_r, y_r, z_r)
                        
                        if coord not in scaned_coords:
                            distance = ((playerX - x) ** 2 + (playerZ - z) ** 2) ** 0.5
                            
                            if (abs(playerX - x) + abs(playerZ - z)) < 400:
                                found_stashes.append((distance, x, y, z))
                                scaned_coords.add(coord)
                except:
                    continue
            print(found_stashes)
            while pm.overlay_loop():
                pm.begin_drawing()  
                for distance, x, y, z in found_stashes:
                    try:
                        scrn = world2screen((x, y, z))
                        if scrn:
                            pm.draw_line(
                                startPosX=1920/2,# тут нужно гетать ширину экрана но для тестов я не юзал это ибо мне лень было написать целые лишнии 2 строчки + я эксперементировал где трейсера будут лучше смотреться
                                startPosY=0, #  тоже самое с высотой
                                endPosX=scrn[0],
                                endPosY=scrn[1],
                                color=pm.get_color("purple"),
                                thick=1.6
                            )
                    except Exception as e:
                        print(f"Ошибка: {e}")
                pm.end_drawing()



if __name__ == "__main__":
    pm.overlay_init("Rustex Remake", title="goida", fps=60)  
    main()


