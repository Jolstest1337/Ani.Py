import os
import cv2
import json
import base64
from PIL import Image
from tqdm import tqdm
import io
import time
import sys
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame

ASCII_CHARS = "@%#*+=-:. "
RUSSIAN_CHARS = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
JAPANESE_CHARS = "美しい世界"
KOREAN_CHARS = "가각간갇갈감갑강개갠갤갭갯갰갱갸갹갺갻강갔강갗갘같갚갛"
GREEK_CHARS = "αβγδεζηθικλμνξοπρστυφχψω"
FRENCH_CHARS = "àâçéèêëîïôûùüÿœæ"
ITALIAN_CHARS = "àèéìòù"

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def extract_frames(video_path, output_folder):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_filename = os.path.join(output_folder, f"frame_{frame_count:04d}.jpg")
        cv2.imwrite(frame_filename, frame)
        frame_count += 1

        progress_percentage = (frame_count / total_frames) * 100
        print(f"Converting: {frame_count}/{total_frames} frames ({progress_percentage:.2f}%)", end='\r')

    cap.release()
    print(f"\nExtracted {frame_count} frames to {output_folder}")

def jpg_to_json(folder_name):
    base_dir = os.path.abspath(os.path.dirname(__file__))
    jpg_folder = os.path.join(base_dir, 'JPG')
    json_folder = os.path.join(base_dir, 'Json')

    if not os.path.exists(jpg_folder):
        print("The 'JPG' folder was not found.")
        return
    
    if not os.path.exists(json_folder):
        os.makedirs(json_folder)
    
    target_jpg_dir = os.path.join(jpg_folder, folder_name)
    target_json_dir = os.path.join(json_folder, folder_name)
    
    if not os.path.exists(target_jpg_dir):
        print(f"The folder '{folder_name}' does not exist in the JPG directory.")
        return
    
    if not os.path.exists(target_json_dir):
        os.makedirs(target_json_dir)
    
    jpg_files = [f for f in os.listdir(target_jpg_dir) if f.lower().endswith('.jpg')]
    
    if not jpg_files:
        print(f"No .jpg files found in '{folder_name}'.")
        return
    
    all_images_data = []
    
    for jpg_file in tqdm(jpg_files, desc="Converting JPGs to JSON", unit="file"):
        jpg_file_path = os.path.join(target_jpg_dir, jpg_file)
        
        with open(jpg_file_path, "rb") as image_file:
            base64_string = base64.b64encode(image_file.read()).decode('utf-8')
        
        all_images_data.append(base64_string)
    
    json_file_path = os.path.join(target_json_dir, 'Frame.json')
    
    with open(json_file_path, 'w') as json_file:
        json.dump(all_images_data, json_file, indent=4)
    
    print(f"Conversion completed for folder: {folder_name}")

def play_audio(file_path):
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

def resize_image(image, new_width=167, new_height=50):
    (original_width, original_height) = image.size
    aspect_ratio = original_height / float(original_width)
    
    new_height_aspect = int(new_width * aspect_ratio)
    
    if new_height_aspect > new_height:
        image = image.resize((new_width, new_height))
    else:
        image = image.resize((new_width, new_height_aspect))
    
    image = image.resize((new_width, new_height))
    return image

def grayify(image):
    grayscale_image = image.convert("L")
    return grayscale_image

def pixels_to_ascii(image):
    pixels = image.getdata()
    ascii_str = ""
    for pixel in pixels:
        index = pixel * (len(ASCII_CHARS) - 1) // 255
        ascii_str += ASCII_CHARS[index]
    return ascii_str

def image_to_ascii(image, width=167, height=50):
    image = resize_image(image, width, height)
    image = grayify(image)
    ascii_str = pixels_to_ascii(image)
    img_width = image.width
    ascii_str_len = len(ascii_str)
    ascii_img = ""

    for i in range(0, ascii_str_len, img_width):
        ascii_img += ascii_str[i:i + img_width] + "\n"

    return ascii_img

def image_to_chinese_ascii(image, width=84, height=50, chars='美丽的世界'):
    # Resize image to fit the ASCII output dimensions
    image = image.resize((width, height))
    image = image.convert('L')  # Convert to grayscale

    ascii_str = ''
    char_count = len(chars)
    
    for y in range(height):
        for x in range(width):
            pixel = image.getpixel((x, y))
            # Map pixel value to a character in 'chars'
            ascii_char = chars[int(pixel / 256 * (char_count - 1))]
            ascii_str += ascii_char
        ascii_str += '\n'
    
    return ascii_str

def image_to_russian_ascii(image, width=84, height=50):
    image = image.resize((width, height))
    image = image.convert('L')
    ascii_str = ''
    char_count = len(RUSSIAN_CHARS)
    
    for y in range(height):
        for x in range(width):
            pixel = image.getpixel((x, y))
            ascii_char = RUSSIAN_CHARS[int(pixel / 256 * (char_count - 1))]
            ascii_str += ascii_char
        ascii_str += '\n'
    
    return ascii_str

