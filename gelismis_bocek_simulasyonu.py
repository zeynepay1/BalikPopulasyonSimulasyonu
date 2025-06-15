import matplotlib.pyplot as plt
import numpy as np
import random
import pygame
import sys
import json
import math
from dataclasses import dataclass, asdict
from typing import List, Tuple, Dict
from enum import Enum
import time
from datetime import datetime

class BocekTuru(Enum):
    """Böcek türleri"""
    KELEBEK = "kelebek"
    KARINCA = "karinca"
    ARICIK = "aricik"
    BOCEK = "bocek"

class Davranis(Enum):
    """Böcek davranış türleri"""
    AGRESIF = "agresif"
    PASIF = "pasif"
    SOSYAL = "sosyal"
    YALNIZ = "yalniz"

@dataclass
class Cevre:
    """Çevre koşulları"""
    sicaklik: float = 25.0  # Celsius
    nem: float = 50.0       # %
    yiyecek_miktari: float = 100.0
    avcı_sayisi: int = 0
    mevsim: str = "ilkbahar"

@dataclass
class Bocek:
    """Gelişmiş böcek sınıfı"""
    x: float
    y: float
    renk: str
    boyut: float
    hiz: float
    enerji: float
    yas: int
    max_enerji: float
    zeka: float
    guc: float
    dayaniklilik: float
    tur: BocekTuru
    davranis: Davranis
    cinsiyet: str  # "erkek" veya "disi"
    hamile: bool = False
    hamilelik_suresi: int = 0
    hayatta: bool = True
    hastalık: bool = False
    mutasyon_sayisi: int = 0
    nesil: int = 0
    ebeveyn_id: str = ""
    id: str = ""
    
    def __post_init__(self):
        if not self.id:
            self.id = f"{self.tur.value}_{random.randint(1000, 9999)}"
    
    def hareket_et(self, genislik: int, yukseklik: int, cevre: Cevre, diger_bocekler: List['Bocek']):
        """Gelişmiş hareket sistemi"""
        if not self.hayatta:
            return
            
        # Çevre koşullarına göre hareket hızı
        hiz_carpani = 1.0
        if cevre.sicaklik < 10 or cevre.sicaklik > 40:
            hiz_carpani = 0.5  # Aşırı sıcaklıkta yavaşla
        elif 20 <= cevre.sicaklik <= 30:
            hiz_carpani = 1.2  # İdeal sıcaklıkta hızlan
            
        # Davranışa göre hareket
        if self.davranis == Davranis.SOSYAL:
            # Diğer böceklere yaklaş
            en_yakin = self._en_yakin_bocek_bul(diger_bocekler)
            if en_yakin and self._mesafe_hesapla(en_yakin) > 50:
                self._hedefe_hareket_et(en_yakin.x, en_yakin.y, hiz_carpani)
            else:
                self._rastgele_hareket_et(hiz_carpani)
        elif self.davranis == Davranis.AGRESIF:
            # Farklı renkteki böcekleri kovala
            hedef = self._dusman_bul(diger_bocekler)
            if hedef:
                self._hedefe_hareket_et(hedef.x, hedef.y, hiz_carpani * 1.5)
            else:
                self._rastgele_hareket_et(hiz_carpani)
        else:
            self._rastgele_hareket_et(hiz_carpani)
        
        # Sınırları kontrol et
        self.x = max(10, min(genislik - 10, self.x))
        self.y = max(10, min(yukseklik - 10, self.y))
        
        # Enerji tüketimi
        enerji_tuketimi = 0.05 + (self.boyut * 0.01) + (self.hiz * 0.02)
        if self.hamile:
            enerji_tuketimi *= 1.5
        if self.hastalık:
            enerji_tuketimi *= 2.0
            
        self.enerji -= enerji_tuketimi
        self.yas += 1
        
        # Hamilelik kontrolü
        if self.hamile:
            self.hamilelik_suresi += 1
            if self.hamilelik_suresi >= 200:  # 200 zaman birimi sonra doğum
                self.hamile = False
                self.hamilelik_suresi = 0
        
        # Yaşlanma ve ölüm kontrolü
        max_yas = 800 + (self.dayaniklilik * 100)
        if self.enerji <= 0 or self.yas > max_yas:
            self.hayatta = False
    
    def _rastgele_hareket_et(self, hiz_carpani: float):
        """Rastgele hareket"""
        hareket_hizi = self.hiz * hiz_carpani
        self.x += random.uniform(-hareket_hizi, hareket_hizi)
        self.y += random.uniform(-hareket_hizi, hareket_hizi)
    
    def _hedefe_hareket_et(self, hedef_x: float, hedef_y: float, hiz_carpani: float):
        """Hedefe doğru hareket"""
        dx = hedef_x - self.x
        dy = hedef_y - self.y
        mesafe = math.sqrt(dx*dx + dy*dy)
        
        if mesafe > 0:
            hareket_hizi = self.hiz * hiz_carpani
            self.x += (dx / mesafe) * hareket_hizi
            self.y += (dy / mesafe) * hareket_hizi
    
    def _en_yakin_bocek_bul(self, bocekler: List['Bocek']) -> 'Bocek':
        """En yakın böceği bul"""
        en_yakin = None
        en_kisa_mesafe = float('inf')
        
        for bocek in bocekler:
            if bocek.id != self.id and bocek.hayatta:
                mesafe = self._mesafe_hesapla(bocek)
                if mesafe < en_kisa_mesafe:
                    en_kisa_mesafe = mesafe
                    en_yakin = bocek
        
        return en_yakin
    
    def _dusman_bul(self, bocekler: List['Bocek']) -> 'Bocek':
        """Farklı renkteki böcek bul"""
        for bocek in bocekler:
            if (bocek.id != self.id and bocek.hayatta and 
                bocek.renk != self.renk and self._mesafe_hesapla(bocek) < 100):
                return bocek
        return None
    
    def _mesafe_hesapla(self, diger_bocek: 'Bocek') -> float:
        """İki böcek arasındaki mesafe"""
        dx = self.x - diger_bocek.x
        dy = self.y - diger_bocek.y
        return math.sqrt(dx*dx + dy*dy)
    
    def yiyecek_ye(self, yiyecek_miktari: float) -> float:
        """Yiyecek tüketimi"""
        if not self.hayatta:
            return 0
            
        ihtiyac = min(self.max_enerji - self.enerji, yiyecek_miktari * 0.1)
        self.enerji = min(self.max_enerji, self.enerji + ihtiyac)
        return ihtiyac

