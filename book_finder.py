import requests
import json

def query_on_library(isbn):
    """
    使用open library的API进行查询
    """
    url = f"https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&format=json&jscmd=data"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        book_key = f"ISBN:{isbn}"
        if book_key in data:
            book_data = data[book_key]
            print("✅ 查询成功！")
            title = book_data.get("title", "未提供书名")
            authors = [author['name'] for author in book_data.get('authors', [])]
            authors_str = ", ".join(authors) if authors else "未提供作者"
            publishers = [publisher['name'] for publisher in book_data.get('publishers', [])]
            publishers_str = ", ".join(publishers) if publishers else "未提供出版社"
            publish_date = book_data.get('publish_date', '未提供出版日期')
            number_of_pages = book_data.get('number_of_pages', '未提供页数')
            cover_url = book_data.get('cover', {}).get('large', '未提供封面')
            print(f"书名: {title}")
            print(f"作者: {authors_str}")
            print(f"出版社: {publishers_str}")
            print(f"出版日期: {publish_date}")
            print(f"页数: {number_of_pages}")
            print(f"封面链接: {cover_url}")
        else:
            print(f"❌ 在 Open Library 中找不到 ISBN 为 {isbn} 的书籍。")
    except requests.exceptions.RequestException as e:
        print(f"💥 网络请求失败: {e}")
    except json.JSONDecodeError:
        print("💥 解析服务器响应失败，可能不是有效的 JSON 格式。")

if __name__ == "__main__":
    print("===================================")
    print("      ISBN 书籍信息查询程序      ")
    print("===================================")
    while True:
        isbn = input("请输入要查询的 ISBN 号码（输入 'q' 退出程序）: ")
        if isbn.lower() == 'q':
            break
        if not isbn:
            print("⚠️ 輸入不能為空，請重新輸入。")
            continue
        if not isbn.isdigit():
            print("❌ 请输入有效的 ISBN 号码。")
            continue
        query_on_library(isbn)