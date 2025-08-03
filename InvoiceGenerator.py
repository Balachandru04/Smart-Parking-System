from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import os

class InvoiceGenerator:
    def __init__(self, vehicle_data):  
        self.vehicle_data = vehicle_data
        self.output_dir = "./invoices"
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_invoice(self):
        name = self.vehicle_data["name"]
        vehicle_no = self.vehicle_data["vehicle_no"]
        entry_time = datetime.strptime(self.vehicle_data["entry_time"], "%Y-%m-%d %H:%M:%S")
        exit_time = datetime.strptime(self.vehicle_data["exit_time"], "%Y-%m-%d %H:%M:%S")

        duration = (exit_time - entry_time).total_seconds() / 3600  # Duration in hours
        charge_per_hour = 20  # Fixed charge per hour
        total_charge = round(duration * charge_per_hour, 2)

        # Create a blank white image using Pillow
        width, height = 600, 400
        image = Image.new("RGB", (width, height), color="white")
        draw = ImageDraw.Draw(image)

        # Set font (Times New Roman)
        try:
            font_path = "C:/Windows/Fonts/times.ttf"
            title_font = ImageFont.truetype(font_path, 28)
            text_font = ImageFont.truetype(font_path, 20)
        except IOError:
            title_font = ImageFont.load_default()
            text_font = ImageFont.load_default()

        # Title
        title_text = "ABC Parking"
        title_bbox = draw.textbbox((0, 0), title_text, font=title_font)
        title_width = title_bbox[2] - title_bbox[0]
        draw.text(((width - title_width) // 2, 40), title_text, font=title_font, fill="black")

        # Details with padded labels
        label_width = 18  # Adjust this width to align colons
        lines = [
            f"{'Vehicle Number'.ljust(label_width)}: {vehicle_no}",
            f"{'In Time'.ljust(label_width)}: {entry_time.strftime('%Y-%m-%d %H:%M:%S')}",
            f"{'Out Time'.ljust(label_width)}: {exit_time.strftime('%Y-%m-%d %H:%M:%S')}",
            f"{'Duration (hrs)'.ljust(label_width)}: {duration:.2f}",
            f"{'Amount'.ljust(label_width)}: Rs. {total_charge}",
        ]

        # Draw lines
        y_offset = 100
        line_height = 30
        for line in lines:
            draw.text((100, y_offset), line, font=text_font, fill="black")
            y_offset += line_height

        # Thank you
        draw.text((100, y_offset + 10), "Thank you!", font=text_font, fill="black")

        # Save image
        invoice_path = os.path.join(self.output_dir, f"invoice_{vehicle_no}_{int(datetime.now().timestamp())}.png")
        image.save(invoice_path)

        return invoice_path

    def show_invoice(self, image_path):
        img = Image.open(image_path)
        img.show()


# Example usage
if __name__ == "__main__":
    vehicle_data = {
        "name": "John Doe",
        "vehicle_no": "KA-01-H1234",
        "entry_time": "2025-04-24 10:00:00",
        "exit_time": "2025-04-24 14:00:00"
    }

    invoice = InvoiceGenerator(vehicle_data)
    path = invoice.generate_invoice()
    print(f"Invoice saved to: {path}")
    invoice.show_invoice(path)
