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
            checksum: "1ba24db4791e39875c1aa7de57e8a27d464e508a094ccdcdbe2a71cbecd5e263",
        )
    ],
)
