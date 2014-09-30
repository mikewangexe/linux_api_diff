export LINUX_DIR=~/linux/raspberrypi
export REMOVE_INLINE_DEFINITIONS=

export ARCH=arm
export BOARD=bcm2708
export TOOLCHAIN_PREFIX=arm-eabi-
export PLATFORM_CC_FLAGS="-target arm-eabi -marm -mfpu=vfp -mcpu=arm1176jzf-s -mtune=arm1176jzf-s -mfloat-abi=softfp"

export TOP="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
export CLANG=$TOP/bin/clang
export LD_LIBRARY_PATH=$TOP/lib:$TOP/lib64:$LD_LIBRARY_PATH

if [ -d $LINUX_DIR ]; then
    pushd $LINUX_DIR > /dev/null
    if [ ! -f .config ]; then
	make defconfig
	make init
    fi
    popd > /dev/null
fi
