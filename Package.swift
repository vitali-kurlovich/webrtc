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
            checksum: "5914d90b99974d6b543669d48470a0fb66a97d69a12dd925d0faa414843ebcc2",
        )
    ],
)
