#!/bin/bash

python -m unittest discover
if [ $? -ne 0 ]
then
    echo "Unit tests failed."
    exit 1
fi

bash coverage.sh | grep TOTAL | grep "100%"
if [ $? -ne 0 ]
then
    echo "Unit tests coverage less than 100%."
    exit 1
fi

bash pylint_est.sh
if [ $? -ne 0 ]
then
    echo "Pylint not 10/10 for est/."
    exit 1
fi

bash pylint_tests.sh
if [ $? -ne 0 ]
then
    echo "Pylint not 10/10 for tests/."
    exit 1
fi

echo "OK"
