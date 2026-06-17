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
            url: "https://github.com/vitali-kurlovich/webrtc/releases/download/0.149.0/WebRTC-v149.xcframework.zip",
            checksum: "7067fd1ef7e4f82af10387bad098cbc315334aa43bd1ddde343212fab5e3e371",
        )
    ],
)
