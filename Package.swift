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
            checksum: "91d7cd4067a9b11c5429f4fb800ffe60592d1fa7c1487f14a7b65443dbc93bfe",
        )
    ],
)
