from PIL import ImageDraw


class UI:
    def __init__(self, projection):
        self.projection = projection

    def draw(self, img):
        ui = ImageDraw.Draw(img)

        for r in range(0,6):
            r = (r + 1) * 2.5

            ui.ellipse(self.projection.ellipse((-r,-r),(r,r)), outline=(136,136,136,255), width=2)

        ui.line([self.projection.point(0,-17),self.projection.point(0,17)], fill=(136,136,136,255), width=2)
        ui.line([self.projection.point(-17,0),self.projection.point(17,0)], fill=(136,136,136,255), width=2)

        # Outermost ring is slightly different, so ensure it's above our lines
        ui.ellipse(self.projection.ellipse((-17,-17),(17,17)), outline=(238,238,238,255), width=2)

        ## Directional indicators
        ## Drawn last so they overlay our rings/lines
        # Coreward
        points = self.projection.points([
            (18,0),
            (16.6,0.45),
            (16.9,0),
            (16.6,-0.45),
        ])
        ui.polygon(points, fill=(0,0,255,255))

        # Spinward
        points = self.projection.points([
            (0,18),
            (0.45,16.6),
            (0,16.9),
            (-0.45,16.6),
        ])
        ui.polygon(points, fill=(255,0,0,255))
