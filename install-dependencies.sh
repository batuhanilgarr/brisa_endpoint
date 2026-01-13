#!/bin/bash
# Brisa API Bağımlılık Kurulum Scripti

echo "🚀 Brisa API Bağımlılık Kurulumu"
echo "=================================="

# Python3-venv paketini yükle
echo "📦 python3-venv paketi yükleniyor..."
sudo apt update
sudo apt install -y python3-venv python3-pip

# Virtual environment oluştur
echo "🔧 Virtual environment oluşturuluyor..."
python3 -m venv venv

# Virtual environment'ı aktif et
echo "✅ Virtual environment aktif ediliyor..."
source venv/bin/activate

# Bağımlılıkları yükle
echo "📥 Python bağımlılıkları yükleniyor..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "✅ Kurulum tamamlandı!"
echo ""
echo "Test için:"
echo "  source venv/bin/activate"
echo "  python api_server.py"
echo ""