def image_to_japanese_ascii(image, width=84, height=50):
    image = image.resize((width, height))
    image = image.convert('L')
    ascii_str = ''
    char_count = len(JAPANESE_CHARS)
    
    for y in range(height):
        for x in range(width):
            pixel = image.getpixel((x, y))
            ascii_char = JAPANESE_CHARS[int(pixel / 256 * (char_count - 1))]
            ascii_str += ascii_char
        ascii_str += '\n'
    
    return ascii_str

def image_to_korean_ascii(image, width=84, height=50):
    image = image.resize((width, height))
    image = image.convert('L')
    ascii_str = ''
    char_count = len(KOREAN_CHARS)
    
    for y in range(height):
        for x in range(width):
            pixel = image.getpixel((x, y))
            ascii_char = KOREAN_CHARS[int(pixel / 256 * (char_count - 1))]
            ascii_str += ascii_char
        ascii_str += '\n'
    
    return ascii_str

def image_to_greek_ascii(image, width=84, height=50):
    image = image.resize((width, height))
    image = image.convert('L')
    ascii_str = ''
    char_count = len(GREEK_CHARS)
    
    for y in range(height):
        for x in range(width):
            pixel = image.getpixel((x, y))
            ascii_char = GREEK_CHARS[int(pixel / 256 * (char_count - 1))]
            ascii_str += ascii_char
        ascii_str += '\n'
    
    return ascii_str

def image_to_french_ascii(image, width=168, height=50):
    image = image.resize((width, height))
    image = image.convert('L')
    ascii_str = ''
    char_count = len(FRENCH_CHARS)
    
    for y in range(height):
        for x in range(width):
            pixel = image.getpixel((x, y))
            ascii_char = FRENCH_CHARS[int(pixel / 256 * (char_count - 1))]
            ascii_str += ascii_char
        ascii_str += '\n'
    
    return ascii_str

def image_to_italian_ascii(image, width=168, height=50):
    image = image.resize((width, height))
    image = image.convert('L')
    ascii_str = ''
    char_count = len(ITALIAN_CHARS)
    
    for y in range(height):
        for x in range(width):
            pixel = image.getpixel((x, y))
            ascii_char = ITALIAN_CHARS[int(pixel / 256 * (char_count - 1))]
            ascii_str += ascii_char
        ascii_str += '\n'
    
    return ascii_str

def play_animation(images, fps=15, ascii_func=image_to_ascii):
    delay = 1 / fps
    start_time = time.time()
    frame_count = 0

    while True:
        for image in images:
            ascii_art = ascii_func(image)
            display_frame(ascii_art)
            
            frame_count += 1
            expected_time = start_time + frame_count * delay
            sleep_time = expected_time - time.time()

            if sleep_time > 0:
                time.sleep(sleep_time)

def load_images_from_json(json_file_path):
    with open(json_file_path, 'r') as f:
        data = json.load(f)
    
    images = []
    for image_data in data:
        image = base64.b64decode(image_data)
        images.append(Image.open(io.BytesIO(image)))
    
    return images

def display_frame(ascii_art):
    sys.stdout.write(ascii_art)
    sys.stdout.flush()

def loading_screen():
    print("読み込み中...")
    for _ in tqdm(range(100), desc="Loading", bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt}"):
        time.sleep(0.05)
    print("\n")

