import numpy as np
from PIL import Image
import os
import json
import random
import math

# Create output directory for our assets
output_dir = "comedian_assets"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Enhanced color palette (RGBA) with more shades for better detailing
colors = {
    "transparent": (0, 0, 0, 0),
    "black": (0, 0, 0, 255),
    "dark_outline": (20, 20, 35, 255),
    "white": (255, 255, 255, 255),
    "off_white": (245, 245, 240, 255),
    "red": (255, 50, 50, 255),
    "red_dark": (200, 30, 30, 255),
    "red_light": (255, 100, 100, 255),
    "blue": (50, 90, 200, 255),
    "blue_dark": (30, 60, 150, 255),
    "blue_light": (90, 140, 255, 255),
    "blue_highlight": (120, 170, 255, 255),
    "yellow": (255, 255, 0, 255),
    "yellow_dark": (230, 230, 0, 255),
    "gold": (255, 215, 0, 255),
    
    # Skin tones (more variety and shading)
    "skin": (255, 213, 170, 255),
    "skin_shadow": (235, 193, 150, 255),
    "skin_dark": (215, 173, 130, 255),
    "skin_highlight": (255, 233, 190, 255),
    
    # Hair colors
    "brown": (139, 69, 19, 255),
    "brown_dark": (99, 49, 9, 255),
    "brown_light": (159, 89, 39, 255),
    
    # Grays with more variation
    "gray": (120, 120, 120, 255),
    "dark_gray": (70, 70, 70, 255),
    "darker_gray": (40, 40, 40, 255),
    "light_gray": (180, 180, 180, 255),
    "lighter_gray": (220, 220, 220, 255),
    
    # Additional colors
    "purple": (128, 0, 128, 255),
    "purple_dark": (88, 0, 88, 255),
    "curtain_red": (180, 30, 30, 255),
    "curtain_dark": (120, 20, 20, 255),
    "curtain_highlight": (210, 50, 50, 255),
    "stage_wood": (160, 120, 80, 255),
    "stage_wood_dark": (120, 90, 60, 255),
    "stage_wood_light": (190, 150, 110, 255),
}

# Size is now 1.5x larger
CHAR_SIZE = 96  # Up from 64

def create_blank_canvas(width, height):
    """Create a blank transparent canvas."""
    return np.zeros((height, width, 4), dtype=np.uint8)

def save_image(img_array, filename):
    """Save the numpy array as a PNG image."""
    img = Image.fromarray(img_array)
    img.save(os.path.join(output_dir, filename))
    print(f"Saved {filename}")

def draw_pixel(canvas, x, y, color):
    """Draw a single pixel on the canvas."""
    if 0 <= y < canvas.shape[0] and 0 <= x < canvas.shape[1]:
        canvas[y, x] = color

def draw_rectangle(canvas, x, y, width, height, color):
    """Draw a filled rectangle on the canvas."""
    for i in range(height):
        for j in range(width):
            draw_pixel(canvas, x + j, y + i, color)

def draw_circle(canvas, center_x, center_y, radius, color):
    """Draw a filled circle on the canvas."""
    for y in range(center_y - radius, center_y + radius + 1):
        for x in range(center_x - radius, center_x + radius + 1):
            if (x - center_x)**2 + (y - center_y)**2 <= radius**2:
                draw_pixel(canvas, x, y, color)

def draw_line(canvas, x1, y1, x2, y2, color):
    """Draw a line using Bresenham's algorithm."""
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx - dy
    
    while True:
        draw_pixel(canvas, x1, y1, color)
        if x1 == x2 and y1 == y2:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x1 += sx
        if e2 < dx:
            err += dx
            y1 += sy

def add_noise(canvas, region_x, region_y, width, height, intensity=0.1):
    """Add subtle noise to a region for texture."""
    for y in range(region_y, region_y + height):
        for x in range(region_x, region_x + width):
            if 0 <= y < canvas.shape[0] and 0 <= x < canvas.shape[1]:
                pixel = canvas[y, x].copy()
                # Only add noise if pixel is not transparent
                if pixel[3] > 0:
                    # Add noise to RGB channels
                    for i in range(3):
                        noise = int(np.random.normal(0, intensity * 255))
                        pixel[i] = max(0, min(255, pixel[i] + noise))
                    canvas[y, x] = pixel

