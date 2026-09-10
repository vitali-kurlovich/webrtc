// swift-tools-version:6.3

import PackageDescription

let package = Package(
    name: "webrtc",
    platforms: [.iOS(.v16), .macOS(.v14)],
    products: [
        .library(
            name: "WebRTC",
            targets: ["WebRTC"],
        )
    ],
    targets: [
        .binaryTarget(
            name: "WebRTC",
            url: "https://github.com/vitali-kurlovich/webrtc/releases/download/0.152.0/WebRTC-v152.xcframework.zip",
            checksum: "d7d81349f0f029f0c3ed3fcaa63de3e163d451fb7ee73b4471641d184fc018f6",
        )
    ],
)