def main():
    pygame.mixer.init()
    while True:
        clear_terminal()
        print("░█████╗░ ███╗░░██╗ ██╗ ░░░ ██████╗░ ██╗░░░██╗")
        print("██╔══██╗ ████╗░██║ ██║ ░░░ ██╔══██╗ ╚██╗░██╔╝")
        print("███████║ ██╔██╗██║ ██║ ░░░ ██████╔╝ ░╚████╔╝░")
        print("██╔══██║ ██║╚████║ ██║ ░░░ ██╔═══╝░ ░░╚██╔╝░░")
        print("██║░░██║ ██║░╚███║ ██║ ██╗ ██║░░░░░ ░░░██║░░░")
        print("╚═╝░░╚═╝ ╚═╝░░╚══╝ ╚═╝ ╚═╝ ╚═╝░░░░░ ░░░╚═╝░░░")
        print("\n[1] Use MP4 to JPG")
        print("[2] Use JPG to Json")
        print("[3] Play Animation")
        print("[4] Exit")

        choice = input("Enter your choice: ").strip()
        if choice == '1':
            clear_terminal()
            print("░█████╗░ ███╗░░██╗ ██╗ ░░░ ██████╗░ ██╗░░░██╗")
            print("██╔══██╗ ████╗░██║ ██║ ░░░ ██╔══██╗ ╚██╗░██╔╝")
            print("███████║ ██╔██╗██║ ██║ ░░░ ██████╔╝ ░╚████╔╝░")
            print("██╔══██║ ██║╚████║ ██║ ░░░ ██╔═══╝░ ░░╚██╔╝░░")
            print("██║░░██║ ██║░╚███║ ██║ ██╗ ██║░░░░░ ░░░██║░░░")
            print("╚═╝░░╚═╝ ╚═╝░░╚══╝ ╚═╝ ╚═╝ ╚═╝░░░░░ ░░░╚═╝░░░")
            video_name = input("Enter the name of the video file (without extension): ")
            video_path = os.path.join("mp", f"{video_name}.mp4")

            if not os.path.exists(video_path):
                print(f"Error: The file {video_path} does not exist.")
            else:
                output_folder = os.path.join("JPG", video_name)
                extract_frames(video_path, output_folder)
                input("\nPress Enter to continue...")
        
        elif choice == '2':
            clear_terminal()
            print("░█████╗░ ███╗░░██╗ ██╗ ░░░ ██████╗░ ██╗░░░██╗")
            print("██╔══██╗ ████╗░██║ ██║ ░░░ ██╔══██╗ ╚██╗░██╔╝")
            print("███████║ ██╔██╗██║ ██║ ░░░ ██████╔╝ ░╚████╔╝░")
            print("██╔══██║ ██║╚████║ ██║ ░░░ ██╔═══╝░ ░░╚██╔╝░░")
            print("██║░░██║ ██║░╚███║ ██║ ██╗ ██║░░░░░ ░░░██║░░░")
            print("╚═╝░░╚═╝ ╚═╝░░╚══╝ ╚═╝ ╚═╝ ╚═╝░░░░░ ░░░╚═╝░░░")
            folder_name = input("Enter the folder name inside 'JPG': ")
            jpg_to_json(folder_name)
            input("\nPress Enter to continue...")
        
        elif choice == '3':
            clear_terminal()
            print("░█████╗░ ███╗░░██╗ ██╗ ░░░ ██████╗░ ██╗░░░██╗")
            print("██╔══██╗ ████╗░██║ ██║ ░░░ ██╔══██╗ ╚██╗░██╔╝")
            print("███████║ ██╔██╗██║ ██║ ░░░ ██████╔╝ ░╚████╔╝░")
            print("██╔══██║ ██║╚████║ ██║ ░░░ ██╔═══╝░ ░░╚██╔╝░░")
            print("██║░░██║ ██║░╚███║ ██║ ██╗ ██║░░░░░ ░░░██║░░░")
            print("╚═╝░░╚═╝ ╚═╝░░╚══╝ ╚═╝ ╚═╝ ╚═╝░░░░░ ░░░╚═╝░░░")
            subfolder_name = input("Enter the subfolder name inside 'Json': ")
            print("Rendering animation...")
            base_dir = os.path.abspath(os.path.dirname(__file__))
            json_file_path = os.path.join(base_dir, 'Json', subfolder_name, 'Frame.json')

            if not os.path.exists(json_file_path):
                print(f"The file 'Frame.json' does not exist in the subfolder '{subfolder_name}' in the 'Json' directory.")
                input("\nPress Enter to continue...")
                continue

            
            
            images = load_images_from_json(json_file_path)
            
            if images:
                sound_choice = input("Do you want sound? (Y/N): ").strip().upper()
                if sound_choice == 'Y':
                    sound_file = input("Enter the full sound file name: ")
                    sound_file_path = os.path.join(base_dir, 'sound', sound_file)
                    if os.path.exists(sound_file_path):
                        print("Found the audio!")
                    else:
                        print(f"The sound file '{sound_file}' does not exist in the 'sound' directory.")
                        sound_choice = 'N'
                elif sound_choice == 'N':
                    print("Continuing without sound.")
                
                print("Select Animation Mode:")
                print("[1] Default")
                print("[2] Chinese")
                print("[3] Russian")
                print("[4] Japanese")
                print("[5] Korean")
                print("[6] Greek")
                print("[7] French")
                print("[8] Italian")
                char_choice = input("Enter your choice: ").strip()

                if char_choice == '1':
                    ascii_func = image_to_ascii
                elif char_choice == '2':
                    ascii_func = image_to_chinese_ascii
                elif char_choice == '3':
                    ascii_func = image_to_russian_ascii
                elif char_choice == '4':
                    ascii_func = image_to_japanese_ascii
                elif char_choice == '5':
                    ascii_func = image_to_korean_ascii
                elif char_choice == '6':
                    ascii_func = image_to_greek_ascii
                elif char_choice == '7':
                    ascii_func = image_to_french_ascii
                elif char_choice == '8':
                    ascii_func = image_to_italian_ascii
                else:
                    print("Invalid choice. Using default characters.")
                    ascii_func = image_to_ascii

                fps = int(input("Enter the FPS to run the animation: "))
                
                clear_terminal()
                loading_screen()
                
                if sound_choice == 'Y':
                    play_audio(sound_file_path)
                
                play_animation(images, fps=fps, ascii_func=ascii_func)
            else:
                print("No images found to display.")
                input("\nPress Enter to continue...")
        
        elif choice == '4':
            break
        
        else:
            print("Invalid choice. Please try again.")
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
