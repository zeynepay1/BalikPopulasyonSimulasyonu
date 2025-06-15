import json
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import datetime
import glob
import os
from typing import List, Dict, Any
import seaborn as sns

class SimulasyonAnalizi:
    """Simülasyon verilerini analiz etmek için araç"""
    
    def __init__(self):
        self.veriler = []
        self.dosya_adlari = []
        
    def veri_yukle(self, dosya_yolu: str = None):
        """JSON verilerini yükle"""
        if dosya_yolu:
            # Belirli dosya yükle
            try:
                with open(dosya_yolu, 'r', encoding='utf-8') as f:
                    veri = json.load(f)
                    self.veriler.append(veri)
                    self.dosya_adlari.append(dosya_yolu)
                print(f"Veri yüklendi: {dosya_yolu}")
            except Exception as e:
                print(f"Veri yükleme hatası: {e}")
        else:
            # Tüm simulasyon verilerini yükle
            dosyalar = glob.glob("simulasyon_verileri_*.json")
            for dosya in dosyalar:
                try:
                    with open(dosya, 'r', encoding='utf-8') as f:
                        veri = json.load(f)
                        self.veriler.append(veri)
                        self.dosya_adlari.append(dosya)
                except Exception as e:
                    print(f"Dosya yükleme hatası ({dosya}): {e}")
            
            print(f"Toplam {len(self.veriler)} simülasyon verisi yüklendi.")
    
    def temel_istatistikler(self):
        """Temel istatistikleri göster"""
        if not self.veriler:
            print("Önce veri yükleyin!")
            return
        
        print("\n=== TEMEL İSTATİSTİKLER ===")
        
        for i, veri in enumerate(self.veriler):
            print(f"\nSimülasyon {i+1} ({self.dosya_adlari[i]}):")
            print(f"  Toplam Zaman: {veri['zaman']}")
            print(f"  Nesil Sayısı: {veri['nesil']}")
            print(f"  Son Popülasyon: {veri['bocek_sayisi']}")
            
            if veri['populasyon_gecmisi']:
                max_pop = max(veri['populasyon_gecmisi'])
                min_pop = min(veri['populasyon_gecmisi'])
                ort_pop = np.mean(veri['populasyon_gecmisi'])
                print(f"  Maksimum Popülasyon: {max_pop}")
                print(f"  Minimum Popülasyon: {min_pop}")
                print(f"  Ortalama Popülasyon: {ort_pop:.1f}")
            
            # En başarılı renk
            if veri['renk_dagilimi_gecmisi']:
                son_dagilim = veri['renk_dagilimi_gecmisi'][-1]
                en_basarili = max(son_dagilim.items(), key=lambda x: x[1])
                print(f"  En Başarılı Renk: {en_basarili[0]} ({en_basarili[1]} birey)")
    
    def populasyon_karsilastirmasi(self):
        """Farklı simülasyonların popülasyon değişimlerini karşılaştır"""
        if not self.veriler:
            print("Önce veri yükleyin!")
            return
        
        plt.figure(figsize=(14, 8))
        
        for i, veri in enumerate(self.veriler):
            if veri['populasyon_gecmisi']:
                plt.plot(veri['populasyon_gecmisi'], 
                        label=f"Simülasyon {i+1}", 
                        linewidth=2, alpha=0.8)
        
        plt.title('Simülasyonlar Arası Popülasyon Karşılaştırması', fontsize=16, fontweight='bold')
        plt.xlabel('Zaman')
        plt.ylabel('Popülasyon')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()
    
    def renk_evrim_analizi(self):
        """Renk dağılımının evrimini analiz et"""
        if not self.veriler:
            print("Önce veri yükleyin!")
            return
        
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        axes = axes.flatten()
        
        for i, veri in enumerate(self.veriler[:4]):  # İlk 4 simülasyon
            if i >= len(axes):
                break
                
            ax = axes[i]
            
            if veri['renk_dagilimi_gecmisi']:
                # Her renk için zaman serisi oluştur
                renkler = ['kirmizi', 'mavi', 'yesil', 'sari', 'mor', 'turuncu', 'pembe', 'kahverengi']
                
                for renk in renkler:
                    renk_verileri = [dagilim.get(renk, 0) for dagilim in veri['renk_dagilimi_gecmisi']]
                    if max(renk_verileri) > 0:  # Sadece var olan renkleri göster
                        ax.plot(renk_verileri, label=renk.capitalize(), linewidth=2)
                
                ax.set_title(f'Simülasyon {i+1} - Renk Evrimi')
                ax.set_xlabel('Zaman')
                ax.set_ylabel('Birey Sayısı')
                ax.legend()
                ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
    
    def genetik_cesitlilik_analizi(self):
        """Genetik çeşitlilik değişimini analiz et"""
        if not self.veriler:
            print("Önce veri yükleyin!")
            return
        
        fig, axes = plt.subplots(2, 2, figsize=(16, 10))
        
        # Zeka evrimi
        axes[0,0].set_title('Ortalama Zeka Evrimi')
        for i, veri in enumerate(self.veriler):
            if veri['genetik_cesitlilik_gecmisi']:
                zeka_verileri = [g['zeka'] for g in veri['genetik_cesitlilik_gecmisi']]
                axes[0,0].plot(zeka_verileri, label=f'Sim {i+1}', linewidth=2)
        axes[0,0].set_ylabel('Zeka Seviyesi')
        axes[0,0].legend()
        axes[0,0].grid(True, alpha=0.3)
        
        # Güç evrimi
        axes[0,1].set_title('Ortalama Güç Evrimi')
        for i, veri in enumerate(self.veriler):
            if veri['genetik_cesitlilik_gecmisi']:
                guc_verileri = [g['guc'] for g in veri['genetik_cesitlilik_gecmisi']]
                axes[0,1].plot(guc_verileri, label=f'Sim {i+1}', linewidth=2)
        axes[0,1].set_ylabel('Güç Seviyesi')
        axes[0,1].legend()
        axes[0,1].grid(True, alpha=0.3)
        
        # Dayanıklılık evrimi
        axes[1,0].set_title('Ortalama Dayanıklılık Evrimi')
        for i, veri in enumerate(self.veriler):
            if veri['genetik_cesitlilik_gecmisi']:
                dayaniklilik_verileri = [g['dayaniklilik'] for g in veri['genetik_cesitlilik_gecmisi']]
                axes[1,0].plot(dayaniklilik_verileri, label=f'Sim {i+1}', linewidth=2)
        axes[1,0].set_ylabel('Dayanıklılık Seviyesi')
        axes[1,0].legend()
        axes[1,0].grid(True, alpha=0.3)
        
        # Mutasyon sayısı
        axes[1,1].set_title('Toplam Mutasyon Sayısı')
        for i, veri in enumerate(self.veriler):
            if veri['genetik_cesitlilik_gecmisi']:
                mutasyon_verileri = [g['mutasyon'] for g in veri['genetik_cesitlilik_gecmisi']]
                axes[1,1].plot(mutasyon_verileri, label=f'Sim {i+1}', linewidth=2)
        axes[1,1].set_ylabel('Mutasyon Sayısı')
        axes[1,1].legend()
        axes[1,1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
    
    def cevre_etkisi_analizi(self):
        """Çevre koşullarının popülasyon üzerindeki etkisini analiz et"""
        if not self.veriler:
            print("Önce veri yükleyin!")
            return
        
        for i, veri in enumerate(self.veriler):
            if veri['cevre_gecmisi'] and veri['populasyon_gecmisi']:
                fig, axes = plt.subplots(2, 2, figsize=(16, 10))
                fig.suptitle(f'Simülasyon {i+1} - Çevre Etkisi Analizi', fontsize=16)
                
                # Sıcaklık vs Popülasyon
                sicakliklar = [c['sicaklik'] for c in veri['cevre_gecmisi']]
                populasyon = veri['populasyon_gecmisi'][:len(sicakliklar)]
                
                axes[0,0].scatter(sicakliklar, populasyon, alpha=0.6, c='red')
                axes[0,0].set_xlabel('Sıcaklık (°C)')
                axes[0,0].set_ylabel('Popülasyon')
                axes[0,0].set_title('Sıcaklık vs Popülasyon')
                
                # Korelasyon hesapla
                if len(sicakliklar) == len(populasyon):
                    korelasyon = np.corrcoef(sicakliklar, populasyon)[0,1]
                    axes[0,0].text(0.05, 0.95, f'Korelasyon: {korelasyon:.3f}', 
                                  transform=axes[0,0].transAxes, 
                                  bbox=dict(boxstyle="round", facecolor='wheat'))
                
                # Avcı sayısı vs Popülasyon
                avci_sayilari = [c['avci_sayisi'] for c in veri['cevre_gecmisi']]
                
                axes[0,1].scatter(avci_sayilari, populasyon, alpha=0.6, c='darkred')
                axes[0,1].set_xlabel('Avcı Sayısı')
                axes[0,1].set_ylabel('Popülasyon')
                axes[0,1].set_title('Avcı Sayısı vs Popülasyon')
                
                # Zaman serisi - Sıcaklık
                axes[1,0].plot(sicakliklar, color='red', linewidth=2)
                axes[1,0].set_xlabel('Zaman')
                axes[1,0].set_ylabel('Sıcaklık (°C)')
                axes[1,0].set_title('Sıcaklık Değişimi')
                axes[1,0].grid(True, alpha=0.3)
                
                # Zaman serisi - Avcı sayısı
                axes[1,1].plot(avci_sayilari, color='darkred', linewidth=2)
                axes[1,1].set_xlabel('Zaman')
                axes[1,1].set_ylabel('Avcı Sayısı')
                axes[1,1].set_title('Avcı Sayısı Değişimi')
                axes[1,1].grid(True, alpha=0.3)
                
                plt.tight_layout()
                plt.show()
    
    def basari_metrikleri(self):
        """Farklı renk ve türlerin başarı metriklerini hesapla"""
        if not self.veriler:
            print("Önce veri yükleyin!")
            return
        
        print("\n=== BAŞARI METRİKLERİ ===")
        
        # Renk başarı analizi
        renk_basarilari = {}
        
        for veri in self.veriler:
            if veri['renk_dagilimi_gecmisi']:
                for zaman_dilimi in veri['renk_dagilimi_gecmisi']:
                    for renk, sayi in zaman_dilimi.items():
                        if renk not in renk_basarilari:
                            renk_basarilari[renk] = []
                        renk_basarilari[renk].append(sayi)
        
        print("\nRenk Başarı Sıralaması (Ortalama Popülasyon):")
        renk_ortalamalari = {}
        for renk, sayilar in renk_basarilari.items():
            if sayilar:
                renk_ortalamalari[renk] = np.mean(sayilar)
        
        sirali_renkler = sorted(renk_ortalamalari.items(), key=lambda x: x[1], reverse=True)
        for i, (renk, ortalama) in enumerate(sirali_renkler, 1):
            print(f"{i}. {renk.capitalize()}: {ortalama:.1f} birey")
        
        # Görselleştirme
        plt.figure(figsize=(12, 6))
        renkler = [item[0] for item in sirali_renkler]
        degerler = [item[1] for item in sirali_renkler]
        
        bars = plt.bar(renkler, degerler, color=['red', 'blue', 'green', 'yellow', 'purple', 'orange', 'pink', 'brown'][:len(renkler)])
        plt.title('Renklerin Ortalama Başarı Sıralaması', fontsize=14, fontweight='bold')
        plt.xlabel('Renk')
        plt.ylabel('Ortalama Popülasyon')
        plt.xticks(rotation=45)
        
        # Değerleri çubukların üzerine yaz
        for bar, deger in zip(bars, degerler):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, 
                    f'{deger:.1f}', ha='center', va='bottom')
        
        plt.tight_layout()
        plt.show()
    
    def hayatta_kalma_analizi(self):
        """Hayatta kalma eğrilerini analiz et"""
        if not self.veriler:
            print("Önce veri yükleyin!")
            return
        
        plt.figure(figsize=(14, 8))
        
        for i, veri in enumerate(self.veriler):
            if veri['populasyon_gecmisi']:
                # Normalize et (başlangıç popülasyonuna göre)
                populasyon = np.array(veri['populasyon_gecmisi'])
                if len(populasyon) > 0 and populasyon[0] > 0:
                    normalize_pop = populasyon / populasyon[0] * 100
                    plt.plot(normalize_pop, label=f'Simülasyon {i+1}', linewidth=2, alpha=0.8)
        
        plt.title('Normalize Edilmiş Hayatta Kalma Eğrileri', fontsize=16, fontweight='bold')
        plt.xlabel('Zaman')
        plt.ylabel('Başlangıç Popülasyonuna Göre % Oran')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.axhline(y=100, color='red', linestyle='--', alpha=0.5, label='Başlangıç Seviyesi')
        plt.tight_layout()
        plt.show()
    
    def rapor_olustur(self, dosya_adi: str = None):
        """Kapsamlı analiz raporu oluştur"""
        if not self.veriler:
            print("Önce veri yükleyin!")
            return
        
        if not dosya_adi:
            zaman_damgasi = datetime.now().strftime("%Y%m%d_%H%M%S")
            dosya_adi = f"simulasyon_raporu_{zaman_damgasi}.txt"
        
        with open(dosya_adi, 'w', encoding='utf-8') as f:
            f.write("=== SİMÜLASYON ANALİZ RAPORU ===\n")
            f.write(f"Oluşturulma Tarihi: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Analiz Edilen Simülasyon Sayısı: {len(self.veriler)}\n\n")
            
            # Temel istatistikler
            f.write("=== TEMEL İSTATİSTİKLER ===\n")
            for i, veri in enumerate(self.veriler):
                f.write(f"\nSimülasyon {i+1}:\n")
                f.write(f"  Dosya: {self.dosya_adlari[i]}\n")
                f.write(f"  Toplam Zaman: {veri['zaman']}\n")
                f.write(f"  Nesil Sayısı: {veri['nesil']}\n")
                f.write(f"  Son Popülasyon: {veri['bocek_sayisi']}\n")
                
                if veri['populasyon_gecmisi']:
                    max_pop = max(veri['populasyon_gecmisi'])
                    min_pop = min(veri['populasyon_gecmisi'])
                    ort_pop = np.mean(veri['populasyon_gecmisi'])
                    f.write(f"  Maksimum Popülasyon: {max_pop}\n")
                    f.write(f"  Minimum Popülasyon: {min_pop}\n")
                    f.write(f"  Ortalama Popülasyon: {ort_pop:.1f}\n")
                
                # En başarılı renk
                if veri['renk_dagilimi_gecmisi']:
                    son_dagilim = veri['renk_dagilimi_gecmisi'][-1]
                    en_basarili = max(son_dagilim.items(), key=lambda x: x[1])
                    f.write(f"  En Başarılı Renk: {en_basarili[0]} ({en_basarili[1]} birey)\n")
            
            # Genel değerlendirme
            f.write("\n=== GENEL DEĞERLENDİRME ===\n")
            
            # Ortalama simülasyon süresi
            ortalama_zaman = np.mean([veri['zaman'] for veri in self.veriler])
            f.write(f"Ortalama Simülasyon Süresi: {ortalama_zaman:.1f} zaman birimi\n")
            
            # Ortalama nesil sayısı
            ortalama_nesil = np.mean([veri['nesil'] for veri in self.veriler])
            f.write(f"Ortalama Nesil Sayısı: {ortalama_nesil:.1f}\n")
            
            # En başarılı renk genel
            tum_renk_verileri = {}
            for veri in self.veriler:
                if veri['renk_dagilimi_gecmisi']:
                    for zaman_dilimi in veri['renk_dagilimi_gecmisi']:
                        for renk, sayi in zaman_dilimi.items():
                            if renk not in tum_renk_verileri:
                                tum_renk_verileri[renk] = []
                            tum_renk_verileri[renk].append(sayi)
            
            if tum_renk_verileri:
                renk_ortalamalari = {renk: np.mean(sayilar) for renk, sayilar in tum_renk_verileri.items()}
                en_basarili_genel = max(renk_ortalamalari.items(), key=lambda x: x[1])
                f.write(f"Genel En Başarılı Renk: {en_basarili_genel[0]} (Ort: {en_basarili_genel[1]:.1f})\n")
        
        print(f"Rapor oluşturuldu: {dosya_adi}")

