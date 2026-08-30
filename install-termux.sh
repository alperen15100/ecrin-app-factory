#!/data/data/com.termux/files/usr/bin/bash
set -e
REPO="https://github.com/alperen15100/ecrin-app-factory.git"
DIR="$HOME/ecrin-app-factory"
pkg update -y
pkg install -y git unzip
rm -rf "$DIR"
git clone "$REPO" "$DIR"
cd "$DIR"
echo "Repo ready: $DIR"
