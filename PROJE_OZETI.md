# 🦋 Böcek Popülasyonu Simülasyon Projesi

Bu proje, Python kullanarak geliştirilmiş kapsamlı bir böcek popülasyonu simülasyon sistemidir. Doğal seçilim, genetik kalıtım, çevresel faktörler ve ekolojik etkileşimleri modelleyen iki farklı simülasyon seviyesi sunar.

## 📁 Proje Dosyaları

### 🎮 Simülasyon Dosyaları
- **`bocek_simulasyonu.py`** - Temel böcek simülasyonu (292 satır)
- **`gelismis_bocek_simulasyonu.py`** - Gelişmiş ekosisteemi simülasyonu (1046 satır)

### 📊 Analiz Araçları
- **`simulasyon_analizi.py`** - Veri analizi ve görselleştirme aracı (420 satır)

### 📚 Dokümantasyon
- **`README.md`** - Temel simülasyon kılavuzu
- **`README_GELISMIS.md`** - Gelişmiş simülasyon detaylı kılavuzu
- **`PROJE_OZETI.md`** - Bu dosya (genel proje özeti)

### ⚙️ Konfigürasyon
- **`requirements.txt`** - Python kütüphane gereksinimleri

## 🚀 Hızlı Başlangıç

```bash
# 1. Kütüphaneleri yükle
pip install -r requirements.txt

# 2. Temel simülasyonu çalıştır
python bocek_simulasyonu.py

# 3. Gelişmiş simülasyonu çalıştır
python gelismis_bocek_simulasyonu.py

# 4. Veri analizi aracını çalıştır
python simulasyon_analizi.py
```

## 🎯 Simülasyon Seviyeleri

### 🟢 Temel Simülasyon (`bocek_simulasyonu.py`)
**Özellikler:**
- 5 farklı renk (kırmızı, mavi, yeşil, sarı, mor)
- Basit doğal seçilim
- Temel üreme sistemi
- Mutasyon (%5 şans)
- Pygame ile görselleştirme
- Matplotlib ile grafikler

**Kontroller:**
- R: Yeniden başlat
- G: Grafikleri göster

### 🔴 Gelişmiş Simülasyon (`gelismis_bocek_simulasyonu.py`)
**Özellikler:**
- 8 farklı renk + 4 farklı tür
- Karmaşık genetik sistem (zeka, güç, dayanıklılık)
- Davranış türleri (agresif, sosyal, pasif, yalnız)
- Çevre sistemi (mevsim, sıcaklık, nem)
- Yiyecek kaynakları ve avcılar
- Cinsiyet sistemi ve hamilelik
- Hastalık mekaniği
- 3 farklı görünüm modu

**Kontroller:**
- SPACE: Duraklat/Devam
- F: Hızlı mod
- 1,2,3: Görünüm modları
- R: Yeniden başlat
- G: Grafikler
- S: Veri kaydet

### 📈 Analiz Aracı (`simulasyon_analizi.py`)
**Özellikler:**
- JSON veri yükleme
- 10 farklı analiz türü
- Karşılaştırmalı grafikler
- İstatistiksel analiz
- Rapor oluşturma

## 🧬 Bilimsel Modelleme

### Doğal Seçilim Faktörleri
- **Renk Avantajı**: Kamuflaj ve görünürlük
- **Tür Avantajı**: Sosyal vs bireysel yaşam
- **Çevresel Stres**: Sıcaklık, yiyecek kıtlığı
- **Yaşlanma**: Yaşa bağlı ölüm riski
- **Hastalık**: Enerji tüketimi artışı

### Genetik Sistem
- **Kalıtım**: Ebeveyn özelliklerinin karışımı
- **Mutasyon**: Rastgele genetik değişiklikler
- **Çeşitlilik**: Popülasyon içi varyasyon
- **Adaptasyon**: Çevresel baskılara uyum

## 📊 Veri Analizi Özellikleri

### Analiz Türleri
1. **Temel İstatistikler** - Popülasyon özeti
2. **Popülasyon Karşılaştırması** - Simülasyonlar arası
3. **Renk Evrim Analizi** - Renk dağılımı değişimi
4. **Genetik Çeşitlilik** - Özellik evrimleri
5. **Çevre Etkisi** - Korelasyon analizleri
6. **Başarı Metrikleri** - Renk/tür performansı
7. **Hayatta Kalma** - Normalize eğriler
8. **Rapor Oluşturma** - Kapsamlı analiz

