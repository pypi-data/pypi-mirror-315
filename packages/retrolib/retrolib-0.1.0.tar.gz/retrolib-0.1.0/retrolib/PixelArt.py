"""
Fait un Pixel Art.

Arguments : 
    image_path : Chemin de l'image à convertir en Pixel Art.
    output_path_and_image_name : Répertoire de sortie de l'image avec le nom de l'image.
    save_picture : True si tu veux enregistrer l'image, False si tu ne veux pas l'enregistrer. Tu peux te servir de cette fonction avec cet argument sur False si tu veux simplement mettre les pixels avec leur couleur dans une variable.
    
Versions :
    1 : Convertit une image en Pixel Art mais le texte est illisible. Peu de problèmes à rêgler. Cette version ne pourra pas être accesible par les autres.
    2 : Problème résolu : 
        Avant : 
            Taille de l'image : PX x 15, 23 ou 31 / 15, 23 ou 31 x PX / 15, 23 ou 31 x 15, 23 ou 31

        Après :
            Taille de l'image : PX x 16, 24 ou 32 / 16, 24 ou 32 x PX / 16, 24 ou 32 x 16, 24 ou 32

            

Make a Pixel Art.

Arguments:
    image_path: Path of the image to convert to Pixel Art.
    output_path_and_image_name: Output directory of the image with the name of the image.
    save_picture: True if you want to save the image, False if you don't want to save it. You can use this function with this argument set to False if you just want to put the pixels with their color into a variable.
    
Versions:
    1: Convert an image to Pixel Art, but the text is unreadable. A bit of problems to fix. This version will not be able to be available by others.
    2: Solved problem: 
        Before: 
            Image size: PX x 15, 23 or 31 / 15, 23 or 31 x PX / 15, 23 or 31 x 15, 23 or 31

        After:
            Image size: PX x 16, 24 or 32 / 16, 24 or 32 x PX / 16, 24 or 32 x 16, 24 or 32
"""

from PIL import Image
from collections import Counter

def __PixelArtByXX(n: int, image_path: str, output_path_and_image_name: str, save_picture: bool):
    
    if save_picture != True or False:
        save_picture = True

    image = Image.open(image_path)
    image = image.convert("RGBA")
    x, y = image.size

    too_small_picture_error_message = f"Image trop petite pour y en faire un Pixel Art {str(n)}x{str(n)} ou > {str(n)}x{str(n)}.\n\nToo small picture to make a Pixel Art = {str(n)}x{str(n)} or > {str(n)}x{str(n)}."

    if x <= n+1 or y <= n+1:
        raise ValueError(too_small_picture_error_message)

    if x == y:
        new_x = n
        new_y = n
    elif x > y:
        new_x = (x // y) * n
        new_y = n
    else:
        new_x = n
        new_y = (y // x) * n

    x_sections = x // new_x
    y_sections = y // new_y

    pixels = {}
    pixel_art = {}

    for X in range(1, new_x + 1):
        for Y in range(1, new_y + 1):
            pixels[(X, Y)] = []

    for X in range(1, new_x + 1):
        for Y in range(1, new_y + 1):
            try:
                pixels[(X, Y)].append(image.getpixel((min(x_sections * X, x - 1), min(y_sections * Y, y - 1))))
            except IndexError:
                pass

    for X in range(1, new_x + 1):
        for Y in range(1, new_y + 1):
            if pixels[(X, Y)]:
                pixel_art[(X, Y)] = Counter(pixels[(X, Y)]).most_common(1)[0][0]

    if save_picture == True:
        pixel_art_image = Image.new("RGBA", (new_x, new_y), (0, 0, 0, 0))

        pixels_in_pixel_art = pixel_art_image.load()

        for X in range(0, new_x):
            for Y in range(0, new_y):
                try:
                    pixels_in_pixel_art[X, Y] = pixel_art[X+1, Y+1]
                except KeyError:
                    pass

        pixel_art_image.save(output_path_and_image_name)

    return pixel_art

def By16(
        image_path: str,
        output_path_and_image_name: str = "./PixelArt.png", 
        save_picture: bool = True
        ): 
    return __PixelArtByXX(16, image_path=image_path, output_path_and_image_name=output_path_and_image_name, save_picture=save_picture)

def By24(
        image_path: str,
        output_path_and_image_name: str = "./PixelArt.png", 
        save_picture: bool = True
        ): 
    return __PixelArtByXX(24, image_path=image_path, output_path_and_image_name=output_path_and_image_name, save_picture=save_picture)

def By32(image_path: str,
        output_path_and_image_name: str = "./PixelArt.png", 
        save_picture: bool = True
        ): 
    return __PixelArtByXX(32, image_path=image_path, output_path_and_image_name=output_path_and_image_name, save_picture=save_picture)