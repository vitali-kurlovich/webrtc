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
            url: "https://github.com/vitali-kurlovich/webrtc/releases/download/0.155.0/WebRTC-v155.xcframework.zip",
            checksum: "0088c10b36e714a923b26f64332438037b85ad9328a1e1b3dd9ed0a826f63a4d",
        )
    ],
)