### Görselleştirme
- Zaman serisi grafikleri
- Scatter plot analizleri
- Pasta grafikleri
- Çoklu subplot karşılaştırmaları
- İstatistiksel korelasyonlar

## 🎓 Eğitim Değeri

### Biyoloji Kavramları
- Doğal seçilim ve evrim
- Popülasyon dinamikleri
- Genetik kalıtım
- Ekolojik etkileşimler
- Av-avcı ilişkileri

### Matematik ve İstatistik
- Olasılık hesaplamaları
- İstatistiksel analiz
- Korelasyon analizi
- Veri görselleştirme

### Programlama
- Nesne yönelimli tasarım
- Simülasyon algoritmaları
- Veri yapıları
- Görselleştirme teknikleri

## 🔬 Araştırma Fırsatları

### Deneysel Senaryolar
- İklim değişikliği etkisi
- Habitat kaybı simülasyonu
- İnvaziv tür etkisi
- Genetik çeşitlilik kaybı
- Sosyal davranış avantajları

### Geliştirme Alanları
- Makine öğrenmesi entegrasyonu
- Web tabanlı arayüz
- Gerçek zamanlı veri analizi
- Çoklu habitat modelleme
- Hibridizasyon sistemi

## 📈 Performans ve Optimizasyon

### Teknik Özellikler
- 60-120 FPS simülasyon hızı
- Binlerce böcek desteği
- Efficient collision detection
- Memory management
- Real-time statistics

### Sistem Gereksinimleri
- Python 3.7+
- 4GB RAM (önerilen)
- Grafik kartı (pygame için)
- 100MB disk alanı

## 🤝 Katkıda Bulunma

### Geliştirme Alanları
1. **Yeni Özellikler**
   - Ek böcek türleri
   - Çevre faktörleri
   - Davranış modelleri

2. **Optimizasyon**
   - Performans iyileştirmeleri
   - Bellek kullanımı
   - Algoritma optimizasyonu

3. **Görselleştirme**
   - 3D modelleme
   - Gelişmiş animasyonlar
   - VR/AR desteği

4. **Analiz**
   - İleri istatistiksel yöntemler
   - Makine öğrenmesi
   - Tahmin modelleri

## 📚 Referanslar ve Kaynaklar

### Bilimsel Temeller
- Population Biology Theory
- Evolutionary Algorithms
- Ecological Modeling
- Genetic Programming

### Teknik Kaynaklar
- Pygame Documentation
- Matplotlib Tutorials
- NumPy Scientific Computing
- Object-Oriented Design Patterns

## 🏆 Proje Başarıları

### Teknik Başarılar
- ✅ Kapsamlı genetik modelleme
- ✅ Gerçek zamanlı görselleştirme
- ✅ Çoklu analiz araçları
- ✅ Modüler kod yapısı
- ✅ Kapsamlı dokümantasyon

### Eğitim Başarıları
- ✅ Biyoloji kavramlarını görselleştirme
- ✅ İstatistiksel düşünce geliştirme
- ✅ Programlama becerilerini artırma
- ✅ Bilimsel yöntem öğretimi

## 🔮 Gelecek Planları

### Kısa Vadeli (1-3 ay)
- Web tabanlı arayüz
- Mobil uygulama versiyonu
- Çoklu dil desteği
- Performans optimizasyonları

### Orta Vadeli (3-6 ay)
- Makine öğrenmesi entegrasyonu
- Bulut tabanlı simülasyon
- Sosyal özellikler (paylaşım)
- Eğitim modülü geliştirme

### Uzun Vadeli (6+ ay)
- VR/AR desteği
- Gerçek ekolojik veri entegrasyonu
- Akademik araştırma işbirlikleri
- Ticari eğitim paketi

---

**Proje İstatistikleri:**
- Toplam Kod Satırı: ~1,800
- Dosya Sayısı: 6
- Kütüphane Sayısı: 5
- Geliştirme Süresi: Kapsamlı
- Eğitim Seviyesi: Başlangıç-İleri

**Lisans:** Eğitim amaçlı açık kaynak proje

**İletişim:** Geliştirme ve katkı için GitHub üzerinden iletişime geçebilirsiniz. 