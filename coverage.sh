#!/bin/bash

coverage run --source=est,tests -m unittest discover
coverage report -m
coverage html
