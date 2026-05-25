#!/bin/sh

BRANCH="${BRANCH:-main}"
BUILD_DEBUG="${BUILD_DEBUG:-}"

if [ -z "$ROOT_DIR" ]; then
  echo "Variable ROOT_DIR is not set or empty"
  exit 1
fi

if [ -z "$SRC_DIR" ]; then
  echo "Variable SRC_DIR is not set or empty"
  exit 1
fi

if [ -z "$OUTPUT_DIR" ]; then
  echo "Variable OUTPUT_DIR is not set or empty"
  exit 1
fi

if [ -z "$OUTPUT_ARTIFACTS_DIR" ]; then
  echo "Variable OUTPUT_ARTIFACTS_DIR is not set or empty"
  exit 1
fi

SRIPTS_DIR="${ROOT_DIR}/scripts"
BUILD_SCRIPTS_DIR="${SRIPTS_DIR}/ios_macos"

OUTPUT_MACOS_SDK_DIR="${OUTPUT_DIR}/macos_arm64_libs/gen/sdk"
OUTPUT_MACOS_SDK_HEADERS_DIR="${OUTPUT_MACOS_SDK_DIR}/WebRTC.framework/Headers"

OUTPUT_XCFRAMEWORK_DIR="${OUTPUT_DIR}/WebRTC.xcframework"
OUTPUT_MACOS_FRAMEWORK_VERSION_DIR="${OUTPUT_XCFRAMEWORK_DIR}/macos-arm64/WebRTC.framework/Versions/A"

# Download and install depot tools
if [ ! -d depot_tools ]; then
    git clone https://chromium.googlesource.com/chromium/tools/depot_tools.git
else
    cd depot_tools
    git pull origin main
    cd ..
fi
export PATH=$(pwd)/depot_tools:$PATH

# Download and build WebRTC
if [ ! -d src ]; then
    fetch --nohooks webrtc_ios
fi
cd src
git fetch --all

echo "Branch fot checkout ${BRANCH}"

git checkout $BRANCH
cd ..
gclient sync --with_branch_heads --with_tags
cd src

# Cleanup output directory
rm -rf $OUTPUT_DIR

# Copy build scripts
if [ ! -d ./tools_webrtc/ios_macos ]; then
    cp -r $BUILD_SCRIPTS_DIR ./tools_webrtc
fi

if [ ! -n "$BUILD_DEBUG" ]; then
  echo "Building release..."

# Compile and build all frameworks
./tools_webrtc/ios_macos/build_libs.sh -o $OUTPUT_DIR

#  Fix Headers in MacOS target
cp -r $OUTPUT_MACOS_SDK_HEADERS_DIR $OUTPUT_MACOS_FRAMEWORK_VERSION_DIR

# Archive the framework
cd "${OUTPUT_DIR}"
NOW=$(date -u +"%Y-%m-%dT%H-%M-%S")
OUTPUT_NAME=WebRTC-$NOW.xcframework.zip
zip --symlinks -r $OUTPUT_NAME WebRTC.xcframework/

else

echo "Building debug..."

./tools_webrtc/ios_macos/build_libs.sh -o $OUTPUT_DIR --build_config=debug

# Fix Headers in MacOS target
cp -r $OUTPUT_MACOS_SDK_HEADERS_DIR $OUTPUT_MACOS_FRAMEWORK_VERSION_DIR

# Archive the framework
cd "${OUTPUT_DIR}"
NOW=$(date -u +"%Y-%m-%dT%H-%M-%S")
OUTPUT_NAME=WebRTC-$NOW-debug.xcframework.zip
zip --symlinks -r $OUTPUT_NAME WebRTC.xcframework/

fi

# Calculate SHA256 checksum
CHECKSUM=$(shasum -a 256 $OUTPUT_NAME | awk '{ print $1 }')
COMMIT_HASH=$(git rev-parse HEAD)

echo "{ \"file\": \"${OUTPUT_NAME}\", \"checksum\": \"${CHECKSUM}\", \"commit\": \"${COMMIT_HASH}\", \"branch\": \"${BRANCH}\" }" > metadata.json
cat metadata.json

#  Move files to release dir
if [ ! -d $OUTPUT_ARTIFACTS_DIR ]; then
    mkdir -p $OUTPUT_ARTIFACTS_DIR
fi

mv "${OUTPUT_DIR}/${OUTPUT_NAME}" ${OUTPUT_ARTIFACTS_DIR}
mv "${OUTPUT_DIR}/metadata.json" ${OUTPUT_ARTIFACTS_DIR}

cd $SRC_DIR
