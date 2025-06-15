import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk, messagebox
import random
import math
from dataclasses import dataclass
from typing import List
import json
from datetime import datetime

@dataclass
class CevreselFaktorler:
    """Çevresel faktörlerin popülasyon üzerindeki etkisi"""
    sicaklik_ortalama: float = 15.0
    sicaklik_varyasyon: float = 8.0
    besin_bolluğu: float = 1.0
    ph_seviyesi: float = 7.0
    kirlilik_seviyesi: float = 0.1
    yirtici_yogunlugu: float = 0.3

class OptimizeBalikPopulasyonu:
    """Spyder için optimize edilmiş balık popülasyonu"""
    
    def __init__(self, baslangic_boyutu: int = 1000):
        self.baslangic_boyutu = baslangic_boyutu
        self.reset_populasyon()
        self.cevre = CevreselFaktorler()
        self.yil = 0
        self.mevsim = 0
        
        # Veri saklama
        self.tarihce = {
            'yillar': [], 'toplam_populasyon': [], 'k_allel_frekansi': [],
            'b_allel_frekansi': [], 'kk_genotip': [], 'kb_genotip': [],
            'bb_genotip': [], 'cevre_sicaklik': [], 'cevre_besin': [],
            'cevre_kirlilik': [], 'olaylar': []
        }
        
    def reset_populasyon(self):
        """Popülasyonu Hardy-Weinberg dengesinde başlat"""
        p, q = 0.6, 0.4
        kk_sayi = int(self.baslangic_boyutu * p * p)
        kb_sayi = int(self.baslangic_boyutu * 2 * p * q)
        bb_sayi = self.baslangic_boyutu - kk_sayi - kb_sayi
        self.populasyon = {'KK': kk_sayi, 'KB': kb_sayi, 'BB': bb_sayi}
        
    def mevsimsel_etki_hesapla(self):
        """Mevsimsel faktörleri güncelle"""
        mevsim_radyan = (self.mevsim / 4.0) * 2 * math.pi
        sicaklik_degisimi = self.cevre.sicaklik_varyasyon * math.cos(mevsim_radyan)
        mevcut_sicaklik = self.cevre.sicaklik_ortalama + sicaklik_degisimi
        
        besin_multipliers = [1.3, 1.5, 0.9, 0.5]
        besin_carpani = besin_multipliers[self.mevsim]
        
        self.cevre.besin_bolluğu = max(0.2, min(2.0, 
            self.cevre.besin_bolluğu * 0.9 + besin_carpani * 0.1))
        
        self.cevre.kirlilik_seviyesi += random.uniform(-0.01, 0.01)
        self.cevre.kirlilik_seviyesi = max(0.0, min(1.0, self.cevre.kirlilik_seviyesi))
        
        return mevcut_sicaklik
    
    def catastrofik_olay_kontrol(self):
        """Catastrofik olayları kontrol et"""
        olay_listesi = []
        
        if random.random() < 0.02:  # Hastalık
            olum_orani = random.uniform(0.2, 0.5)
            self.populasyon_azalt(olum_orani)
            olay_listesi.append(f"Hastalık Salgını - %{olum_orani*100:.1f} kayıp")
            
        if random.random() < 0.015:  # Yırtıcı
            yirtici_olum = random.uniform(0.15, 0.35)
            kk_kayip = int(self.populasyon['KK'] * yirtici_olum * 1.2)
            kb_kayip = int(self.populasyon['KB'] * yirtici_olum * 1.0)
            bb_kayip = int(self.populasyon['BB'] * yirtici_olum * 0.8)
            
            self.populasyon['KK'] = max(0, self.populasyon['KK'] - kk_kayip)
            self.populasyon['KB'] = max(0, self.populasyon['KB'] - kb_kayip)
            self.populasyon['BB'] = max(0, self.populasyon['BB'] - bb_kayip)
            olay_listesi.append("Yırtıcı İstilası")
            
        if random.random() < 0.008:  # İklim değişikliği
            self.cevre.sicaklik_ortalama += random.uniform(-1, 2)
            self.cevre.kirlilik_seviyesi += random.uniform(0.02, 0.08)
            olay_listesi.append("İklim Değişikliği")
            
        return olay_listesi
    
    def populasyon_azalt(self, oran: float):
        """Popülasyonu belirtilen oranda azalt"""
        for genotip in self.populasyon:
            kayip = int(self.populasyon[genotip] * oran)
            self.populasyon[genotip] = max(0, self.populasyon[genotip] - kayip)
    
    def fitness_hesapla(self, genotip: str, sicaklik: float) -> float:
        """Fitness değerini hesapla"""
        base_fitness = 1.0
        
        if genotip == 'KK' and sicaklik < 10:
            base_fitness *= 1.1
        elif genotip == 'BB' and sicaklik > 20:
            base_fitness *= 1.1
        elif genotip == 'KB':
            base_fitness *= 1.05
            
        base_fitness *= (0.6 + 0.4 * self.cevre.besin_bolluğu)
        base_fitness *= (1.0 - 0.2 * self.cevre.kirlilik_seviyesi)
        
        return max(0.2, base_fitness)
    
    def ureme_ve_sekillenme(self, sicaklik: float):
        """Üreme ve seçilim süreçleri"""
        toplam = sum(self.populasyon.values())
        if toplam < 10:
            return
            
        # Fitness uygula
        for genotip in self.populasyon:
            fitness = self.fitness_hesapla(genotip, sicaklik)
            self.populasyon[genotip] = int(self.populasyon[genotip] * fitness)
        
        # Üreme mevsimi
        if self.mevsim in [0, 1]:
            toplam = sum(self.populasyon.values())
            ureme_carpani = 1.6 if self.mevsim == 0 else 1.3
            
            if toplam > 0:
                k_allel_freq = (2*self.populasyon['KK'] + self.populasyon['KB']) / (2*toplam)
                b_allel_freq = 1 - k_allel_freq
                
                yeni_toplam = int(toplam * ureme_carpani)
                yeni_toplam = max(50, min(yeni_toplam, self.baslangic_boyutu * 1.5))
                
                self.populasyon['KK'] = int(yeni_toplam * k_allel_freq * k_allel_freq)
                self.populasyon['KB'] = int(yeni_toplam * 2 * k_allel_freq * b_allel_freq)
                self.populasyon['BB'] = yeni_toplam - self.populasyon['KK'] - self.populasyon['KB']
        
        # Mutasyon
        if random.random() < 0.05:
            self.basit_mutasyon()
    
    def basit_mutasyon(self):
        """Basit mutasyon işlemi"""
        toplam = sum(self.populasyon.values())
        if toplam < 100:
            return
            
        degisim = max(1, int(toplam * 0.005))
        
        if random.random() < 0.5:
            if self.populasyon['KK'] > degisim:
                self.populasyon['KK'] -= degisim
                self.populasyon['KB'] += degisim
        else:
            if self.populasyon['BB'] > degisim:
                self.populasyon['BB'] -= degisim
                self.populasyon['KB'] += degisim
    
    def bir_yil_simule_et(self):
        """Bir yılı (4 mevsim) simüle et"""
        yil_olaylari = []
        
        for mevsim in range(4):
            self.mevsim = mevsim
            sicaklik = self.mevsimsel_etki_hesapla()
            olaylar = self.catastrofik_olay_kontrol()
            yil_olaylari.extend(olaylar)
            self.ureme_ve_sekillenme(sicaklik)
        
        self.yil += 1
        self.veri_kaydet(sicaklik, yil_olaylari)
        
        return sum(self.populasyon.values()) > 0
    
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

