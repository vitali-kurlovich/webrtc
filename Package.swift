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
            url: "https://github.com/vitali-kurlovich/webrtc/releases/download/0.156.0/WebRTC-v156.xcframework.zip",
            checksum: "c14d580ccf43ad42d013a85dc9b4fc0652ad86675e4036ab1d30c2062a312d2d",
        )
    ],
)
