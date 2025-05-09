from flask import Flask, request, send_file, render_template
import qrcode
from io import BytesIO
from urllib.parse import urlparse

app = Flask(__name__)

# Home route
@app.route("/")
def index():
    return render_template("index.html")

# Utility to extract domain name for file naming
def get_domain_name(url):
    try:
        parsed_url = urlparse(url)
        domain = parsed_url.hostname or 'qrcode'
        if domain.startswith("www."):
            domain = domain[4:]
        return domain.split('.')[0]
    except:
        return 'qrcode'

# Route to generate QR code and send as image preview (no download)
@app.route("/preview_qrcode", methods=["POST"])
def preview_qrcode():
    url = request.form.get("url")
    if not url:
        return "Invalid URL", 400

    img = qrcode.make(url)
    img_io = BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)

    return send_file(img_io, mimetype='image/png')

# Route to generate QR code and force download with proper filename
@app.route("/download_qrcode", methods=["POST"])
def download_qrcode():
    url = request.form.get("url")
    if not url:
        return "Invalid URL", 400

    img = qrcode.make(url)
    img_io = BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)

    domain = get_domain_name(url)
    filename = f"{domain}_qrcode.png"

    return send_file(img_io, mimetype='image/png', as_attachment=True, download_name=filename)

if __name__ == "__main__":
    app.run(debug=True)