def draw_outfit(canvas, x, y, width, height, colors_main, colors_shadow, colors_highlight):
    """Draw a detailed outfit with proper shading."""
    # Main body of outfit
    draw_rectangle(canvas, x, y, width, height, colors_main)
    
    # Left shadow
    shadow_width = max(2, width // 8)
    draw_rectangle(canvas, x, y, shadow_width, height, colors_shadow)
    
    # Bottom shadow
    shadow_height = max(2, height // 8)
    draw_rectangle(canvas, x, y + height - shadow_height, width, shadow_height, colors_shadow)
    
    # Right and top highlights
    highlight_width = max(2, width // 10)
    highlight_height = max(2, height // 10)
    draw_rectangle(canvas, x + width - highlight_width, y, highlight_width, height - shadow_height, colors_highlight)
    draw_rectangle(canvas, x + shadow_width, y, width - shadow_width - highlight_width, highlight_height, colors_highlight)

def draw_face(canvas, x, y, expression="neutral", facing="front"):
    """Draw a detailed face with the specified expression."""
    # Face shape (more oval than rectangle)
    face_width, face_height = 24, 26
    
    # Apply offset for side-facing
    offset_x = 0
    if facing == "left":
        offset_x = -4
    elif facing == "right":
        offset_x = 4
    
    # Base face
    for iy in range(face_height):
        for ix in range(face_width):
            # Create an oval shape
            dx = ix - face_width // 2
            dy = iy - face_height // 2
            distance = (dx**2 / ((face_width//2)**2)) + (dy**2 / ((face_height//2)**2))
            
            if distance <= 1:
                # Base skin
                skin_color = colors["skin"]
                
                # Add shading based on facing direction
                if facing == "front":
                    if ix < face_width // 3:
                        # Left side shadow
                        skin_color = colors["skin_shadow"]
                    elif ix > 2 * face_width // 3:
                        # Right side highlight
                        skin_color = colors["skin_highlight"]
                elif facing == "left":
                    if ix < face_width // 2:
                        skin_color = colors["skin_shadow"]
                elif facing == "right":
                    if ix > face_width // 2:
                        skin_color = colors["skin_highlight"]
                
                draw_pixel(canvas, x + ix + offset_x, y + iy, skin_color)
    
    # Add outline to the face
    for iy in range(face_height):
        for ix in range(face_width):
            dx = ix - face_width // 2
            dy = iy - face_height // 2
            distance = (dx**2 / ((face_width//2)**2)) + (dy**2 / ((face_height//2)**2))
            
            if 0.9 < distance <= 1:
                draw_pixel(canvas, x + ix + offset_x, y + iy, colors["dark_outline"])
    
    # Eyes position based on facing direction
    eye_y = y + face_height // 3
    
    if facing == "front":
        left_eye_x = x + face_width // 3
        right_eye_x = x + 2 * face_width // 3
        
        if expression == "neutral" or expression == "talking":
            # Regular eyes
            draw_rectangle(canvas, left_eye_x - 2, eye_y, 4, 4, colors["white"])
            draw_rectangle(canvas, right_eye_x - 2, eye_y, 4, 4, colors["white"])
            draw_rectangle(canvas, left_eye_x, eye_y + 1, 2, 2, colors["black"])
            draw_rectangle(canvas, right_eye_x, eye_y + 1, 2, 2, colors["black"])
            
        elif expression == "laughing":
            # Happy closed eyes
            draw_line(canvas, left_eye_x - 3, eye_y, left_eye_x + 2, eye_y - 1, colors["dark_outline"])
            draw_line(canvas, right_eye_x - 2, eye_y - 1, right_eye_x + 3, eye_y, colors["dark_outline"])
            
        elif expression == "thinking":
            # Squinting one eye, raising eyebrow
            draw_rectangle(canvas, left_eye_x - 2, eye_y, 4, 1, colors["dark_outline"])
            draw_rectangle(canvas, right_eye_x - 2, eye_y - 1, 4, 3, colors["white"])
            draw_rectangle(canvas, right_eye_x, eye_y, 2, 2, colors["black"])
            # Raised eyebrow
            draw_line(canvas, left_eye_x - 3, eye_y - 3, left_eye_x + 2, eye_y - 4, colors["dark_outline"])
            
    elif facing == "left":
        # Only show the visible eye when facing left
        visible_eye_x = x + 2 * face_width // 3 + offset_x
        
        if expression == "neutral" or expression == "talking":
            draw_rectangle(canvas, visible_eye_x - 2, eye_y, 4, 4, colors["white"])
            draw_rectangle(canvas, visible_eye_x, eye_y + 1, 2, 2, colors["black"])
        elif expression == "laughing":
            draw_line(canvas, visible_eye_x - 2, eye_y - 1, visible_eye_x + 3, eye_y, colors["dark_outline"])
        elif expression == "thinking":
            draw_rectangle(canvas, visible_eye_x - 2, eye_y - 1, 4, 3, colors["white"])
            draw_rectangle(canvas, visible_eye_x, eye_y, 2, 2, colors["black"])
            
    elif facing == "right":
        # Only show the visible eye when facing right
        visible_eye_x = x + face_width // 3 + offset_x
        
        if expression == "neutral" or expression == "talking":
            draw_rectangle(canvas, visible_eye_x - 2, eye_y, 4, 4, colors["white"])
            draw_rectangle(canvas, visible_eye_x, eye_y + 1, 2, 2, colors["black"])
        elif expression == "laughing":
            draw_line(canvas, visible_eye_x - 3, eye_y, visible_eye_x + 2, eye_y - 1, colors["dark_outline"])
        elif expression == "thinking":
            draw_rectangle(canvas, visible_eye_x - 2, eye_y - 1, 4, 3, colors["white"])
            draw_rectangle(canvas, visible_eye_x, eye_y, 2, 2, colors["black"])
    
    # Mouth based on expression
    mouth_y = y + 3 * face_height // 4
    mouth_x = x + face_width // 2 - 5 + offset_x
    
    if expression == "neutral":
        draw_line(canvas, mouth_x, mouth_y, mouth_x + 10, mouth_y, colors["dark_outline"])
        
    elif expression == "talking":
        # More expressive talking mouth
        draw_rectangle(canvas, mouth_x, mouth_y - 2, 10, 5, colors["dark_outline"])
        draw_rectangle(canvas, mouth_x + 1, mouth_y - 1, 8, 3, colors["red_dark"])
        # Add teeth for more expression
        for i in range(1, 8, 2):
            draw_rectangle(canvas, mouth_x + i, mouth_y - 1, 1, 1, colors["white"])
        
    elif expression == "laughing":
        # Big happy smile with teeth
        draw_rectangle(canvas, mouth_x - 1, mouth_y - 4, 12, 7, colors["dark_outline"])
        draw_rectangle(canvas, mouth_x, mouth_y - 3, 10, 5, colors["red_dark"])
        
        # Teeth
        for i in range(1, 9, 2):
            draw_rectangle(canvas, mouth_x + i, mouth_y - 3, 1, 2, colors["white"])
            
        # Add laugh lines around eyes
        if facing == "front":
            draw_line(canvas, x + face_width // 4, eye_y - 5, x + face_width // 3 - 2, eye_y - 2, colors["dark_outline"])
            draw_line(canvas, x + 3*face_width // 4, eye_y - 5, x + 2*face_width // 3 + 2, eye_y - 2, colors["dark_outline"])
    
    elif expression == "thinking":
        # Thoughtful expression - mouth to the side
        draw_line(canvas, mouth_x + 2, mouth_y, mouth_x + 8, mouth_y, colors["dark_outline"])
        draw_line(canvas, mouth_x + 2, mouth_y + 1, mouth_x + 5, mouth_y + 2, colors["dark_outline"])

def draw_hair(canvas, x, y, style="comedian", facing="front"):
    """Draw detailed hair with style variations."""
    face_width, face_height = 24, 26
    
    # Apply offset for side-facing
    offset_x = 0
    if facing == "left":
        offset_x = -4
    elif facing == "right":
        offset_x = 4
        
    if style == "comedian":
        # Classic comedian hairstyle with receding hairline
        # Balding top with side hair
        for ix in range(-3, face_width + 3):
            if ix < face_width // 3 - 3 or ix > 2 * face_width // 3 + 3:
                height = 4 - abs(ix - face_width // 2) // 6
                for iy in range(height):
                    hair_color = colors["brown_dark"]
                    if ix > face_width // 2:
                        hair_color = colors["brown"]
                    draw_pixel(canvas, x + ix + offset_x, y - iy - 1, hair_color)
        
        # Hair sides - adjust based on facing
        if facing == "front":
            # Both sides visible
            for iy in range(face_height // 2):
                side_width = 4 if iy < face_height // 4 else 3
                # Left side
                for ix in range(side_width):
                    draw_pixel(canvas, x - ix - 1, y + iy, colors["brown_dark"])
                # Right side
                for ix in range(side_width):
                    draw_pixel(canvas, x + face_width + ix, y + iy, colors["brown"])
        elif facing == "left":
            # Right side hair more visible
            for iy in range(face_height // 2):
                side_width = 5 if iy < face_height // 4 else 4
                for ix in range(side_width):
                    draw_pixel(canvas, x + face_width + ix + offset_x, y + iy, colors["brown"])
        elif facing == "right":
            # Left side hair more visible
            for iy in range(face_height // 2):
                side_width = 5 if iy < face_height // 4 else 4
                for ix in range(side_width):
                    draw_pixel(canvas, x - ix - 1 + offset_x, y + iy, colors["brown_dark"])
                
        # Add some hair texture
        for i in range(0, face_width, 6):
            if i < face_width // 3 - 3 or i > 2 * face_width // 3 + 3:
                draw_line(canvas, x + i + offset_x, y - 1, x + i + 1 + offset_x, y - 3, colors["brown_dark"])

def draw_bow_tie(canvas, x, y, size=10):
    """Draw a fancy bow tie."""
    # Center knot
    draw_rectangle(canvas, x - size//6, y - size//6, size//3, size//3, colors["red_dark"])
    
    # Left bow
    for i in range(size//2):
        for j in range(size//3):
            dx = i - size//4
            dy = j - size//6
            if dx**2 + dy**2 <= (size//3)**2:
                color = colors["red"]
                if i < size//6:
                    color = colors["red_dark"]
                draw_pixel(canvas, x - size//2 - i, y - size//6 + j, color)
    
    # Right bow
    for i in range(size//2):
        for j in range(size//3):
            dx = i - size//4
            dy = j - size//6
            if dx**2 + dy**2 <= (size//3)**2:
                color = colors["red"]
                if i > size//3:
                    color = colors["red_light"]
                draw_pixel(canvas, x + size//2 + i - size//2, y - size//6 + j, color)

# =========================
# IMPROVED PACING ANIMATION
# =========================

def create_pacing_frames(size=CHAR_SIZE, num_frames=4):
    """Create multiple frames for pacing animation in both directions."""
    frames_right = []
    frames_left = []
    
    # Create walking animation frames for right direction
    for frame in range(num_frames):
        canvas = create_blank_canvas(size, size)
        
        # Character positioning variables
        center_x = size // 2
        head_size = 24
        head_x = center_x - head_size // 2
        head_y = size // 4
        
        # Body variables
        body_width = 30
        body_height = 40
        body_x = center_x - body_width // 2
        body_y = head_y + head_size - 5
        
        # Draw detailed suit (jacket)
        draw_outfit(canvas, body_x, body_y, body_width, body_height, 
                   colors["blue"], colors["blue_dark"], colors["blue_light"])
        
        # Draw shirt collar
        collar_width = body_width - 10
        collar_height = 8
        collar_x = body_x + 5
        collar_y = body_y
        draw_rectangle(canvas, collar_x, collar_y, collar_width, collar_height, colors["white"])
        
        # Draw face - facing right for this direction
        draw_face(canvas, head_x, head_y, "neutral", "right")
        
        # Draw hair
        draw_hair(canvas, head_x, head_y, "comedian", "right")
        
        # Draw bow tie
        bow_tie_x = center_x
        bow_tie_y = body_y + 6
        draw_bow_tie(canvas, bow_tie_x, bow_tie_y, 12)
        
        # Draw arms behind back
        arm_width = 6
        arm_height = 25
        arm_gap = 6
        
        # Draw arms meeting at the back
        draw_outfit(canvas, center_x - arm_gap//2 - arm_width, body_y + 8, 
                   arm_width, arm_height, colors["blue"], colors["blue_dark"], colors["blue_light"])
        draw_outfit(canvas, center_x + arm_gap//2, body_y + 8, 
                   arm_width, arm_height, colors["blue"], colors["blue_dark"], colors["blue_light"])
        
        # Hands clasped behind back
        hand_width = 16
        hand_height = 8
        draw_rectangle(canvas, center_x - hand_width//2, body_y + 8 + arm_height - 4, 
                      hand_width, hand_height, colors["skin"])
        
        # Draw legs with animation
        leg_width = 10
        leg_spacing = 3
        
        # Animation parameters
        stride = 8  # Maximum stride length
        leg_offset = int(stride * math.sin(2 * math.pi * frame / num_frames))
        
        # Forward leg
        forward_leg_x = center_x - leg_width - leg_spacing + leg_offset
        draw_rectangle(canvas, forward_leg_x, body_y + body_height - 5, 
                      leg_width, 35, colors["dark_gray"])
        
        # Back leg
        back_leg_x = center_x + leg_spacing - leg_offset
        draw_rectangle(canvas, back_leg_x, body_y + body_height - 5, 
                      leg_width, 35, colors["dark_gray"])
        
        # Draw shoes
        shoe_width = 14
        shoe_height = 6
        
        # Forward shoe
        draw_rectangle(canvas, forward_leg_x - 2, body_y + body_height - 5 + 35 - 1, 
                      shoe_width, shoe_height, colors["brown_dark"])
        
        # Back shoe
        draw_rectangle(canvas, back_leg_x - 2, body_y + body_height - 5 + 35 - 1, 
                      shoe_width, shoe_height, colors["brown_dark"])
        
        # Add final details
        add_noise(canvas, 0, 0, size, size, 0.02)
        
        frames_right.append(canvas)
        
        # Save this frame
        save_image(canvas, f"comedian_pacing_right_{frame+1}.png")
    
    # Create walking animation frames for left direction
    for frame in range(num_frames):
        canvas = create_blank_canvas(size, size)
        
        # Character positioning variables
        center_x = size // 2
        head_size = 24
        head_x = center_x - head_size // 2
        head_y = size // 4
        
        # Body variables
        body_width = 30
        body_height = 40
        body_x = center_x - body_width // 2
        body_y = head_y + head_size - 5
        
        # Draw detailed suit (jacket)
        draw_outfit(canvas, body_x, body_y, body_width, body_height, 
                   colors["blue"], colors["blue_dark"], colors["blue_light"])
        
        # Draw shirt collar
        collar_width = body_width - 10
        collar_height = 8
        collar_x = body_x + 5
        collar_y = body_y
        draw_rectangle(canvas, collar_x, collar_y, collar_width, collar_height, colors["white"])
        
        # Draw face - facing left for this direction
        draw_face(canvas, head_x, head_y, "neutral", "left")
        
        # Draw hair
        draw_hair(canvas, head_x, head_y, "comedian", "left")
        
        # Draw bow tie
        bow_tie_x = center_x
        bow_tie_y = body_y + 6
        draw_bow_tie(canvas, bow_tie_x, bow_tie_y, 12)
        
        # Draw arms behind back
        arm_width = 6
        arm_height = 25
        arm_gap = 6
        
        # Draw arms meeting at the back
        draw_outfit(canvas, center_x - arm_gap//2 - arm_width, body_y + 8, 
                   arm_width, arm_height, colors["blue"], colors["blue_dark"], colors["blue_light"])
        draw_outfit(canvas, center_x + arm_gap//2, body_y + 8, 
                   arm_width, arm_height, colors["blue"], colors["blue_dark"], colors["blue_light"])
        
        # Hands clasped behind back
        hand_width = 16
        hand_height = 8
        draw_rectangle(canvas, center_x - hand_width//2, body_y + 8 + arm_height - 4, 
                      hand_width, hand_height, colors["skin"])
        
        # Draw legs with animation
        leg_width = 10
        leg_spacing = 3
        
        # Animation parameters
        stride = 8  # Maximum stride length
        leg_offset = int(stride * math.sin(2 * math.pi * frame / num_frames))
        
        # Forward leg (reversed for left direction)
        forward_leg_x = center_x + leg_spacing - leg_offset
        draw_rectangle(canvas, forward_leg_x, body_y + body_height - 5, 
                      leg_width, 35, colors["dark_gray"])
        
        # Back leg (reversed for left direction)
        back_leg_x = center_x - leg_width - leg_spacing + leg_offset
        draw_rectangle(canvas, back_leg_x, body_y + body_height - 5, 
                      leg_width, 35, colors["dark_gray"])
        
        # Draw shoes
        shoe_width = 14
        shoe_height = 6
        
        # Forward shoe
        draw_rectangle(canvas, forward_leg_x - 2, body_y + body_height - 5 + 35 - 1, 
                      shoe_width, shoe_height, colors["brown_dark"])
        
        # Back shoe
        draw_rectangle(canvas, back_leg_x - 2, body_y + body_height - 5 + 35 - 1, 
                      shoe_width, shoe_height, colors["brown_dark"])
        
        # Add final details
        add_noise(canvas, 0, 0, size, size, 0.02)
        
        frames_left.append(canvas)
        
        # Save this frame
        save_image(canvas, f"comedian_pacing_left_{frame+1}.png")
    
    return frames_right, frames_left

# =========================
# IMPROVED TALKING ANIMATION
# =========================

def create_talking_frames(size=CHAR_SIZE, num_frames=3):
    """Create multiple frames for talking animation with expressive gestures."""
    frames = []
    
    for frame in range(num_frames):
        canvas = create_blank_canvas(size, size)
        
        # Character positioning variables
        center_x = size // 2
        head_size = 24
        head_x = center_x - head_size // 2
        head_y = size // 4
        
        # Body variables
        body_width = 30
        body_height = 40
        body_x = center_x - body_width // 2
        body_y = head_y + head_size - 5
        
        # Draw detailed suit (jacket)
        draw_outfit(canvas, body_x, body_y, body_width, body_height, 
                   colors["blue"], colors["blue_dark"], colors["blue_light"])
        
        # Draw shirt collar
        collar_width = body_width - 10
        collar_height = 8
        collar_x = body_x + 5
        collar_y = body_y
        draw_rectangle(canvas, collar_x, collar_y, collar_width, collar_height, colors["white"])
        
        # Draw face
        # Different mouth positions for talking
        mouth_expressions = ["talking", "neutral", "talking"]
        draw_face(canvas, head_x, head_y, mouth_expressions[frame % len(mouth_expressions)])
        
        # Draw hair
        draw_hair(canvas, head_x, head_y, "comedian")
        
        # Draw bow tie
        bow_tie_x = center_x
        bow_tie_y = body_y + 6
        draw_bow_tie(canvas, bow_tie_x, bow_tie_y, 12)
        
        # Draw arms with different gestures based on frame
        arm_width = 8
        
        if frame == 0:
            # First frame: One arm pointing upward, other arm relaxed
            # Left arm relaxed
            left_arm_angle = math.pi / 6  # 30 degrees
            left_arm_length = 28
            
            for y in range(left_arm_length):
                x_offset = int(y * math.sin(left_arm_angle))
                y_offset = int(y * math.cos(left_arm_angle))
                
                draw_rectangle(canvas, body_x - arm_width - x_offset, body_y + 5 + y_offset, 
                              arm_width, 4, colors["blue"])
            
            # Right arm pointing up
            right_arm_angle = -math.pi / 2  # -90 degrees (straight up)
            right_arm_length = 30
            
            for y in range(right_arm_length):
                x_offset = int(y * math.sin(right_arm_angle))
                y_offset = int(y * math.cos(right_arm_angle))
                
                draw_rectangle(canvas, body_x + body_width + x_offset, body_y + 5 + y_offset, 
                              arm_width, 4, colors["blue"])
            
            # Hands
            # Left hand
            left_hand_x = body_x - arm_width - int(left_arm_length * math.sin(left_arm_angle))
            left_hand_y = body_y + 5 + int(left_arm_length * math.cos(left_arm_angle))
            draw_rectangle(canvas, left_hand_x - 10, left_hand_y - 5, 
                          10, 10, colors["skin"])
            
            # Right hand
            right_hand_x = body_x + body_width + int(right_arm_length * math.sin(right_arm_angle))
            right_hand_y = body_y + 5 + int(right_arm_length * math.cos(right_arm_angle))
            draw_rectangle(canvas, right_hand_x - 5, right_hand_y - 10, 
                          10, 10, colors["skin"])
            
        elif frame == 1:
            # Second frame: Both arms gesturing outward
            # Left arm out
            left_arm_angle = math.pi / 4  # 45 degrees
            left_arm_length = 30
            
            for y in range(left_arm_length):
                x_offset = int(y * math.sin(left_arm_angle))
                y_offset = int(y * math.cos(left_arm_angle))
                
                draw_rectangle(canvas, body_x - arm_width - x_offset, body_y + 5 + y_offset, 
                              arm_width, 4, colors["blue"])
            
            # Right arm out
            right_arm_angle = -math.pi / 4  # -45 degrees
            right_arm_length = 30
            
            for y in range(right_arm_length):
                x_offset = int(y * math.sin(right_arm_angle))
                y_offset = int(y * math.cos(right_arm_angle))
                
                draw_rectangle(canvas, body_x + body_width + x_offset, body_y + 5 + y_offset, 
                              arm_width, 4, colors["blue"])
            
            # Hands
            # Left hand
            left_hand_x = body_x - arm_width - int(left_arm_length * math.sin(left_arm_angle))
            left_hand_y = body_y + 5 + int(left_arm_length * math.cos(left_arm_angle))
            draw_rectangle(canvas, left_hand_x - 10, left_hand_y - 5, 
                          10, 10, colors["skin"])
            
            # Right hand
            right_hand_x = body_x + body_width + int(right_arm_length * math.sin(right_arm_angle))
            right_hand_y = body_y + 5 + int(right_arm_length * math.cos(right_arm_angle))
            draw_rectangle(canvas, right_hand_x, right_hand_y - 5, 
                          10, 10, colors["skin"])
            
        elif frame == 2:
            # Third frame: One arm forward in explanation
            # Left arm relaxed
            left_arm_angle = math.pi / 12  # 15 degrees
            left_arm_length = 25
            
            for y in range(left_arm_length):
                x_offset = int(y * math.sin(left_arm_angle))
                y_offset = int(y * math.cos(left_arm_angle))
                
                draw_rectangle(canvas, body_x - arm_width - x_offset, body_y + 5 + y_offset, 
                              arm_width, 4, colors["blue"])
            
            # Right arm forward
            right_arm_angle = -math.pi / 12  # -15 degrees
            right_arm_length = 25
            
            for y in range(right_arm_length):
                x_offset = int(y * math.sin(right_arm_angle))
                y_offset = int(y * math.cos(right_arm_angle))
                
                # First part of arm
                draw_rectangle(canvas, body_x + body_width + x_offset, body_y + 5 + y_offset, 
                              arm_width, 4, colors["blue"])
            
            # Second part of right arm (bent)
            second_arm_angle = 0  # straight forward
            second_arm_length = 15
            second_arm_start_x = body_x + body_width + int(right_arm_length * math.sin(right_arm_angle))
            second_arm_start_y = body_y + 5 + int(right_arm_length * math.cos(right_arm_angle))
            
            for y in range(second_arm_length):
                x_offset = int(y * math.sin(second_arm_angle))
                y_offset = int(y * math.cos(second_arm_angle))
                
                draw_rectangle(canvas, second_arm_start_x + x_offset, second_arm_start_y + y_offset, 
                              arm_width, 4, colors["blue"])
            
            # Hands
            # Left hand
            left_hand_x = body_x - arm_width - int(left_arm_length * math.sin(left_arm_angle))
            left_hand_y = body_y + 5 + int(left_arm_length * math.cos(left_arm_angle))
            draw_rectangle(canvas, left_hand_x - 10, left_hand_y - 5, 
                          10, 10, colors["skin"])
            
            # Right hand
            right_hand_x = second_arm_start_x + int(second_arm_length * math.sin(second_arm_angle))
            right_hand_y = second_arm_start_y + int(second_arm_length * math.cos(second_arm_angle))
            draw_rectangle(canvas, right_hand_x, right_hand_y - 5, 
                          10, 10, colors["skin"])
        
        # Draw legs
        leg_width = 10
        leg_gap = 5
        
        # Left leg
        draw_rectangle(canvas, center_x - leg_width - leg_gap//2, body_y + body_height - 5, 
                      leg_width, 35, colors["dark_gray"])
        
        # Right leg
        draw_rectangle(canvas, center_x + leg_gap//2, body_y + body_height - 5, 
                      leg_width, 35, colors["dark_gray"])
        
        # Draw shoes
        shoe_width = 14
        shoe_height = 6
        
        # Left shoe
        draw_rectangle(canvas, center_x - leg_width - leg_gap//2 - 2, 
                      body_y + body_height - 5 + 35 - 1, 
                      shoe_width, shoe_height, colors["brown_dark"])
        
        # Right shoe
        draw_rectangle(canvas, center_x + leg_gap//2 - 2, 
                      body_y + body_height - 5 + 35 - 1, 
                      shoe_width, shoe_height, colors["brown_dark"])
        
        # Add final details
        add_noise(canvas, 0, 0, size, size, 0.02)
        
        frames.append(canvas)
        
        # Save this frame
        save_image(canvas, f"comedian_talking_{frame+1}.png")
    
    return frames

# =========================
# IMPROVED LAUGHING ANIMATION
# =========================

def create_laughing_frames(size=CHAR_SIZE, num_frames=3):
    """Create multiple frames for laughing animation with expressive body movement."""
    frames = []
    
    for frame in range(num_frames):
        canvas = create_blank_canvas(size, size)
        
        # Character positioning variables with slight up/down movement for laughter
        center_x = size // 2
        vertical_bounce = int(3 * math.sin(2 * math.pi * frame / num_frames))
        
        head_size = 24
        head_x = center_x - head_size // 2
        head_y = size // 4 + vertical_bounce
        
        # Body variables
        body_width = 30
        body_height = 40
        body_x = center_x - body_width // 2
        body_y = head_y + head_size - 5
        
        # Draw detailed suit (jacket)
        draw_outfit(canvas, body_x, body_y, body_width, body_height, 
                   colors["blue"], colors["blue_dark"], colors["blue_light"])
        
        # Draw shirt collar
        collar_width = body_width - 10
        collar_height = 8
        collar_x = body_x + 5
        collar_y = body_y
        draw_rectangle(canvas, collar_x, collar_y, collar_width, collar_height, colors["white"])
        
        # Draw face with laughing expression
        draw_face(canvas, head_x, head_y, "laughing")
        
        # Draw hair
        draw_hair(canvas, head_x, head_y, "comedian")
        
        # Draw bow tie
        bow_tie_x = center_x
        bow_tie_y = body_y + 6
        draw_bow_tie(canvas, bow_tie_x, bow_tie_y, 12)
        
        # Draw arms with different gestures based on frame for laughing animation
        arm_width = 8
        
        # Animation parameters
        laugh_intensity = 0.8 + 0.2 * math.sin(2 * math.pi * frame / num_frames)  # 0.8-1.0 range
        
        # Left arm raised and moving
        left_arm_angle = math.pi / 3 * laugh_intensity  # 60 degrees * intensity
        left_arm_length = 30
        
        for y in range(left_arm_length):
            x_offset = int(y * math.sin(left_arm_angle))
            y_offset = int(y * math.cos(left_arm_angle))
            
            draw_rectangle(canvas, body_x - arm_width - x_offset, body_y + 5 - y_offset, 
                          arm_width, 4, colors["blue"])
        
        # Right arm raised and moving
        right_arm_angle = -math.pi / 3 * laugh_intensity  # -60 degrees * intensity
        right_arm_length = 30
        
        for y in range(right_arm_length):
            x_offset = int(y * math.sin(right_arm_angle))
            y_offset = int(y * math.cos(right_arm_angle))
            
            draw_rectangle(canvas, body_x + body_width + x_offset, body_y + 5 - y_offset, 
                          arm_width, 4, colors["blue"])
        
        # Hands with slight movement
        hand_size = 10
        
        # Left hand
        left_hand_x = body_x - arm_width - int(left_arm_length * math.sin(left_arm_angle))
        left_hand_y = body_y + 5 - int(left_arm_length * math.cos(left_arm_angle))
        draw_rectangle(canvas, left_hand_x - hand_size, left_hand_y - hand_size // 2, 
                      hand_size, hand_size, colors["skin"])
        
        # Right hand
        right_hand_x = body_x + body_width + int(right_arm_length * math.sin(right_arm_angle))
        right_hand_y = body_y + 5 - int(right_arm_length * math.cos(right_arm_angle))
        draw_rectangle(canvas, right_hand_x, right_hand_y - hand_size // 2, 
                      hand_size, hand_size, colors["skin"])
        
        # Draw legs with slight knee bend for laughing animation
        leg_width = 10
        leg_gap = 5
        
        # Animation for legs (slight bend at knees)
        knee_bend = int(3 * laugh_intensity)
        
        # Left leg
        left_leg_x = center_x - leg_width - leg_gap//2
        left_leg_upper_height = 20 - knee_bend
        draw_rectangle(canvas, left_leg_x, body_y + body_height - 5, 
                      leg_width, left_leg_upper_height, colors["dark_gray"])
        
        # Left leg lower part (bent at knee)
        left_leg_lower_x = left_leg_x - knee_bend
        draw_rectangle(canvas, left_leg_lower_x, body_y + body_height - 5 + left_leg_upper_height, 
                      leg_width, 35 - left_leg_upper_height, colors["dark_gray"])
        
        # Right leg
        right_leg_x = center_x + leg_gap//2
        right_leg_upper_height = 20 - knee_bend
        draw_rectangle(canvas, right_leg_x, body_y + body_height - 5, 
                      leg_width, right_leg_upper_height, colors["dark_gray"])
        
        # Right leg lower part (bent at knee)
        right_leg_lower_x = right_leg_x + knee_bend
        draw_rectangle(canvas, right_leg_lower_x, body_y + body_height - 5 + right_leg_upper_height, 
                      leg_width, 35 - right_leg_upper_height, colors["dark_gray"])
        
        # Draw shoes
        shoe_width = 14
        shoe_height = 6
        
        # Left shoe
        draw_rectangle(canvas, left_leg_lower_x - 2, 
                      body_y + body_height - 5 + 35 - 1, 
                      shoe_width, shoe_height, colors["brown_dark"])
        
        # Right shoe
        draw_rectangle(canvas, right_leg_lower_x - 2, 
                      body_y + body_height - 5 + 35 - 1, 
                      shoe_width, shoe_height, colors["brown_dark"])
        
        # Add "haha" text bubble for laughing animation (only on certain frames)
        if frame == 1:
            laugh_text_x = head_x + head_size + 5
            laugh_text_y = head_y - 10
            
            # Simple speech bubble
            bubble_width = 30
            bubble_height = 15
            
            # Bubble outline
            for y in range(-1, bubble_height + 1):
                for x in range(-1, bubble_width + 1):
                    if (y == -1 or y == bubble_height or x == -1 or x == bubble_width):
                        draw_pixel(canvas, laugh_text_x + x, laugh_text_y + y, colors["black"])
            
            # Bubble fill
            for y in range(bubble_height):
                for x in range(bubble_width):
                    draw_pixel(canvas, laugh_text_x + x, laugh_text_y + y, colors["white"])
            
            # Draw "HA!" text
            text_pixels = [
                # H
                (3, 3), (3, 4), (3, 5), (3, 6), (3, 7),
                (4, 5),
                (5, 3), (5, 4), (5, 5), (5, 6), (5, 7),
                # A
                (8, 7), (8, 6), (8, 5), (8, 4),
                (9, 3), (9, 5),
                (10, 7), (10, 6), (10, 5), (10, 4),
                # !
                (13, 3), (13, 4), (13, 5), (13, 7)
            ]
            
            for x, y in text_pixels:
                draw_pixel(canvas, laugh_text_x + x, laugh_text_y + y, colors["black"])
        
        # Add final details
        add_noise(canvas, 0, 0, size, size, 0.02)
        
        frames.append(canvas)
        
        # Save this frame
        save_image(canvas, f"comedian_laughing_{frame+1}.png")
    
    return frames

def create_curtain():
    """Create a detailed theater curtain with folds and texture."""
    width, height = 256, 512
    canvas = create_blank_canvas(width, height)
    
    # Create a more realistic curtain with deeper folds
    for x in range(width):
        for y in range(height):
            # Create multiple wave patterns for more realistic folds
            major_fold = 15 * math.sin(y / 60) + 8 * math.sin(y / 30 + 2)
            minor_fold = 5 * math.sin(y / 15 + x / 40) + 3 * math.sin(y / 8)
            fold_pattern = major_fold + minor_fold
            
            # Calculate distance from center for shadow effect
            center_distance = abs(x - width / 2) / (width / 2)
            shadow_factor = center_distance * 0.7  # 0-0.7 range for shadow
            
            # Base color
            color = list(colors["curtain_red"])
            
            # Apply fold shading
            if fold_pattern > 10:
                # Deep fold (shadow)
                color = list(colors["curtain_dark"])
            elif fold_pattern > 5:
                # Medium fold
                color = [max(0, c - int(50 * shadow_factor)) for c in color[:3]] + [255]
            elif fold_pattern < -5:
                # Highlight
                color = list(colors["curtain_highlight"])
                color = [min(255, c + int(30 * (1 - shadow_factor))) for c in color[:3]] + [255]
            else:
                # Normal with slight shadow gradient
                color = [max(0, c - int(30 * shadow_factor)) for c in color[:3]] + [255]
            
            draw_pixel(canvas, x, y, tuple(color))
    
    # Add curtain top
    rod_height = 15
    for y in range(rod_height):
        for x in range(width):
            # Rod gradient
            if y < rod_height // 3:
                color = colors["light_gray"]
            elif y < 2 * rod_height // 3:
                color = colors["gray"]
            else:
                color = colors["dark_gray"]
            
            # Add highlight
            if x % 30 < 5 and y < rod_height // 2:
                color = colors["lighter_gray"]
                
            draw_pixel(canvas, x, y, color)
    
    # Add curtain ties and details
    tie_positions = [(30, 100), (40, 250), (50, 400)]
    for pos_x, pos_y in tie_positions:
        # Gold/yellow tie rope
        rope_width, rope_height = 20, 30
        
        # Draw fancy rope
        for y in range(rope_height):
            rope_curve = 5 * math.sin(y / 5)
            for x in range(rope_width):
                dist = abs(x - rope_width / 2 - rope_curve)
                if dist < 4:
                    color = colors["gold"] if dist < 2 else colors["yellow_dark"]
                    draw_pixel(canvas, pos_x + x, pos_y + y, color)
        
        # Rope tassel
        tassel_width, tassel_height = 16, 15
        for y in range(tassel_height):
            for x in range(tassel_width):
                if (x + y) % 4 < 2:  # Create a pattern
                    draw_pixel(canvas, pos_x + rope_width // 2 - tassel_width // 2 + x, 
                              pos_y + rope_height + y, colors["gold"])
    
    # Save left and right curtains separately
    left_curtain = canvas.copy()
    right_curtain = np.flip(canvas, axis=1).copy()
    
    save_image(left_curtain, "curtain_left.png")
    save_image(right_curtain, "curtain_right.png")
    
    # Also save the full curtain
    save_image(canvas, "curtain.png")
    
    return canvas

def create_sample_jokes():
    """Create an expanded set of dad jokes in JSON format."""
    jokes = [
        {"joke": "Why don't scientists trust atoms?", "punchline": False},
        {"joke": "Because they make up everything!", "punchline": True},
        
        {"joke": "Did you hear about the mathematician who's afraid of negative numbers?", "punchline": False},
        {"joke": "He'll stop at nothing to avoid them!", "punchline": True},
        
        {"joke": "I told my wife she was drawing her eyebrows too high.", "punchline": False},
        {"joke": "She looked surprised!", "punchline": True},
        
        {"joke": "What do you call a fake noodle?", "punchline": False},
        {"joke": "An impasta!", "punchline": True},
        
        {"joke": "How do you organize a space party?", "punchline": False},
        {"joke": "You planet!", "punchline": True},
        
        {"joke": "Why don't eggs tell jokes?", "punchline": False},
        {"joke": "They'd crack each other up!", "punchline": True},
        
        {"joke": "I'm reading a book on anti-gravity.", "punchline": False},
        {"joke": "It's impossible to put down!", "punchline": True},
        
        {"joke": "What do you call a lazy kangaroo?", "punchline": False},
        {"joke": "A pouch potato!", "punchline": True},
        
        {"joke": "How does a penguin build its house?", "punchline": False},
        {"joke": "Igloos it together!", "punchline": True},
        
        {"joke": "What did the janitor say when he jumped out of the closet?", "punchline": False},
        {"joke": "Supplies!", "punchline": True},
        
        {"joke": "Why did the scarecrow win an award?", "punchline": False},
        {"joke": "Because he was outstanding in his field!", "punchline": True},
        
        {"joke": "Why don't skeletons fight each other?", "punchline": False},
        {"joke": "They don't have the guts!", "punchline": True},
        
        {"joke": "What's the best time to go to the dentist?", "punchline": False},
        {"joke": "Tooth-hurty!", "punchline": True},
        
        {"joke": "I tried to catch some fog earlier.", "punchline": False},
        {"joke": "I mist.", "punchline": True},
        
        {"joke": "Why did the golfer bring two pairs of pants?", "punchline": False},
        {"joke": "In case he got a hole in one!", "punchline": True},
        
        {"joke": "What do you call a cow with no legs?", "punchline": False},
        {"joke": "Ground beef!", "punchline": True},
        
        {"joke": "I used to play piano by ear...", "punchline": False},
        {"joke": "Now I use my hands!", "punchline": True},
        
        {"joke": "What did the ocean say to the beach?", "punchline": False},
        {"joke": "Nothing, it just waved!", "punchline": True},
        
        {"joke": "I'm on a seafood diet...", "punchline": False},
        {"joke": "I see food and I eat it!", "punchline": True}
    ]
    
    with open(os.path.join(output_dir, "dadJokes.json"), "w") as f:
        json.dump(jokes, f, indent=2)
    
    print("Created expanded dad jokes JSON file with multiple joke formats")

# Generate all assets
def generate_all_assets():
    """Generate all assets for the improved comedian animation."""
    print("Generating enhanced pixel art comedian assets with multi-frame animations...")
    
    # Generate pacing animation frames (4 frames each direction)
    print("\nGenerating pacing animation frames...")
    create_pacing_frames(CHAR_SIZE, 4)
    
    # Generate talking animation frames (3 frames)
    print("\nGenerating talking animation frames...")
    create_talking_frames(CHAR_SIZE, 3)
    
    # Generate laughing animation frames (3 frames)
    print("\nGenerating laughing animation frames...")
    create_laughing_frames(CHAR_SIZE, 3)
    
    # Generate environment assets
    print("\nGenerating environment assets...")
    create_curtain()
    
    # Generate the jokes
    print("\nGenerating joke content...")
    create_sample_jokes()
    
    print("\nAll enhanced assets generated successfully!")
    print(f"Assets saved to: {os.path.abspath(output_dir)}")

if __name__ == "__main__":
    generate_all_assets()