import pygame
from threading import Timer

from characters.player import Player
from characters.texture import Texture

from components.config import CONFIG, CONST, debug
from components.sprites.sprite import Sprite

class Enemy(Player):
    def follow_player(self, obstacles: list[Texture]):
        """
        적이 플레이어를 따라가도록 합니다.
        :param obstacles: 적이 지나다닐 수 없는 장애물 배열
        """
        if self.hp <= 0:
            return  # 사망
        
        if self.is_camera_bound(1.02):  # 플레이어 화면 범위에 있는 경우 (보정값 추가)
            velocity_x = 0.7  # 적의 이동 속도

            if self.x > CONFIG.player_x:  # 플레이어보다 뒤에 있는 경우 따라가기 위해 속도를 음수로 설정
                velocity_x *= -1

            if self.x != CONFIG.player_x and abs(velocity_x * 10) <= abs(CONFIG.player_x - self.x):  # 따라가야할 위치가 플레이어에게 따라갈 수 있는 최소 위치보다 많은 경우
                self.move_x(velocity_x)  # 움직임

            # 장애물을 인식하고 피해 다님
            for obstacle in obstacles:
                if obstacle.is_bound(5, 40, self.x, self.y, self.width, self.height):  # 주변에 장애물이 있다면
                    self.move_y(13)  # 점프