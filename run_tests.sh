#!/bin/bash
# run_tests.sh

echo "🔍 Ejecutando tests..."
export PYTHONPATH=$(pwd)
pytest
