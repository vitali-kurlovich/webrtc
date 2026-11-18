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
            url: "https://github.com/vitali-kurlovich/webrtc/releases/download/0.158.0/WebRTC-v158.xcframework.zip",
            checksum: "7d5ce2852b23d1ee83cac0978cae18f6d904789f2211c95af1d1f8b35e4f77a5",
        )
    ],
)
