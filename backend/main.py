from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title = "Voice Color AI")

# Enable CORS so frontend can talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],    # allow all origins (for testing)
    allow_credentials=True,
    allow_methods=["*"],    # allow POST, GET, OPTIONS...
    allow_headers=["*"],
)

# Request body model
class ColorRequest(BaseModel):
    color: str

# Simple CSS colors dictionary
CSS_COLORS = {
    "black": "#000000",
    "white": "#ffffff",
    "red": "#ff0000",
    "green": "#008000",
    "blue": "#0000ff",
    "yellow": "#ffff00",
    "orange": "#ffa500",
    "purple": "#800080",
    "pink": "#ffc0cb",
    "brown": "#a52a2a",
    "gray": "#808080",
    "lime": "#00ff00",
    "cyan": "#00ffff",
    "magenta": "#ff00ff",
    "navy": "#000080",
    "teal": "#008080",
    "maroon": "#800000",
    "olive": "#808000",
}

# Normalize hex code (#f00 → #ff0000)
def normalize_hex(hex_code: str):
    hex_code = hex_code.strip().lower()
    if not hex_code.startswith("#"):
        hex_code = "#" + hex_code
    if len(hex_code) == 4:  # short form like #f00
        hex_code = "#" + hex_code[1]*2 + hex_code[2]*2 + hex_code[3]*2
    return hex_code

# Find closest color name
def closest_color_name(input_color: str):
    input_color = input_color.strip().lower()

    # Recognized color name
    if input_color in CSS_COLORS:
        return CSS_COLORS[input_color], input_color

    # Looks like hex code
    if input_color.startswith("#") or len(input_color) in (3, 6):
        try:
            hex_value = normalize_hex(input_color)
            for name, hex_val in CSS_COLORS.items():
                if hex_val.lower() == hex_value:
                    return hex_value, name
            return hex_value, "Unknown"
        except:
            return input_color, "Unknown"

    return input_color, "Unknown"

# POST /api/color
@app.post("/api/color")
def get_color_name(request: ColorRequest):
    hex_value, name = closest_color_name(request.color)
    return {"input": request.color, "hex": hex_value, "name": name}

# Run server directly
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000)
