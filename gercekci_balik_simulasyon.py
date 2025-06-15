import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk, messagebox
import random
import math
from dataclasses import dataclass
from typing import List, Dict, Tuple
import json
from datetime import datetime

@dataclass
class CevreselFaktorler:
    """Çevresel faktörlerin popülasyon üzerindeki etkisi"""
    sicaklik_ortalama: float = 15.0  # °C
    sicaklik_varyasyon: float = 8.0   # Mevsimsel değişim
    besin_bolluğu: float = 1.0        # 0.2-2.0 arası
    ph_seviyesi: float = 7.0          # Su pH'ı
    kirlilik_seviyesi: float = 0.1    # 0.0-1.0 arası
    yirtici_yogunlugu: float = 0.3    # 0.0-1.0 arası

class BalikPopulasyonu:
    """Balık popülasyonunu ve genetik yapısını modelleyen sınıf"""
    
    def __init__(self, baslangic_boyutu: int = 1000):
        # Genetik yapı: K (kırmızı dominant), B (beyaz resesif)
        self.baslangic_boyutu = baslangic_boyutu
        self.reset_populasyon()
        
        # Çevresel faktörler
        self.cevre = CevreselFaktorler()
        
        # Zaman takibi
        self.yil = 0
        self.mevsim = 0  # 0: İlkbahar, 1: Yaz, 2: Sonbahar, 3: Kış
        
        # Veri toplama
        self.tarihce = {
            'yillar': [],
            'toplam_populasyon': [],
            'k_allel_frekansi': [],
            'b_allel_frekansi': [],
            'kk_genotip': [],
            'kb_genotip': [],
            'bb_genotip': [],
            'cevre_sicaklik': [],
            'cevre_besin': [],
            'cevre_kirlilik': [],
            'olaylar': []
        }
        
    def reset_populasyon(self):
        """Popülasyonu sıfırla ve Hardy-Weinberg dengesinde başlat"""
        # Başlangıçta p(K) = 0.6, q(B) = 0.4 (doğal seçilim avantajı simüle etmek için)
        p = 0.6  # K allel frekansı
        q = 0.4  # B allel frekansı
        
        # Hardy-Weinberg dengesi: KK = p², KB = 2pq, BB = q²
        kk_sayi = int(self.baslangic_boyutu * p * p)
        kb_sayi = int(self.baslangic_boyutu * 2 * p * q)
        bb_sayi = self.baslangic_boyutu - kk_sayi - kb_sayi
        
        self.populasyon = {
            'KK': kk_sayi,
            'KB': kb_sayi, 
            'BB': bb_sayi
        }
        
    def mevsimsel_etki_hesapla(self):
        """Mevsime göre çevresel faktörleri güncelle"""
        # Sıcaklık değişimi (sinüzoidal)
        mevsim_radyan = (self.mevsim / 4.0) * 2 * math.pi
        sicaklik_degisimi = self.cevre.sicaklik_varyasyon * math.cos(mevsim_radyan)
        mevcut_sicaklik = self.cevre.sicaklik_ortalama + sicaklik_degisimi
        
        # Besin bolluğu mevsimsel değişim
        if self.mevsim == 0:  # İlkbahar - besin artışı
            besin_carpani = 1.3
        elif self.mevsim == 1:  # Yaz - optimal koşullar
            besin_carpani = 1.5
        elif self.mevsim == 2:  # Sonbahar - azalma başlangıcı
            besin_carpani = 0.9
        else:  # Kış - zorlu koşullar
            besin_carpani = 0.5
            
        self.cevre.besin_bolluğu = max(0.2, min(2.0, 
            self.cevre.besin_bolluğu * 0.9 + besin_carpani * 0.1))
        
        # Rastgele çevresel değişimler
        self.cevre.kirlilik_seviyesi += random.uniform(-0.02, 0.02)
        self.cevre.kirlilik_seviyesi = max(0.0, min(1.0, self.cevre.kirlilik_seviyesi))
        
        return mevcut_sicaklik
    
    def catastrofik_olay_kontrol(self):
        """Nadir ama etkili olayları simüle et"""
        olay_listesi = []
        
        # Hastalık salgını (% 3 şans)
        if random.random() < 0.03:
            olum_orani = random.uniform(0.3, 0.7)
            self.populasyon_azalt(olum_orani)
            olay_listesi.append(f"Hastalık Salgını - %{olum_orani*100:.1f} kayıp")
            
        # Yırtıcı istilası (% 2 şans)
        if random.random() < 0.02:
            yirtici_olum = random.uniform(0.2, 0.5)
            # Renkli balıklar daha çok hedef alınır (kamuflaj eksikliği)
            kk_kayip = int(self.populasyon['KK'] * yirtici_olum * 1.3)
            kb_kayip = int(self.populasyon['KB'] * yirtici_olum * 1.1)
            bb_kayip = int(self.populasyon['BB'] * yirtici_olum * 0.8)
            
            self.populasyon['KK'] = max(0, self.populasyon['KK'] - kk_kayip)
            self.populasyon['KB'] = max(0, self.populasyon['KB'] - kb_kayip)
            self.populasyon['BB'] = max(0, self.populasyon['BB'] - bb_kayip)
            
            olay_listesi.append(f"Yırtıcı İstilası - Renkli balıklar daha çok etkilendi")
            
        # İklim değişikliği olayı (% 1 şans)
        if random.random() < 0.01:
            self.cevre.sicaklik_ortalama += random.uniform(-2, 3)
            self.cevre.kirlilik_seviyesi += random.uniform(0.05, 0.15)
            olay_listesi.append("İklim Değişikliği - Sıcaklık ve kirlilik artışı")
            
        # Habitat bozulması (% 1.5 şans)
        if random.random() < 0.015:
            habitat_kaybi = random.uniform(0.1, 0.3)
            self.populasyon_azalt(habitat_kaybi)
            self.cevre.besin_bolluğu *= (1 - habitat_kaybi)
            olay_listesi.append(f"Habitat Bozulması - %{habitat_kaybi*100:.1f} habitat kaybı")
            
        return olay_listesi
    
    def populasyon_azalt(self, oran: float):
        """Belirtilen oranda popülasyonu azalt"""
        for genotip in self.populasyon:
            kayip = int(self.populasyon[genotip] * oran)
            self.populasyon[genotip] = max(0, self.populasyon[genotip] - kayip)
    
    def fitness_hesapla(self, genotip: str, sicaklik: float) -> float:
        """Genotipe ve çevresel koşullara göre fitness hesapla"""
        base_fitness = 1.0
        
        # Sıcaklık etkisi - her genotip farklı tepki verir
        if genotip == 'KK':
            # Kırmızı balıklar soğuk suyu daha iyi tolere eder
            if sicaklik < 10:
                base_fitness *= 1.2
            elif sicaklik > 25:
                base_fitness *= 0.8
        elif genotip == 'BB':
            # Beyaz balıklar sıcak suyu daha iyi tolere eder
            if sicaklik > 20:
                base_fitness *= 1.1
            elif sicaklik < 5:
                base_fitness *= 0.7
        else:  # KB - heterozygot avantajı
            base_fitness *= 1.05
            
        # Besin bolluğu etkisi
        base_fitness *= (0.5 + 0.5 * self.cevre.besin_bolluğu)
        
        # Kirlilik etkisi
        base_fitness *= (1.0 - 0.3 * self.cevre.kirlilik_seviyesi)
        
        # pH etkisi
        optimal_ph = 7.0
        ph_fark = abs(self.cevre.ph_seviyesi - optimal_ph)
        base_fitness *= max(0.5, 1.0 - ph_fark * 0.1)
        
        return max(0.1, base_fitness)
    
    def ureme_ve_sekillenme(self, sicaklik: float):
        """Üreme, seçilim ve genetik sürüklenme"""
        toplam_populasyon = sum(self.populasyon.values())
        
        if toplam_populasyon < 10:  # Kritik popülasyon seviyesi
            return
            
        # Fitness değerlerini hesapla
        fitness_kk = self.fitness_hesapla('KK', sicaklik)
        fitness_kb = self.fitness_hesapla('KB', sicaklik)
        fitness_bb = self.fitness_hesapla('BB', sicaklik)
        
        # Seçilim baskısı uygula
        self.populasyon['KK'] = int(self.populasyon['KK'] * fitness_kk)
        self.populasyon['KB'] = int(self.populasyon['KB'] * fitness_kb)
        self.populasyon['BB'] = int(self.populasyon['BB'] * fitness_bb)
        
        # Üreme (çiftleşme mevsimi - ilkbahar ve yaz)
        if self.mevsim in [0, 1]:
            ureme_carpani = 1.8 if self.mevsim == 0 else 1.4
            
            # Mevcut allel frekanslarını hesapla
            toplam = sum(self.populasyon.values())
            if toplam > 0:
                k_allel_freq = (2*self.populasyon['KK'] + self.populasyon['KB']) / (2*toplam)
                b_allel_freq = 1 - k_allel_freq
                
                # Yeni nesil Hardy-Weinberg dağılımına göre
                yeni_toplam = int(toplam * ureme_carpani)
                
                # Rastgele çiftleşme
                self.populasyon['KK'] = int(yeni_toplam * k_allel_freq * k_allel_freq)
                self.populasyon['KB'] = int(yeni_toplam * 2 * k_allel_freq * b_allel_freq)
                self.populasyon['BB'] = yeni_toplam - self.populasyon['KK'] - self.populasyon['KB']
                
        # Mutasyon (düşük oran)
        self.mutasyon_uygula()
        
        # Genetik sürüklenme (küçük popülasyonlarda daha güçlü)
        if toplam_populasyon < 500:
            self.genetik_suruklenme_uygula()
    
    def mutasyon_uygula(self):
        """Düşük oranlı mutasyon uygula"""
        mutasyon_orani = 0.001  # %0.1
        
        for genotip in list(self.populasyon.keys()):
            mutasyon_sayisi = int(self.populasyon[genotip] * mutasyon_orani)
            
            if mutasyon_sayisi > 0:
                self.populasyon[genotip] -= mutasyon_sayisi
                
                # Rastgele diğer genotiplere dağıt
                for _ in range(mutasyon_sayisi):
                    hedef_genotipler = [g for g in self.populasyon.keys() if g != genotip]
                    hedef = random.choice(hedef_genotipler)
                    self.populasyon[hedef] += 1
    
    def genetik_suruklenme_uygula(self):
        """Küçük popülasyonlarda genetik sürüklenme"""
        toplam = sum(self.populasyon.values())
        
        if toplam < 100:
            # Güçlü sürüklenme
            suruklenme_gucu = 0.1
        elif toplam < 300:
            # Orta sürüklenme  
            suruklenme_gucu = 0.05
        else:
            return
            
        for genotip in self.populasyon:
            degisim = int(self.populasyon[genotip] * suruklenme_gucu * random.uniform(-1, 1))
            self.populasyon[genotip] = max(0, self.populasyon[genotip] + degisim)
    
    def bir_mevsim_simule_et(self):
        """Bir mevsimi simüle et ve verileri kaydet"""
        # Çevresel faktörleri güncelle
        sicaklik = self.mevsimsel_etki_hesapla()
        
        # Katastrofik olayları kontrol et
        olaylar = self.catastrofik_olay_kontrol()
        
        # Popülasyon dinamiklerini uygula
        self.ureme_ve_sekillenme(sicaklik)
        
        # Mevsimi ilerlet
        self.mevsim = (self.mevsim + 1) % 4
        if self.mevsim == 0:  # Yıl tamamlandı
            self.yil += 1
            self.veri_kaydet(sicaklik, olaylar)
    
    def veri_kaydet(self, sicaklik: float, olaylar: List[str]):
        """Yıllık verileri kaydet"""
        toplam = sum(self.populasyon.values())
        
        if toplam > 0:
            k_freq = (2*self.populasyon['KK'] + self.populasyon['KB']) / (2*toplam)
            b_freq = 1 - k_freq
            kk_freq = self.populasyon['KK'] / toplam
            kb_freq = self.populasyon['KB'] / toplam
            bb_freq = self.populasyon['BB'] / toplam
        else:
            k_freq = b_freq = kk_freq = kb_freq = bb_freq = 0
            
        self.tarihce['yillar'].append(self.yil)
        self.tarihce['toplam_populasyon'].append(toplam)
        self.tarihce['k_allel_frekansi'].append(k_freq)
        self.tarihce['b_allel_frekansi'].append(b_freq)
        self.tarihce['kk_genotip'].append(kk_freq)
        self.tarihce['kb_genotip'].append(kb_freq)
        self.tarihce['bb_genotip'].append(bb_freq)
        self.tarihce['cevre_sicaklik'].append(sicaklik)
        self.tarihce['cevre_besin'].append(self.cevre.besin_bolluğu)
        self.tarihce['cevre_kirlilik'].append(self.cevre.kirlilik_seviyesi)
        self.tarihce['olaylar'].append(olaylar)

