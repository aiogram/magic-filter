#!/usr/bin/env bash

for file in /io/dist/*.whl; do
  auditwheel repair "$file"
done

rm /io/dist/*-linux*.whl
cp /wheelhouse/*.whl /io/dist/
