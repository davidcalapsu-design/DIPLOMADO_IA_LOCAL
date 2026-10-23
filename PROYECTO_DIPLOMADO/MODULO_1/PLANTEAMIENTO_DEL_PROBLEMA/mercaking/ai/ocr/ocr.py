"""OCR multimodal: extrae texto de imágenes de productos."""
import os


def extract_text(image_path: str) -> str:
    """Extract text from an image using pytesseract if available, else return a stub."""
    try:
        import pytesseract
        from PIL import Image
        img = Image.open(image_path)
        return pytesseract.image_to_string(img, lang="spa")
    except ImportError:
        return "[OCR no disponible: instala pytesseract y Pillow]"
    except Exception as e:
        return f"[Error OCR: {e}]"


def suggest_product_name(text: str) -> str:
    """Heuristic: first non-empty line as suggested name."""
    for line in text.splitlines():
        line = line.strip()
        if line:
            return line[:80]
    return ""
