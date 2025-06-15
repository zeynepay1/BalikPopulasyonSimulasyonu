import matplotlib.pyplot as plt
import numpy as np
import random
import pygame
import sys
from dataclasses import dataclass
from typing import List, Tuple
import time

@dataclass
class Bocek:
    """Böcek sınıfı - her böceğin özelliklerini temsil eder"""
    x: float
    y: float
    renk: str
    boyut: float
    hiz: float
    enerji: float
    yas: int
    hayatta: bool = True
    
    def hareket_et(self, genislik: int, yukseklik: int):
        """Böceğin rastgele hareketi"""
        if self.hayatta:
            self.x += random.uniform(-self.hiz, self.hiz)
            self.y += random.uniform(-self.hiz, self.hiz)
            
            # Sınırları kontrol et
            self.x = max(0, min(genislik, self.x))
            self.y = max(0, min(yukseklik, self.y))
            
            # Enerji azalt
            self.enerji -= 0.1
            self.yas += 1
            
            # Yaşlanma ve enerji kontrolü
            if self.enerji <= 0 or self.yas > 1000:
                self.hayatta = False

class BocekSimulasyonu:
    """Ana simülasyon sınıfı"""
    
    def __init__(self, genislik=800, yukseklik=600):
        self.genislik = genislik
        self.yukseklik = yukseklik
        self.bocekler: List[Bocek] = []
        self.nesil = 0
        self.zaman = 0
        
        # Renk tanımları
        self.renkler = {
            'kirmizi': (255, 0, 0),
            'mavi': (0, 0, 255),
            'yesil': (0, 255, 0),
            'sari': (255, 255, 0),
            'mor': (128, 0, 128)
        }
        
        # İstatistik takibi
        self.populasyon_gecmisi = []
        self.renk_dagilimi_gecmisi = []
        
        # Pygame başlatma
        pygame.init()
        self.ekran = pygame.display.set_mode((genislik, yukseklik))
        pygame.display.set_caption("Böcek Popülasyonu Simülasyonu")
        self.saat = pygame.time.Clock()
        
    def baslangic_populasyonu_olustur(self, sayi=100):
        """Başlangıç böcek popülasyonunu oluştur"""
        self.bocekler.clear()
        renk_listesi = list(self.renkler.keys())
        
        for _ in range(sayi):
            bocek = Bocek(
                x=random.uniform(0, self.genislik),
                y=random.uniform(0, self.yukseklik),
                renk=random.choice(renk_listesi),
                boyut=random.uniform(3, 8),
                hiz=random.uniform(1, 3),
                enerji=random.uniform(50, 100),
                yas=0
            )
            self.bocekler.append(bocek)
    
    def dogal_secilim_uygula(self):
        """Doğal seçilim kurallarını uygula"""
        # Kırmızı böcekler daha avantajlı (daha yüksek hayatta kalma şansı)
        # Mavi böcekler orta seviye
        # Diğer renkler daha dezavantajlı
        
        for bocek in self.bocekler:
            if bocek.hayatta:
                # Renk bazlı hayatta kalma şansı
                if bocek.renk == 'kirmizi':
                    olum_sansi = 0.01
                elif bocek.renk == 'mavi':
                    olum_sansi = 0.02
                elif bocek.renk == 'yesil':
                    olum_sansi = 0.03
                else:
                    olum_sansi = 0.04
                
                if random.random() < olum_sansi:
                    bocek.hayatta = False
    
    def ureme_gerceklestir(self):
        """Böceklerin üremesini simüle et"""
        hayatta_bocekler = [b for b in self.bocekler if b.hayatta]
        
        if len(hayatta_bocekler) < 2:
            return
        
        # Üreme için yeterli enerji ve yaş kontrolü
        ureme_adaylari = [b for b in hayatta_bocekler if b.enerji > 30 and b.yas > 50]
        
        yeni_bocekler = []
        for _ in range(min(len(ureme_adaylari) // 2, 20)):  # Maksimum 20 yeni böcek
            if len(ureme_adaylari) >= 2:
                ebeveyn1 = random.choice(ureme_adaylari)
                ebeveyn2 = random.choice(ureme_adaylari)
                
                # Yavru böcek özellikleri (genetik karışım)
                yavru_renk = random.choice([ebeveyn1.renk, ebeveyn2.renk])
                
                # Mutasyon şansı (%5)
                if random.random() < 0.05:
                    yavru_renk = random.choice(list(self.renkler.keys()))
                
                yavru = Bocek(
                    x=random.uniform(0, self.genislik),
                    y=random.uniform(0, self.yukseklik),
                    renk=yavru_renk,
                    boyut=(ebeveyn1.boyut + ebeveyn2.boyut) / 2 + random.uniform(-0.5, 0.5),
                    hiz=(ebeveyn1.hiz + ebeveyn2.hiz) / 2 + random.uniform(-0.2, 0.2),
                    enerji=random.uniform(60, 90),
                    yas=0
                )
                yeni_bocekler.append(yavru)
                
                # Ebeveynlerin enerjisini azalt
                ebeveyn1.enerji -= 10
                ebeveyn2.enerji -= 10
        
        self.bocekler.extend(yeni_bocekler)
    
    def istatistikleri_guncelle(self):
        """Popülasyon istatistiklerini güncelle"""
        hayatta_bocekler = [b for b in self.bocekler if b.hayatta]
        toplam_sayi = len(hayatta_bocekler)
        
        # Renk dağılımı
        renk_sayilari = {}
        for renk in self.renkler.keys():
            renk_sayilari[renk] = len([b for b in hayatta_bocekler if b.renk == renk])
        
        self.populasyon_gecmisi.append(toplam_sayi)
        self.renk_dagilimi_gecmisi.append(renk_sayilari.copy())
    
    def ciz(self):
        """Simülasyonu ekrana çiz"""
        self.ekran.fill((240, 240, 240))  # Açık gri arka plan
        
        # Böcekleri çiz
        for bocek in self.bocekler:
            if bocek.hayatta:
                renk = self.renkler[bocek.renk]
                pygame.draw.circle(
                    self.ekran, 
                    renk, 
                    (int(bocek.x), int(bocek.y)), 
                    int(bocek.boyut)
                )
        
        # Bilgi metni
        font = pygame.font.Font(None, 36)
        hayatta_sayi = len([b for b in self.bocekler if b.hayatta])
        
        metin_satiri = [
            f"Zaman: {self.zaman}",
            f"Nesil: {self.nesil}",
            f"Hayatta Böcek: {hayatta_sayi}",
            "",
            "Renk Dağılımı:"
        ]
        
        # Renk dağılımını göster
        hayatta_bocekler = [b for b in self.bocekler if b.hayatta]
        for renk in self.renkler.keys():
            sayi = len([b for b in hayatta_bocekler if b.renk == renk])
            metin_satiri.append(f"{renk.capitalize()}: {sayi}")
        
        y_offset = 10
        for satir in metin_satiri:
            metin = font.render(satir, True, (0, 0, 0))
            self.ekran.blit(metin, (10, y_offset))
            y_offset += 25
        
        pygame.display.flip()
    
    def simulasyonu_calistir(self, max_zaman=5000):
        """Ana simülasyon döngüsü"""
        self.baslangic_populasyonu_olustur(150)
        
        calisir = True
        while calisir and self.zaman < max_zaman:
            for olay in pygame.event.get():
                if olay.type == pygame.QUIT:
                    calisir = False
                elif olay.type == pygame.KEYDOWN:
                    if olay.key == pygame.K_r:  # R tuşu ile yeniden başlat
                        self.baslangic_populasyonu_olustur(150)
                        self.zaman = 0
                        self.nesil = 0
                        self.populasyon_gecmisi.clear()
                        self.renk_dagilimi_gecmisi.clear()
                    elif olay.key == pygame.K_g:  # G tuşu ile grafik göster
                        self.grafikleri_goster()
            
            # Simülasyon adımları
            for bocek in self.bocekler:
                bocek.hareket_et(self.genislik, self.yukseklik)
            
            self.dogal_secilim_uygula()
            
            # Her 100 zaman biriminde üreme
            if self.zaman % 100 == 0:
                self.ureme_gerceklestir()
                self.nesil += 1
            
            self.istatistikleri_guncelle()
            self.ciz()
            
            self.zaman += 1
            self.saat.tick(60)  # 60 FPS
            
            # Popülasyon çok azaldıysa yeniden başlat
            hayatta_sayi = len([b for b in self.bocekler if b.hayatta])
            if hayatta_sayi < 10:
                print(f"Popülasyon çok azaldı ({hayatta_sayi}), yeniden başlatılıyor...")
                self.baslangic_populasyonu_olustur(100)
                self.nesil += 1
        
        pygame.quit()
        
        # Simülasyon bittiğinde grafikleri göster
        if len(self.populasyon_gecmisi) > 0:
            self.grafikleri_goster()
    
    def grafikleri_goster(self):
        """Simülasyon sonuçlarının grafiklerini göster"""
        if len(self.populasyon_gecmisi) == 0:
            return
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
        
        # Toplam popülasyon grafiği
        ax1.plot(self.populasyon_gecmisi, linewidth=2, color='black')
        ax1.set_title('Zaman İçinde Toplam Böcek Popülasyonu', fontsize=14, fontweight='bold')
        ax1.set_xlabel('Zaman')
        ax1.set_ylabel('Böcek Sayısı')
        ax1.grid(True, alpha=0.3)
        
        # Renk dağılımı grafiği
        if len(self.renk_dagilimi_gecmisi) > 0:
            for renk in self.renkler.keys():
                renk_verileri = [veri.get(renk, 0) for veri in self.renk_dagilimi_gecmisi]
                ax2.plot(renk_verileri, label=renk.capitalize(), linewidth=2)
        
        ax2.set_title('Zaman İçinde Renk Dağılımı', fontsize=14, fontweight='bold')
        ax2.set_xlabel('Zaman')
        ax2.set_ylabel('Böcek Sayısı')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()

def main():
    """Ana fonksiyon"""
    print("=== BÖCEK POPÜLASYONU SİMÜLASYONU ===")
    print("Kontroller:")
    print("- R tuşu: Simülasyonu yeniden başlat")
    print("- G tuşu: Grafikleri göster")
    print("- Pencereyi kapatarak çıkış yapabilirsiniz")
    print("\nSimülasyon başlatılıyor...")
    
    simulasyon = BocekSimulasyonu()
    simulasyon.simulasyonu_calistir()

if __name__ == "__main__":
    main() 