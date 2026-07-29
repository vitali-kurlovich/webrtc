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
            url: "https://github.com/vitali-kurlovich/webrtc/releases/download/0.151.0/WebRTC-v151.xcframework.zip",
            checksum: "2246c108649822a97cb0fb731e16f76320ea5ee2d60831f32d940eb01b906fbe",
        )
    ],
)
