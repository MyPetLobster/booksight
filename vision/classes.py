

class Spine:
    def __init__(self, spine_image_path, avg_color, dominant_color, height, width, text):
        self.spine_image_path = spine_image_path
        self.avg_color = avg_color
        self.dominant_color = dominant_color
        self.height = height
        self.width = width
        self.text = text    

    def __str__(self):
        return f"Spine Image Path: {self.spine_image_path}, \nAverage Color: {self.avg_color}, \nDominant Color: {self.dominant_color}, \nHeight: {self.height}, \nWidth: {self.width}, \nText: {self.text}"

        
