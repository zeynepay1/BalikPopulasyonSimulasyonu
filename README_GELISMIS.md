# 🦋 Gelişmiş Böcek Ekosisteemi Simülasyonu

Bu proje, karmaşık ekolojik etkileşimleri, genetik çeşitliliği ve çevresel faktörleri içeren son derece gelişmiş bir böcek popülasyonu simülasyonudur.

## 🌟 Yeni Özellikler

### 🧬 Genetik Sistem
- **4 Farklı Böcek Türü**: Kelebek, Karınca, Arıcık, Böcek
- **8 Farklı Renk**: Kırmızı, Mavi, Yeşil, Sarı, Mor, Turuncu, Pembe, Kahverengi
- **Genetik Özellikler**: Zeka, Güç, Dayanıklılık
- **Mutasyon Sistemi**: %5-8 mutasyon şansı
- **Kalıtım**: Ebeveyn özelliklerinin karışımı

### 🎭 Davranış Türleri
- **Agresif**: Farklı renkteki böcekleri kovalama
- **Sosyal**: Diğer böceklere yaklaşma eğilimi
- **Pasif**: Sakin hareket
- **Yalnız**: Bağımsız yaşam

### 🌍 Çevre Sistemi
- **Mevsimsel Değişiklikler**: İlkbahar, Yaz, Sonbahar, Kış
- **Sıcaklık Etkisi**: Hareket hızını ve hayatta kalmayı etkiler
- **Nem Oranı**: Çevresel stres faktörü
- **Yiyecek Kaynakları**: 15 farklı yenilenebilir kaynak

### 🦅 Avcı Sistemi
- **Dinamik Avcılar**: Rastgele ortaya çıkan ve kaybolan avcılar
- **Av-Avcı İlişkisi**: Gerçekçi takip ve yakalama mekaniği
- **Menzil Sistemi**: Sınırlı algı alanı

### 👶 Gelişmiş Üreme
- **Cinsiyet Sistemi**: Erkek ve dişi böcekler
- **Hamilelik**: 200 zaman birimlik hamilelik süreci
- **Çoklu Yavru**: 1-4 yavru doğurma
- **Uyumluluk**: Tür bazlı üreme tercihleri

### 🏥 Sağlık Sistemi
- **Hastalık Mekaniği**: %0.2 hastalık riski
- **Enerji Sistemi**: Dinamik enerji tüketimi ve yenilenmesi
- **Yaşlanma**: Yaşa bağlı ölüm riski

## 🎮 Kontroller

| Tuş | Fonksiyon |
|-----|-----------|
| **SPACE** | Simülasyonu duraklat/devam ettir |
| **F** | Hızlı mod (120 FPS) aç/kapat |
| **1** | Normal görünüm modu |
| **2** | İstatistik görünümü |
| **3** | Genetik görünüm |
| **R** | Simülasyonu yeniden başlat |
| **G** | Grafikleri göster |
| **S** | Verileri JSON formatında kaydet |

## 👁️ Görünüm Modları

### 1. Normal Görünüm
- Böcekleri türlerine göre farklı şekillerde gösterir
- Kelebek: Kanat şekli
- Karınca: Segmentli gövde
- Enerji çubukları (kırmızı/sarı/yeşil)
- Hamilelik göstergeleri (pembe halka)
- Yiyecek kaynakları (yeşil daireler)
- Avcılar (kırmızı daireler + menzil)

### 2. İstatistik Görünümü
- Renk dağılımı pasta grafiği
- Anlık popülasyon bilgileri
- Çevre koşulları

### 3. Genetik Görünüm
- Böcekleri zeka seviyelerine göre renklendirir
- Mutasyon geçirmiş bireyleri beyaz halka ile işaretler
- Genetik çeşitliliği görsel olarak gösterir

## 📊 İstatistikler ve Grafikler

### 6 Farklı Grafik Türü:
1. **Toplam Popülasyon**: Zaman içinde popülasyon değişimi
2. **Renk Dağılımı**: Her rengin popülasyon içindeki oranı
3. **Çevre Koşulları**: Sıcaklık değişimleri
4. **Genetik Özellikler**: Ortalama zeka, güç, dayanıklılık
5. **Tür Dağılımı**: Böcek türlerinin sayısal dağılımı
6. **Avcı-Av İlişkisi**: Avcı sayısı ile popülasyon korelasyonu

