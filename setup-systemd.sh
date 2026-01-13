#!/bin/bash
# Brisa API Systemd Service Kurulum Scripti

echo "🚀 Brisa API Systemd Service Kurulumu"
echo "======================================"

# Service dosyasını systemd dizinine kopyala
sudo cp brisa-api.service /etc/systemd/system/

# Service'i yeniden yükle
sudo systemctl daemon-reload

# Service'i etkinleştir (boot'ta otomatik başlasın)
sudo systemctl enable brisa-api.service

# Service'i başlat
sudo systemctl start brisa-api.service

# Durumu kontrol et
echo ""
echo "✅ Service durumu:"
sudo systemctl status brisa-api.service --no-pager

echo ""
echo "📋 Kullanışlı komutlar:"
echo "  Service durumu:     sudo systemctl status brisa-api"
echo "  Service başlat:     sudo systemctl start brisa-api"
echo "  Service durdur:     sudo systemctl stop brisa-api"
echo "  Service yeniden:    sudo systemctl restart brisa-api"
echo "  Logları görüntüle:  sudo journalctl -u brisa-api -f"
echo ""
echo "🌐 API: http://$(hostname -I | awk '{print $1}'):5001"
echo "📄 Web: http://$(hostname -I | awk '{print $1}'):8090"
