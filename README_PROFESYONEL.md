# 🐠 Profesyonel Balık Evrim Simülasyonu

Bu profesyonel evrim simülasyonu, Hardy-Weinberg dengesi, doğal seçilim, mutasyon, göç ve seçici çiftleşme gibi tüm temel evrimsel mekanizmaları içerir.

## 🚀 Terminal'de Çalıştırma

### Adım 1: Gerekli Kütüphaneleri Kontrol Edin
```bash
pip list | findstr -i "matplotlib tkinter numpy"
```

### Adım 2: Simülasyonu Başlatın
```bash
python profesyonel_balik_simulasyonu.py
```

## 🎯 Arayüz Özellikleri

### **📊 Scroll Bar**
- Sol panelde **dikey scroll bar** eklenmiştir
- **Mouse wheel** ile yukarı/aşağı kaydırabilirsiniz
- Tüm kontrollere kolayca erişebilirsiniz

### **🎮 Gelişmiş Butonlar**
- **▲ Yeşil butonlar**: Değeri artırır
- **▼ Kırmızı butonlar**: Değeri azaltır
- **Beyaz kutular**: Mevcut değeri gösterir
- Butonlar artık **düzgün çalışır**

## 🧬 Kontrol Paneli

### **Population Demographics**
| Parametre | Açıklama | Aralık |
|-----------|----------|--------|
| **Initial Size** | Başlangıç popülasyon boyutu | 50-500 |
| **Carrying Capacity** | Maksimum taşıma kapasitesi | 100-1000 |
| **Mortality Rate** | Ölüm oranı | 0.01-0.5 |
| **Brood Size** | Üreme başına yavru sayısı | 2-20 |
| **Sex-Ratio Female:Male** | Dişi/erkek oranı | 0.1-0.9 |
| **Initial 'R' Allele Prop.** | Başlangıç kırmızı allel oranı | 0.0-1.0 |

### **Evolutionary Parameters**

#### **Migration (Göç)**
- **Migration Rate**: Göç oranı (0.0-0.1)
- **Migrant 'R' Allele Prop.**: Göçmenlerdeki kırmızı allel oranı

#### **Mutation Rate (Mutasyon)**
- **R to r**: Kırmızıdan beyaza mutasyon oranı
- **r to R**: Beyazdan kırmızıya mutasyon oranı

### **Genotype Relative Fitness**
- **RR**: Kırmızı-kırmızı genotip fitness'ı (0.0-2.0)
- **Rr**: Kırmızı-beyaz genotip fitness'ı (0.0-2.0)
- **rr**: Beyaz-beyaz genotip fitness'ı (0.0-2.0)

### **Assortative Mating**
- **Strength of Assortment**: Seçici çiftleşme gücü (0.0-1.0)

## 📈 Gerçek Zamanlı Grafikler

### **1. 🐠 Population Size Over Time**
- Popülasyon boyutunun nesiller boyunca değişimi
- Mavi çizgi ile gösterilir

### **2. 🔴⚪ Allele Frequencies**
- **Kırmızı çizgi**: K (kırmızı) allel frekansı
- **Gri çizgi**: B (beyaz) allel frekansı
- 0-1 arasında değişir

### **3. 📊 Genotype Distribution**
- **Koyu kırmızı**: KK genotip frekansı
- **Turuncu**: KB genotip frekansı  
- **Gri**: BB genotip frekansı

### **4. 💪 Average Fitness**
- Popülasyonun ortalama fitness değeri
- Mor çizgi ile gösterilir

## 🎮 Kontrol Butonları

| Buton | Fonksiyon |
|-------|-----------|
| **▶ Start** | Simülasyonu başlatır |
| **⏸ Pause** | Simülasyonu duraklatır |
| **🔄 Reset** | Simülasyonu sıfırlar |
| **💾 Save Data** | Verileri JSON formatında kaydeder |

### **Simulation Speed**
- **Kaydırıcı**: 0.1x - 5.0x hız aralığı
- Simülasyon hızını gerçek zamanlı ayarlayabilirsiniz

## 🔬 Bilimsel Kavramlar

### **Hardy-Weinberg Dengesi**
- Başlangıç genotip frekansları: p² (KK), 2pq (KB), q² (BB)
- p = kırmızı allel frekansı, q = beyaz allel frekansı

### **Doğal Seçilim**
- Fitness değerlerine göre hayatta kalma
- Yüksek fitness = düşük ölüm riski

### **Mutasyon**
- İki yönlü: K ↔ B
- Allel frekanslarını değiştirir

### **Göç (Gene Flow)**
- Dış popülasyondan gen akışı
- Allel frekanslarını etkiler

### **Seçici Çiftleşme**
- Aynı fenotipli bireyler arası tercih
- Genotip frekanslarını değiştirir

## 📊 Veri Kaydetme

**💾 Save Data** butonuna basarak:
- Tüm parametreler
- Nesil verileri
- Popülasyon değişimi
- Allel frekansları
- Fitness değerleri

JSON formatında kaydedilir.

## 🎯 Deneyim Önerileri

### **Doğal Seçilim Testi**
1. RR fitness'ını 1.5'e ayarlayın
2. Diğerlerini 1.0'da bırakın
3. Start'a basın
4. Kırmızı allel frekansının artışını izleyin

### **Mutasyon Etkisi**
1. R to r mutasyonu 0.05'e ayarlayın
2. r to R mutasyonu 0.01'de bırakın
3. Beyaz allel frekansının artışını gözlemleyin

### **Göç Etkisi**
1. Migration Rate'i 0.02'ye ayarlayın
2. Migrant R Allele Prop.'u 0.8'e ayarlayın
3. Kırmızı allel frekansının artışını izleyin

### **Seçici Çiftleşme**
1. Strength of Assortment'ı 0.8'e ayarlayın
2. Hardy-Weinberg dengesinden sapmaları gözlemleyin

## 🐛 Sorun Giderme

### **Emoji Uyarıları**
- Font eksikliği uyarıları normal
- Simülasyon çalışmasını etkilemez

### **Scroll Problemi**
- Mouse wheel kullanın
- Scroll bar'ı sürükleyin

### **Buton Çalışmıyor**
- ▲▼ butonları güncellenmiştir
- Değer kutularında sonucu görebilirsiniz

## 🎓 Eğitim Değeri

Bu simülasyon şunları öğretir:
- **Popülasyon Genetiği**: Allel frekansları
- **Evrim Mekanizmaları**: Seçilim, mutasyon, göç
- **Hardy-Weinberg Dengesi**: Teorik vs gerçek
- **Matematiksel Modelleme**: Olasılık ve istatistik

## 📚 Bilimsel Referanslar

- Hardy-Weinberg Principle
- Population Genetics Theory
- Evolutionary Biology
- Mathematical Biology

Bu simülasyon, üniversite düzeyinde biyoloji ve evrim derslerinde kullanılabilir! 🧬✨ 