import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import random
import threading
import time
from dataclasses import dataclass
from typing import List, Dict, Tuple
import json
from datetime import datetime
import math

@dataclass
class CevreselParametreler:
    """Çevresel faktörler"""
    su_sicakligi: float = 18.0  # °C
    oksijen_seviyesi: float = 8.0  # mg/L
    yiyecek_miktari: float = 1.0  # 0-2 arası
    avci_yogunlugu: float = 0.3  # 0-1 arası
    hastalik_riski: float = 0.1  # 0-1 arası
    kirlilik_seviyesi: float = 0.2  # 0-1 arası

class Mevsim:
    """Mevsim sınıfı"""
    def __init__(self):
        self.mevsimler = ["İlkbahar", "Yaz", "Sonbahar", "Kış"]
        self.mevcut_mevsim = 0
        self.gun = 0
        
    def guncelle(self):
        """Günü ve mevsimi güncelle"""
        self.gun += 1
        if self.gun >= 90:  # Her 90 gün bir mevsim değişir
            self.gun = 0
            self.mevcut_mevsim = (self.mevcut_mevsim + 1) % 4
            
    def mevcut_mevsim_adi(self):
        return self.mevsimler[self.mevcut_mevsim]
        
    def mevsimsel_faktorler(self) -> CevreselParametreler:
        """Mevsime göre çevresel faktörleri ayarla"""
        if self.mevcut_mevsim == 0:  # İlkbahar
            return CevreselParametreler(
                su_sicakligi=15.0 + random.uniform(-2, 2),
                oksijen_seviyesi=9.0 + random.uniform(-0.5, 0.5),
                yiyecek_miktari=1.2 + random.uniform(-0.2, 0.3),
                avci_yogunlugu=0.4 + random.uniform(-0.1, 0.1),
                hastalik_riski=0.15 + random.uniform(-0.05, 0.05),
                kirlilik_seviyesi=0.1 + random.uniform(0, 0.1)
            )
        elif self.mevcut_mevsim == 1:  # Yaz
            return CevreselParametreler(
                su_sicakligi=25.0 + random.uniform(-3, 5),
                oksijen_seviyesi=7.0 + random.uniform(-1, 0.5),
                yiyecek_miktari=1.5 + random.uniform(-0.3, 0.5),
                avci_yogunlugu=0.6 + random.uniform(-0.1, 0.2),
                hastalik_riski=0.25 + random.uniform(-0.05, 0.15),
                kirlilik_seviyesi=0.3 + random.uniform(0, 0.2)
            )
        elif self.mevcut_mevsim == 2:  # Sonbahar
            return CevreselParametreler(
                su_sicakligi=12.0 + random.uniform(-2, 3),
                oksijen_seviyesi=8.5 + random.uniform(-0.5, 0.5),
                yiyecek_miktari=0.8 + random.uniform(-0.3, 0.2),
                avci_yogunlugu=0.3 + random.uniform(-0.1, 0.1),
                hastalik_riski=0.2 + random.uniform(-0.05, 0.1),
                kirlilik_seviyesi=0.15 + random.uniform(0, 0.1)
            )
        else:  # Kış
            return CevreselParametreler(
                su_sicakligi=5.0 + random.uniform(-2, 3),
                oksijen_seviyesi=9.5 + random.uniform(-0.3, 0.3),
                yiyecek_miktari=0.4 + random.uniform(-0.2, 0.1),
                avci_yogunlugu=0.2 + random.uniform(-0.05, 0.05),
                hastalik_riski=0.3 + random.uniform(-0.1, 0.2),
                kirlilik_seviyesi=0.25 + random.uniform(0, 0.15)
            )

