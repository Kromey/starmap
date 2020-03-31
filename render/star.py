class Star:
    def __init__(self, projection):
        self.projection = projection

    def ellipse(self, star):
        coord = self.projection.point(*star.coords)
        p1 = (coord[0]-2, coord[1]-2)
        p2 = (coord[0]+2, coord[1]+2)

        return p1, p2

    def color(self, star):
        if star.name == 'Sol':
            color = (0,255,0,255)
        elif star.name == 'Gl 447':
            color = (0,136,255,255)
        elif star.name == 'Gl 46':
            color = (255,0,0,255)
        elif star.name == 'NN 4013':
            color = (255,0,255,255)
        elif star.name == 'NN 4219':
            color = (255,255,0,255)
        else:
            color = (170,170,170,255)

        return color

    def fill_color(self, star):
        if star.is_habitable:
            return self.color(star)
        else:
            return (0,0,0,255)

