# filters.py
from PIL import Image, ImageOps, ImageChops, ImageEnhance, ImageFilter

def apply_filter(img, filter_name, strength=1.0):
    try:
        if filter_name == "Negativ":
            blend_factor = min(max(strength, 0), 1)
            inverted = ImageOps.invert(img)
            return Image.blend(img, inverted, blend_factor)
        elif filter_name == "Multiplikation":
            blend_factor = min(max(strength, 0), 1)
            overlay_value = int(255 * blend_factor)
            overlay = Image.new("RGB", img.size, (overlay_value, overlay_value, overlay_value))
            return ImageChops.multiply(img, overlay)
        elif filter_name == "Helligkeit":
            enhancer = ImageEnhance.Brightness(img)
            effect = enhancer.enhance(2.0)
            return Image.blend(img, effect, strength)
        # Weitere Filterimplementierungen...
        elif filter_name == "Custom":
            return img.copy()
        else:
            return img.copy()
    except Exception as e:
        raise Exception(f"Fehler beim Anwenden des Filters: {e}")
