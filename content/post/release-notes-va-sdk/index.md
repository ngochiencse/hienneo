---
title: "Release notes và lịch nâng cấp SDK: thứ dễ lười mà dễ hại"
date: 2026-04-05
description: Mỗi mùa Xcode và iOS mới, Apple ghi rất nhiều thay đổi — mình chọn cách đọc lường trước thay vì đợi build đỏ mới quay lại tìm.
categories:
    - iOS
tags:
    - iOS
    - Xcode
    - release-notes
---

Mình từng có giai đoạn chỉ cập nhật **deployment target** hoặc **Swift** khi CI gãy hoặc App Store báo lỗi. Làm vậy chạy được, nhưng hay dính kiểu “sửa cho qua” — mất thời gian hơn là đọc trước vài trang release notes.

<!--more-->

## Mình đọc gì trước

Khi có bản **Xcode / iOS SDK** mới, mình ưu tiên:

1. **Phần Deprecated và Removed** — chỗ này hay gắn trực tiếp với warning hoặc crash lúc runtime.
2. **Thay đổi liên quan API mình đang dùng** — tìm theo tên framework (UIKit, SwiftUI, Foundation…) thay vì đọc từ đầu đến cuối.
3. **Ghi chú build / linker** — đôi khi chỉ một cờ biên dịch mới là đủ làm team kẹt nửa buổi.

Không cần thuộc hết; chỉ cần **đánh dấu chỗ có khả năng đụng tới code của dự án**.

## Lịch nâng cấp trong đầu

Mình thích tách hai việc: **nâng công cụ** (Xcode, Swift) và **nâng yêu cầu hệ điều hành tối thiểu** của app. Hai thứ này không phải lúc nào cũng đi cùng nhau; gộp một lần cho nhanh dễ khiến PR phình to và khó review.

Một mốc đơn giản mình hay dùng: sau khi đọc xong phần “gai” trong notes, mình **ghi một dòng vào backlog** (hoặc issue nội bộ) — “đã rà soát iOS xx / Xcode yy, chưa thấy điểm chạm: …”. Sau này ai hỏi “sao lúc đó không biết API này đổi?” còn có chỗ trả lời.

## Kết

Release notes tẻ nhạt, nhưng là **bản đồ miễn phí** do Apple phát. Bỏ qua được vài bản, nhưng bỏ quen thì mỗi lần nâng cấp lại giống như mò mẫm trong tối — trong khi đèn vốn đã bật sẵn.
