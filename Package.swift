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
            checksum: "a7f93a8dd086fadfa968a5ece05d120aaff1cdde32c6c799854e66fead9ae823",
        )
    ],
)
