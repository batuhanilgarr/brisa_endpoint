# Brisa HybrisSync API Dokümantasyonu

Bu repo, Brisa HybrisSync uygulamasında kullanılan API endpoint'lerini ve URL pattern'lerini dokümante eden bir web sitesi içerir.

## İçerik

- **Brisa API Endpoint'leri** - 11 aktif endpoint
- **JATO Veri Endpoint'leri** - 5 araç veri endpoint'i
- **TyreCategoryLink Patternleri** - SEO dostu URL pattern'leri

## Kullanım

```bash
open index.html
```

veya herhangi bir web sunucusunda barındırabilirsiniz.

## Dosyalar

- `index.html` - Ana dokümantasyon sayfası
- `styles.css` - Modern karanlık tema stilleri
- `Brisa_API_Endpoints_Brisa.txt` - Brisa endpoint analizi
- `Brisa_API_Endpoints_Jato.txt` - JATO endpoint analizi
- `TyreCategoryLink_Patternleri.txt` - URL pattern dokümantasyonu


## Systemd Service Kurulumu (Production)

API sunucusunu sürekli çalışır halde tutmak için systemd service kullanın:

### 1. Service Dosyasını Kopyalayın

```bash
sudo cp brisa-api.service /etc/systemd/system/
```

### 2. Service'i Etkinleştirin ve Başlatın

```bash
# Otomatik kurulum scripti ile
chmod +x setup-systemd.sh
./setup-systemd.sh

# Veya manuel olarak
sudo systemctl daemon-reload
sudo systemctl enable brisa-api.service
sudo systemctl start brisa-api.service
```

### 3. Durumu Kontrol Edin

```bash
sudo systemctl status brisa-api.service
```

### 4. Logları İzleyin

```bash
# Canlı loglar
sudo journalctl -u brisa-api -f

# Son 100 satır
sudo journalctl -u brisa-api -n 100
```

### Service Komutları

```bash
sudo systemctl start brisa-api      # Başlat
sudo systemctl stop brisa-api       # Durdur
sudo systemctl restart brisa-api    # Yeniden başlat
sudo systemctl status brisa-api     # Durum
```

### Önemli Notlar

- Service dosyasındaki `User`, `WorkingDirectory` ve `ExecStart` path'lerini kendi sisteminize göre düzenleyin
- Virtual environment path'i doğru olmalı: `/home/bitiz/Desktop/brisa_endpoint/venv/bin/python`
- API sunucusu port 5001'de çalışır
- Web sitesi port 8090'da çalışır (mevcut `brisa-http.service` ile)
