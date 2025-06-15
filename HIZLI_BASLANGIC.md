# 🚀 Hızlı Başlangıç Kılavuzu

## 📦 Kurulum

### Gerekli Kütüphaneler
```bash
pip install numpy matplotlib tkinter
```

### Dosyaları İndirin
- `gercekci_balik_simulasyon.py` - Ana simülasyon dosyası

## ▶️ Çalıştırma

### Windows
```cmd
python gercekci_balik_simulasyon.py
```

### Linux/Mac
```bash
python3 gercekci_balik_simulasyon.py
```

## 🎮 Nasıl Kullanılır

### 1. Program Açılışı
- Uygulama başladığında 6 panel grafik görünür
- Sol üstte parametre ayar paneli
- Sağ üstte kontrol butonları

### 2. Parametreleri Ayarlayın
- **Başlangıç Popülasyonu**: 500-5000 arası (varsayılan: 1000)
- **Simülasyon Süresi**: 50-500 yıl (varsayılan: 200)

### 3. Simülasyonu Başlatın
- **🚀 Simülasyonu Başlat** butonuna tıklayın
- Progress bar simülasyon ilerlemesini gösterir
- Simülasyon otomatik olarak çalışır (yaklaşık 2-5 dakika)

### 4. Sonuçları İnceleyin
- **6 farklı grafik** otomatik güncellenir:
  1. **Allel Frekansları** (ana grafik)
  2. **Genotip Dağılımı**
  3. **Popülasyon Boyutu**
  4. **Çevresel Faktörler**
  5. **Catastrofik Olaylar**
  6. **Hardy-Weinberg Sapması**

### 5. Özet İstatistikleri
- Simülasyon bitince otomatik özet penceresi açılır
- Allel frekans değişimi
- Popülasyon değişimi
- Çevresel olay sayıları

## 💾 Veri Kaydetme

### Otomatik Kayıt
- **💾 Veriyi Kaydet** butonuna tıklayın
- JSON formatında detaylı veri kaydedilir
- Dosya adı: `balik_populasyon_genetigi_TARIH.json`

### İçerik
- Tüm simülasyon parametreleri
- Yıllık popülasyon verileri
- Çevresel koşul geçmişi
- Catastrofik olay kayıtları

## 🔄 Yeni Denemeler

### Farklı Senaryolar
- **🔄 Yeni Simülasyon** ile parametreleri değiştirin
- Farklı popülasyon boyutları deneyin
- Değişik sürelerde nasıl sonuçlar alacağınızı gözlemleyin

## 📊 Grafik Okuma Rehberi

### 1. Allel Frekansları (Sol Üst - ANA GRAFİK)
- **Kırmızı çizgi**: K (kırmızı) alleli frekansı
- **Gri çizgi**: B (beyaz) alleli frekansı
- **Y ekseni**: 0-1 arası frekans değerleri
- **Dikkat edilecekler**: Ani değişimler, trend yönü

### 2. Genotip Dağılımı (Orta Üst)
- **Koyu kırmızı**: KK genotipi
- **Turuncu**: KB genotipi (heterozygot)
- **Gri**: BB genotipi
- **Dolgu alanları**: Oransal dağılım

### 3. Popülasyon Boyutu (Sağ Üst)
- **Mavi çizgi**: Toplam birey sayısı
- **Dalgalanmalar**: Çevresel etkilerin sonucu
- **Dramatik düşüşler**: Catastrofik olaylar

### 4. Çevresel Faktörler (Sol Alt)
- **Turuncu**: Sıcaklık değişimi
- **Yeşil**: Besin bolluğu
- **Kahverengi**: Kirlilik seviyesi

### 5. Catastrofik Olaylar (Orta Alt)
- **Bar grafiği**: Olay türlerinin sayısı
- **Kırmızı X'ler**: Olay zamanları

### 6. Hardy-Weinberg Sapması (Sağ Alt)
- **Mor alan**: Sapma derecesi
- **Yüksek değerler**: Dengeden uzaklaşma
- **Düşük değerler**: Dengeye yakınlık

## ⚠️ Dikkat Edilecekler

### Beklenen Çalışma Süreleri
- 50 yıl: ~30 saniye
- 100 yıl: ~1 dakika
- 200 yıl: ~2-3 dakika
- 500 yıl: ~5-8 dakika

### Sistem Gereksinimleri
- Python 3.6+
- 4GB RAM (önerilen)
- 100MB boş disk alanı

### Sorun Giderme
- Program donuyorsa: Parametreleri küçültün
- Grafik görünmüyorsa: Pencereyi yeniden boyutlandırın
- Hata alıyorsanız: Python kütüphanelerini kontrol edin

## 🎯 Önerilen İlk Denemeler

1. **Varsayılan ayarlarla** ilk çalıştırma
2. **Küçük popülasyon** (500 birey) ile dene
3. **Büyük popülasyon** (3000 birey) ile karşılaştır
4. **Uzun süre** (300-400 yıl) simülasyon çalıştır

---

**İyi çalışmalar! 🐠📊** 