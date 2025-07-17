import pygame as pg


class Debug:
    rect_color = "blue"
    mask_color = "red"
    coords_color = "white"

    def show(self,
             screen: pg.Surface,
             rect: pg.Rect = None,
             mask: pg.Mask = None,
             position: pg.Vector2 = None,
             rect_color: str = None,
             mask_color: str = None):
        if rect:
            self.draw_rect(screen, rect, rect_color)
        if rect and mask:
            self.draw_mask(screen, rect, mask, mask_color)
        if position:
            self.draw_coords(screen, position)

    def draw_rect(self, screen: pg.Surface, rect: pg.Rect, color=None):
        """Draw the collision rectangle for debugging"""
        color = color or self.rect_color
        pg.draw.rect(screen, color, rect, 2)

    def draw_mask(self, screen, rect: pg.Rect, mask: pg.Mask, color=None):
        """Draw the collision mask outline for debugging"""
        color = color or self.mask_color
        mask_outline = mask.outline()
        if mask_outline:
            # Convert mask coordinates to screen coordinates
            screen_points = [(x + rect.x, y + rect.y) for x, y in mask_outline]
            if len(screen_points) > 2:
                pg.draw.polygon(screen, color, screen_points, 2)

    def draw_coords(self, screen, position: pg.Vector2):
        # Draw center point
        pg.draw.circle(screen, self.coords_color, (int(position.x), int(position.y)), 2)

        # Draw position text
        font = pg.font.Font(None, 20)
        pos_text = font.render(f"({int(position.x)}, {int(position.y)})", True, self.coords_color)
        screen.blit(pos_text, (position.x + 10, position.y - 10))
