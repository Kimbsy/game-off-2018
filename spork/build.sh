python3 setup.py build

pushd .
mv build/exe.linux-x86_64-3.6 build/spork
cd build
zip -r spork.zip spork
popd