class BalikBireyi:
    """Gelişmiş balık bireyini temsil eden sınıf"""
    def __init__(self, genotip: str, cinsiyet: str, yas: int = 0):
        self.genotip = genotip  # Çoklu gen: renk, boyut, direnç
        self.cinsiyet = cinsiyet
        self.yas = yas
        self.hayatta = True
        self.saglik = 1.0  # 0-1 arası
        self.boyut = self.boyut_hesapla()
        self.direnc = self.direnc_hesapla()
        self.uretkenlik = self.uretkenlik_hesapla()
        self.son_ureme = 0
        
    @property
    def fenotip(self):
        """Görünür özellikler"""
        renk_gen = self.genotip[:2]
        if renk_gen in ["KK", "KB"]:
            renk = "kirmizi"
        else:
            renk = "beyaz"
            
        boyut_gen = self.genotip[2:4]
        if boyut_gen in ["BB", "BK"]:
            boyut = "buyuk"
        else:
            boyut = "kucuk"
            
        return {"renk": renk, "boyut": boyut}
    
    def boyut_hesapla(self):
        """Boyutu genetiğe göre hesapla"""
        boyut_gen = self.genotip[2:4]
        if boyut_gen == "BB":
            return random.uniform(0.8, 1.0)
        elif boyut_gen in ["BK", "KB"]:
            return random.uniform(0.6, 0.8) 
        else:
            return random.uniform(0.4, 0.6)
    
    def direnc_hesapla(self):
        """Hastalık direncini hesapla"""
        direnc_gen = self.genotip[4:6] if len(self.genotip) >= 6 else "DD"
        if direnc_gen == "DD":
            return random.uniform(0.8, 1.0)
        elif direnc_gen in ["DY", "YD"]:
            return random.uniform(0.5, 0.8)
        else:
            return random.uniform(0.2, 0.5)
    
    def uretkenlik_hesapla(self):
        """Üretkenlik hesapla"""
        if self.yas < 1:
            return 0.0
        elif self.yas > 8:
            return 0.2
        else:
            return 0.8 * self.saglik * (self.boyut + 0.5)
    
    def yaslan(self):
        """Yaşlanma ve sağlık kaybı"""
        self.yas += 1
        if self.yas > 5:
            self.saglik *= 0.95  # Yaşlanma ile sağlık kaybı
        self.uretkenlik = self.uretkenlik_hesapla()
    
    def cevresel_stress_uygula(self, cevre: CevreselParametreler):
        """Çevresel stress uygulaması"""
        # Sıcaklık stresi
        optimal_sicaklik = 18.0
        sicaklik_stresi = abs(cevre.su_sicakligi - optimal_sicaklik) / 20.0
        
        # Oksijen stresi
        oksijen_stresi = max(0, (6.0 - cevre.oksijen_seviyesi) / 6.0)
        
        # Kirlilik stresi
        kirlilik_stresi = cevre.kirlilik_seviyesi
        
        # Hastalık riski
        hastalik_stresi = cevre.hastalik_riski * (1 - self.direnc)
        
        # Toplam stress
        toplam_stress = (sicaklik_stresi + oksijen_stresi + kirlilik_stresi + hastalik_stresi) / 4
        
        # Sağlığı etkileme
        self.saglik *= (1 - toplam_stress * 0.1)
        self.saglik = max(0, min(1, self.saglik))
        
        return toplam_stress
    
    def olum_riski_hesapla(self, cevre: CevreselParametreler):
        """Ölüm riskini hesapla"""
        # Temel ölüm riski
        temel_risk = 0.02
        
        # Yaş riski
        yas_riski = 0.01 * max(0, self.yas - 5)
        
        # Sağlık riski
        saglik_riski = 0.05 * (1 - self.saglik)
        
        # Çevresel risk
        cevresel_risk = cevre.avci_yogunlugu * 0.03
        
        # Yiyecek eksikliği riski
        yiyecek_riski = max(0, (0.5 - cevre.yiyecek_miktari)) * 0.04
        
        return min(0.5, temel_risk + yas_riski + saglik_riski + cevresel_risk + yiyecek_riski)

