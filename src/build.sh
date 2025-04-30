SOURCE_PROJECT=$HOME/test/pac/Pacman-AI/pacman/src
BUILD_DIR=$HOME/test/test-pac/pacman/src/

cp -r "$SOURCE_PROJECT/"* $BUILD_DIR
# cp *.py $BUILD_DIR
CURRENT=$(pwd)

cd $BUILD_DIR
python3 pacman.py -p ReflexAgent -l mediumClassic --frameTime 0

cd $CURRENT
