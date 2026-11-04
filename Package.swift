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
            url: "https://github.com/vitali-kurlovich/webrtc/releases/download/0.157.0/WebRTC-v157.xcframework.zip",
            checksum: "873491189ebdb373df8b3805706a53f6d18a794e3bcaa51c7b48f4f1915f5f5c",
        )
    ],
)
