import os
import pygame
from typing import List


def _scale_surface_keep_aspect(img_surf, target_w, target_h):
    w, h = img_surf.get_size()
    scale = min(target_w / w, target_h / h)
    new_size = (max(1, int(w * scale)), max(1, int(h * scale)))
    return pygame.transform.smoothscale(img_surf, new_size)


class Slideshow:
    def __init__(self, image_paths: List[str], interval: float = 5.0):
        self.paths = image_paths
        self.interval = interval

    def run(self):
        if not self.paths:
            print('No images to show.')
            return

        pygame.init()
        info = pygame.display.Info()
        screen = pygame.display.set_mode((info.current_w, info.current_h), pygame.FULLSCREEN)
        pygame.mouse.set_visible(False)

        clock = pygame.time.Clock()

        idx = 0
        timer = 0.0

        # Preload scaled surfaces lazily
        surfaces = [None] * len(self.paths)

        running = True
        while running:
            dt = clock.tick(30) / 1000.0
            timer += dt

            for ev in pygame.event.get():
                if ev.type == pygame.KEYDOWN:
                    if ev.key in (pygame.K_ESCAPE, pygame.K_q):
                        running = False
                if ev.type == pygame.QUIT:
                    running = False

            if surfaces[idx] is None:
                try:
                    img = pygame.image.load(self.paths[idx])
                    surf = _scale_surface_keep_aspect(img, info.current_w, info.current_h)
                    # center
                    final = pygame.Surface((info.current_w, info.current_h))
                    final.fill((0, 0, 0))
                    x = (info.current_w - surf.get_width()) // 2
                    y = (info.current_h - surf.get_height()) // 2
                    final.blit(surf, (x, y))
                    surfaces[idx] = final
                except Exception as e:
                    print('Failed to load', self.paths[idx], e)
                    surfaces[idx] = pygame.Surface((info.current_w, info.current_h))
                    surfaces[idx].fill((0, 0, 0))

            screen.blit(surfaces[idx], (0, 0))
            pygame.display.flip()

            if timer >= self.interval:
                timer = 0.0
                idx = (idx + 1) % len(self.paths)

        pygame.quit()
