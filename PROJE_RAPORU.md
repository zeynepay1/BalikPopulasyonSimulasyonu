# 🐠 Gerçekçi Balık Popülasyon Genetiği Simülasyonu

## 📋 Proje Özeti

Bu simülasyon, bir balık popülasyonundaki genetik değişimleri 200 yıllık süreçte gerçekçi çevresel faktörlerle birlikte modellemektedir. Hardy-Weinberg prensipleri temel alınarak, doğal seçilim, genetik sürüklenme, mutasyon ve çevresel felaketlerin allel frekanslarına etkisi incelenmiştir.

## 🧬 Genetik Model

### Allel Yapısı
- **K (Kırmızı)**: Dominant allel - sıcak renkli fenotip
- **B (Beyaz)**: Resesif allel - beyaz fenotip
- **Genotip Kombinasyonları**: KK, KB, BB

### Başlangıç Koşulları
- **Hardy-Weinberg Dengesi**: p(K) = 0.6, q(B) = 0.4
- **Genotip Frekansları**: 
  - KK: 36% (p²)
  - KB: 48% (2pq) 
  - BB: 16% (q²)

## 🌍 Çevresel Faktörler ve Gerçek Dünya Etkisi

### Mevsimsel Döngüler
```
İlkbahar (0): Üreme mevsimi, besin artışı (%30)
Yaz (1):      Optimal koşullar, maksimum besin (%50)
Sonbahar (2): Besin azalması başlangıcı (%10 azalma)
Kış (3):      Zorlu koşullar, besin kıtlığı (%50 azalma)
```

### Sıcaklık Dinamikleri
- **Sinüzoidal değişim**: T(t) = T₀ + A×cos(2π×mevsim/4)
- **Genotip-spesifik tolerans**:
  - KK: Soğuk adaptasyonu (T < 10°C → fitness +20%)
  - BB: Sıcak adaptasyonu (T > 20°C → fitness +10%)
  - KB: Heterozygot avantajı (fitness +5%)

### Çevresel Stres Faktörleri
- **pH Değişimleri**: Optimal pH 7.0'dan sapma fitness azaltır
- **Kirlilik Seviyesi**: 0-100% arasında, fitness'ı %30'a kadar azaltabilir
- **Besin Bolluğu**: 0.2-2.0 arasında değişken

## ⚡ Catastrofik Olaylar ve Etki Analizi

### 1. Hastalık Salgınları (%3 olasılık/yıl)
- **Etki**: %30-70 popülasyon kaybı
- **Genetik Nötr**: Tüm genotipleri eşit etkiler
- **Genetik Sürüklenme**: Küçük popülasyonlarda frekans değişimi

### 2. Yırtıcı İstilaları (%2 olasılık/yıl)
- **Seçici Avlanma**: Renkli balıklar daha görünür
  - KK kayıp: Baz oran × 1.3
  - KB kayıp: Baz oran × 1.1  
  - BB kayıp: Baz oran × 0.8
- **Doğal Seçilim**: Kamuflaj avantajı

### 3. İklim Değişikliği (%1 olasılık/yıl)
- **Sıcaklık Kayması**: ±2-3°C kalıcı değişim
- **Kirlilik Artışı**: +%5-15 kirlilik seviyesi
- **Uzun Vadeli Etki**: Fitness dengelerini değiştirir

### 4. Habitat Bozulması (%1.5 olasılık/yıl)
- **Taşıma Kapasitesi**: %10-30 azalma
- **Besin Kaynağı**: Orantılı azalma
- **Popülasyon Baskısı**: Rekabet artışı

## 📊 Analiz Metodolojileri

### 1. Allel Frekans Takibi
```python
p(t) = (2×N_KK + N_KB) / (2×N_total)
q(t) = 1 - p(t)
```

### 2. Hardy-Weinberg Sapma Analizi
```python
Sapma = |f_KK_gözlenen - p²| + |f_KB_gözlenen - 2pq| + |f_BB_gözlenen - q²|
```

### 3. Fitness Hesaplama
```python
W_genotip = W_base × W_sıcaklık × W_besin × W_kirlilik × W_pH
```

### 4. Genetik Sürüklenme
- **Küçük popülasyon** (N < 100): %10 rastgele değişim
- **Orta popülasyon** (100 < N < 300): %5 rastgele değişim
- **Büyük popülasyon** (N > 300): Ihmal edilebilir

## 🔬 Bilimsel Temel ve Referanslar

### Popülasyon Genetiği Prensipleri
1. **Hardy-Weinberg Dengesi**: İdeal koşullarda allel frekansları sabit kalır
2. **Doğal Seçilim**: Fitness farklılıkları frekans değişimine neden olur
3. **Genetik Sürüklenme**: Sonlu popülasyonlarda rastgele örnekleme etkisi
4. **Mutasyon**: Düşük oranlı (%0.1) rastgele allel değişimi

### Ekolojik Gerçekçilik
- **Mevsimsel Dinamikler**: Gerçek ekosistem döngüleri
- **Taşıma Kapasitesi**: Çevresel limitler
- **Yırtıcı-Av İlişkileri**: Seçici avlanma baskısı
- **İklim Etkileri**: Küresel ısınma simülasyonu

## 📈 Sonuç İnterpreteasyonu

### Beklenen Evrimsel Trendler
1. **Yırtıcı Baskısı**: B alleli frekansında artış (kamuflaj avantajı)
2. **İklim Değişikliği**: Sıcaklık toleransına göre KK/BB dengesi
3. **Heterozygot Avantajı**: KB genotipi frekansında stabilizasyon
4. **Stokastik Faktörler**: Küçük popülasyonlarda dramatik değişimler

### Kritik Gözlem Noktaları
- **Allel Fiksasyonu**: Bir allelin tamamen kaybolması
- **Dengede Sapma**: Hardy-Weinberg'den uzaklaşma
- **Popülasyon Bottleneck**: Kritik popülasyon seviyesi (N < 50)
- **Evrimsel Rescue**: Çevresel değişime adaptasyon

## 🎯 Eğitimsel Değer

Bu simülasyon öğrencilere şunları öğretir:
- Popülasyon genetiği temel kavramları
- Çevresel faktörlerin evrime etkisi
- Stokastik vs deterministik süreçler
- Gerçek dünya ekolojik dinamikleri
- Veri analizi ve görselleştirme

## ⚙️ Teknik Spesifikasyonlar

- **Programlama Dili**: Python 3.8+
- **Kütüphaneler**: NumPy, Matplotlib, Tkinter
- **Simülasyon Süresi**: 200 yıl / 800 mevsim
- **Veri Noktaları**: Yıllık kayıt sistemi
- **Görselleştirme**: 6 panel interaktif grafik sistemi

## 🔄 Reproducibility (Tekrarlanabilirlik)

Simülasyon verileri JSON formatında kaydedilir:
- Başlangıç parametreleri
- Yıllık popülasyon verileri  
- Çevresel koşul kayıtları
- Catastrofik olay geçmişi
- Özet istatistikler

---

*Bu simülasyon, popülasyon genetiği ve ekolojinin temel prensiplerini gerçekçi bir modelde birleştirerek, öğrencilere evrimsel süreçlerin karmaşıklığını praktik bir şekilde göstermektedir.* 