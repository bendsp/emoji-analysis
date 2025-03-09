#!/usr/bin/env python3
import sys
import AppKit

def render_emoji(emoji, output_path, font_size=128):
    # Use the Apple Color Emoji via the system font
    font = AppKit.NSFont.systemFontOfSize_(font_size)
    attributes = {AppKit.NSFontAttributeName: font}
    attr_str = AppKit.NSAttributedString.alloc().initWithString_attributes_(emoji, attributes)
    
    # Fixed image size
    image_size = (128, 128)
    image = AppKit.NSImage.alloc().initWithSize_(image_size)
    
    # Get actual text size for centering
    text_size = attr_str.size()
    text_x = (image_size[0] - text_size.width) / 2
    text_y = (image_size[1] - text_size.height) / 2

    # Render emoji onto the fixed-size image
    image.lockFocus()
    attr_str.drawAtPoint_((text_x, text_y))
    image.unlockFocus()

    # Save as PNG
    tiff_data = image.TIFFRepresentation()
    bitmap = AppKit.NSBitmapImageRep.imageRepWithData_(tiff_data)
    png_data = bitmap.representationUsingType_properties_(AppKit.NSPNGFileType, {})
    png_data.writeToFile_atomically_(output_path, True)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python render_emoji.py <emoji> <output_file>")
        sys.exit(1)
    render_emoji(sys.argv[1], sys.argv[2])