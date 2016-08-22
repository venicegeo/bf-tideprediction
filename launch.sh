sudo ./install.sh
git clone https://github.com/barnabassprague/DataDependency
mkdir app/data
cp -r DataDependency/data app/data
rm -r DataDependency
./run.py