class EkolojikBalikSimulasyonu:
    """Ana ekolojik balık simülasyonu sınıfı"""
    
    def __init__(self):
        self.populasyon: List[BalikBireyi] = []
        self.mevsim = Mevsim()
        self.cevre = CevreselParametreler()
        self.nesil = 0
        self.gun = 0
        self.calisir = False
        
        # Veri takibi
        self.zaman_verileri = []
        self.populasyon_verileri = []
        self.cevresel_veriler = []
        self.genetik_veriler = []
        self.yas_dagilimi_verileri = []
        
        # Kritik olaylar
        self.kritik_olaylar = []
        
        self.arayuz_olustur()
        
    def arayuz_olustur(self):
        """Ana arayüz oluştur"""
        self.root = tk.Tk()
        self.root.title("🌊 Ekolojik Balık Popülasyonu Simülasyonu")
        self.root.geometry("1600x1000")
        self.root.configure(bg='#2c3e50')
        
        # Ana çerçeveler
        self.sol_panel_olustur()
        self.sag_panel_olustur()
        
        # Başlangıç popülasyonu oluştur
        self.baslangic_populasyonu_olustur()
        self.grafikleri_guncelle()
        
    def sol_panel_olustur(self):
        """Sol kontrol paneli"""
        self.sol_frame = tk.Frame(self.root, bg='#34495e', width=400)
        self.sol_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        self.sol_frame.pack_propagate(False)
        
        # Başlık
        baslik = tk.Label(self.sol_frame, text="🌊 Ekolojik Balık Simülasyonu", 
                         font=("Arial", 16, "bold"), bg='#34495e', fg='white')
        baslik.pack(pady=10)
        
        # Kontrol butonları
        buton_frame = tk.Frame(self.sol_frame, bg='#34495e')
        buton_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.baslat_btn = tk.Button(buton_frame, text="▶ Başlat", command=self.simulasyonu_baslat,
                                   bg='#27ae60', fg='white', font=("Arial", 12, "bold"))
        self.baslat_btn.pack(side=tk.LEFT, padx=5)
        
        self.durdur_btn = tk.Button(buton_frame, text="⏸ Duraklat", command=self.simulasyonu_durdur,
                                   bg='#e67e22', fg='white', font=("Arial", 12, "bold"))
        self.durdur_btn.pack(side=tk.LEFT, padx=5)
        
        self.sifirla_btn = tk.Button(buton_frame, text="🔄 Sıfırla", command=self.simulasyonu_sifirla,
                                    bg='#e74c3c', fg='white', font=("Arial", 12, "bold"))
        self.sifirla_btn.pack(side=tk.LEFT, padx=5)
        
        # Durum paneli
        self.durum_paneli_olustur()
        
        # Çevresel faktörler paneli
        self.cevresel_panel_olustur()
        
    def durum_paneli_olustur(self):
        """Durum paneli oluştur"""
        durum_frame = tk.LabelFrame(self.sol_frame, text="Durum Bilgileri", 
                                   font=("Arial", 12, "bold"), bg='#34495e', fg='white')
        durum_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.durum_label = tk.Label(durum_frame, text="", bg='#34495e', fg='white',
                                   font=("Arial", 10), justify=tk.LEFT)
        self.durum_label.pack(fill=tk.X, padx=10, pady=10)
        
    def cevresel_panel_olustur(self):
        """Çevresel faktörler paneli"""
        cevre_frame = tk.LabelFrame(self.sol_frame, text="Çevresel Faktörler", 
                                   font=("Arial", 12, "bold"), bg='#34495e', fg='white')
        cevre_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.cevre_label = tk.Label(cevre_frame, text="", bg='#34495e', fg='white',
                                   font=("Arial", 10), justify=tk.LEFT)
        self.cevre_label.pack(fill=tk.X, padx=10, pady=10)
        
    def sag_panel_olustur(self):
        """Sağ grafik paneli"""
        self.sag_frame = tk.Frame(self.root, bg='white')
        self.sag_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Grafik alanı
        self.fig, ((self.ax1, self.ax2), (self.ax3, self.ax4)) = plt.subplots(2, 2, figsize=(12, 8))
        self.fig.patch.set_facecolor('#ecf0f1')
        
        self.canvas = FigureCanvasTkAgg(self.fig, self.sag_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        plt.tight_layout()
        
    def baslangic_populasyonu_olustur(self):
        """Başlangıç popülasyonunu oluştur"""
        self.populasyon.clear()
        self.zaman_verileri.clear()
        self.populasyon_verileri.clear()
        self.cevresel_veriler.clear()
        self.genetik_veriler.clear()
        self.kritik_olaylar.clear()
        
        # İlk popülasyon - çeşitli genetik kombinasyonlar
        for i in range(200):
            # Renk geni (K=kırmızı, B=beyaz)
            renk = random.choices(["K", "B"], weights=[0.6, 0.4], k=2)
            # Boyut geni (B=büyük, K=küçük) 
            boyut = random.choices(["B", "K"], weights=[0.3, 0.7], k=2)
            # Direnç geni (D=dirençli, Y=zayıf)
            direnc = random.choices(["D", "Y"], weights=[0.7, 0.3], k=2)
            
            genotip = "".join(sorted(renk, reverse=True)) + "".join(sorted(boyut, reverse=True)) + "".join(sorted(direnc, reverse=True))
            cinsiyet = random.choice(["erkek", "disi"])
            yas = random.randint(1, 5)
            
            birey = BalikBireyi(genotip, cinsiyet, yas)
            self.populasyon.append(birey)
        
        self.nesil = 0
        self.gun = 0
        self.mevsim = Mevsim()
        
    def simulasyonu_baslat(self):
        """Simülasyonu başlat"""
        if not self.calisir:
            self.calisir = True
            self.simulasyon_thread = threading.Thread(target=self.simulasyon_dongusu)
            self.simulasyon_thread.daemon = True
            self.simulasyon_thread.start()
    
    def simulasyonu_durdur(self):
        """Simülasyonu durdur"""
        self.calisir = False
        
    def simulasyonu_sifirla(self):
        """Simülasyonu sıfırla"""
        self.calisir = False
        time.sleep(0.1)
        self.baslangic_populasyonu_olustur()
        self.grafikleri_guncelle()
        
    def simulasyon_dongusu(self):
        """Ana simülasyon döngüsü"""
        while self.calisir and len(self.populasyon) > 0:
            self.gun += 1
            
            # Mevsimi güncelle
            self.mevsim.guncelle()
            
            # Çevresel faktörleri güncelle
            self.cevre = self.mevsim.mevsimsel_faktorler()
            
            # Kritik olayları kontrol et
            self.kritik_olaylari_kontrol_et()
            
            # Popülasyon dinamikleri
            self.gunluk_yasam_dongusu()
            
            # Her 30 günde bir veri kaydet
            if self.gun % 30 == 0:
                self.verileri_kaydet()
                self.root.after(0, self.grafikleri_guncelle)
            
            # Hız kontrolü
            time.sleep(0.1)
            
    def kritik_olaylari_kontrol_et(self):
        """Kritik çevresel olayları kontrol et"""
        # Hastalık salgını (düşük olasılık)
        if random.random() < 0.001:
            self.cevre.hastalik_riski = min(1.0, self.cevre.hastalik_riski * 3)
            self.kritik_olaylar.append({
                'gun': self.gun,
                'olay': 'Hastalık Salgını',
                'etki': 'Yüksek ölüm oranı'
            })
            
        # Kirlilik artışı
        if random.random() < 0.002:
            self.cevre.kirlilik_seviyesi = min(1.0, self.cevre.kirlilik_seviyesi * 2)
            self.kritik_olaylar.append({
                'gun': self.gun,
                'olay': 'Kirlilik Artışı',
                'etki': 'Çevresel stress'
            })
            
        # Avcı istilası
        if random.random() < 0.0015:
            self.cevre.avci_yogunlugu = min(1.0, self.cevre.avci_yogunlugu * 2)
            self.kritik_olaylar.append({
                'gun': self.gun,
                'olay': 'Avcı İstilası',
                'etki': 'Yüksek avcılık baskısı'
            })
    
    def gunluk_yasam_dongusu(self):
        """Günlük yaşam döngüsü"""
        # Yaşlanma
        for balik in self.populasyon:
            if random.random() < 0.01:  # Her 100 günde bir yaşlanır
                balik.yaslan()
            
            # Çevresel stress uygula
            balik.cevresel_stress_uygula(self.cevre)
            
        # Ölümler
        yeni_populasyon = []
        for balik in self.populasyon:
            olum_riski = balik.olum_riski_hesapla(self.cevre)
            if random.random() > olum_riski:
                yeni_populasyon.append(balik)
                
        self.populasyon = yeni_populasyon
        
        # Üreme (ilkbahar ve yazda daha fazla)
        if self.mevsim.mevcut_mevsim in [0, 1] and len(self.populasyon) >= 2:
            self.ureme_gerceklestir()
    
    def ureme_gerceklestir(self):
        """Üreme işlemi"""
        if len(self.populasyon) < 2:
            return
            
        uygun_erkekler = [b for b in self.populasyon if b.cinsiyet == "erkek" and b.yas >= 1]
        uygun_disiler = [b for b in self.populasyon if b.cinsiyet == "disi" and b.yas >= 1]
        
        if not uygun_erkekler or not uygun_disiler:
            return
            
        # Yiyecek miktarına göre üreme oranı
        ureme_orani = min(0.3, self.cevre.yiyecek_miktari * 0.2)
        
        for disi in uygun_disiler:
            if random.random() < ureme_orani * disi.uretkenlik:
                erkek = random.choice(uygun_erkekler)
                yavru_sayisi = random.randint(1, 5)
                
                for _ in range(yavru_sayisi):
                    yavru_genotip = self.genotip_olustur(disi.genotip, erkek.genotip)
                    yavru_cinsiyet = random.choice(["erkek", "disi"])
                    yavru = BalikBireyi(yavru_genotip, yavru_cinsiyet, 0)
                    self.populasyon.append(yavru)
    
    def genotip_olustur(self, anne_genotip: str, baba_genotip: str) -> str:
        """Çaprazlama ile yavru genotipi oluştur"""
        yavru_genotip = ""
        
        # Her gen için çaprazlama
        for i in range(0, len(anne_genotip), 2):
            anne_gen = anne_genotip[i:i+2]
            baba_gen = baba_genotip[i:i+2]
            
            anne_allel = random.choice([anne_gen[0], anne_gen[1]])
            baba_allel = random.choice([baba_gen[0], baba_gen[1]])
            
            # Mutasyon kontrolü
            if random.random() < 0.01:  # %1 mutasyon şansı
                anne_allel = self.mutasyon_uygula(anne_allel)
            if random.random() < 0.01:
                baba_allel = self.mutasyon_uygula(baba_allel)
                
            yavru_gen = "".join(sorted([anne_allel, baba_allel], reverse=True))
            yavru_genotip += yavru_gen
            
        return yavru_genotip
    
    def mutasyon_uygula(self, allel: str) -> str:
        """Allel mutasyonu"""
        mutasyon_tablosu = {
            'K': 'B', 'B': 'K',  # Renk
            'D': 'Y', 'Y': 'D'   # Direnç
        }
        return mutasyon_tablosu.get(allel, allel)
    
    def verileri_kaydet(self):
        """Veri kaydetme"""
        if not self.populasyon:
            return
            
        # Popülasyon istatistikleri
        toplam = len(self.populasyon)
        kirmizi_sayisi = len([b for b in self.populasyon if b.fenotip["renk"] == "kirmizi"])
        buyuk_sayisi = len([b for b in self.populasyon if b.fenotip["boyut"] == "buyuk"])
        
        # Yaş dağılımı
        yas_dagilimi = {}
        for balik in self.populasyon:
            yas_grubu = f"{balik.yas//2*2}-{balik.yas//2*2+1}"
            yas_dagilimi[yas_grubu] = yas_dagilimi.get(yas_grubu, 0) + 1
        
        # Veriler kaydet
        self.zaman_verileri.append(self.gun)
        self.populasyon_verileri.append({
            'toplam': toplam,
            'kirmizi': kirmizi_sayisi,
            'beyaz': toplam - kirmizi_sayisi,
            'buyuk': buyuk_sayisi,
            'kucuk': toplam - buyuk_sayisi
        })
        
        self.cevresel_veriler.append({
            'sicaklik': self.cevre.su_sicakligi,
            'oksijen': self.cevre.oksijen_seviyesi,
            'yiyecek': self.cevre.yiyecek_miktari,
            'avci': self.cevre.avci_yogunlugu,
            'hastalik': self.cevre.hastalik_riski,
            'kirlilik': self.cevre.kirlilik_seviyesi,
            'mevsim': self.mevsim.mevcut_mevsim
        })
        
        self.yas_dagilimi_verileri.append(yas_dagilimi)
    
    def grafikleri_guncelle(self):
        """Grafikleri güncelle"""
        if not self.zaman_verileri:
            return
            
        # Grafikleri temizle
        for ax in [self.ax1, self.ax2, self.ax3, self.ax4]:
            ax.clear()
        
        gunler = np.array(self.zaman_verileri)
        
        # 1. Popülasyon Dinamikleri
        toplam_pop = [p['toplam'] for p in self.populasyon_verileri]
        kirmizi_pop = [p['kirmizi'] for p in self.populasyon_verileri]
        beyaz_pop = [p['beyaz'] for p in self.populasyon_verileri]
        
        self.ax1.plot(gunler, toplam_pop, 'k-', linewidth=2, label='Toplam')
        self.ax1.plot(gunler, kirmizi_pop, 'r-', linewidth=2, label='Kırmızı')
        self.ax1.plot(gunler, beyaz_pop, 'lightgray', linewidth=2, label='Beyaz')
        self.ax1.set_title('🐠 Popülasyon Dinamikleri', fontweight='bold')
        self.ax1.set_xlabel('Gün')
        self.ax1.set_ylabel('Birey Sayısı')
        self.ax1.legend()
        self.ax1.grid(True, alpha=0.3)
        
        # Kritik olayları işaretle
        for olay in self.kritik_olaylar:
            self.ax1.axvline(x=olay['gun'], color='red', linestyle='--', alpha=0.7)
            self.ax1.text(olay['gun'], max(toplam_pop)*0.9, olay['olay'], 
                         rotation=90, fontsize=8, ha='right')
        
        # 2. Çevresel Faktörler
        sicakliklar = [c['sicaklik'] for c in self.cevresel_veriler]
        oksijenler = [c['oksijen'] for c in self.cevresel_veriler]
        yiyecekler = [c['yiyecek'] for c in self.cevresel_veriler]
        
        ax2_twin = self.ax2.twinx()
        self.ax2.plot(gunler, sicakliklar, 'orange', linewidth=2, label='Sıcaklık (°C)')
        ax2_twin.plot(gunler, oksijenler, 'blue', linewidth=2, label='Oksijen (mg/L)')
        ax2_twin.plot(gunler, yiyecekler, 'green', linewidth=2, label='Yiyecek')
        
        self.ax2.set_title('🌡️ Çevresel Faktörler', fontweight='bold')
        self.ax2.set_xlabel('Gün')
        self.ax2.set_ylabel('Sıcaklık (°C)', color='orange')
        ax2_twin.set_ylabel('Oksijen & Yiyecek', color='blue')
        self.ax2.grid(True, alpha=0.3)
        
        # 3. Mevsimsel Değişim
        mevsimler = [c['mevsim'] for c in self.cevresel_veriler]
        mevsim_isimleri = ['İlkbahar', 'Yaz', 'Sonbahar', 'Kış']
        colors = ['green', 'red', 'orange', 'blue']
        
        for i, mevsim_num in enumerate(set(mevsimler)):
            mevsim_gunleri = [g for g, m in zip(gunler, mevsimler) if m == mevsim_num]
            mevsim_poplari = [p for g, p, m in zip(gunler, toplam_pop, mevsimler) if m == mevsim_num]
            if mevsim_gunleri:
                self.ax3.scatter(mevsim_gunleri, mevsim_poplari, 
                               c=colors[mevsim_num], label=mevsim_isimleri[mevsim_num], alpha=0.7)
        
        self.ax3.set_title('🍂 Mevsimsel Popülasyon Değişimi', fontweight='bold')
        self.ax3.set_xlabel('Gün')
        self.ax3.set_ylabel('Popülasyon')
        self.ax3.legend()
        self.ax3.grid(True, alpha=0.3)
        
        # 4. Genetik Çeşitlilik
        if len(self.populasyon_verileri) > 1:
            kirmizi_oranları = [p['kirmizi']/max(1, p['toplam']) for p in self.populasyon_verileri]
            buyuk_oranlari = [p['buyuk']/max(1, p['toplam']) for p in self.populasyon_verileri]
            
            self.ax4.plot(gunler, kirmizi_oranları, 'red', linewidth=2, label='Kırmızı Oranı')
            self.ax4.plot(gunler, buyuk_oranlari, 'blue', linewidth=2, label='Büyük Boyut Oranı')
            
        self.ax4.set_title('🧬 Genetik Çeşitlilik', fontweight='bold')
        self.ax4.set_xlabel('Gün')
        self.ax4.set_ylabel('Oran')
        self.ax4.legend()
        self.ax4.grid(True, alpha=0.3)
        self.ax4.set_ylim(0, 1)
        
        plt.tight_layout()
        self.canvas.draw()
        
        # Durum panelini güncelle
        self.durum_panelini_guncelle()
    
    def durum_panelini_guncelle(self):
        """Durum panelini güncelle"""
        if not self.populasyon:
            durum_text = "Popülasyon: 0\nSimülasyon durdu!"
        else:
            toplam = len(self.populasyon)
            kirmizi = len([b for b in self.populasyon if b.fenotip["renk"] == "kirmizi"])
            buyuk = len([b for b in self.populasyon if b.fenotip["boyut"] == "buyuk"])
            ort_yas = sum(b.yas for b in self.populasyon) / len(self.populasyon)
            ort_saglik = sum(b.saglik for b in self.populasyon) / len(self.populasyon)
            
            durum_text = f"""📊 POPÜLASYON İSTATİSTİKLERİ
            
Gün: {self.gun}
Mevsim: {self.mevsim.mevcut_mevsim_adi()}

Toplam Balık: {toplam}
🔴 Kırmızı: {kirmizi} ({kirmizi/toplam*100:.1f}%)
⚪ Beyaz: {toplam-kirmizi} ({(toplam-kirmizi)/toplam*100:.1f}%)

🐋 Büyük: {buyuk} ({buyuk/toplam*100:.1f}%)
🐟 Küçük: {toplam-buyuk} ({(toplam-buyuk)/toplam*100:.1f}%)

⏳ Ortalama Yaş: {ort_yas:.1f}
💚 Ortalama Sağlık: {ort_saglik:.2f}
"""
        
        self.durum_label.config(text=durum_text)
        
        # Çevresel faktörler paneli
        cevre_text = f"""🌍 ÇEVRESEL FAKTÖRLER

🌡️ Su Sıcaklığı: {self.cevre.su_sicakligi:.1f}°C
💨 Oksijen: {self.cevre.oksijen_seviyesi:.1f} mg/L
🍽️ Yiyecek: {self.cevre.yiyecek_miktari:.2f}
🦈 Avcı Yoğunluğu: {self.cevre.avci_yogunlugu:.2f}
🦠 Hastalık Riski: {self.cevre.hastalik_riski:.2f}
🏭 Kirlilik: {self.cevre.kirlilik_seviyesi:.2f}

⚠️ Son Kritik Olaylar:
"""
        
        # Son 3 kritik olayı göster
        for olay in self.kritik_olaylar[-3:]:
            cevre_text += f"• {olay['olay']} (Gün {olay['gun']})\n"
            
        self.cevre_label.config(text=cevre_text)
    
    def calistir(self):
        """Uygulamayı çalıştır"""
        self.root.mainloop()

def main():
    """Ana fonksiyon"""
    print("🌊 Ekolojik Balık Popülasyonu Simülasyonu başlatılıyor...")
    simulasyon = EkolojikBalikSimulasyonu()
    simulasyon.calistir()

if __name__ == "__main__":
    main() 