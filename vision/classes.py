class Spine:
    def __init__(self, image_path=None, avg_color=None, dominant_color=None, color_palette=None, height=None, width=None, text=None, title=None, author=None, possible_matches=None):
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
    def __init__(self):
        self.title = None
        self.subtitle = None
        self.authors = None
        self.language = None
        self.publisher = None
        self.date_published = None
        self.description = None
        self.isbn = None
        self.isbn10 = None
        self.isbn13 = None
        self.pages = None
        self.binding = None
        self.image_path = None
        self.confidence = None


    def __str__(self):
        return f"""
        Title: {self.title}
        Subtitle: {self.subtitle}
        Authors: {self.authors}
        Language: {self.language}
        Publisher: {self.publisher}
        Publish Date: {self.date_published}
        Description: {self.description}
        ISBN: {self.isbn}
        ISBN10: {self.isbn10}
        ISBN13: {self.isbn13}
        Pages: {self.pages}
        Binding: {self.binding}
        Image: {self.image_path}
        Confidence: {self.confidence}
        """ 
    
    def __repr__(self):
        return self.__str__()