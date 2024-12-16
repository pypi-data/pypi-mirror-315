class Widget:
    
    def __init__(self, x: int, y: int, text: str, screen, font_size: int = 25):
        self.x = x
        self.y = y
        self.text = text
        self.screen = screen
        self.font_size = font_size
    
    def draw(self):
        self.pantalla.blit(self.image, (self.rect.x, self.rect.y))
