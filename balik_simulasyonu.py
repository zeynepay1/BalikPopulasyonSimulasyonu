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

class BalikTuru(Enum):
    """Balık türleri"""
    JAPON_BALIGI = "japon_baligi"
    KOI = "koi"
    GUPPY = "guppy"
    NEON = "neon"

class Davranis(Enum):
    """Balık davranış türleri"""
    AGRESIF = "agresif"
    PASIF = "pasif"
    SOSYAL = "sosyal"
    YALNIZ = "yalniz"

@dataclass
class SuOrtami:
    """Su ortamı koşulları"""
    sicaklik: float = 25.0  # Celsius
    ph: float = 7.0         # pH seviyesi
    oksijen: float = 100.0  # Oksijen miktarı
    yiyecek_miktari: float = 100.0
    avcı_sayisi: int = 0
    mevsim: str = "ilkbahar"

@dataclass
class Balik:
    """Gelişmiş balık sınıfı"""
    x: float
    y: float
    renk: str  # "kirmizi" veya "beyaz"
    boyut: float
    hiz: float
    enerji: float
    yas: int
    max_enerji: float
    zeka: float
    guc: float
    dayaniklilik: float
    tur: BalikTuru
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
    
    def hareket_et(self, genislik: int, yukseklik: int, su_ortami: SuOrtami, diger_baliklar: List['Balik']):
        """Gelişmiş hareket sistemi"""
        if not self.hayatta:
            return
            
        # Su sıcaklığına göre hareket hızı
        hiz_carpani = 1.0
        if su_ortami.sicaklik < 15 or su_ortami.sicaklik > 35:
            hiz_carpani = 0.4  # Aşırı sıcaklıkta yavaşla
        elif 20 <= su_ortami.sicaklik <= 28:
            hiz_carpani = 1.3  # İdeal sıcaklıkta hızlan
            
        # pH etkisi
        if su_ortami.ph < 6.0 or su_ortami.ph > 8.5:
            hiz_carpani *= 0.7  # Kötü pH'ta yavaşla
            
        # Davranışa göre hareket
        if self.davranis == Davranis.SOSYAL:
            # Diğer balıklara yaklaş (sürü halinde yüzme)
            en_yakin = self._en_yakin_balik_bul(diger_baliklar)
            if en_yakin and self._mesafe_hesapla(en_yakin) > 40:
                self._hedefe_hareket_et(en_yakin.x, en_yakin.y, hiz_carpani)
            else:
                self._rastgele_hareket_et(hiz_carpani)
        elif self.davranis == Davranis.AGRESIF:
            # Farklı renkteki balıkları kovala
            hedef = self._rakip_bul(diger_baliklar)
            if hedef:
                self._hedefe_hareket_et(hedef.x, hedef.y, hiz_carpani * 1.4)
            else:
                self._rastgele_hareket_et(hiz_carpani)
        else:
            self._rastgele_hareket_et(hiz_carpani)
        
        # Sınırları kontrol et (akvaryum duvarları)
        self.x = max(15, min(genislik - 15, self.x))
        self.y = max(15, min(yukseklik - 15, self.y))
        
        # Enerji tüketimi
        enerji_tuketimi = 0.04 + (self.boyut * 0.008) + (self.hiz * 0.015)
        if self.hamile:
            enerji_tuketimi *= 1.4
        if self.hastalık:
            enerji_tuketimi *= 2.2
            
        self.enerji -= enerji_tuketimi
        self.yas += 1
        
        # Hamilelik kontrolü
        if self.hamile:
            self.hamilelik_suresi += 1
            if self.hamilelik_suresi >= 180:  # 180 zaman birimi sonra doğum
                self.hamile = False
                self.hamilelik_suresi = 0
        
        # Yaşlanma ve ölüm kontrolü
        max_yas = 900 + (self.dayaniklilik * 120)
        if self.enerji <= 0 or self.yas > max_yas:
            self.hayatta = False
    
    def _rastgele_hareket_et(self, hiz_carpani: float):
        """Rastgele yüzme hareketi"""
        hareket_hizi = self.hiz * hiz_carpani
        # Balıklar daha akıcı hareket eder
        self.x += random.uniform(-hareket_hizi, hareket_hizi) * 0.8
        self.y += random.uniform(-hareket_hizi, hareket_hizi) * 0.8
    
    def _hedefe_hareket_et(self, hedef_x: float, hedef_y: float, hiz_carpani: float):
        """Hedefe doğru yüzme"""
        dx = hedef_x - self.x
        dy = hedef_y - self.y
        mesafe = math.sqrt(dx*dx + dy*dy)
        
        if mesafe > 0:
            hareket_hizi = self.hiz * hiz_carpani
            self.x += (dx / mesafe) * hareket_hizi * 0.9
            self.y += (dy / mesafe) * hareket_hizi * 0.9
    
    def _en_yakin_balik_bul(self, baliklar: List['Balik']) -> 'Balik':
        """En yakın balığı bul"""
        en_yakin = None
        en_kisa_mesafe = float('inf')
        
        for balik in baliklar:
            if balik.id != self.id and balik.hayatta:
                mesafe = self._mesafe_hesapla(balik)
                if mesafe < en_kisa_mesafe:
                    en_kisa_mesafe = mesafe
                    en_yakin = balik
        
        return en_yakin
    
    def _rakip_bul(self, baliklar: List['Balik']) -> 'Balik':
        """Farklı renkteki balık bul"""
        for balik in baliklar:
            if (balik.id != self.id and balik.hayatta and 
                balik.renk != self.renk and self._mesafe_hesapla(balik) < 80):
                return balik
        return None
    
    def _mesafe_hesapla(self, diger_balik: 'Balik') -> float:
        """İki balık arasındaki mesafe"""
        dx = self.x - diger_balik.x
        dy = self.y - diger_balik.y
        return math.sqrt(dx*dx + dy*dy)
    
    def yiyecek_ye(self, yiyecek_miktari: float) -> float:
        """Yiyecek tüketimi"""
        if not self.hayatta:
            return 0
            
        ihtiyac = min(self.max_enerji - self.enerji, yiyecek_miktari * 0.12)
        self.enerji = min(self.max_enerji, self.enerji + ihtiyac)
        return ihtiyac

