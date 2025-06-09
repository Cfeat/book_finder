import requests
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

def query_book_from_open_library(isbn):
    """
    根据 ISBN 从 Open Library API 查询书籍数据并返回一个字典。
    """
    url = f"https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&format=json&jscmd=data"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        book_key = f"ISBN:{isbn}"
        if book_key in data:
            book_data = data[book_key]

            authors = [author['name'] for author in book_data.get('authors', [])]
            publishers = [p['name'] for p in book_data.get('publishers', [])]

            result = {
                "found": True,
                "title": book_data.get("title", "未提供书名"),
                "authors": ", ".join(authors) if authors else "未提供作者",
                "publishers": ", ".join(publishers) if publishers else "未提供出版社",
                "publish_date": book_data.get('publish_date', '未提供出版日期'),
                "number_of_pages": book_data.get('number_of_pages', '未提供页数'),
                "cover_url": book_data.get('cover', {}).get('large'),
                "subjects": [s['name'] for s in book_data.get('subjects', [])] 
            }
            return result
        else:
            return {"found": False, "message": f"找不到 ISBN 为 {isbn} 的书籍。"}

    except requests.exceptions.RequestException as e:
        return {"found": False, "message": f"网络请求失败: {e}"}
    except Exception:
        return {"found": False, "message": "解析服务器响应或处理数据时发生错误。"}

@app.route('/api/query')
def api_query():
    isbn = request.args.get('isbn')
    if not isbn:
        return jsonify({"found": False, "message": "请输入有效的 ISBN 号码。"}), 400
    
    book_info = query_book_from_open_library(isbn)
    return jsonify(book_info)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)