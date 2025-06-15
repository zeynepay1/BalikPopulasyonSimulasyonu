# 🐠 Gelişmiş Balık Akvaryumu Simülasyonu

Bu proje, genetik kalıtım, doğal seçilim ve ekolojik etkileşimleri gösteren gelişmiş bir balık akvaryumu simülasyonudur.

## 🎯 Özellikler

### **Allel Sistemi (Renk Genetiği)**
- **🔴 Kırmızı Balıklar**: Daha güçlü, saldırgan davranış eğilimi
- **⚪ Beyaz Balıklar**: Daha dayanıklı, uzun yaşam süresi
- **Genetik Kalıtım**: Ebeveynlerden renk aktarımı
- **Mutasyon**: %6 şansla renk değişimi

### **Balık Türleri**
1. **Koi Balığı**: En dayanıklı, büyük boyutlu
2. **Japon Balığı**: Orta dayanıklılık, yuvarlak şekil
3. **Guppy**: Hızlı üreme, küçük boyut
4. **Neon**: En küçük, hızlı hareket

### **Su Ortamı Koşulları**
- **Sıcaklık**: 15-35°C (İdeal: 20-28°C)
- **pH Seviyesi**: 6.0-8.5 (İdeal: 7.0)
- **Oksijen**: %70-100
- **Mevsimsel Değişiklikler**: İlkbahar, yaz, sonbahar, kış

### **Davranış Türleri**
- **Sosyal**: Sürü halinde yüzme
- **Agresif**: Farklı renkteki balıkları kovalama
- **Pasif**: Sakin hareket
- **Yalnız**: Tek başına yüzme

### **Ekolojik Sistem**
- **Yiyecek Kaynakları**: 12 adet balık yemi noktası
- **Avcı Balıklar**: Büyük avcı balıklar (dinamik sayı)
- **Hastalık Sistemi**: %0.15 hastalık riski
- **Yaşlanma**: Yaşa bağlı ölüm riski

## 🎮 Kontroller

| Tuş | Fonksiyon |
|-----|-----------|
| **SPACE** | Simülasyonu duraklat/devam ettir |
| **F** | Hızlı mod aç/kapat (2x hız) |
| **1** | Normal görünüm |
| **2** | İstatistik görünümü (pasta grafik) |
| **3** | Genetik görünüm (zeka bazlı renklendirme) |
| **R** | Simülasyonu yeniden başlat |
| **G** | Detaylı grafikleri göster |
| **S** | Verileri JSON formatında kaydet |

## 📊 Görünüm Modları

### 1. Normal Görünüm
- Balıkları gerçek renklerinde gösterir
- Enerji çubukları (kırmızı/sarı/yeşil)
- Hamilelik göstergesi (pembe halka)
- Yiyecek kaynakları (sarı daireler)
- Avcılar (büyük kırmızı daireler)

### 2. İstatistik Görünümü
- Renk dağılımı pasta grafiği
- Popülasyon bilgileri
- Su ortamı koşulları

### 3. Genetik Görünüm
- Zeka seviyesine göre renklendirme
- Mutasyon göstergeleri (beyaz halka)
- Genetik çeşitlilik analizi

## 🧬 Genetik Sistem

### **Kalıtım Özellikleri**
- **Zeka**: 0.1-1.0 arası
- **Güç**: 0.1-1.0 arası
- **Dayanıklılık**: 0.1-1.0 arası
- **Boyut**: 3-20 piksel arası
- **Hız**: 0.8-5.0 arası

### **Mutasyon Oranları**
- **Renk Mutasyonu**: %6
- **Tür Mutasyonu**: %4
- **Davranış Mutasyonu**: %5
- **Özellik Varyasyonu**: ±0.12

### **Üreme Sistemi**
- **Hamilelik Süresi**: 180 zaman birimi
- **Yavru Sayısı**: 2-6 adet
- **Üreme Yaşı**: 100+ zaman birimi
- **Enerji Gereksinimi**: 50+ enerji

## 📈 İstatistik Takibi

Simülasyon şu verileri takip eder:
- Toplam popülasyon değişimi
- Renk dağılımı (kırmızı vs beyaz)
- Tür dağılımı
- Su ortamı koşulları
- Genetik çeşitlilik
- Avcı-av ilişkileri

## 🔬 Bilimsel Kavramlar

### **Doğal Seçilim**
- Renk avantajları
- Tür avantajları
- Çevresel baskılar
- Hayatta kalma oranları

### **Genetik Çeşitlilik**
- Allel frekansları
- Mutasyon etkileri
- Genetik sürüklenme
- Popülasyon darboğazları

### **Ekolojik Etkileşimler**
- Av-avcı dinamikleri
- Kaynak rekabeti
- Çevresel stres
- Popülasyon döngüleri

## 🚀 Kurulum ve Çalıştırma

### Gereksinimler
```bash
pip install pygame matplotlib numpy pandas seaborn
```

### Çalıştırma
```bash
python balik_simulasyonu.py
```

## 📁 Veri Kaydetme

**S** tuşuna basarak simülasyon verilerini JSON formatında kaydedebilirsiniz:
- Popülasyon geçmişi
- Renk dağılımı
- Su ortamı koşulları
- Genetik çeşitlilik
- Tür dağılımı

## 🎓 Eğitim Değeri

Bu simülasyon şu konuları öğretir:
- **Biyoloji**: Genetik, evrim, ekoloji
- **Matematik**: İstatistik, olasılık
- **Programlama**: OOP, veri analizi
- **Sistem Düşüncesi**: Karmaşık etkileşimler

## 🔧 Teknik Detaylar

- **Dil**: Python 3.11+
- **Grafik**: Pygame
- **Analiz**: Matplotlib, NumPy
- **Veri**: JSON, Pandas
- **Mimari**: Nesne yönelimli programlama

## 📊 Performans

- **Başlangıç Popülasyonu**: 180 balık
- **Kritik Eşik**: 25 balık (otomatik yenileme)
- **FPS**: 60 (normal), 120 (hızlı mod)
- **Akvaryum Boyutu**: 1200x800 piksel

## 🐟 Balık Şekilleri

Simülasyon farklı balık türleri için özel şekiller kullanır:
- **Koi**: Büyük oval gövde + yüzgeçler
- **Japon Balığı**: Yuvarlak gövde + kuyruk
- **Diğerleri**: Elips gövde + üçgen kuyruk

## 🌊 Su Ortamı Etkileri

### Sıcaklık Etkileri
- **Soğuk (<15°C)**: Yavaş hareket, yüksek ölüm riski
- **İdeal (20-28°C)**: Optimal performans
- **Sıcak (>35°C)**: Stres, enerji kaybı

### pH Etkileri
- **Asidik (<6.0)**: Sağlık problemleri
- **İdeal (6.5-7.5)**: Optimal yaşam
- **Bazik (>8.5)**: Stres faktörü

### Oksijen Etkileri
- **Düşük (<70%)**: Yüksek ölüm riski
- **Normal (70-100%)**: Sağlıklı yaşam
- **Yüksek (>100%)**: Bonus sağlık

## 🎯 Simülasyon Hedefleri

1. **Popülasyon Dengesi**: Sürdürülebilir balık sayısı
2. **Genetik Çeşitlilik**: Renk ve tür çeşitliliği
3. **Ekolojik Denge**: Avcı-av dengeleri
4. **Adaptasyon**: Çevresel değişikliklere uyum

Bu simülasyon, karmaşık biyolojik sistemlerin nasıl çalıştığını anlamak için mükemmel bir araçtır! 🐠✨ 