class YiyecekKaynagi:
    """Balık yemi kaynağı"""
    def __init__(self, x: float, y: float, miktar: float = 120.0):
        self.x = x
        self.y = y
        self.miktar = miktar
        self.max_miktar = miktar
        self.yenilenme_hizi = 0.6
    
    def guncelle(self):
        """Yiyecek kaynağını güncelle"""
        if self.miktar < self.max_miktar:
            self.miktar = min(self.max_miktar, self.miktar + self.yenilenme_hizi)
    
    def tuket(self, miktar: float) -> float:
        """Yiyecek tüket"""
        tuketilen = min(self.miktar, miktar)
        self.miktar -= tuketilen
        return tuketilen

class Avcı:
    """Avcı balık (büyük balık)"""
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        self.hiz = 1.8
        self.menzil = 90.0
        self.tokluk = 120.0
        self.hedef = None
    
    def hareket_et(self, genislik: int, yukseklik: int, baliklar: List[Balik]):
        """Avcının hareketi"""
        if self.tokluk <= 0:
            return
            
        # Hedef bul
        if not self.hedef or not self.hedef.hayatta:
            self.hedef = self._en_yakin_balik_bul(baliklar)
        
        if self.hedef:
            # Hedefe doğru hareket et
            dx = self.hedef.x - self.x
            dy = self.hedef.y - self.y
            mesafe = math.sqrt(dx*dx + dy*dy)
            
            if mesafe > 0:
                self.x += (dx / mesafe) * self.hiz
                self.y += (dy / mesafe) * self.hiz
            
            # Yakınsa yakala
            if mesafe < 18:
                self.hedef.hayatta = False
                self.tokluk += 60
                self.hedef = None
        else:
            # Rastgele hareket
            self.x += random.uniform(-self.hiz, self.hiz)
            self.y += random.uniform(-self.hiz, self.hiz)
        
        # Sınırları kontrol et
        self.x = max(0, min(genislik, self.x))
        self.y = max(0, min(yukseklik, self.y))
        
        # Tokluk azalt
        self.tokluk -= 0.4
    
    def _en_yakin_balik_bul(self, baliklar: List[Balik]) -> Balik:
        """En yakın balığı bul"""
        en_yakin = None
        en_kisa_mesafe = float('inf')
        
        for balik in baliklar:
            if balik.hayatta:
                dx = self.x - balik.x
                dy = self.y - balik.y
                mesafe = math.sqrt(dx*dx + dy*dy)
                
                if mesafe < self.menzil and mesafe < en_kisa_mesafe:
                    en_kisa_mesafe = mesafe
                    en_yakin = balik
        
        return en_yakin

