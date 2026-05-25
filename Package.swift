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
            url: "https://github.com/vitali-kurlovich/webrtc/releases/download/0.148.0/WebRTC-v148.xcframework.zip",
            checksum: "49c44eecb09baefbde170ef2a642f76245032b998222f9da9613cd59e4014c30",
        )
    ],
)
