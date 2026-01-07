# `doc_nhanh`

Công cụ giúp mình tải các bài viết trên Internet mình muốn đọc và gói thành EPUB.

Cần có [`pandoc`](https://github.com/jgm/pandoc), [`papeer`](https://github.com/lapwat/papeer).

Setup này tôi dùng trên Linux (Debian 13) nên không biết là có hỗ trợ tốt trên MacOS hay Windows này kia không đâu nhé :>.

## Cách dùng

Thêm các tệp Markdown (`.md`) vào trong thư mục `content/` rồi chạy lệnh `make` trên thư mục đó là xong. À nhớ chỉnh sửa tệp `metadata.yaml` nhé (Kiểu thông tin sách này kia thôi chứ không có gì đâu).

### Tự thêm tệp

Các bác có thể tải bài viết từ trình duyệt về bằng cách sử dụng [MarkDownload - Markdown Web Clipper](https://github.com/deathau/markdownload) (Không còn dùng được trên Google Chrome nữa rồi thì phải).

### Tải tự động toàn bộ các bài viết

Bước 1: Tạo tệp `links.txt`

Bước 2: Cho hết links bài viết các bác muốn đọc vào đấy, à mà nếu được thì bác để một dòng trống ở cuối tệp nhé. Kiểu như thế này

```
https://vi-du1.com
https://vi-du2.com

# Để một dòng trống không ở cuối tệp links.txt nhé.
```

Bước 3: Chạy lệnh sau (nhớ tải `papeer` nhé). Để tệp `links.txt` trong thư mục `content/` rồi chạy trong đó.

```bash
while read p; do papeer get "$p"; done <links.txt
```

Bước 4: Tải xong rồi thì chạy giúp tôi lệnh sau:

```bash
for i in content/*.md; do python3 fetch-images.py "$i"; done
```

Tải xong hết ảnh rồi thì sẽ có thư mục `assets/` trong thư mục `content/`, mấy ông ném thư mục `assets/` ra root folder (cùng với `Makefile`) là được nhé.

Bước 5: Chạy lệnh `make` để gói `.epub` là xong.

