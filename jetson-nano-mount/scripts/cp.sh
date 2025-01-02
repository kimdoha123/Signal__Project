#!/bin/bash
rsync -av --progress signal-masters/ cuda_test --exclude='.venv'