class SpyderBalikArayuz:
    """Spyder IDE için optimize edilmiş arayüz"""
    
    def __init__(self):
        self.populasyon = None
        self.arayuz_olustur()
        
    def arayuz_olustur(self):
        """Ana arayüz"""
        self.root = tk.Tk()
        self.root.title("🐠 Spyder Balık Popülasyon Genetiği")
        self.root.geometry("1500x900")
        self.root.configure(bg='#f0f8ff')
        
        # Başlık
        baslik_frame = tk.Frame(self.root, bg='#f0f8ff')
        baslik_frame.pack(fill=tk.X, pady=8)
        
        baslik = tk.Label(baslik_frame, 
                         text="🌊 Gerçekçi Balık Popülasyon Genetiği - Spyder Versiyonu 🌊",
                         font=("Arial", 16, "bold"), bg='#f0f8ff', fg='#2c3e50')
        baslik.pack()
        
        alt_baslik = tk.Label(baslik_frame,
                             text="Mevsimsel Döngüler • Çevresel Felaketler • Doğal Seçilim • Hardy-Weinberg",
                             font=("Arial", 11), bg='#f0f8ff', fg='#7f8c8d')
        alt_baslik.pack()
        
        # Kontrol paneli
        kontrol_frame = tk.Frame(self.root, bg='#ecf0f1')
        kontrol_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Parametreler
        param_frame = tk.LabelFrame(kontrol_frame, text="Simülasyon Parametreleri", 
                                   font=("Arial", 11, "bold"), bg='#ecf0f1')
        param_frame.pack(side=tk.LEFT, padx=8, pady=5)
        
        tk.Label(param_frame, text="Başlangıç Popülasyonu:", bg='#ecf0f1').pack(anchor='w')
        self.pop_var = tk.IntVar(value=1000)
        tk.Spinbox(param_frame, from_=500, to=3000, textvariable=self.pop_var, width=10).pack(anchor='w', pady=2)
        
        tk.Label(param_frame, text="Simülasyon Süresi (Yıl):", bg='#ecf0f1').pack(anchor='w')
        self.yil_var = tk.IntVar(value=150)
        tk.Spinbox(param_frame, from_=50, to=300, textvariable=self.yil_var, width=10).pack(anchor='w', pady=2)
        
        # Butonlar
        buton_frame = tk.Frame(kontrol_frame, bg='#ecf0f1')
        buton_frame.pack(side=tk.RIGHT, padx=8, pady=5)
        
        tk.Button(buton_frame, text="🚀 Simülasyonu Başlat", command=self.simulasyonu_calistir,
                 bg='#27ae60', fg='white', font=("Arial", 11, "bold")).pack(pady=2)
        
        tk.Button(buton_frame, text="🔄 Yeni Simülasyon", command=self.yeni_simulasyon,
                 bg='#3498db', fg='white', font=("Arial", 11, "bold")).pack(pady=2)
        
        tk.Button(buton_frame, text="💾 Veriyi Kaydet", command=self.veriyi_kaydet,
                 bg='#9b59b6', fg='white', font=("Arial", 11, "bold")).pack(pady=2)
        
        # Progress
        progress_frame = tk.Frame(self.root, bg='#f0f8ff')
        progress_frame.pack(fill=tk.X, padx=10, pady=3)
        
        self.progress = ttk.Progressbar(progress_frame, mode='determinate')
        self.progress.pack(fill=tk.X, pady=2)
        
        self.status_label = tk.Label(progress_frame, text="Simülasyon bekleniyor...", 
                                   bg='#f0f8ff', font=("Arial", 9))
        self.status_label.pack()
        
        # Grafik alanı
        self.grafik_frame = tk.Frame(self.root, bg='white')
        self.grafik_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.grafikleri_olustur()
        
    def grafikleri_olustur(self):
        """6 panel grafik sistemi"""
        self.fig, axes = plt.subplots(2, 3, figsize=(15, 8))
        self.fig.patch.set_facecolor('#f8f9fa')
        
        self.ax_allel, self.ax_genotip, self.ax_populasyon = axes[0]
        self.ax_cevre, self.ax_olaylar, self.ax_denge = axes[1]
        
        self.canvas = FigureCanvasTkAgg(self.fig, self.grafik_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        plt.tight_layout()
        self.bos_grafikleri_goster()
        
    def bos_grafikleri_goster(self):
        """Başlangıç grafikler"""
        for ax in [self.ax_allel, self.ax_genotip, self.ax_populasyon, 
                   self.ax_cevre, self.ax_olaylar, self.ax_denge]:
            ax.clear()
            ax.text(0.5, 0.5, 'Simülasyon bekleniyor...', 
                   ha='center', va='center', transform=ax.transAxes, fontsize=11)
            
        self.canvas.draw()
        
    def simulasyonu_calistir(self):
        """Ana simülasyon - Threading yok"""
        try:
            self.populasyon = OptimizeBalikPopulasyonu(self.pop_var.get())
            hedef_yil = self.yil_var.get()
            
            self.progress['maximum'] = hedef_yil
            self.progress['value'] = 0
            self.status_label.config(text="Simülasyon başlatılıyor...")
            
            # Simülasyonu direkt çalıştır
            for yil in range(hedef_yil):
                if yil % 10 == 0:  # Her 10 yılda güncelle
                    self.progress['value'] = yil
                    self.status_label.config(text=f"Yıl {yil}/{hedef_yil}")
                    self.root.update_idletasks()
                
                devam = self.populasyon.bir_yil_simule_et()
                if not devam:
                    self.status_label.config(text=f"Popülasyon {yil}. yılda yok oldu!")
                    break
                    
            self.progress['value'] = hedef_yil
            self.status_label.config(text="Grafikleri oluşturuluyor...")
            self.root.update_idletasks()
            
            self.sonuclari_gorsellestir()
            
        except Exception as e:
            messagebox.showerror("Hata", f"Simülasyon hatası: {e}")
            self.status_label.config(text="Hata oluştu!")
        
    def sonuclari_gorsellestir(self):
        """Sonuçları görselleştir"""
        if not self.populasyon or not self.populasyon.tarihce['yillar']:
            return
            
        for ax in [self.ax_allel, self.ax_genotip, self.ax_populasyon, 
                   self.ax_cevre, self.ax_olaylar, self.ax_denge]:
            ax.clear()
            
        yillar = self.populasyon.tarihce['yillar']
        
        # 1. Allel Frekansları
        self.ax_allel.plot(yillar, self.populasyon.tarihce['k_allel_frekansi'], 
                          'r-', linewidth=3, label='K (Kırmızı)', alpha=0.8)
        self.ax_allel.plot(yillar, self.populasyon.tarihce['b_allel_frekansi'], 
                          'gray', linewidth=3, label='B (Beyaz)', alpha=0.8)
        self.ax_allel.set_title('🧬 Allel Frekans Değişimi', fontsize=12, fontweight='bold')
        self.ax_allel.set_xlabel('Yıl')
        self.ax_allel.set_ylabel('Allel Frekansı')
        self.ax_allel.legend()
        self.ax_allel.grid(True, alpha=0.3)
        self.ax_allel.set_ylim(0, 1)
        
        # 2. Genotip Dağılımı
        self.ax_genotip.fill_between(yillar, 0, self.populasyon.tarihce['kk_genotip'], 
                                    color='darkred', alpha=0.7, label='KK')
        kk_kb = np.array(self.populasyon.tarihce['kk_genotip']) + np.array(self.populasyon.tarihce['kb_genotip'])
        self.ax_genotip.fill_between(yillar, self.populasyon.tarihce['kk_genotip'], kk_kb,
                                    color='orange', alpha=0.7, label='KB')
        self.ax_genotip.fill_between(yillar, kk_kb, 1, color='lightgray', alpha=0.7, label='BB')
        self.ax_genotip.set_title('📊 Genotip Dağılımı', fontsize=12, fontweight='bold')
        self.ax_genotip.set_xlabel('Yıl')
        self.ax_genotip.set_ylabel('Genotip Frekansı')
        self.ax_genotip.legend()
        self.ax_genotip.grid(True, alpha=0.3)
        
        # 3. Popülasyon Boyutu
        self.ax_populasyon.plot(yillar, self.populasyon.tarihce['toplam_populasyon'], 'b-', linewidth=2)
        self.ax_populasyon.fill_between(yillar, 0, self.populasyon.tarihce['toplam_populasyon'], alpha=0.3, color='lightblue')
        self.ax_populasyon.set_title('🐠 Toplam Popülasyon', fontsize=12, fontweight='bold')
        self.ax_populasyon.set_xlabel('Yıl')
        self.ax_populasyon.set_ylabel('Birey Sayısı')
        self.ax_populasyon.grid(True, alpha=0.3)
        
        # 4. Çevresel Faktörler
        ax2 = self.ax_cevre.twinx()
        self.ax_cevre.plot(yillar, self.populasyon.tarihce['cevre_sicaklik'], 'orange', linewidth=2, label='Sıcaklık')
        ax2.plot(yillar, self.populasyon.tarihce['cevre_besin'], 'green', linewidth=2, label='Besin')
        ax2.plot(yillar, self.populasyon.tarihce['cevre_kirlilik'], 'brown', linewidth=2, label='Kirlilik')
        
        self.ax_cevre.set_title('🌡️ Çevresel Faktörler', fontsize=12, fontweight='bold')
        self.ax_cevre.set_xlabel('Yıl')
        self.ax_cevre.set_ylabel('Sıcaklık (°C)', color='orange')
        ax2.set_ylabel('Besin/Kirlilik', color='green')
        self.ax_cevre.grid(True, alpha=0.3)
        
        lines1, labels1 = self.ax_cevre.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        self.ax_cevre.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
        
        # 5. Catastrofik Olaylar
        tum_olaylar = {}
        for olay_listesi in self.populasyon.tarihce['olaylar']:
            for olay in olay_listesi:
                if olay:
                    olay_tipi = olay.split(' ')[0]
                    tum_olaylar[olay_tipi] = tum_olaylar.get(olay_tipi, 0) + 1
                    
        if tum_olaylar:
            olay_isimleri = list(tum_olaylar.keys())
            olay_sayilari = list(tum_olaylar.values())
            colors = ['red', 'orange', 'purple'][:len(olay_isimleri)]
            
            bars = self.ax_olaylar.bar(range(len(olay_isimleri)), olay_sayilari, color=colors, alpha=0.8)
            self.ax_olaylar.set_xticks(range(len(olay_isimleri)))
            self.ax_olaylar.set_xticklabels(olay_isimleri, rotation=45, ha='right')
            
            for bar, sayi in zip(bars, olay_sayilari):
                self.ax_olaylar.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                                   str(sayi), ha='center', va='bottom', fontweight='bold')
            
        self.ax_olaylar.set_title('⚡ Catastrofik Olaylar', fontsize=12, fontweight='bold')
        self.ax_olaylar.set_ylabel('Olay Sayısı')
        self.ax_olaylar.grid(True, alpha=0.3)
        
        # 6. Hardy-Weinberg Sapması
        hardy_weinberg_sapma = []
        for i in range(len(yillar)):
            p = self.populasyon.tarihce['k_allel_frekansi'][i]
            q = self.populasyon.tarihce['b_allel_frekansi'][i]
            
            beklenen_kk = p * p
            beklenen_kb = 2 * p * q
            beklenen_bb = q * q
            
            gozlenen_kk = self.populasyon.tarihce['kk_genotip'][i]
            gozlenen_kb = self.populasyon.tarihce['kb_genotip'][i] 
            gozlenen_bb = self.populasyon.tarihce['bb_genotip'][i]
            
            sapma = (abs(gozlenen_kk - beklenen_kk) + 
                    abs(gozlenen_kb - beklenen_kb) + 
                    abs(gozlenen_bb - beklenen_bb))
            hardy_weinberg_sapma.append(sapma)
            
        self.ax_denge.plot(yillar, hardy_weinberg_sapma, 'purple', linewidth=2, alpha=0.8)
        self.ax_denge.fill_between(yillar, 0, hardy_weinberg_sapma, alpha=0.3, color='purple')
        self.ax_denge.set_title('⚖️ Hardy-Weinberg Sapması', fontsize=12, fontweight='bold')
        self.ax_denge.set_xlabel('Yıl')
        self.ax_denge.set_ylabel('Sapma Derecesi')
        self.ax_denge.grid(True, alpha=0.3)
        
        plt.tight_layout()
        self.canvas.draw()
        
        self.ozet_istatistikler_goster()
        self.status_label.config(text="✅ Simülasyon başarıyla tamamlandı!")
        
    def ozet_istatistikler_goster(self):
        """Özet istatistikler"""
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
   • K (Kırmızı): {baslangic_k:.3f} → {son_k:.3f}
   • Değişim: {'↗️' if son_k > baslangic_k else '↘️'} {abs(son_k-baslangic_k):.3f}

