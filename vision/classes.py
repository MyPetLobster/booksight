class Spine:
    def __init__(self, image_path, avg_color, dominant_color, color_palette, height, width, text, title=None, author=None, possible_matches=None):
        self.image_path = image_path
        self.avg_color = avg_color
        self.dominant_color = dominant_color
        self.color_palette = color_palette
        self.height = height
        self.width = width
        self.text = text
        self.title = title
        self.author = author
        self.possible_matches = possible_matches

    def __str__(self):
        return f"""
        Image Path: {self.image_path}
        Average Color: {self.avg_color}
        Dominant Color: {self.dominant_color}
        Color Palette: {self.color_palette}
        Height: {self.height}
        Width: {self.width}
        Text: {self.text}
        Title: {self.title}
        Author: {self.author}
        Possible Matches: {self.possible_matches}
        """
    
    def __repr__(self):
        return self.__str__()

        
class Book:
    def __init__(self, title, subtitle, author, publisher, publish_date, isbn):
        self.title = title
        self.subtitle = subtitle
        self.author = author
        self.publisher = publisher
        self.publish_date = publish_date
        self.isbn = isbn