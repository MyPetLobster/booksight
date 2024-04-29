class Spine:
    def __init__(self, image_path, avg_color, dominant_color, color_palette, height, width, text):
        self.image_path = image_path
        self.avg_color = avg_color
        self.dominant_color = dominant_color
        self.color_palette = color_palette
        self.height = height
        self.width = width
        self.text = text    

    def __str__(self):
        return f"Spine Image Path: {self.image_path}, \nAverage Color: {self.avg_color}, \nDominant Color: {self.dominant_color}, \nColor Palette:\n{self.color_palette}, \nHeight: {self.height}, \nWidth: {self.width}, \nText: {self.text}"

        
class Book:
    def __init__(self, title, subtitle, author, publisher, publish_date, isbn):
        self.title = title
        self.subtitle = subtitle
        self.author = author
        self.publisher = publisher
        self.publish_date = publish_date
        self.isbn = isbn