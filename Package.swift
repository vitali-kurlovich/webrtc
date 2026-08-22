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
            checksum: "07eaef6905af98c7bf806a2e70d97be51f278232bb76ad0b722e83ce980be23c",
        )
    ],
)