class PopulasyonGenetigiArayuz:
    """Ana arayüz ve görselleştirme sınıfı"""
    
    def __init__(self):
        self.populasyon = BalikPopulasyonu()
        self.arayuz_olustur()
        
    def arayuz_olustur(self):
        """Tkinter arayüzünü oluştur"""
        self.root = tk.Tk()
        self.root.title("🐠 Gerçekçi Balık Popülasyon Genetiği Simülasyonu")
        self.root.geometry("1600x1000")
        self.root.configure(bg='#f0f8ff')
        
        # Ana başlık
        baslik_frame = tk.Frame(self.root, bg='#f0f8ff')
        baslik_frame.pack(fill=tk.X, pady=10)
        
        baslik = tk.Label(baslik_frame, 
                         text="🌊 Balık Popülasyon Genetiği: 200 Yıllık Evrimsel Değişim 🌊",
                         font=("Arial", 18, "bold"), bg='#f0f8ff', fg='#2c3e50')
        baslik.pack()
        
        alt_baslik = tk.Label(baslik_frame,
                             text="Mevsimsel Değişimler • Çevresel Felaketler • İklim Etkisi • Doğal Seçilim",
                             font=("Arial", 12), bg='#f0f8ff', fg='#7f8c8d')
        alt_baslik.pack()
        
        # Kontrol paneli
        kontrol_frame = tk.Frame(self.root, bg='#ecf0f1')
        kontrol_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Parametreler
        param_frame = tk.LabelFrame(kontrol_frame, text="Başlangıç Parametreleri", 
                                   font=("Arial", 12, "bold"), bg='#ecf0f1')
        param_frame.pack(side=tk.LEFT, padx=10, pady=5)
        
        tk.Label(param_frame, text="Başlangıç Popülasyonu:", bg='#ecf0f1').pack(anchor='w')
        self.pop_var = tk.IntVar(value=1000)
        tk.Spinbox(param_frame, from_=500, to=5000, textvariable=self.pop_var, width=10).pack(anchor='w')
        
        tk.Label(param_frame, text="Simülasyon Süresi (Yıl):", bg='#ecf0f1').pack(anchor='w')
        self.yil_var = tk.IntVar(value=200)
        tk.Spinbox(param_frame, from_=50, to=500, textvariable=self.yil_var, width=10).pack(anchor='w')
        
        # Butonlar
        buton_frame = tk.Frame(kontrol_frame, bg='#ecf0f1')
        buton_frame.pack(side=tk.RIGHT, padx=10, pady=5)
        
        tk.Button(buton_frame, text="🚀 Simülasyonu Başlat", command=self.simulasyonu_calistir,
                 bg='#27ae60', fg='white', font=("Arial", 12, "bold"), pady=5).pack(pady=2)
        
        tk.Button(buton_frame, text="🔄 Yeni Simülasyon", command=self.yeni_simulasyon,
                 bg='#3498db', fg='white', font=("Arial", 12, "bold"), pady=5).pack(pady=2)
        
        tk.Button(buton_frame, text="💾 Veriyi Kaydet", command=self.veriyi_kaydet,
                 bg='#9b59b6', fg='white', font=("Arial", 12, "bold"), pady=5).pack(pady=2)
        
        # Progress bar
        self.progress = ttk.Progressbar(self.root, mode='determinate')
        self.progress.pack(fill=tk.X, padx=10, pady=5)
        
        # Ana grafik alanı
        self.grafik_frame = tk.Frame(self.root, bg='white')
        self.grafik_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.grafikleri_olustur()
        
    def grafikleri_olustur(self):
        """Grafik panellerini oluştur"""
        # 2x3 grafik düzeni
        self.fig, axes = plt.subplots(2, 3, figsize=(16, 10))
        self.fig.patch.set_facecolor('#f8f9fa')
        
        self.ax_allel, self.ax_genotip, self.ax_populasyon = axes[0]
        self.ax_cevre, self.ax_olaylar, self.ax_denge = axes[1]
        
        # Canvas
        self.canvas = FigureCanvasTkAgg(self.fig, self.grafik_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        plt.tight_layout()
        self.bos_grafikleri_goster()
        
    def bos_grafikleri_goster(self):
        """Başlangıç için boş grafikler"""
        for ax in [self.ax_allel, self.ax_genotip, self.ax_populasyon, 
                   self.ax_cevre, self.ax_olaylar, self.ax_denge]:
            ax.clear()
            ax.text(0.5, 0.5, 'Simülasyon bekleniyor...', 
                   ha='center', va='center', transform=ax.transAxes, fontsize=12)
            
        self.canvas.draw()
        
    def simulasyonu_calistir(self):
        """Ana simülasyon döngüsü"""
        # Yeni popülasyon oluştur
        self.populasyon = BalikPopulasyonu(self.pop_var.get())
        hedef_yil = self.yil_var.get()
        
        self.progress['maximum'] = hedef_yil
        self.progress['value'] = 0
        
        # Simülasyonu çalıştır
        while self.populasyon.yil < hedef_yil:
            # 4 mevsimi simüle et (1 yıl)
            for _ in range(4):
                self.populasyon.bir_mevsim_simule_et()
                
            # Progress bar güncelle
            self.progress['value'] = self.populasyon.yil
            self.root.update_idletasks()
            
            # Popülasyon çok azaldıysa dur
            if sum(self.populasyon.populasyon.values()) < 5:
                messagebox.showwarning("Uyarı", f"Popülasyon {self.populasyon.yil}. yılda kritik seviyeye düştü!")
                break
                
        # Sonuçları görselleştir
        self.sonuclari_gorsellestir()
        self.progress['value'] = hedef_yil
        
    def sonuclari_gorsellestir(self):
        """Simülasyon sonuçlarını görselleştir"""
        if not self.populasyon.tarihce['yillar']:
            return
            
        # Grafikleri temizle
        for ax in [self.ax_allel, self.ax_genotip, self.ax_populasyon, 
                   self.ax_cevre, self.ax_olaylar, self.ax_denge]:
            ax.clear()
            
        yillar = self.populasyon.tarihce['yillar']
        
        # 1. Allel Frekansları (ANA GRAFİK)
        self.ax_allel.plot(yillar, self.populasyon.tarihce['k_allel_frekansi'], 
                          'r-', linewidth=3, label='K (Kırmızı) Alleli', alpha=0.8)
        self.ax_allel.plot(yillar, self.populasyon.tarihce['b_allel_frekansi'], 
                          'lightgray', linewidth=3, label='B (Beyaz) Alleli', alpha=0.8)
        self.ax_allel.set_title('🧬 Allel Frekans Değişimi (200 Yıl)', fontsize=14, fontweight='bold')
        self.ax_allel.set_xlabel('Yıl')
        self.ax_allel.set_ylabel('Allel Frekansı')
        self.ax_allel.legend()
        self.ax_allel.grid(True, alpha=0.3)
        self.ax_allel.set_ylim(0, 1)
        
        # 2. Genotip Dağılımı
        self.ax_genotip.fill_between(yillar, 0, self.populasyon.tarihce['kk_genotip'], 
                                    color='darkred', alpha=0.7, label='KK (Kırmızı)')
        self.ax_genotip.fill_between(yillar, self.populasyon.tarihce['kk_genotip'], 
                                    np.array(self.populasyon.tarihce['kk_genotip']) + np.array(self.populasyon.tarihce['kb_genotip']),
                                    color='orange', alpha=0.7, label='KB (Karma)')
        self.ax_genotip.fill_between(yillar, 
                                    np.array(self.populasyon.tarihce['kk_genotip']) + np.array(self.populasyon.tarihce['kb_genotip']),
                                    1, color='lightgray', alpha=0.7, label='BB (Beyaz)')
        self.ax_genotip.set_title('📊 Genotip Dağılım Değişimi', fontsize=14, fontweight='bold')
        self.ax_genotip.set_xlabel('Yıl')
        self.ax_genotip.set_ylabel('Genotip Frekansı')
        self.ax_genotip.legend()
        self.ax_genotip.grid(True, alpha=0.3)
        
        # 3. Popülasyon Boyutu
        self.ax_populasyon.plot(yillar, self.populasyon.tarihce['toplam_populasyon'], 
                               'b-', linewidth=2, alpha=0.8)
        self.ax_populasyon.fill_between(yillar, 0, self.populasyon.tarihce['toplam_populasyon'], 
                                       alpha=0.3, color='lightblue')
        self.ax_populasyon.set_title('🐠 Toplam Popülasyon Değişimi', fontsize=14, fontweight='bold')
        self.ax_populasyon.set_xlabel('Yıl')
        self.ax_populasyon.set_ylabel('Birey Sayısı')
        self.ax_populasyon.grid(True, alpha=0.3)
        
        # 4. Çevresel Faktörler
        ax2 = self.ax_cevre.twinx()
        self.ax_cevre.plot(yillar, self.populasyon.tarihce['cevre_sicaklik'], 
                          'orange', linewidth=2, label='Sıcaklık (°C)', alpha=0.8)
        ax2.plot(yillar, self.populasyon.tarihce['cevre_besin'], 
                'green', linewidth=2, label='Besin Bolluğu', alpha=0.8)
        ax2.plot(yillar, self.populasyon.tarihce['cevre_kirlilik'], 
                'brown', linewidth=2, label='Kirlilik Seviyesi', alpha=0.8)
        
        self.ax_cevre.set_title('🌡️ Çevresel Faktör Değişimleri', fontsize=14, fontweight='bold')
        self.ax_cevre.set_xlabel('Yıl')
        self.ax_cevre.set_ylabel('Sıcaklık (°C)', color='orange')
        ax2.set_ylabel('Besin/Kirlilik Seviyesi', color='green')
        self.ax_cevre.grid(True, alpha=0.3)
        
        # Efsaneler
        lines1, labels1 = self.ax_cevre.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        self.ax_cevre.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
        
        # 5. Önemli Olaylar
        olay_yillari = []
        olay_tipleri = []
        for i, olay_listesi in enumerate(self.populasyon.tarihce['olaylar']):
            if olay_listesi:
                olay_yillari.append(yillar[i])
                olay_tipleri.append(len(olay_listesi))
                
        if olay_yillari:
            self.ax_olaylar.scatter(olay_yillari, olay_tipleri, 
                                   c='red', s=100, alpha=0.7, marker='X')
            
        # Tüm olayları listele
        tum_olaylar = {}
        for olay_listesi in self.populasyon.tarihce['olaylar']:
            for olay in olay_listesi:
                olay_tipi = olay.split(' - ')[0] if ' - ' in olay else olay
                tum_olaylar[olay_tipi] = tum_olaylar.get(olay_tipi, 0) + 1
                
        if tum_olaylar:
            olay_isimleri = list(tum_olaylar.keys())
            olay_sayilari = list(tum_olaylar.values())
            colors = plt.cm.Set3(np.linspace(0, 1, len(olay_isimleri)))
            
            self.ax_olaylar.bar(range(len(olay_isimleri)), olay_sayilari, color=colors, alpha=0.8)
            self.ax_olaylar.set_xticks(range(len(olay_isimleri)))
            self.ax_olaylar.set_xticklabels(olay_isimleri, rotation=45, ha='right')
            
        self.ax_olaylar.set_title('⚡ Catastrofik Olaylar', fontsize=14, fontweight='bold')
        self.ax_olaylar.set_ylabel('Olay Sayısı')
        self.ax_olaylar.grid(True, alpha=0.3)
        
        # 6. Hardy-Weinberg Dengesi Analizi
        hardy_weinberg_sapma = []
        for i in range(len(yillar)):
            p = self.populasyon.tarihce['k_allel_frekansi'][i]
            q = self.populasyon.tarihce['b_allel_frekansi'][i]
            
            # Beklenen Hardy-Weinberg frekansları
            beklenen_kk = p * p
            beklenen_kb = 2 * p * q
            beklenen_bb = q * q
            
            # Gözlenen frekanslar
            gozlenen_kk = self.populasyon.tarihce['kk_genotip'][i]
            gozlenen_kb = self.populasyon.tarihce['kb_genotip'][i] 
            gozlenen_bb = self.populasyon.tarihce['bb_genotip'][i]
            
            # Sapma hesabı (Chi-kare testi mantığı)
            sapma = abs(gozlenen_kk - beklenen_kk) + abs(gozlenen_kb - beklenen_kb) + abs(gozlenen_bb - beklenen_bb)
            hardy_weinberg_sapma.append(sapma)
            
        self.ax_denge.plot(yillar, hardy_weinberg_sapma, 'purple', linewidth=2, alpha=0.8)
        self.ax_denge.fill_between(yillar, 0, hardy_weinberg_sapma, alpha=0.3, color='purple')
        self.ax_denge.set_title('⚖️ Hardy-Weinberg Dengesi Sapması', fontsize=14, fontweight='bold')
        self.ax_denge.set_xlabel('Yıl')
        self.ax_denge.set_ylabel('Sapma Derecesi')
        self.ax_denge.grid(True, alpha=0.3)
        
        plt.tight_layout()
        self.canvas.draw()
        
        # Özet istatistikler göster
        self.ozet_istatistikler_goster()
        
    def ozet_istatistikler_goster(self):
        """Simülasyon özet istatistiklerini göster"""
        if not self.populasyon.tarihce['yillar']:
            return
            
        baslangic_k = self.populasyon.tarihce['k_allel_frekansi'][0]
        son_k = self.populasyon.tarihce['k_allel_frekansi'][-1]
        
        baslangic_pop = self.populasyon.tarihce['toplam_populasyon'][0]
        son_pop = self.populasyon.tarihce['toplam_populasyon'][-1]
        
        toplam_olay = sum(len(olaylar) for olaylar in self.populasyon.tarihce['olaylar'])
        
        ozet = f"""
🔬 SİMÜLASYON ÖZETİ ({self.populasyon.yil} Yıl)

📊 ALLEL FREKANS DEĞİŞİMİ:
   • K (Kırmızı) Alleli: {baslangic_k:.3f} → {son_k:.3f} ({'↗️' if son_k > baslangic_k else '↘️'} {abs(son_k-baslangic_k):.3f})
   • B (Beyaz) Alleli: {1-baslangic_k:.3f} → {1-son_k:.3f}

🐠 POPÜLASYON DEĞİŞİMİ:
   • Başlangıç: {baslangic_pop:,} birey
   • Son durum: {son_pop:,} birey
   • Değişim: %{((son_pop-baslangic_pop)/baslangic_pop)*100:+.1f}

⚡ ÇEVRESEL OLAYLAR:
   • Toplam catastrofik olay: {toplam_olay}
   • Ortalama sıklık: {toplam_olay/self.populasyon.yil:.2f} olay/yıl

🌡️ ÇEVRESEL KOŞULLAR:
   • Ortalama sıcaklık: {np.mean(self.populasyon.tarihce['cevre_sicaklik']):.1f}°C
   • Ortalama besin bolluğu: {np.mean(self.populasyon.tarihce['cevre_besin']):.2f}
   • Ortalama kirlilik: {np.mean(self.populasyon.tarihce['cevre_kirlilik']):.2f}
        """
        
        messagebox.showinfo("Simülasyon Tamamlandı", ozet)
        
    def yeni_simulasyon(self):
        """Yeni simülasyon için sıfırla"""
        self.populasyon = BalikPopulasyonu(self.pop_var.get())
        self.progress['value'] = 0
        self.bos_grafikleri_goster()
        
    def veriyi_kaydet(self):
        """Simülasyon verilerini kaydet"""
        if not self.populasyon.tarihce['yillar']:
            messagebox.showwarning("Uyarı", "Henüz simülasyon çalıştırılmadı!")
            return
            
        zaman_damgasi = datetime.now().strftime("%Y%m%d_%H%M%S")
        dosya_adi = f"balik_populasyon_genetigi_{zaman_damgasi}.json"
        
        kayit_verisi = {
            'simulasyon_parametreleri': {
                'baslangic_populasyonu': self.pop_var.get(),
                'simulasyon_suresi': self.yil_var.get(),
                'tamamlanan_yil': self.populasyon.yil
            },
            'sonuclar': self.populasyon.tarihce,
            'ozet_istatistikler': {
                'baslangic_k_allel': self.populasyon.tarihce['k_allel_frekansi'][0] if self.populasyon.tarihce['k_allel_frekansi'] else 0,
                'son_k_allel': self.populasyon.tarihce['k_allel_frekansi'][-1] if self.populasyon.tarihce['k_allel_frekansi'] else 0,
                'baslangic_populasyon': self.populasyon.tarihce['toplam_populasyon'][0] if self.populasyon.tarihce['toplam_populasyon'] else 0,
                'son_populasyon': self.populasyon.tarihce['toplam_populasyon'][-1] if self.populasyon.tarihce['toplam_populasyon'] else 0,
                'toplam_catastrofik_olay': sum(len(olaylar) for olaylar in self.populasyon.tarihce['olaylar'])
            }
        }
        
        try:
            with open(dosya_adi, 'w', encoding='utf-8') as f:
                json.dump(kayit_verisi, f, indent=2, ensure_ascii=False)
            messagebox.showinfo("Başarılı", f"Veriler {dosya_adi} dosyasına kaydedildi.")
        except Exception as e:
            messagebox.showerror("Hata", f"Veri kaydetme hatası: {e}")
            
    def calistir(self):
        """Uygulamayı başlat"""
        self.root.mainloop()

def main():
    """Ana fonksiyon"""
    print("🌊 Gerçekçi Balık Popülasyon Genetiği Simülasyonu başlatılıyor...")
    uygulama = PopulasyonGenetigiArayuz()
    uygulama.calistir()

if __name__ == "__main__":
    main() 