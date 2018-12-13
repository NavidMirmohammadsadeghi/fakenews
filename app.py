import socketserver
from http.server import BaseHTTPRequestHandler, SimpleHTTPRequestHandler
import json
from urllib.parse import urlparse, parse_qs
import csv
import InputFileAnalyzer as m

PORT = 8000

class MyHandler(SimpleHTTPRequestHandler):
    url = ""
    author = ""
    json_response = {}
    article = ""

    def do_POST(self):
        self.__set_post_data()
        self.__respond()
        if self.persist == True:
            self.__persist()
        return

    def __set_post_data(self):
        print(self.path)
        content_length = int(self.headers['Content-Length'])
        post_data = str(self.rfile.read(content_length).decode("utf-8"))
        parsed = parse_qs(post_data)
        print(post_data)
        self.title = parsed["title"][0].strip()
        self.text = parsed["text"][0].strip()
        self.description = parsed["description"][0].strip()
        self.author = parsed["author"][0].strip()
        self.url = parsed["url"][0].strip()
        self.ad_count = int(parsed["adCount"][0])
        self.updated_date = int(parsed["updateDate"][0])
        self.persist = True
        if parsed["persist"][0] == "false":
            self.persist = False
        print(self.persist)
        print(self.url)
        print(self.author)

    def __respond(self):
        self.json_response = m.ExtractingNumericFeatures({
            "title": self.title,
            "text": self.text,
            "description": self.description,
            "author": self.author,
            "url": self.url,
            "ad_count": self.ad_count,
            "updated_date": self.updated_date
        })
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(self.json_response).encode())
    
    def __persist(self):
        row = [
            self.json_response["title"],
            self.json_response["text"],
            self.json_response["description"],
            self.json_response["author"],
            self.json_response["url"],
            self.json_response["ad_count"],
            self.json_response["updated_date"],
            self.json_response["PotentialFake"],
            self.json_response["NumberAuthor"],
            self.json_response["TitleLength"],
            self.json_response["FullTextLength"],
            self.json_response["TextLength"],
            self.json_response["CapitalWordTitle"],
            self.json_response["NumberOfQuotes"],
            self.json_response["Title_sentiment"],
            self.json_response["Text_sentiment"],
            self.json_response["Description_sentiment"],
            self.json_response["EmotionalLanguage"]
        ]
        with open('Fake-news-original.csv', mode='a', newline="") as input_file:
            input_writer = csv.writer(input_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            input_writer.writerow(row)
        with open('Fake-news-original-with-nonEnglish.csv', mode='a', newline="") as input_file:
            input_writer = csv.writer(input_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            input_writer.writerow(row)
        



Handler = MyHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()
