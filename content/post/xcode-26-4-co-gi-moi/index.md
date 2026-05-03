---
title: "Xcode 26.4 có gì mới? (Tóm tắt cho dev iOS)"
date: 2026-04-05
description: Swift 6.3, SDK 26.4, Instruments so sánh run, Swift Testing đính kèm ảnh, String Catalog, và vài điểm cần lưu ý khi nâng Xcode.
categories:
    - iOS
tags:
    - Xcode
    - Apple
    - release-notes
---

Theo [release notes chính thức](https://developer.apple.com/documentation/xcode-release-notes/xcode-26_4-release-notes), **Xcode 26.4** là bản **ổn định** mới (Apple cũng đang mở **Xcode 26.5 beta** — ai cần thử sớm có thể xem mục tương ứng trên trang release notes). Dưới đây là phần mình chọn lọc cho **làm app iOS**, không nhằm thay thế bản gốc tiếng Anh.

<!--more-->

## Tổng quan

- **Swift 6.3** và SDK cho **iOS / iPadOS / tvOS / macOS / visionOS 26.4**.
- **Debug trên thiết bị thật:** iOS 15 trở lên, tvOS 15+, watchOS 8+, visionOS (theo mô tả của Apple).
- **Yêu cầu máy Mac:** **macOS Tahoe 26.2** trở lên.

## Nếu bạn dùng Address Sanitizer / Thread Sanitizer

Apple ghi **known issue:** trên **macOS / iOS / tvOS / watchOS / visionOS 26.4**, build bằng **Xcode 26.3 hoặc cũ hơn** có thể khiến **ASan / TSan treo**. **Workaround:** dùng **Xcode 26.4** khi bật các sanitizer. Đây là lý do “nên lên bản mới” rất thực dụng nếu team vẫn profile với sanitizer.

## Instruments

- **Run Comparison:** so sánh **call tree** giữa các lần chạy (menu *View → Detail Area → Compare With…* hoặc nút ⇆ trên jump bar).
- **Top Functions:** chế độ xem tổng hợp **hàm tốn thời gian nhất** trong trace.
- **Power Profiler:** trace mở từ thiết bị có thể xem **hoạt động CPU theo từng nhân**.
- **Import nhiều file vào cùng một trace** (*File → Import As Run…*); **`xctrace import`** hỗ trợ **`--append-run`** để gộp thêm run vào file trace có sẵn.
- Thêm instrument theo dõi **băng thông và độ trễ** trong hệ **Foveated Streaming** (visionOS).

## Swift Package & trình soạn thảo

- Trong **Package Dependencies**, có thể **bật package traits** cho dependency (tính năng mới).
- **Source editor extensions** hiển thị tên đã bản địa hóa theo **CFBundleName** trong Info.plist của extension.

## Kiểm thử (Swift Testing & XCTest)

- **Swift Testing** có thể **đính kèm ảnh** vào test: `CGImage`, `NSImage`, `UIImage`, `CIImage`.
- Ghi **Issue** có thể kèm **Severity**.
- **XCTest ↔ Swift Testing interoperability** không còn **bật mặc định**; muốn dùng (thử nghiệm) cần set biến môi trường `SWIFT_TESTING_XCTEST_INTEROP_MODE` = `limited` trong test plan (xem [ST-0021](https://github.com/swiftlang/swift-evolution/blob/main/proposals/testing/0021-targeted-interoperability-swift-testing-and-xctest.md)).

## Localization & String Catalog

- Xóa ngôn ngữ trong **String Catalog** (chỉ catalog hoặc cả project).
- Thêm ngôn ngữ mới trong Project Editor có thể **prefill** từ ngôn ngữ đã có.
- Hỗ trợ **cut / copy / paste / duplicate** chuỗi giữa các catalog.
- Build setting **`BUILD_ONLY_KNOWN_LOCALIZATIONS`**: chỉ build các bản địa hóa khai báo trong project.
- Mặc định **không** trích chuỗi từ **comment trong code**; nếu cần, bật lại bằng **`LOCALIZED_STRING_CODE_COMMENTS` = YES**.

## Build & thư viện mergeable

- Thư viện **mergeable** không cần truy cập resource qua Bundle API chuẩn có thể set **`SKIP_MERGEABLE_LIBRARY_BUNDLE_HOOK`** để **giảm overhead lúc launch**.

## Simulator

- **`xcodebuild` export/import** runtime simulator qua thư mục **`.exportedBundle`** (metadata an toàn hơn khi import).
- **dyld shared cache** cho runtime được tạo lại tự động để **cải thiện thời gian boot** (lần đầu có thể chậm khi đang quét/build cache; có thể chạy `simctl runtime dyld_shared_cache update --all`).
- Sửa lỗi **simdiskimaged / simctl / `-runFirstLaunch`** treo khi cài runtime.

## Swift / C++ (điểm chạm nhỏ)

- **Swift ↔ C++:** khởi tạo Swift `String` từ C++ `std::wstring` và ngược lại; thêm macro **`SWIFT_COPYABLE_IF(...)`** cho template.
- **Span / MutableSpan:** các accessor raw và `append` liên quan được đánh **`@unsafe`** (bổ sung đúng hướng an toàn bộ nhớ — đọc kỹ đoạn giải thích trong release notes nếu bạn dùng Span).

## Ký & Enhanced Security

- App có **Enhanced Security Capability** không còn crash trên OS **trước 26.0**; Apple hướng dẫn **đổi entitlement** sang biến thể dạng **string** (xem đúng mục *Signing and Capabilities* trong release notes để không copy nhầm key).

---

**Kết:** Bài này chỉ là **lọc theo góc iOS / công cụ**. Phần **C++26**, **libc++** và danh sách sửa lỗi dài nằm trong [Xcode 26.4 Release Notes](https://developer.apple.com/documentation/xcode-release-notes/xcode-26_4-release-notes). Trước khi nâng Xcode trên CI, nhớ đối chiếu **phiên bản macOS trên runner** với yêu cầu **Tahoe 26.2+**.