class YiyecekKaynagi:
    """Yiyecek kaynağı sınıfı"""
    def __init__(self, x: float, y: float, miktar: float = 100.0):
        self.x = x
        self.y = y
        self.miktar = miktar
        self.max_miktar = miktar
        self.yenilenme_hizi = 0.5
    
    def guncelle(self):
        """Yiyecek kaynağını güncelle"""
        if self.miktar < self.max_miktar:
            self.miktar = min(self.max_miktar, self.miktar + self.yenilenme_hizi)
    
    def tuket(self, miktar: float) -> float:
        """Yiyecek tüket"""
        tuketilen = min(self.miktar, miktar)
        self.miktar -= tuketilen
        return tuketilen

class Avci:
    """Avcı sınıfı"""
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        self.hiz = 2.0
        self.menzil = 80.0
        self.tokluk = 100.0
        self.hedef = None
    
    def hareket_et(self, genislik: int, yukseklik: int, bocekler: List[Bocek]):
        """Avcının hareketi"""
        if self.tokluk <= 0:
            return
            
        # Hedef bul
        if not self.hedef or not self.hedef.hayatta:
            self.hedef = self._en_yakin_bocek_bul(bocekler)
        
        if self.hedef:
            # Hedefe doğru hareket et
            dx = self.hedef.x - self.x
            dy = self.hedef.y - self.y
            mesafe = math.sqrt(dx*dx + dy*dy)
            
            if mesafe > 0:
                self.x += (dx / mesafe) * self.hiz
                self.y += (dy / mesafe) * self.hiz
            
            # Yakınsa yakala
            if mesafe < 15:
                self.hedef.hayatta = False
                self.tokluk += 50
                self.hedef = None
        else:
            # Rastgele hareket
            self.x += random.uniform(-self.hiz, self.hiz)
            self.y += random.uniform(-self.hiz, self.hiz)
        
        # Sınırları kontrol et
        self.x = max(0, min(genislik, self.x))
        self.y = max(0, min(yukseklik, self.y))
        
        # Tokluk azalt
        self.tokluk -= 0.5
    
    def _en_yakin_bocek_bul(self, bocekler: List[Bocek]) -> Bocek:
        """En yakın böceği bul"""
        en_yakin = None
        en_kisa_mesafe = float('inf')
        
        for bocek in bocekler:
            if bocek.hayatta:
                dx = self.x - bocek.x
                dy = self.y - bocek.y
                mesafe = math.sqrt(dx*dx + dy*dy)
                
                if mesafe < self.menzil and mesafe < en_kisa_mesafe:
                    en_kisa_mesafe = mesafe
                    en_yakin = bocek
        
        return en_yakin

