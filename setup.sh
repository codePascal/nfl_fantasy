# check python version
python3 --version

# check pip
python3 -m pip --version

# bootstrap from standard library if fails
# python3 -m pip ensurepip --default-pip

# upgrade setuptools, wheel, pip
python3 -m pip install --upgrade pip setuptools wheel

# create and source venv
python3 -m venv venv
source venv/bin/activate

# install requirements
python3 -m pip install -r requirements.txt

# add search path for python (currently requires python3.8)
echo $PWD >> venv/lib/python3.8/site-packages/search_path.pth

# add build directory
mkdir $PWD/build

# symlink and run tests
ln -s $PWD/tests $PWD/build
python -m unittest
