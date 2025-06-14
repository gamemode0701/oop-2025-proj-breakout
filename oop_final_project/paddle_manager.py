class PaddleManager:
    def __init__(self, paddle):
        self.paddle = paddle
        self.original_width = paddle.width
        self.original_height = paddle.height

    def move_to(self, x):
        self.paddle.x = x

    def set_width(self, width):
        self.paddle.set_size(width, self.paddle.height)

    def enlarge(self, factor=1.5):
        new_width = self.original_width * factor
        self.paddle.set_size(new_width, self.original_height)

    def restore(self):
        self.paddle.set_size(self.original_width, self.original_height)