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
            url: "https://github.com/vitali-kurlovich/webrtc/releases/download/0.154.0/WebRTC-v154.xcframework.zip",
            checksum: "d27800d91caac60ee1d1d5f40329bfa9eb7ed6bb889de9debb12601fa726d9fe",
        )
    ],
)
