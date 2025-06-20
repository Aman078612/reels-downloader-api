from flask import Flask, request, jsonify
from yt_dlp import YoutubeDL

app = Flask(__name__)

@app.route('/download', methods=['POST'])
def download_reel():
    data = request.get_json()
    url = data.get('url')
    if not url or "instagram.com/reel/" not in url:
        return jsonify({"error": "Invalid Instagram Reel URL"}), 400

    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'force_generic_extractor': False,
        'extract_flat': False,
        'format': 'best',
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            video_url = info.get("url")
            return jsonify({"video_url": video_url})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
