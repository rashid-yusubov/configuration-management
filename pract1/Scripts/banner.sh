#!/bin/bash

if [ -z "$1" ]; then
  echo "Usage: $0 \"Your message here\""
  exit 1
fi

message="$1"

length=${#message}

echo "+$(printf '%0.s-' $(seq 1 $((length + 2))))+"

echo "| $message |"

echo "+$(printf '%0.s-' $(seq 1 $((length + 2))))+"