def main():
    """Ana fonksiyon"""
    print("=== SİMÜLASYON VERİ ANALİZ ARACI ===")
    
    analiz = SimulasyonAnalizi()
    
    while True:
        print("\n--- MENÜ ---")
        print("1. Veri Yükle (Tüm dosyalar)")
        print("2. Belirli Dosya Yükle")
        print("3. Temel İstatistikler")
        print("4. Popülasyon Karşılaştırması")
        print("5. Renk Evrim Analizi")
        print("6. Genetik Çeşitlilik Analizi")
        print("7. Çevre Etkisi Analizi")
        print("8. Başarı Metrikleri")
        print("9. Hayatta Kalma Analizi")
        print("10. Rapor Oluştur")
        print("0. Çıkış")
        
        secim = input("\nSeçiminizi yapın (0-10): ").strip()
        
        if secim == "0":
            print("Çıkılıyor...")
            break
        elif secim == "1":
            analiz.veri_yukle()
        elif secim == "2":
            dosya = input("Dosya adını girin: ").strip()
            analiz.veri_yukle(dosya)
        elif secim == "3":
            analiz.temel_istatistikler()
        elif secim == "4":
            analiz.populasyon_karsilastirmasi()
        elif secim == "5":
            analiz.renk_evrim_analizi()
        elif secim == "6":
            analiz.genetik_cesitlilik_analizi()
        elif secim == "7":
            analiz.cevre_etkisi_analizi()
        elif secim == "8":
            analiz.basari_metrikleri()
        elif secim == "9":
            analiz.hayatta_kalma_analizi()
        elif secim == "10":
            dosya_adi = input("Rapor dosya adı (boş bırakabilirsiniz): ").strip()
            analiz.rapor_olustur(dosya_adi if dosya_adi else None)
        else:
            print("Geçersiz seçim!")

if __name__ == "__main__":
    main() 