## 💾 Veri Kaydetme

Simülasyon verileri JSON formatında kaydedilir:
- Popülasyon geçmişi
- Renk ve tür dağılımları
- Çevre koşulları geçmişi
- Genetik çeşitlilik verileri
- Zaman damgası ile dosya adlandırma

## 🧪 Bilimsel Modelleme

### Doğal Seçilim Faktörleri:
- **Renk Avantajı**: Kahverengi (kamuflaj) > Kırmızı > Yeşil > Mavi > Turuncu > Sarı > Mor > Pembe
- **Tür Avantajı**: Karınca (sosyal) > Arıcık > Kelebek > Böcek
- **Çevre Stresi**: Aşırı sıcaklık, yiyecek kıtlığı
- **Yaşlanma**: 500+ yaş sonrası artan ölüm riski
- **Hastalık**: 2x enerji tüketimi

### Genetik Kalıtım:
- Ebeveyn özelliklerinin ortalaması + rastgele varyasyon
- Mutasyon şansları: Renk (%8), Tür (%5), Davranış (%6)
- Nesil takibi ve soy ağacı

## 🚀 Kurulum ve Çalıştırma

```bash
# Kütüphaneleri yükle
pip install -r requirements.txt

# Gelişmiş simülasyonu çalıştır
python gelismis_bocek_simulasyonu.py
```

## 🎯 Eğitim Hedefleri

Bu simülasyon şu kavramları öğretir:

### Biyoloji:
- Doğal seçilim ve evrim
- Genetik kalıtım ve mutasyon
- Popülasyon dinamikleri
- Ekolojik etkileşimler
- Av-avcı ilişkileri
- Çevresel adaptasyon

### Matematik ve İstatistik:
- Olasılık hesaplamaları
- İstatistiksel analiz
- Veri görselleştirme
- Trend analizi

### Bilgisayar Bilimi:
- Nesne yönelimli programlama
- Simülasyon tasarımı
- Veri yapıları
- Algoritma optimizasyonu

## 🔬 Araştırma Fırsatları

### Deneyebileceğiniz Senaryolar:
1. **İklim Değişikliği**: Sıcaklık artışının etkilerini gözlemleyin
2. **Habitat Kaybı**: Yiyecek kaynaklarını azaltın
3. **İnvaziv Türler**: Yeni avcılar ekleyin
4. **Genetik Çeşitlilik**: Mutasyon oranlarını değiştirin
5. **Sosyal Davranış**: Farklı davranış türlerinin başarısını karşılaştırın

### Geliştirebileceğiniz Özellikler:
- **Hastalık Yayılımı**: Bulaşıcı hastalık modeli
- **Göç Davranışı**: Mevsimsel göç
- **Öğrenme**: Deneyim bazlı davranış değişikliği
- **Kooperasyon**: Grup halinde yaşam
- **Rekabet**: Kaynak için mücadele
- **Hibridizasyon**: Türler arası çiftleşme

## 📈 Performans Optimizasyonları

- Efficient collision detection
- Spatial partitioning for neighbor searches
- Vectorized calculations where possible
- Memory management for large populations
- Adaptive simulation speed

## 🐛 Bilinen Özellikler

- Popülasyon kritik seviyeye düştüğünde otomatik yenileme
- Avcılar açlıktan öldüğünde otomatik temizleme
- Enerji sistemi dengelemesi
- Mutasyon oranları fine-tuning

## 🤝 Katkıda Bulunma

Bu simülasyonu geliştirmek için:
1. Yeni böcek türleri ekleyin
2. Çevre faktörlerini genişletin
3. Görselleştirme seçeneklerini artırın
4. Makine öğrenmesi entegrasyonu
5. Web tabanlı arayüz geliştirin

## 📚 Referanslar

- Population Biology and Evolution Theory
- Genetic Algorithms and Natural Selection
- Ecological Modeling Principles
- Agent-Based Modeling Techniques

---

**Not**: Bu simülasyon eğitim amaçlıdır ve gerçek ekolojik sistemlerin basitleştirilmiş bir modelidir. Bilimsel araştırma için daha detaylı modeller gerekebilir. 