class BalikSimulasyonu:
    """Gelişmiş balık simülasyonu sınıfı"""
    
    def __init__(self, genislik=1200, yukseklik=800):
        self.genislik = genislik
        self.yukseklik = yukseklik
        self.baliklar: List[Balik] = []
        self.yiyecek_kaynaklari: List[YiyecekKaynagi] = []
        self.avcilar: List[Avcı] = []
        self.nesil = 0
        self.zaman = 0
        self.su_ortami = SuOrtami()
        
        # Sadece kırmızı ve beyaz renkler
        self.renkler = {
            'kirmizi': (255, 50, 50),    # Parlak kırmızı
            'beyaz': (255, 255, 255)     # Beyaz
        }
        
        # İstatistik takibi
        self.populasyon_gecmisi = []
        self.renk_dagilimi_gecmisi = []
        self.su_ortami_gecmisi = []
        self.genetik_cesitlilik_gecmisi = []
        self.tur_dagilimi_gecmisi = []
        
        # Pygame başlatma
        pygame.init()
        self.ekran = pygame.display.set_mode((genislik, yukseklik))
        pygame.display.set_caption("🐠 Gelişmiş Balık Akvaryumu Simülasyonu 🐠")
        self.saat = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)
        self.buyuk_font = pygame.font.Font(None, 36)
        
        # Simülasyon ayarları
        self.duraklat = False
        self.hizli_mod = False
        self.gosterim_modu = "normal"  # normal, istatistik, genetik
        
    def baslangic_akvaryumu_olustur(self):
        """Başlangıç akvaryumunu oluştur"""
        self.baliklar.clear()
        self.yiyecek_kaynaklari.clear()
        self.avcilar.clear()
        
        # Çeşitli balıklar oluştur
        renk_listesi = list(self.renkler.keys())
        tur_listesi = list(BalikTuru)
        davranis_listesi = list(Davranis)
        
        for i in range(180):  # Daha fazla balık
            balik = Balik(
                x=random.uniform(80, self.genislik - 80),
                y=random.uniform(80, self.yukseklik - 80),
                renk=random.choice(renk_listesi),
                boyut=random.uniform(5, 15),
                hiz=random.uniform(1.0, 3.0),
                enerji=random.uniform(70, 110),
                max_enerji=random.uniform(90, 130),
                yas=random.randint(0, 120),
                zeka=random.uniform(0.2, 1.0),
                guc=random.uniform(0.2, 1.0),
                dayaniklilik=random.uniform(0.2, 1.0),
                tur=random.choice(tur_listesi),
                davranis=random.choice(davranis_listesi),
                cinsiyet=random.choice(["erkek", "disi"]),
                nesil=0
            )
            self.baliklar.append(balik)
        
        # Yiyecek kaynakları oluştur
        for _ in range(12):
            yiyecek = YiyecekKaynagi(
                x=random.uniform(50, self.genislik - 50),
                y=random.uniform(50, self.yukseklik - 50),
                miktar=random.uniform(80, 180)
            )
            self.yiyecek_kaynaklari.append(yiyecek)
        
        # Avcılar oluştur
        for _ in range(2):
            avci = Avcı(
                x=random.uniform(50, self.genislik - 50),
                y=random.uniform(50, self.yukseklik - 50)
            )
            self.avcilar.append(avci)
    
    def su_ortami_guncelle(self):
        """Su ortamı koşullarını güncelle"""
        # Mevsimsel değişiklikler
        mevsim_dongusu = (self.zaman // 1200) % 4
        mevsimler = ["ilkbahar", "yaz", "sonbahar", "kis"]
        self.su_ortami.mevsim = mevsimler[mevsim_dongusu]
        
        # Sıcaklık değişimi
        if self.su_ortami.mevsim == "yaz":
            self.su_ortami.sicaklik = 26 + random.uniform(-3, 6)
        elif self.su_ortami.mevsim == "kis":
            self.su_ortami.sicaklik = 20 + random.uniform(-5, 3)
        else:
            self.su_ortami.sicaklik = 23 + random.uniform(-3, 3)
        
        # pH değişimi
        self.su_ortami.ph = 7.0 + random.uniform(-0.8, 0.8)
        
        # Oksijen seviyesi
        self.su_ortami.oksijen = 100 + random.uniform(-15, 10)
        
        # Yiyecek miktarı mevsimsel
        if self.su_ortami.mevsim == "ilkbahar":
            self.su_ortami.yiyecek_miktari = min(180, self.su_ortami.yiyecek_miktari + 1.2)
        elif self.su_ortami.mevsim == "kis":
            self.su_ortami.yiyecek_miktari = max(30, self.su_ortami.yiyecek_miktari - 0.6)
        
        # Rastgele avcı ekleme/çıkarma
        if random.random() < 0.0008:  # %0.08 şans
            if len(self.avcilar) < 6:
                yeni_avci = Avcı(
                    x=random.uniform(50, self.genislik - 50),
                    y=random.uniform(50, self.yukseklik - 50)
                )
                self.avcilar.append(yeni_avci)
        
        # Avcıları temizle
        self.avcilar = [a for a in self.avcilar if a.tokluk > 0]
    
    def dogal_secilim_uygula(self):
        """Gelişmiş doğal seçilim"""
        for balik in self.baliklar:
            if not balik.hayatta:
                continue
                
            # Renk bazlı hayatta kalma
            renk_avantaji = self._renk_avantaji_hesapla(balik.renk)
            
            # Tür bazlı avantajlar
            tur_avantaji = self._tur_avantaji_hesapla(balik.tur)
            
            # Su ortamı etkisi
            ortam_etkisi = self._ortam_etkisi_hesapla(balik)
            
            # Hastalık riski
            if random.random() < 0.0015:  # %0.15 hastalık riski
                balik.hastalık = True
            
            # Toplam ölüm riski
            olum_riski = 0.006 - (renk_avantaji * 0.0015) - (tur_avantaji * 0.0008) + ortam_etkisi
            if balik.hastalık:
                olum_riski += 0.008
            
            # Yaşlılık etkisi
            if balik.yas > 600:
                olum_riski += (balik.yas - 600) * 0.000008
            
            if random.random() < olum_riski:
                balik.hayatta = False
    
    def _renk_avantaji_hesapla(self, renk: str) -> float:
        """Renk bazlı avantaj hesapla"""
        avantajlar = {
            'kirmizi': 0.7,  # Kırmızı balıklar daha güçlü
            'beyaz': 0.9     # Beyaz balıklar daha dayanıklı
        }
        return avantajlar.get(renk, 0.5)
    
    def _tur_avantaji_hesapla(self, tur: BalikTuru) -> float:
        """Tür bazlı avantaj hesapla"""
        avantajlar = {
            BalikTuru.KOI: 0.8,          # En dayanıklı
            BalikTuru.JAPON_BALIGI: 0.7,
            BalikTuru.GUPPY: 0.6,
            BalikTuru.NEON: 0.5
        }
        return avantajlar.get(tur, 0.5)
    
    def _ortam_etkisi_hesapla(self, balik: Balik) -> float:
        """Su ortamı etkisini hesapla"""
        etki = 0.0
        
        # Sıcaklık etkisi
        if self.su_ortami.sicaklik < 15 or self.su_ortami.sicaklik > 35:
            etki += 0.004
        
        # pH etkisi
        if self.su_ortami.ph < 6.0 or self.su_ortami.ph > 8.5:
            etki += 0.003
        
        # Oksijen etkisi
        if self.su_ortami.oksijen < 70:
            etki += 0.005
        
        # Dayanıklılık etkisi
        etki -= balik.dayaniklilik * 0.0015
        
        return etki
    
    def ureme_gerceklestir(self):
        """Gelişmiş üreme sistemi"""
        hayatta_baliklar = [b for b in self.baliklar if b.hayatta]
        
        if len(hayatta_baliklar) < 15:
            return
        
        # Üreme çiftleri oluştur
        erkekler = [b for b in hayatta_baliklar if b.cinsiyet == "erkek" and b.enerji > 50 and b.yas > 100]
        disiler = [b for b in hayatta_baliklar if b.cinsiyet == "disi" and b.enerji > 50 and b.yas > 100 and not b.hamile]
        
        yeni_baliklar = []
        for _ in range(min(len(erkekler), len(disiler), 25)):
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
                for _ in range(random.randint(2, 6)):  # 2-6 yavru
                    yavru = self._yavru_olustur(erkek, disi)
                    yeni_baliklar.append(yavru)
                
                # Ebeveyn enerji kaybı
                erkek.enerji -= 12
                disi.enerji -= 18
                
                # Listelerden çıkar
                if erkek in erkekler:
                    erkekler.remove(erkek)
                if disi in disiler:
                    disiler.remove(disi)
        
        self.baliklar.extend(yeni_baliklar)
    
    def _ureme_uyumlulugu_kontrol(self, erkek: Balik, disi: Balik) -> bool:
        """Üreme uyumluluğunu kontrol et"""
        # Aynı tür tercihi
        if erkek.tur == disi.tur:
            return random.random() < 0.85
        else:
            return random.random() < 0.25
    
    def _yavru_olustur(self, erkek: Balik, disi: Balik) -> Balik:
        """Yavru balık oluştur"""
        # Genetik karışım
        yavru_renk = random.choice([erkek.renk, disi.renk])
        yavru_tur = random.choice([erkek.tur, disi.tur])
        yavru_davranis = random.choice([erkek.davranis, disi.davranis])
        
        # Mutasyon kontrolü
        mutasyon_sayisi = 0
        if random.random() < 0.06:  # %6 renk mutasyon şansı
            yavru_renk = random.choice(list(self.renkler.keys()))
            mutasyon_sayisi += 1
        
        if random.random() < 0.04:  # %4 tür mutasyonu
            yavru_tur = random.choice(list(BalikTuru))
            mutasyon_sayisi += 1
        
        if random.random() < 0.05:  # %5 davranış mutasyonu
            yavru_davranis = random.choice(list(Davranis))
            mutasyon_sayisi += 1
        
        # Özellik kalıtımı
        yavru = Balik(
            x=disi.x + random.uniform(-25, 25),
            y=disi.y + random.uniform(-25, 25),
            renk=yavru_renk,
            boyut=(erkek.boyut + disi.boyut) / 2 + random.uniform(-1.5, 1.5),
            hiz=(erkek.hiz + disi.hiz) / 2 + random.uniform(-0.4, 0.4),
            enerji=random.uniform(80, 110),
            max_enerji=(erkek.max_enerji + disi.max_enerji) / 2 + random.uniform(-12, 12),
            yas=0,
            zeka=(erkek.zeka + disi.zeka) / 2 + random.uniform(-0.12, 0.12),
            guc=(erkek.guc + disi.guc) / 2 + random.uniform(-0.12, 0.12),
            dayaniklilik=(erkek.dayaniklilik + disi.dayaniklilik) / 2 + random.uniform(-0.12, 0.12),
            tur=yavru_tur,
            davranis=yavru_davranis,
            cinsiyet=random.choice(["erkek", "disi"]),
            mutasyon_sayisi=mutasyon_sayisi,
            nesil=max(erkek.nesil, disi.nesil) + 1,
            ebeveyn_id=f"{erkek.id}+{disi.id}"
        )
        
        # Sınır kontrolü
        yavru.boyut = max(3, min(20, yavru.boyut))
        yavru.hiz = max(0.8, min(5, yavru.hiz))
        yavru.zeka = max(0.1, min(1.0, yavru.zeka))
        yavru.guc = max(0.1, min(1.0, yavru.guc))
        yavru.dayaniklilik = max(0.1, min(1.0, yavru.dayaniklilik))
        
        return yavru
    
    def yiyecek_sistemi_guncelle(self):
        """Yiyecek sistemini güncelle"""
        # Yiyecek kaynaklarını güncelle
        for kaynak in self.yiyecek_kaynaklari:
            kaynak.guncelle()
        
        # Balıkların yiyecek tüketimi
        for balik in self.baliklar:
            if not balik.hayatta:
                continue
                
            # En yakın yiyecek kaynağını bul
            en_yakin_kaynak = None
            en_kisa_mesafe = float('inf')
            
            for kaynak in self.yiyecek_kaynaklari:
                if kaynak.miktar > 0:
                    dx = balik.x - kaynak.x
                    dy = balik.y - kaynak.y
                    mesafe = math.sqrt(dx*dx + dy*dy)
                    
                    if mesafe < en_kisa_mesafe:
                        en_kisa_mesafe = mesafe
                        en_yakin_kaynak = kaynak
            
            # Yiyecek ye
            if en_yakin_kaynak and en_kisa_mesafe < 35:
                tuketilen = en_yakin_kaynak.tuket(balik.boyut * 2.5)
                balik.enerji = min(balik.max_enerji, balik.enerji + tuketilen * 0.6)
    
    def istatistikleri_guncelle(self):
        """Gelişmiş istatistik takibi"""
        hayatta_baliklar = [b for b in self.baliklar if b.hayatta]
        toplam_sayi = len(hayatta_baliklar)
        
        # Renk dağılımı
        renk_sayilari = {}
        for renk in self.renkler.keys():
            renk_sayilari[renk] = len([b for b in hayatta_baliklar if b.renk == renk])
        
        # Tür dağılımı
        tur_sayilari = {}
        for tur in BalikTuru:
            tur_sayilari[tur.value] = len([b for b in hayatta_baliklar if b.tur == tur])
        
        # Genetik çeşitlilik
        if hayatta_baliklar:
            ortalama_zeka = sum(b.zeka for b in hayatta_baliklar) / len(hayatta_baliklar)
            ortalama_guc = sum(b.guc for b in hayatta_baliklar) / len(hayatta_baliklar)
            ortalama_dayaniklilik = sum(b.dayaniklilik for b in hayatta_baliklar) / len(hayatta_baliklar)
            toplam_mutasyon = sum(b.mutasyon_sayisi for b in hayatta_baliklar)
        else:
            ortalama_zeka = ortalama_guc = ortalama_dayaniklilik = toplam_mutasyon = 0
        
        # Kayıt
        self.populasyon_gecmisi.append(toplam_sayi)
        self.renk_dagilimi_gecmisi.append(renk_sayilari.copy())
        self.tur_dagilimi_gecmisi.append(tur_sayilari.copy())
        self.su_ortami_gecmisi.append({
            'sicaklik': self.su_ortami.sicaklik,
            'ph': self.su_ortami.ph,
            'oksijen': self.su_ortami.oksijen,
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
        # Akvaryum arka planı (mavi tonları)
        self.ekran.fill((30, 144, 255))  # Dodger blue
        
        if self.gosterim_modu == "normal":
            self._normal_cizim()
        elif self.gosterim_modu == "istatistik":
            self._istatistik_cizim()
        elif self.gosterim_modu == "genetik":
            self._genetik_cizim()
        
        pygame.display.flip()
    
    def _normal_cizim(self):
        """Normal görünüm çizimi"""
        # Yiyecek kaynaklarını çiz (balık yemi)
        for kaynak in self.yiyecek_kaynaklari:
            renk_yogunlugu = int(200 * (kaynak.miktar / kaynak.max_miktar))
            pygame.draw.circle(self.ekran, (255, 215, 0), 
                             (int(kaynak.x), int(kaynak.y)), 6)
        
        # Avcıları çiz (büyük balık)
        for avci in self.avcilar:
            pygame.draw.circle(self.ekran, (139, 0, 0), 
                             (int(avci.x), int(avci.y)), 15)
            # Menzil göster
            pygame.draw.circle(self.ekran, (139, 0, 0), 
                             (int(avci.x), int(avci.y)), int(avci.menzil), 1)
        
        # Balıkları çiz
        for balik in self.baliklar:
            if balik.hayatta:
                renk = self.renkler[balik.renk]
                
                # Balık şekli (türe göre)
                if balik.tur == BalikTuru.KOI:
                    self._koi_ciz(balik, renk)
                elif balik.tur == BalikTuru.JAPON_BALIGI:
                    self._japon_baligi_ciz(balik, renk)
                else:
                    # Basit balık şekli
                    pygame.draw.ellipse(self.ekran, renk, 
                                      (int(balik.x - balik.boyut), int(balik.y - balik.boyut//2), 
                                       int(balik.boyut * 2), int(balik.boyut)))
                    # Kuyruk
                    pygame.draw.polygon(self.ekran, renk,
                                      [(int(balik.x - balik.boyut), int(balik.y)),
                                       (int(balik.x - balik.boyut * 1.5), int(balik.y - balik.boyut//2)),
                                       (int(balik.x - balik.boyut * 1.5), int(balik.y + balik.boyut//2))])
                
                # Enerji çubuğu
                if balik.enerji < balik.max_enerji * 0.3:
                    enerji_rengi = (255, 0, 0)
                elif balik.enerji < balik.max_enerji * 0.6:
                    enerji_rengi = (255, 255, 0)
                else:
                    enerji_rengi = (0, 255, 0)
                
                enerji_orani = balik.enerji / balik.max_enerji
                pygame.draw.rect(self.ekran, enerji_rengi,
                               (balik.x - 10, balik.y - balik.boyut - 12, 
                                20 * enerji_orani, 4))
                
                # Hamilelik göstergesi
                if balik.hamile:
                    pygame.draw.circle(self.ekran, (255, 192, 203), 
                                     (int(balik.x), int(balik.y)), int(balik.boyut + 3), 2)
        
        # Bilgi paneli
        self._bilgi_paneli_ciz()
    
    def _koi_ciz(self, balik: Balik, renk: Tuple[int, int, int]):
        """Koi balığı şeklinde çiz"""
        x, y = int(balik.x), int(balik.y)
        boyut = int(balik.boyut)
        
        # Gövde (büyük oval)
        pygame.draw.ellipse(self.ekran, renk, (x-boyut, y-boyut//2, boyut*2, boyut))
        # Kuyruk (üçgen)
        pygame.draw.polygon(self.ekran, renk,
                          [(x-boyut, y), (x-boyut*1.6, y-boyut//2), (x-boyut*1.6, y+boyut//2)])
        # Yüzgeçler
        pygame.draw.ellipse(self.ekran, renk, (x-boyut//2, y-boyut*1.2, boyut//2, boyut//2))
        pygame.draw.ellipse(self.ekran, renk, (x-boyut//2, y+boyut//2, boyut//2, boyut//2))
    
    def _japon_baligi_ciz(self, balik: Balik, renk: Tuple[int, int, int]):
        """Japon balığı şeklinde çiz"""
        x, y = int(balik.x), int(balik.y)
        boyut = int(balik.boyut)
        
        # Yuvarlak gövde
        pygame.draw.circle(self.ekran, renk, (x, y), boyut)
        # Kuyruk
        pygame.draw.polygon(self.ekran, renk,
                          [(x-boyut, y), (x-boyut*1.4, y-boyut//3), (x-boyut*1.4, y+boyut//3)])
    
    def _bilgi_paneli_ciz(self):
        """Bilgi panelini çiz"""
        hayatta_baliklar = [b for b in self.baliklar if b.hayatta]
        
        bilgiler = [
            f"🐠 Akvaryum Simülasyonu 🐠",
            f"Zaman: {self.zaman}",
            f"Nesil: {self.nesil}",
            f"Balık Sayısı: {len(hayatta_baliklar)}",
            f"Mevsim: {self.su_ortami.mevsim.capitalize()}",
            f"Su Sıcaklığı: {self.su_ortami.sicaklik:.1f}°C",
            f"pH: {self.su_ortami.ph:.1f}",
            f"Oksijen: {self.su_ortami.oksijen:.1f}%",
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
            bilgiler.insert(1, "*** DURAKLATILDI ***")
        
        if self.hizli_mod:
            bilgiler.insert(-7, "*** HIZLI MOD ***")
        
        # Renk dağılımını göster
        bilgiler.append("")
        bilgiler.append("Renk Dağılımı:")
        for renk in self.renkler.keys():
            sayi = len([b for b in hayatta_baliklar if b.renk == renk])
            bilgiler.append(f"🔴 {renk.capitalize()}: {sayi}" if renk == "kirmizi" else f"⚪ {renk.capitalize()}: {sayi}")
        
        y_offset = 10
        for bilgi in bilgiler:
            if bilgi.startswith("***"):
                metin = self.buyuk_font.render(bilgi, True, (255, 255, 0))
            elif bilgi.startswith("🐠"):
                metin = self.buyuk_font.render(bilgi, True, (255, 255, 255))
            else:
                metin = self.font.render(bilgi, True, (255, 255, 255))
            self.ekran.blit(metin, (10, y_offset))
            y_offset += 25
    
    def _istatistik_cizim(self):
        """İstatistik görünümü"""
        self.ekran.fill((30, 144, 255))
        
        # Renk dağılımı pasta grafiği
        if self.renk_dagilimi_gecmisi:
            son_dagilim = self.renk_dagilimi_gecmisi[-1]
            toplam = sum(son_dagilim.values())
            
            if toplam > 0:
                merkez_x, merkez_y = 400, 250
                radius = 100
                baslangic_aci = 0
                
                for renk, sayi in son_dagilim.items():
                    if sayi > 0:
                        aci = (sayi / toplam) * 360
                        pygame.draw.arc(self.ekran, self.renkler[renk],
                                      (merkez_x-radius, merkez_y-radius, radius*2, radius*2),
                                      math.radians(baslangic_aci), 
                                      math.radians(baslangic_aci + aci), 15)
                        baslangic_aci += aci
        
        self._bilgi_paneli_ciz()
    
    def _genetik_cizim(self):
        """Genetik görünüm"""
        self.ekran.fill((30, 144, 255))
        
        # Balıkları genetik özelliklerine göre renklendir
        for balik in self.baliklar:
            if balik.hayatta:
                # Zeka seviyesine göre renk
                zeka_rengi = int(255 * balik.zeka)
                renk = (zeka_rengi, 100, 255 - zeka_rengi)
                
                pygame.draw.circle(self.ekran, renk, 
                                 (int(balik.x), int(balik.y)), int(balik.boyut))
                
                # Mutasyon göstergesi
                if balik.mutasyon_sayisi > 0:
                    pygame.draw.circle(self.ekran, (255, 255, 255), 
                                     (int(balik.x), int(balik.y)), int(balik.boyut + 4), 3)
        
        self._bilgi_paneli_ciz()
    
    def simulasyonu_calistir(self):
        """Ana simülasyon döngüsü"""
        self.baslangic_akvaryumu_olustur()
        
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
                self.su_ortami_guncelle()
                
                # Balık hareketleri
                for balik in self.baliklar:
                    balik.hareket_et(self.genislik, self.yukseklik, self.su_ortami, self.baliklar)
                
                # Avcı hareketleri
                for avci in self.avcilar:
                    avci.hareket_et(self.genislik, self.yukseklik, self.baliklar)
                
                self.yiyecek_sistemi_guncelle()
                self.dogal_secilim_uygula()
                
                # Üreme (her 120 zaman biriminde)
                if self.zaman % 120 == 0:
                    self.ureme_gerceklestir()
                    self.nesil += 1
                
                self.istatistikleri_guncelle()
                self.zaman += 1
                
                # Popülasyon kontrolü
                hayatta_sayi = len([b for b in self.baliklar if b.hayatta])
                if hayatta_sayi < 25:
                    print(f"Balık popülasyonu kritik seviyede ({hayatta_sayi}), yeni balıklar ekleniyor...")
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
        hayatta_baliklar = [b for b in self.baliklar if b.hayatta]
        
        if len(hayatta_baliklar) > 0:
            # Mevcut balıklardan örnekleyerek yenilerini oluştur
            for _ in range(40):
                ornek = random.choice(hayatta_baliklar)
                yeni_balik = Balik(
                    x=random.uniform(80, self.genislik - 80),
                    y=random.uniform(80, self.yukseklik - 80),
                    renk=ornek.renk,
                    boyut=ornek.boyut + random.uniform(-1.5, 1.5),
                    hiz=ornek.hiz + random.uniform(-0.3, 0.3),
                    enerji=random.uniform(80, 110),
                    max_enerji=ornek.max_enerji,
                    yas=0,
                    zeka=ornek.zeka + random.uniform(-0.12, 0.12),
                    guc=ornek.guc + random.uniform(-0.12, 0.12),
                    dayaniklilik=ornek.dayaniklilik + random.uniform(-0.12, 0.12),
                    tur=ornek.tur,
                    davranis=ornek.davranis,
                    cinsiyet=random.choice(["erkek", "disi"]),
                    nesil=ornek.nesil + 1
                )
                self.baliklar.append(yeni_balik)
        else:
            # Tamamen yeni popülasyon
            self.baslangic_akvaryumu_olustur()
    
    def yeniden_baslat(self):
        """Simülasyonu yeniden başlat"""
        self.zaman = 0
        self.nesil = 0
        self.populasyon_gecmisi.clear()
        self.renk_dagilimi_gecmisi.clear()
        self.su_ortami_gecmisi.clear()
        self.genetik_cesitlilik_gecmisi.clear()
        self.tur_dagilimi_gecmisi.clear()
        self.baslangic_akvaryumu_olustur()
    
    def veri_kaydet(self):
        """Simülasyon verilerini kaydet"""
        zaman_damgasi = datetime.now().strftime("%Y%m%d_%H%M%S")
        dosya_adi = f"balik_simulasyon_verileri_{zaman_damgasi}.json"
        
        veri = {
            'zaman': self.zaman,
            'nesil': self.nesil,
            'populasyon_gecmisi': self.populasyon_gecmisi,
            'renk_dagilimi_gecmisi': self.renk_dagilimi_gecmisi,
            'su_ortami_gecmisi': self.su_ortami_gecmisi,
            'genetik_cesitlilik_gecmisi': self.genetik_cesitlilik_gecmisi,
            'tur_dagilimi_gecmisi': self.tur_dagilimi_gecmisi,
            'balik_sayisi': len([b for b in self.baliklar if b.hayatta])
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
        plt.plot(self.populasyon_gecmisi, linewidth=2, color='blue')
        plt.title('🐠 Toplam Balık Popülasyonu Değişimi', fontweight='bold')
        plt.xlabel('Zaman')
        plt.ylabel('Balık Sayısı')
        plt.grid(True, alpha=0.3)
        
        # 2. Renk dağılımı
        ax2 = plt.subplot(3, 2, 2)
        if self.renk_dagilimi_gecmisi:
            for renk in self.renkler.keys():
                renk_verileri = [veri.get(renk, 0) for veri in self.renk_dagilimi_gecmisi]
                if max(renk_verileri) > 0:
                    color = 'red' if renk == 'kirmizi' else 'lightgray'
                    plt.plot(renk_verileri, label=renk.capitalize(), linewidth=2, color=color)
        plt.title('🔴⚪ Renk Dağılımı (Kırmızı vs Beyaz)', fontweight='bold')
        plt.xlabel('Zaman')
        plt.ylabel('Balık Sayısı')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # 3. Su ortamı koşulları
        ax3 = plt.subplot(3, 2, 3)
        if self.su_ortami_gecmisi:
            sicakliklar = [veri['sicaklik'] for veri in self.su_ortami_gecmisi]
            ph_verileri = [veri['ph'] for veri in self.su_ortami_gecmisi]
            plt.plot(sicakliklar, label='Sıcaklık (°C)', color='red', linewidth=2)
            plt.plot([p*10 for p in ph_verileri], label='pH x10', color='green', linewidth=2)
            plt.title('🌡️ Su Ortamı Koşulları', fontweight='bold')
            plt.xlabel('Zaman')
            plt.ylabel('Değer')
            plt.legend()
            plt.grid(True, alpha=0.3)
        
        # 4. Genetik çeşitlilik
        ax4 = plt.subplot(3, 2, 4)
        if self.genetik_cesitlilik_gecmisi:
            zeka_verileri = [veri['zeka'] for veri in self.genetik_cesitlilik_gecmisi]
            guc_verileri = [veri['guc'] for veri in self.genetik_cesitlilik_gecmisi]
            dayaniklilik_verileri = [veri['dayaniklilik'] for veri in self.genetik_cesitlilik_gecmisi]
            
            plt.plot(zeka_verileri, label='Ortalama Zeka', linewidth=2, color='purple')
            plt.plot(guc_verileri, label='Ortalama Güç', linewidth=2, color='orange')
            plt.plot(dayaniklilik_verileri, label='Ortalama Dayanıklılık', linewidth=2, color='brown')
            
        plt.title('🧠 Genetik Özellikler', fontweight='bold')
        plt.xlabel('Zaman')
        plt.ylabel('Değer')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # 5. Tür dağılımı
        ax5 = plt.subplot(3, 2, 5)
        if self.tur_dagilimi_gecmisi:
            for tur in BalikTuru:
                tur_verileri = [veri.get(tur.value, 0) for veri in self.tur_dagilimi_gecmisi]
                if max(tur_verileri) > 0:
                    plt.plot(tur_verileri, label=tur.value.replace('_', ' ').title(), linewidth=2)
        plt.title('🐟 Balık Türü Dağılımı', fontweight='bold')
        plt.xlabel('Zaman')
        plt.ylabel('Balık Sayısı')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # 6. Avcı etkisi
        ax6 = plt.subplot(3, 2, 6)
        if self.su_ortami_gecmisi:
            avci_sayilari = [veri['avci_sayisi'] for veri in self.su_ortami_gecmisi]
            plt.plot(avci_sayilari, label='Avcı Sayısı', color='darkred', linewidth=3)
            plt.plot(self.populasyon_gecmisi, label='Balık Popülasyonu', color='blue', alpha=0.7)
        plt.title('🦈 Avcı-Av İlişkisi', fontweight='bold')
        plt.xlabel('Zaman')
        plt.ylabel('Sayı')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()

def main():
    """Ana fonksiyon"""
    print("=== 🐠 GELİŞMİŞ BALIK AKVARYUMU SİMÜLASYONU 🐠 ===")
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
    print("- 🔴 Kırmızı ve ⚪ Beyaz balıklar")
    print("- 4 farklı balık türü (Koi, Japon Balığı, Guppy, Neon)")
    print("- Su ortamı koşulları (sıcaklık, pH, oksijen)")
    print("- Balık yemi kaynakları ve avcı balıklar")
    print("- Genetik kalıtım ve mutasyonlar")
    print("- Davranış türleri (agresif, sosyal, vb.)")
    print("- Hastalık sistemi")
    print("- Kapsamlı istatistikler")
    print("\nAkvaryum başlatılıyor...")
    
    simulasyon = BalikSimulasyonu()
    simulasyon.simulasyonu_calistir()

if __name__ == "__main__":
    main() 