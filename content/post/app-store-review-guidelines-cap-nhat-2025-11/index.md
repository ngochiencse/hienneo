---
title: "App Store: bản cập nhật App Review Guidelines gần nhất (11/2025)"
date: 2026-04-05
description: Tóm tắt thay đổi chính trong App Review Guidelines mà Apple công bố tháng 11/2025 — creator & độ tuổi, mini app, vay tiền, thương hiệu, crypto, và chia sẻ dữ liệu với AI bên thứ ba.
categories:
    - iOS
tags:
    - App Store
    - Apple
    - policy
links:
  - title: GitHub
    description: GitHub is the world's largest software development platform.
    website: https://github.com
    image: https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png
  - title: TypeScript
    description: TypeScript is a typed superset of JavaScript that compiles to plain JavaScript.
    website: https://www.typescriptlang.org
    image: ts-logo-128.jpg
menu:
    main: 
        weight: -50
        params:
            icon: link
comments: false
---

Bản **cập nhật gần đây nhất** mình bám theo là thông báo của Apple ngày **13 tháng 11 năm 2025**: [Updated App Review Guidelines now available](https://developer.apple.com/news/?id=ey6d8onl). Toàn văn luôn nên đọc trực tiếp [App Review Guidelines](https://developer.apple.com/app-store/review/guidelines/) vì Apple có thể chỉnh thêm sau này.

<!--more-->

## 1.2.1(a) — App creator & nội dung vượt độ tuổi

**Guideline mới:** app dạng **creator** phải cho người dùng **nhận biết** nội dung **vượt quá mức xếp hạng độ tuổi** của app, và phải có **cơ chế hạn chế theo tuổi** dựa trên **tuổi đã xác minh hoặc đã khai báo** để hạn chế truy cập với người chưa đủ tuổi.

## 2.5.10 — Quảng cáo “rỗng”

**Đoạn cấm** nội dung kiểu *“Apps should not be submitted with empty ad banners or test advertisements”* đã **bị xóa**. (Nghĩa là khung chính sách không còn ghi rõ câu đó; vẫn nên submit app ở trạng thái production-ready, tránh gây từ chối vì lý do khác.)

## 3.2.2(ix) — App cho vay

**Làm rõ:** app cho vay **không được** tính **APR tối đa trên 36%** (gồm **cả chi phí và phí**), và **không được** yêu cầu **trả hết trong 60 ngày hoặc ít hơn**.

## 4.1(c) — Icon & tên app

**Guideline mới:** **không được** dùng **icon, thương hiệu hoặc tên sản phẩm của developer khác** trong **icon hoặc tên app** của bạn, **trừ khi có sự đồng ý** từ họ.

## 4.7, 4.7.2, 4.7.5 — Mini app / phần mềm không nhúng trong binary

- **4.7:** Làm rõ **mini app / mini game HTML5 & JavaScript** **nằm trong phạm vi** guideline này.
- **4.7.2:** App cung cấp **phần mềm không nhúng trong binary** **không được** mở rộng hay **lộ API / công nghệ nền tảng native** cho phần mềm đó **nếu chưa được Apple cho phép trước**.
- **4.7.5:** Với phần mềm không nhúng trong binary: phải có cách **nhận biết nội dung vượt độ tuổi** và **cơ chế hạn chế theo tuổi** (xác minh hoặc khai báo), tương tự tinh thần **1.2.1(a)**.

## 5.1.1(ix) — Dịch vụ siêu quản lý

Bổ sung **sàn giao dịch tiền mã hóa (crypto exchanges)** vào danh sách app cung cấp dịch vụ trong **lĩnh vực bị quản lý chặt**.

## 5.1.2(i) — Dữ liệu cá nhân & AI bên thứ ba

**Làm rõ:** phải **công bố rõ** **nơi / phạm vi** dữ liệu cá nhân sẽ được chia sẻ cho **bên thứ ba**, **kể cả dịch vụ AI bên thứ ba**, và phải **xin phép rõ ràng (explicit)** trước khi làm.

---

## Bạn nên làm gì?

1. Mở [bản guidelines hiện tại](https://developer.apple.com/app-store/review/guidelines/) và rà các mục **1.2.1, 2.5, 3.2.2, 4.1, 4.7, 5.1** nếu app của bạn đụng creator, ads, fintech, mini game, hay tích hợp AI.
2. Lưu link tin gốc để team **compliance / legal** đối chiếu: [developer.apple.com/news/?id=ey6d8onl](https://developer.apple.com/news/?id=ey6d8onl).

**Chú thích (4.7.2, 4.7.5):** Cụm tiếng Anh trong guidelines là *software not embedded in the binary* — tức phần mềm **không nằm sẵn trong binary** của bản app nộp lên Store (ví dụ mini app / game HTML5 & JavaScript, nội dung tải thêm, chạy trong WebView…), khác với phần đã **đóng gói trực tiếp** trong build.

*Nội dung bài dựa trên bullet list trong thông báo Apple ngày 13/11/2025; không thay cho tư vấn pháp lý.*
