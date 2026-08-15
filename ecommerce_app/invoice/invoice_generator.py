from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
import os

class InvoiceGenerator:
    def generate_invoice(self, order_id, customer_name, email, order_date,status, items, total_amount):
        os.makedirs("invoices", exist_ok=True)

        file_path = f"invoices/invoice_{order_id}.pdf"

        pdf = canvas.Canvas(file_path, pagesize=A4)

        width, height = A4

        y = height - 40   #starts at top of the page

        pdf.setFont("Helvetica-Bold", 18)
        pdf.drawString(70 * mm, y, "E-COMMERCE INVOICE")   

        y -= 30 #move down

        pdf.setFont("Helvetica", 11)
        pdf.drawString(20 * mm, y, f"Order ID: {order_id}")

        y -= 10

        pdf.drawString(20 * mm, y, f"Customer: {customer_name}")
        y -= 10

        pdf.drawString(20 * mm, y, f"Email: {email}")
        y -= 10

        pdf.drawString(20 * mm, y, f"Date: {order_date}")
        y -= 10

        pdf.drawString(20 * mm, y, f"Status: {status}")

        y -= 20
        pdf.line(20 * mm, y, 190 * mm, y)  

        y -= 15
        pdf.setFont("Helvetica-Bold", 11)
        pdf.drawString(20 * mm, y, "Product")
        pdf.drawString(110 * mm, y, "Quantity")
        pdf.drawString(140 * mm, y, "Price")
        pdf.drawString(170 * mm, y, "Total")

        y -= 10

        pdf.setFont("Helvetica", 10)
        for item in items:
            product_name = item[0]
            quantity = item[1]
            price = item[2]

            item_total = quantity * price

            pdf.drawString(20 * mm, y, str(product_name))
            pdf.drawString(115 * mm, y, str(quantity))
            pdf.drawString(140 * mm, y, f"Rs. {price:.2f}")
            pdf.drawString(170 * mm, y, f"Rs. {item_total:.2f}")
            y -= 10

        y -= 10
        pdf.line(20 * mm, y, 190 * mm, y)

        y -= 20
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(135 * mm,y,f"Grand Total: Rs. {total_amount:.2f}")

        y -= 30
        pdf.setFont("Helvetica", 10)
        pdf.drawString(20 * mm,y,"Thank you for shopping with us!")

        pdf.save()
        
        return file_path