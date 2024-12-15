"""
Fait un Pixel Art.

Arguments : 
    image_path : Chemin de l'image à convertir en Pixel Art.
    output_path_and_image_name : Répertoire de sortie de l'image avec le nom de l'image.
    save_image : True si tu veux enregistrer l'image, False si tu ne veux pas l'enregistrer. Tu peux te servir de cette fonction avec cet argument sur False si tu veux simplement mettre les pixels avec leur couleur dans une variable.
    colors : Fait le Pixel Art avec les couleurs de votre choix.
    n : Uniquement dans la fonction ByNumber(args) car dans cette fonction, du décides le Pixel Art est par combien.

Versions :
    1 : Convertit une image en Pixel Art mais le texte est illisible. Peu de problèmes à rêgler. Cette version ne pourra pas être accesible par les autres.
    2 : Problème résolu : 
        Avant : 
            Taille de l'image : PX × 15, 23 ou 31 / 15, 23 ou 31 × PX / 15, 23 ou 31 × 15, 23 ou 31

        Après :
            Taille de l'image : PX × 16, 24 ou 32 / 16, 24 ou 32 × PX / 16, 24 ou 32 × 16, 24 ou 32

    3. Problème résolu : À la version 2, les Pixel Arts générés étaient toujours une image carrée mais c'est réparé maintenant.
    4. Ajout des l'arguments colors, n, et les fonctions By48(args) et ByNumber(n, args). L'argument color fait le Pixel Art avec les couleurs de ton choix. Exemple : retrolib.PixelArt.By24(... colors=[(255, 0, 0), (0, 255, 0), (0, 0, 255)]). ByNumber(n, args) function, you decide the Pixel Art is by how much with the argument n.

     

Make a Pixel Art.

Arguments:
    image_path: Path of the image to convert to Pixel Art.
    output_path_and_image_name: Output directory of the image with the name of the image.
    save_image: True if you want to save the image, False if you don't want to save it. You can use this function with this argument set to False if you just want to put the pixels with their color into a variable.
    colors: Make the Pixel Art with the colors of your choice.
    n: Only in the ByNumber(args) function because in this function, you decide the Pixel Art is by how much.
    
Versions:
    1: Convert an image to Pixel Art, but the text is unreadable. A bit of problems to fix. This version will not be able to be available by others.
    2: Problem solved: 
        Before: 
            Image size: PX × 15, 23 or 31 / 15, 23 or 31 × PX / 15, 23 or 31 × 15, 23 or 31

        After:
            Image size: PX × 16, 24 or 32 / 16, 24 or 32 × PX / 16, 24 or 32 × 16, 24 or 32
    
    3. Problem solved : At version 2, generated Pixel Arts was always a square image but it's fixed now.
    4. Added these arguments : color, n, and these functions : ByNumber(arg) and By48(args). The color argument makes the Pixel Art with the colors of your choice. Example: retrolib.PixelArt.By24(... colors=[(255, 0, 0), (0, 255, 0), (0, 0, 255)])
"""

from PIL import Image
from collections import Counter
import math

def ByNumber(n: int, image_path: str, output_path_and_image_name: str = "./PixelArt.png", save_image: bool = True, colors=None):
    def __change_colors_if_wanted(color_of_pixel):
        if colors is not None:
            return min(colors, key=lambda color: math.sqrt(sum((color_of_pixel[i] - color[i]) ** 2 for i in range(4))))
        return color_of_pixel

    if save_image is not True or False:
        save_image = True

    image = Image.open(image_path)
    image = image.convert("RGBA")
    x, y = image.size

    too_small_image_error_message = f"Image trop petite pour y en faire un Pixel Art {str(n)}×{str(n)} ou > {str(n)}×{str(n)}.\n\nToo small image to make a Pixel Art = {str(n)}×{str(n)} or > {str(n)}×{str(n)}."

    if x <= n+1 or y <= n+1:
        raise ValueError(too_small_image_error_message)

    if x == y:
        new_x = n
        new_y = n
    elif x >= y:
        new_x = int(n * x / y)
        new_y = n
    else:
        new_x = n
        new_y = int(n * y / x)

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
                pixels[(X, Y)].append(image.getpixel((x_sections * (X - 1), y_sections * (Y - 1))))
            except IndexError:
                pass

    for X in range(1, new_x + 1):
        for Y in range(1, new_y + 1):
            if pixels[(X, Y)]:
                pixel_art[(X, Y)] = __change_colors_if_wanted(Counter(pixels[(X, Y)]).most_common(1)[0][0])

    if save_image == True:
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
        save_image: bool = True,
        colors=None
        ): 
    return ByNumber(16, image_path=image_path, output_path_and_image_name=output_path_and_image_name, save_image=save_image, colors=colors)

def By16(
        image_path: str,
        output_path_and_image_name: str = "./PixelArt.png", 
        save_image: bool = True,
        colors=None
        ): 
    return ByNumber(24, image_path=image_path, output_path_and_image_name=output_path_and_image_name, save_image=save_image, colors=colors)

def By32(image_path: str,
        output_path_and_image_name: str = "./PixelArt.png", 
        save_image: bool = True,
        colors=None
        ): 
    return ByNumber(32, image_path=image_path, output_path_and_image_name=output_path_and_image_name, save_image=save_image, colors=colors)

def By48(image_path: str,
        output_path_and_image_name: str = "./PixelArt.png", 
        save_image: bool = True,
        colors=None
        ): 
    return ByNumber(48, image_path=image_path, output_path_and_image_name=output_path_and_image_name, save_image=save_image, colors=colors)