class GelismisSimulasyon:
    """Gelişmiş simülasyon sınıfı"""
    
    def __init__(self, genislik=1200, yukseklik=800):
        self.genislik = genislik
        self.yukseklik = yukseklik
        self.bocekler: List[Bocek] = []
        self.yiyecek_kaynaklari: List[YiyecekKaynagi] = []
        self.avcilar: List[Avci] = []
        self.nesil = 0
        self.zaman = 0
        self.cevre = Cevre()
        
        # Renk tanımları
        self.renkler = {
            'kirmizi': (255, 0, 0),
            'mavi': (0, 0, 255),
            'yesil': (0, 255, 0),
            'sari': (255, 255, 0),
            'mor': (128, 0, 128),
            'turuncu': (255, 165, 0),
            'pembe': (255, 192, 203),
            'kahverengi': (139, 69, 19)
        }
        
        # İstatistik takibi
        self.populasyon_gecmisi = []
        self.renk_dagilimi_gecmisi = []
        self.cevre_gecmisi = []
        self.genetik_cesitlilik_gecmisi = []
        self.tur_dagilimi_gecmisi = []
        
        # Pygame başlatma
        pygame.init()
        self.ekran = pygame.display.set_mode((genislik, yukseklik))
        pygame.display.set_caption("Gelişmiş Böcek Ekosisteemi Simülasyonu")
        self.saat = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)
        self.buyuk_font = pygame.font.Font(None, 36)
        
        # Simülasyon ayarları
        self.duraklat = False
        self.hizli_mod = False
        self.gosterim_modu = "normal"  # normal, istatistik, genetik
        
    def baslangic_ekosistemi_olustur(self):
        """Başlangıç ekosistemini oluştur"""
        self.bocekler.clear()
        self.yiyecek_kaynaklari.clear()
        self.avcilar.clear()
        
        # Çeşitli böcekler oluştur
        renk_listesi = list(self.renkler.keys())
        tur_listesi = list(BocekTuru)
        davranis_listesi = list(Davranis)
        
        for i in range(200):
            bocek = Bocek(
                x=random.uniform(50, self.genislik - 50),
                y=random.uniform(50, self.yukseklik - 50),
                renk=random.choice(renk_listesi),
                boyut=random.uniform(4, 12),
                hiz=random.uniform(0.8, 2.5),
                enerji=random.uniform(60, 100),
                max_enerji=random.uniform(80, 120),
                yas=random.randint(0, 100),
                zeka=random.uniform(0.1, 1.0),
                guc=random.uniform(0.1, 1.0),
                dayaniklilik=random.uniform(0.1, 1.0),
                tur=random.choice(tur_listesi),
                davranis=random.choice(davranis_listesi),
                cinsiyet=random.choice(["erkek", "disi"]),
                nesil=0
            )
            self.bocekler.append(bocek)
        
        # Yiyecek kaynakları oluştur
        for _ in range(15):
            yiyecek = YiyecekKaynagi(
                x=random.uniform(0, self.genislik),
                y=random.uniform(0, self.yukseklik),
                miktar=random.uniform(50, 150)
            )
            self.yiyecek_kaynaklari.append(yiyecek)
        
        # Avcılar oluştur
        for _ in range(3):
            avci = Avci(
                x=random.uniform(0, self.genislik),
                y=random.uniform(0, self.yukseklik)
            )
            self.avcilar.append(avci)
    
    def cevre_guncelle(self):
        """Çevre koşullarını güncelle"""
        # Mevsimsel değişiklikler
        mevsim_dongusu = (self.zaman // 1000) % 4
        mevsimler = ["ilkbahar", "yaz", "sonbahar", "kis"]
        self.cevre.mevsim = mevsimler[mevsim_dongusu]
        
        # Sıcaklık değişimi
        if self.cevre.mevsim == "yaz":
            self.cevre.sicaklik = 25 + random.uniform(-5, 10)
        elif self.cevre.mevsim == "kis":
            self.cevre.sicaklik = 15 + random.uniform(-10, 5)
        else:
            self.cevre.sicaklik = 20 + random.uniform(-5, 5)
        
        # Nem değişimi
        self.cevre.nem = 50 + random.uniform(-20, 20)
        
        # Yiyecek miktarı mevsimsel
        if self.cevre.mevsim == "ilkbahar":
            self.cevre.yiyecek_miktari = min(150, self.cevre.yiyecek_miktari + 1)
        elif self.cevre.mevsim == "kis":
            self.cevre.yiyecek_miktari = max(20, self.cevre.yiyecek_miktari - 0.5)
        
        # Rastgele avcı ekleme/çıkarma
        if random.random() < 0.001:  # %0.1 şans
            if len(self.avcilar) < 8:
                yeni_avci = Avci(
                    x=random.uniform(0, self.genislik),
                    y=random.uniform(0, self.yukseklik)
                )
                self.avcilar.append(yeni_avci)
        
        # Avcıları temizle
        self.avcilar = [a for a in self.avcilar if a.tokluk > 0]
    
    def dogal_secilim_uygula(self):
        """Gelişmiş doğal seçilim"""
        for bocek in self.bocekler:
            if not bocek.hayatta:
                continue
                
            # Renk bazlı hayatta kalma (çevre koşullarına bağlı)
            renk_avantaji = self._renk_avantaji_hesapla(bocek.renk)
            
            # Tür bazlı avantajlar
            tur_avantaji = self._tur_avantaji_hesapla(bocek.tur)
            
            # Çevre koşulları etkisi
            cevre_etkisi = self._cevre_etkisi_hesapla(bocek)
            
            # Hastalık riski
            if random.random() < 0.002:  # %0.2 hastalık riski
                bocek.hastalık = True
            
            # Toplam ölüm riski
            olum_riski = 0.008 - (renk_avantaji * 0.002) - (tur_avantaji * 0.001) + cevre_etkisi
            if bocek.hastalık:
                olum_riski += 0.01
            
            # Yaşlılık etkisi
            if bocek.yas > 500:
                olum_riski += (bocek.yas - 500) * 0.00001
            
            if random.random() < olum_riski:
                bocek.hayatta = False
    
    def _renk_avantaji_hesapla(self, renk: str) -> float:
        """Renk bazlı avantaj hesapla"""
        avantajlar = {
            'kirmizi': 0.8,
            'mavi': 0.6,
            'yesil': 0.7,
            'sari': 0.4,
            'mor': 0.3,
            'turuncu': 0.5,
            'pembe': 0.2,
            'kahverengi': 0.9  # Kamuflaj avantajı
        }
        return avantajlar.get(renk, 0.5)
    
    def _tur_avantaji_hesapla(self, tur: BocekTuru) -> float:
        """Tür bazlı avantaj hesapla"""
        avantajlar = {
            BocekTuru.KELEBEK: 0.6,
            BocekTuru.KARINCA: 0.8,  # Sosyal avantaj
            BocekTuru.ARICIK: 0.7,
            BocekTuru.BOCEK: 0.5
        }
        return avantajlar.get(tur, 0.5)
    
    def _cevre_etkisi_hesapla(self, bocek: Bocek) -> float:
        """Çevre koşullarının etkisini hesapla"""
        etki = 0.0
        
        # Sıcaklık etkisi
        if self.cevre.sicaklik < 5 or self.cevre.sicaklik > 45:
            etki += 0.005
        
        # Yiyecek kıtlığı
        if self.cevre.yiyecek_miktari < 30:
            etki += 0.003
        
        # Dayanıklılık etkisi
        etki -= bocek.dayaniklilik * 0.002
        
        return etki
    
    def ureme_gerceklestir(self):
        """Gelişmiş üreme sistemi"""
        hayatta_bocekler = [b for b in self.bocekler if b.hayatta]
        
        if len(hayatta_bocekler) < 10:
            return
        
        # Üreme çiftleri oluştur
        erkekler = [b for b in hayatta_bocekler if b.cinsiyet == "erkek" and b.enerji > 40 and b.yas > 80]
        disiler = [b for b in hayatta_bocekler if b.cinsiyet == "disi" and b.enerji > 40 and b.yas > 80 and not b.hamile]
        
        yeni_bocekler = []
        for _ in range(min(len(erkekler), len(disiler), 30)):
            if not erkekler or not disiler:
                break
                
            erkek = random.choice(erkekler)
            disi = random.choice(disiler)
            
            # Uyumluluk kontrolü
            if self._ureme_uyumlulugu_kontrol(erkek, disi):
                # Hamilelik
                disi.hamile = True
                disi.hamilelik_suresi = 0
                
                # Yavru oluştur
                for _ in range(random.randint(1, 4)):  # 1-4 yavru
                    yavru = self._yavru_olustur(erkek, disi)
                    yeni_bocekler.append(yavru)
                
                # Ebeveyn enerji kaybı
                erkek.enerji -= 15
                disi.enerji -= 20
                
                # Listelerden çıkar
                if erkek in erkekler:
                    erkekler.remove(erkek)
                if disi in disiler:
                    disiler.remove(disi)
        
        self.bocekler.extend(yeni_bocekler)
    
    def _ureme_uyumlulugu_kontrol(self, erkek: Bocek, disi: Bocek) -> bool:
        """Üreme uyumluluğunu kontrol et"""
        # Aynı tür tercihi
        if erkek.tur == disi.tur:
            return random.random() < 0.8
        else:
            return random.random() < 0.3
    
    def _yavru_olustur(self, erkek: Bocek, disi: Bocek) -> Bocek:
        """Yavru böcek oluştur"""
        # Genetik karışım
        yavru_renk = random.choice([erkek.renk, disi.renk])
        yavru_tur = random.choice([erkek.tur, disi.tur])
        yavru_davranis = random.choice([erkek.davranis, disi.davranis])
        
        # Mutasyon kontrolü
        mutasyon_sayisi = 0
        if random.random() < 0.08:  # %8 mutasyon şansı
            yavru_renk = random.choice(list(self.renkler.keys()))
            mutasyon_sayisi += 1
        
        if random.random() < 0.05:  # %5 tür mutasyonu
            yavru_tur = random.choice(list(BocekTuru))
            mutasyon_sayisi += 1
        
        if random.random() < 0.06:  # %6 davranış mutasyonu
            yavru_davranis = random.choice(list(Davranis))
            mutasyon_sayisi += 1
        
        # Özellik kalıtımı (ebeveyn ortalama + varyasyon)
        yavru = Bocek(
            x=disi.x + random.uniform(-20, 20),
            y=disi.y + random.uniform(-20, 20),
            renk=yavru_renk,
            boyut=(erkek.boyut + disi.boyut) / 2 + random.uniform(-1, 1),
            hiz=(erkek.hiz + disi.hiz) / 2 + random.uniform(-0.3, 0.3),
            enerji=random.uniform(70, 100),
            max_enerji=(erkek.max_enerji + disi.max_enerji) / 2 + random.uniform(-10, 10),
            yas=0,
            zeka=(erkek.zeka + disi.zeka) / 2 + random.uniform(-0.1, 0.1),
            guc=(erkek.guc + disi.guc) / 2 + random.uniform(-0.1, 0.1),
            dayaniklilik=(erkek.dayaniklilik + disi.dayaniklilik) / 2 + random.uniform(-0.1, 0.1),
            tur=yavru_tur,
            davranis=yavru_davranis,
            cinsiyet=random.choice(["erkek", "disi"]),
            mutasyon_sayisi=mutasyon_sayisi,
            nesil=max(erkek.nesil, disi.nesil) + 1,
            ebeveyn_id=f"{erkek.id}+{disi.id}"
        )
        
        # Sınır kontrolü
        yavru.boyut = max(2, min(15, yavru.boyut))
        yavru.hiz = max(0.5, min(4, yavru.hiz))
        yavru.zeka = max(0.1, min(1.0, yavru.zeka))
        yavru.guc = max(0.1, min(1.0, yavru.guc))
        yavru.dayaniklilik = max(0.1, min(1.0, yavru.dayaniklilik))
        
        return yavru
    
    def yiyecek_sistemi_guncelle(self):
        """Yiyecek sistemini güncelle"""
        # Yiyecek kaynaklarını güncelle
        for kaynak in self.yiyecek_kaynaklari:
            kaynak.guncelle()
        
        # Böceklerin yiyecek tüketimi
        for bocek in self.bocekler:
            if not bocek.hayatta:
                continue
                
            # En yakın yiyecek kaynağını bul
            en_yakin_kaynak = None
            en_kisa_mesafe = float('inf')
            
            for kaynak in self.yiyecek_kaynaklari:
                if kaynak.miktar > 0:
                    dx = bocek.x - kaynak.x
                    dy = bocek.y - kaynak.y
                    mesafe = math.sqrt(dx*dx + dy*dy)
                    
                    if mesafe < en_kisa_mesafe:
                        en_kisa_mesafe = mesafe
                        en_yakin_kaynak = kaynak
            
            # Yiyecek ye
            if en_yakin_kaynak and en_kisa_mesafe < 30:
                tuketilen = en_yakin_kaynak.tuket(bocek.boyut * 2)
                bocek.enerji = min(bocek.max_enerji, bocek.enerji + tuketilen * 0.5)
    
    def istatistikleri_guncelle(self):
        """Gelişmiş istatistik takibi"""
        hayatta_bocekler = [b for b in self.bocekler if b.hayatta]
        toplam_sayi = len(hayatta_bocekler)
        
        # Renk dağılımı
        renk_sayilari = {}
        for renk in self.renkler.keys():
            renk_sayilari[renk] = len([b for b in hayatta_bocekler if b.renk == renk])
        
        # Tür dağılımı
        tur_sayilari = {}
        for tur in BocekTuru:
            tur_sayilari[tur.value] = len([b for b in hayatta_bocekler if b.tur == tur])
        
        # Genetik çeşitlilik
        if hayatta_bocekler:
            ortalama_zeka = sum(b.zeka for b in hayatta_bocekler) / len(hayatta_bocekler)
            ortalama_guc = sum(b.guc for b in hayatta_bocekler) / len(hayatta_bocekler)
            ortalama_dayaniklilik = sum(b.dayaniklilik for b in hayatta_bocekler) / len(hayatta_bocekler)
            toplam_mutasyon = sum(b.mutasyon_sayisi for b in hayatta_bocekler)
        else:
            ortalama_zeka = ortalama_guc = ortalama_dayaniklilik = toplam_mutasyon = 0
        
        # Kayıt
        self.populasyon_gecmisi.append(toplam_sayi)
        self.renk_dagilimi_gecmisi.append(renk_sayilari.copy())
        self.tur_dagilimi_gecmisi.append(tur_sayilari.copy())
        self.cevre_gecmisi.append({
            'sicaklik': self.cevre.sicaklik,
            'nem': self.cevre.nem,
            'yiyecek': self.cevre.yiyecek_miktari,
            'avci_sayisi': len(self.avcilar)
        })
        self.genetik_cesitlilik_gecmisi.append({
            'zeka': ortalama_zeka,
            'guc': ortalama_guc,
            'dayaniklilik': ortalama_dayaniklilik,
            'mutasyon': toplam_mutasyon
        })
    
    def ciz(self):
        """Gelişmiş çizim sistemi"""
        self.ekran.fill((240, 248, 255))  # Alice blue arka plan
        
        if self.gosterim_modu == "normal":
            self._normal_cizim()
        elif self.gosterim_modu == "istatistik":
            self._istatistik_cizim()
        elif self.gosterim_modu == "genetik":
            self._genetik_cizim()
        
        pygame.display.flip()
    
    def _normal_cizim(self):
        """Normal görünüm çizimi"""
        # Yiyecek kaynaklarını çiz
        for kaynak in self.yiyecek_kaynaklari:
            renk_yogunlugu = int(255 * (kaynak.miktar / kaynak.max_miktar))
            pygame.draw.circle(self.ekran, (0, renk_yogunlugu, 0), 
                             (int(kaynak.x), int(kaynak.y)), 8)
        
        # Avcıları çiz
        for avci in self.avcilar:
            pygame.draw.circle(self.ekran, (139, 0, 0), 
                             (int(avci.x), int(avci.y)), 12)
            # Menzil göster
            pygame.draw.circle(self.ekran, (139, 0, 0), 
                             (int(avci.x), int(avci.y)), int(avci.menzil), 1)
        
        # Böcekleri çiz
        for bocek in self.bocekler:
            if bocek.hayatta:
                renk = self.renkler[bocek.renk]
                
                # Böcek şekli (türe göre)
                if bocek.tur == BocekTuru.KELEBEK:
                    self._kelebek_ciz(bocek, renk)
                elif bocek.tur == BocekTuru.KARINCA:
                    self._karinca_ciz(bocek, renk)
                else:
                    pygame.draw.circle(self.ekran, renk, 
                                     (int(bocek.x), int(bocek.y)), int(bocek.boyut))
                
                # Enerji çubuğu
                if bocek.enerji < bocek.max_enerji * 0.3:  # Düşük enerji
                    enerji_rengi = (255, 0, 0)
                elif bocek.enerji < bocek.max_enerji * 0.6:
                    enerji_rengi = (255, 255, 0)
                else:
                    enerji_rengi = (0, 255, 0)
                
                enerji_orani = bocek.enerji / bocek.max_enerji
                pygame.draw.rect(self.ekran, enerji_rengi,
                               (bocek.x - 8, bocek.y - bocek.boyut - 8, 
                                16 * enerji_orani, 3))
                
                # Hamilelik göstergesi
                if bocek.hamile:
                    pygame.draw.circle(self.ekran, (255, 192, 203), 
                                     (int(bocek.x), int(bocek.y)), int(bocek.boyut + 2), 2)
        
        # Bilgi paneli
        self._bilgi_paneli_ciz()
    
    def _kelebek_ciz(self, bocek: Bocek, renk: Tuple[int, int, int]):
        """Kelebek şeklinde çiz"""
        x, y = int(bocek.x), int(bocek.y)
        boyut = int(bocek.boyut)
        
        # Kanatlar
        pygame.draw.ellipse(self.ekran, renk, (x-boyut, y-boyut//2, boyut, boyut))
        pygame.draw.ellipse(self.ekran, renk, (x, y-boyut//2, boyut, boyut))
        pygame.draw.ellipse(self.ekran, renk, (x-boyut, y, boyut//2, boyut//2))
        pygame.draw.ellipse(self.ekran, renk, (x+boyut//2, y, boyut//2, boyut//2))
        
        # Gövde
        pygame.draw.line(self.ekran, (0, 0, 0), (x, y-boyut), (x, y+boyut), 2)
    
    def _karinca_ciz(self, bocek: Bocek, renk: Tuple[int, int, int]):
        """Karınca şeklinde çiz"""
        x, y = int(bocek.x), int(bocek.y)
        boyut = int(bocek.boyut)
        
        # Gövde parçaları
        pygame.draw.circle(self.ekran, renk, (x, y-boyut//2), boyut//3)  # Kafa
        pygame.draw.circle(self.ekran, renk, (x, y), boyut//2)  # Göğüs
        pygame.draw.circle(self.ekran, renk, (x, y+boyut//2), boyut//3)  # Karın
    
    def _bilgi_paneli_ciz(self):
        """Bilgi panelini çiz"""
        hayatta_bocekler = [b for b in self.bocekler if b.hayatta]
        
        bilgiler = [
            f"Zaman: {self.zaman}",
            f"Nesil: {self.nesil}",
            f"Popülasyon: {len(hayatta_bocekler)}",
            f"Mevsim: {self.cevre.mevsim.capitalize()}",
            f"Sıcaklık: {self.cevre.sicaklik:.1f}°C",
            f"Nem: {self.cevre.nem:.1f}%",
            f"Avcı Sayısı: {len(self.avcilar)}",
            "",
            "Kontroller:",
            "SPACE: Duraklat/Devam",
            "F: Hızlı Mod",
            "1,2,3: Görünüm Modu",
            "R: Yeniden Başlat",
            "G: Grafikler",
            "S: Kaydet"
        ]
        
        if self.duraklat:
            bilgiler.insert(0, "*** DURAKLATILDI ***")
        
        if self.hizli_mod:
            bilgiler.insert(-6, "*** HIZLI MOD ***")
        
        y_offset = 10
        for bilgi in bilgiler:
            if bilgi.startswith("***"):
                metin = self.buyuk_font.render(bilgi, True, (255, 0, 0))
            else:
                metin = self.font.render(bilgi, True, (0, 0, 0))
            self.ekran.blit(metin, (10, y_offset))
            y_offset += 25
    
    def _istatistik_cizim(self):
        """İstatistik görünümü"""
        # Arka plan
        self.ekran.fill((240, 248, 255))
        
        # Renk dağılımı pasta grafiği çiz (basit)
        if self.renk_dagilimi_gecmisi:
            son_dagilim = self.renk_dagilimi_gecmisi[-1]
            toplam = sum(son_dagilim.values())
            
            if toplam > 0:
                merkez_x, merkez_y = 300, 200
                radius = 80
                baslangic_aci = 0
                
                for renk, sayi in son_dagilim.items():
                    if sayi > 0:
                        aci = (sayi / toplam) * 360
                        pygame.draw.arc(self.ekran, self.renkler[renk],
                                      (merkez_x-radius, merkez_y-radius, radius*2, radius*2),
                                      math.radians(baslangic_aci), 
                                      math.radians(baslangic_aci + aci), 10)
                        baslangic_aci += aci
        
        # İstatistik metinleri
        self._bilgi_paneli_ciz()
    
    def _genetik_cizim(self):
        """Genetik görünüm"""
        self.ekran.fill((240, 248, 255))
        
        # Böcekleri genetik özelliklerine göre renklendir
        for bocek in self.bocekler:
            if bocek.hayatta:
                # Zeka seviyesine göre renk
                zeka_rengi = int(255 * bocek.zeka)
                renk = (zeka_rengi, 0, 255 - zeka_rengi)
                
                pygame.draw.circle(self.ekran, renk, 
                                 (int(bocek.x), int(bocek.y)), int(bocek.boyut))
                
                # Mutasyon göstergesi
                if bocek.mutasyon_sayisi > 0:
                    pygame.draw.circle(self.ekran, (255, 255, 255), 
                                     (int(bocek.x), int(bocek.y)), int(bocek.boyut + 3), 2)
        
        self._bilgi_paneli_ciz()
    
    def simulasyonu_calistir(self):
        """Ana simülasyon döngüsü"""
        self.baslangic_ekosistemi_olustur()
        
        calisir = True
        while calisir:
            for olay in pygame.event.get():
                if olay.type == pygame.QUIT:
                    calisir = False
                elif olay.type == pygame.KEYDOWN:
                    if olay.key == pygame.K_SPACE:
                        self.duraklat = not self.duraklat
                    elif olay.key == pygame.K_f:
                        self.hizli_mod = not self.hizli_mod
                    elif olay.key == pygame.K_1:
                        self.gosterim_modu = "normal"
                    elif olay.key == pygame.K_2:
                        self.gosterim_modu = "istatistik"
                    elif olay.key == pygame.K_3:
                        self.gosterim_modu = "genetik"
                    elif olay.key == pygame.K_r:
                        self.yeniden_baslat()
                    elif olay.key == pygame.K_g:
                        self.grafikleri_goster()
                    elif olay.key == pygame.K_s:
                        self.veri_kaydet()
            
            if not self.duraklat:
                # Simülasyon adımları
                self.cevre_guncelle()
                
                # Böcek hareketleri
                for bocek in self.bocekler:
                    bocek.hareket_et(self.genislik, self.yukseklik, self.cevre, self.bocekler)
                
                # Avcı hareketleri
                for avci in self.avcilar:
                    avci.hareket_et(self.genislik, self.yukseklik, self.bocekler)
                
                self.yiyecek_sistemi_guncelle()
                self.dogal_secilim_uygula()
                
                # Üreme (her 150 zaman biriminde)
                if self.zaman % 150 == 0:
                    self.ureme_gerceklestir()
                    self.nesil += 1
                
                self.istatistikleri_guncelle()
                self.zaman += 1
                
                # Popülasyon kontrolü
                hayatta_sayi = len([b for b in self.bocekler if b.hayatta])
                if hayatta_sayi < 20:
                    print(f"Popülasyon kritik seviyede ({hayatta_sayi}), yeni bireyler ekleniyor...")
                    self._acil_populasyon_ekleme()
            
            self.ciz()
            
            if self.hizli_mod:
                self.saat.tick(120)  # Hızlı mod
            else:
                self.saat.tick(60)   # Normal hız
        
        pygame.quit()
        self.grafikleri_goster()
    
    def _acil_populasyon_ekleme(self):
        """Acil durum popülasyon ekleme"""
        hayatta_bocekler = [b for b in self.bocekler if b.hayatta]
        
        if len(hayatta_bocekler) > 0:
            # Mevcut böceklerden örnekleyerek yenilerini oluştur
            for _ in range(50):
                ornek = random.choice(hayatta_bocekler)
                yeni_bocek = Bocek(
                    x=random.uniform(50, self.genislik - 50),
                    y=random.uniform(50, self.yukseklik - 50),
                    renk=ornek.renk,
                    boyut=ornek.boyut + random.uniform(-1, 1),
                    hiz=ornek.hiz + random.uniform(-0.2, 0.2),
                    enerji=random.uniform(70, 100),
                    max_enerji=ornek.max_enerji,
                    yas=0,
                    zeka=ornek.zeka + random.uniform(-0.1, 0.1),
                    guc=ornek.guc + random.uniform(-0.1, 0.1),
                    dayaniklilik=ornek.dayaniklilik + random.uniform(-0.1, 0.1),
                    tur=ornek.tur,
                    davranis=ornek.davranis,
                    cinsiyet=random.choice(["erkek", "disi"]),
                    nesil=ornek.nesil + 1
                )
                self.bocekler.append(yeni_bocek)
        else:
            # Tamamen yeni popülasyon
            self.baslangic_ekosistemi_olustur()
    
    def yeniden_baslat(self):
        """Simülasyonu yeniden başlat"""
        self.zaman = 0
        self.nesil = 0
        self.populasyon_gecmisi.clear()
        self.renk_dagilimi_gecmisi.clear()
        self.cevre_gecmisi.clear()
        self.genetik_cesitlilik_gecmisi.clear()
        self.tur_dagilimi_gecmisi.clear()
        self.baslangic_ekosistemi_olustur()
    
    def veri_kaydet(self):
        """Simülasyon verilerini kaydet"""
        zaman_damgasi = datetime.now().strftime("%Y%m%d_%H%M%S")
        dosya_adi = f"simulasyon_verileri_{zaman_damgasi}.json"
        
        veri = {
            'zaman': self.zaman,
            'nesil': self.nesil,
            'populasyon_gecmisi': self.populasyon_gecmisi,
            'renk_dagilimi_gecmisi': self.renk_dagilimi_gecmisi,
            'cevre_gecmisi': self.cevre_gecmisi,
            'genetik_cesitlilik_gecmisi': self.genetik_cesitlilik_gecmisi,
            'tur_dagilimi_gecmisi': self.tur_dagilimi_gecmisi,
            'bocek_sayisi': len([b for b in self.bocekler if b.hayatta])
        }
        
        try:
            with open(dosya_adi, 'w', encoding='utf-8') as f:
                json.dump(veri, f, indent=2, ensure_ascii=False)
            print(f"Veriler {dosya_adi} dosyasına kaydedildi.")
        except Exception as e:
            print(f"Veri kaydetme hatası: {e}")
    
    def grafikleri_goster(self):
        """Kapsamlı grafikler"""
        if len(self.populasyon_gecmisi) == 0:
            return
        
        fig = plt.figure(figsize=(16, 12))
        
        # 1. Toplam popülasyon
        ax1 = plt.subplot(3, 2, 1)
        plt.plot(self.populasyon_gecmisi, linewidth=2, color='black')
        plt.title('Toplam Popülasyon Değişimi', fontweight='bold')
        plt.xlabel('Zaman')
        plt.ylabel('Böcek Sayısı')
        plt.grid(True, alpha=0.3)
        
        # 2. Renk dağılımı
        ax2 = plt.subplot(3, 2, 2)
        if self.renk_dagilimi_gecmisi:
            for renk in self.renkler.keys():
                renk_verileri = [veri.get(renk, 0) for veri in self.renk_dagilimi_gecmisi]
                if max(renk_verileri) > 0:
                    plt.plot(renk_verileri, label=renk.capitalize(), linewidth=2)
        plt.title('Renk Dağılımı', fontweight='bold')
        plt.xlabel('Zaman')
        plt.ylabel('Böcek Sayısı')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # 3. Çevre koşulları
        ax3 = plt.subplot(3, 2, 3)
        if self.cevre_gecmisi:
            sicakliklar = [veri['sicaklik'] for veri in self.cevre_gecmisi]
            plt.plot(sicakliklar, label='Sıcaklık', color='red')
            plt.title('Çevre Koşulları', fontweight='bold')
            plt.xlabel('Zaman')
            plt.ylabel('Sıcaklık (°C)')
            plt.legend()
            plt.grid(True, alpha=0.3)
        
        # 4. Genetik çeşitlilik
        ax4 = plt.subplot(3, 2, 4)
        if self.genetik_cesitlilik_gecmisi:
            zeka_verileri = [veri['zeka'] for veri in self.genetik_cesitlilik_gecmisi]
            guc_verileri = [veri['guc'] for veri in self.genetik_cesitlilik_gecmisi]
            dayaniklilik_verileri = [veri['dayaniklilik'] for veri in self.genetik_cesitlilik_gecmisi]
            
            plt.plot(zeka_verileri, label='Ortalama Zeka', linewidth=2)
            plt.plot(guc_verileri, label='Ortalama Güç', linewidth=2)
            plt.plot(dayaniklilik_verileri, label='Ortalama Dayanıklılık', linewidth=2)
            
        plt.title('Genetik Özellikler', fontweight='bold')
        plt.xlabel('Zaman')
        plt.ylabel('Değer')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # 5. Tür dağılımı
        ax5 = plt.subplot(3, 2, 5)
        if self.tur_dagilimi_gecmisi:
            for tur in BocekTuru:
                tur_verileri = [veri.get(tur.value, 0) for veri in self.tur_dagilimi_gecmisi]
                if max(tur_verileri) > 0:
                    plt.plot(tur_verileri, label=tur.value.capitalize(), linewidth=2)
        plt.title('Tür Dağılımı', fontweight='bold')
        plt.xlabel('Zaman')
        plt.ylabel('Böcek Sayısı')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # 6. Avcı etkisi
        ax6 = plt.subplot(3, 2, 6)
        if self.cevre_gecmisi:
            avci_sayilari = [veri['avci_sayisi'] for veri in self.cevre_gecmisi]
            plt.plot(avci_sayilari, label='Avcı Sayısı', color='darkred', linewidth=2)
            plt.plot(self.populasyon_gecmisi, label='Popülasyon', color='blue', alpha=0.7)
        plt.title('Avcı-Av İlişkisi', fontweight='bold')
        plt.xlabel('Zaman')
        plt.ylabel('Sayı')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()

def main():
    """Ana fonksiyon"""
    print("=== GELİŞMİŞ BÖCEK EKOSİSTEMİ SİMÜLASYONU ===")
    print("\nKontroller:")
    print("SPACE: Duraklat/Devam")
    print("F: Hızlı Mod Aç/Kapat")
    print("1: Normal Görünüm")
    print("2: İstatistik Görünümü")
    print("3: Genetik Görünüm")
    print("R: Yeniden Başlat")
    print("G: Grafikleri Göster")
    print("S: Verileri Kaydet")
    print("\nÖzellikler:")
    print("- 8 farklı renk, 4 farklı tür")
    print("- Çevre koşulları (sıcaklık, nem, mevsim)")
    print("- Yiyecek kaynakları ve avcılar")
    print("- Genetik kalıtım ve mutasyonlar")
    print("- Davranış türleri (agresif, sosyal, vb.)")
    print("- Hastalık sistemi")
    print("- Kapsamlı istatistikler")
    print("\nSimülasyon başlatılıyor...")
    
    simulasyon = GelismisSimulasyon()
    simulasyon.simulasyonu_calistir()

if __name__ == "__main__":
    main() 