🐠 POPÜLASYON:
   • Başlangıç: {baslangic_pop:,} birey
   • Son durum: {son_pop:,} birey
   • Değişim: %{((son_pop-baslangic_pop)/baslangic_pop)*100:+.1f}

⚡ OLAYLAR:
   • Toplam catastrofik olay: {toplam_olay}

🏆 Spyder'da başarıyla çalıştı!
        """
        
        messagebox.showinfo("Simülasyon Sonuçları", ozet)
        
    def yeni_simulasyon(self):
        """Yeni simülasyon"""
        self.populasyon = None
        self.progress['value'] = 0
        self.status_label.config(text="Yeni simülasyon hazır...")
        self.bos_grafikleri_goster()
        
    def veriyi_kaydet(self):
        """Veriyi kaydet"""
        if not self.populasyon or not self.populasyon.tarihce['yillar']:
            messagebox.showwarning("Uyarı", "Önce simülasyon çalıştırın!")
            return
            
        dosya_adi = f"spyder_balik_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        veri = {
            'parametreler': {
                'baslangic_populasyonu': self.pop_var.get(),
                'simulasyon_suresi': self.yil_var.get(),
                'tamamlanan_yil': self.populasyon.yil
            },
            'sonuclar': self.populasyon.tarihce
        }
        
        try:
            with open(dosya_adi, 'w', encoding='utf-8') as f:
                json.dump(veri, f, indent=2, ensure_ascii=False)
            messagebox.showinfo("Başarılı", f"Veriler {dosya_adi} dosyasına kaydedildi.")
        except Exception as e:
            messagebox.showerror("Hata", f"Kaydetme hatası: {e}")
            
    def calistir(self):
        """Uygulamayı başlat"""
        self.root.mainloop()

def main():
    """Ana fonksiyon"""
    print("🌊 Spyder Balık Popülasyon Genetiği Simülasyonu")
    print("✅ Spyder IDE için optimize edilmiş versiyon")
    print("⚡ Threading yok - direkt simülasyon")
    print("🎯 Tüm özellikler mevcut")
    
    uygulama = SpyderBalikArayuz()
    uygulama.calistir()

if __name__ == "__main__":
    main() 