# WebRTC Binaries for iOS and macOS

[![WebRTC Release](https://github.com/%{repo}%/actions/workflows/release.yml/badge.svg)](https://github.com/%{repo}%/actions/workflows/release.yml)
[![Latest version](https://img.shields.io/github/v/release/%{repo}%)](https://github.com/%{repo}%/releases)
[![Release Date](https://img.shields.io/github/release-date/%{repo}%)](https://github.com/%{repo}%/releases)

## Releases
The binary releases correspond with official Chromium releases  

[Chromium dashboard](https://chromiumdash.appspot.com/branches).

* All binaries are compiled from the official WebRTC [source code](https://webrtc.googlesource.com/src/) .
* Dynamic framework contains multiple binaries for macOS and iOS (arm64 only).
* Do not support macOS Catalyst.
* All frameworks contain dSYM files for debugging.
* Added support for extra encodings: VP9, H264, H265


## Requirements
* iOS 16+
* macOS 14+

## Binaries included
| **Platform / arch** | arm64  | x86_x64 | --build_config=debug  | 
|---------------------|--------|---------|-----------------------|
| **iOS (device)**    |   ✅   |   N/A   | %{build_flag}% | 
| **iOS (simulator)** |   ✅   |   N/A   | %{build_flag}% | 
| **macOS**           |   ✅   |   N/A   | %{build_flag}% | 
| **macOS Catalyst**  |   N/A  |   N/A   |     N/A  |

### SwiftPM

```swift
dependencies: [
    .package(url: "https://github.com/%{repo}%.git", .upToNextMajor("%{tag}%"))
]
```
