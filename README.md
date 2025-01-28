# PCB Defect Detection and Alignment using ORB and Homography

## Giriş
Bu projede bir printed circuit board (PCB) kontrol sistemi geliştirilmiştir. Amaç, belirli bir referans görüntü kullanarak test görüntülerindeki hataları tespit etmektir. Hatalı bölgeler işaretlenecek ve sonuçlar kaydedilecektir.

## Teknolojiler
- Python
- OpenCV
- NumPy

## Kullanılan Yöntemler

### 1. Görüntü Çakıştırma
Projede, görüntüleri hizalamak için **ORB (Oriented FAST and Rotated BRIEF)** özelliği kullanılmıştır. Bu algoritma, görüntüler arasındaki anahtar noktaları ve açıklayıcıları belirler.

#### Adımlar:
- **Özellik Algılama**: ORB algoritması kullanılarak, görüntüdeki önemli anahtar noktalar ve açıklayıcılar bulunur.
- **Özellik Eşleme**: Brute-force eşleyici (BFMatcher) ile açıklayıcılar karşılaştırılır ve en iyi eşleşmeler seçilir.
- **Eşleşme Kontrolü**: Eğer eşleşme sayısı belirli bir eşiğin altındaysa işlem atlanır.

### 2. Homografi Hesaplama
Referans ve test görüntüleri arasındaki dönüşümü sağlamak için homografi matrisi hesaplanır. Bu işlem için **RANSAC** (Random Sample Consensus) yöntemi kullanılır.

#### Adımlar:
- **Noktaların Seçimi**: İyi eşleşmiş olan 10 özellik noktası seçilir.
- **Homografi Matrisi Hesaplama**: `cv2.findHomography` fonksiyonu kullanılarak, iki görüntü arasındaki dönüşüm matrisi hesaplanır.

### 3. Görüntü Hizalama
Hesaplanan homografi matrisi ile test görüntüsü, referans görüntüsüyle hizalanır. Bu işlem, ölçekleme, döndürme ve kaydırma gibi geometrik dönüşümleri içerir.

### 4. Fark Hesaplama ve Kusur Tespiti
Referans görüntüsü ile hizalanan test görüntüsü arasındaki farklar hesaplanır. Bu farklar, kusurları tespit etmek için kullanılır.

#### Adımlar:
- **Piksel Bazında Fark Hesaplama**: `cv2.absdiff` fonksiyonu ile iki görüntü arasındaki fark hesaplanır.
- **Eşikleme**: Küçük farklılıklar yok edilir ve büyük farklar kusur olarak kabul edilir.
- **Kontur Analizi**: Kusurların büyüklüğü ölçülür ve yalnızca büyük kusurlar dikkate alınır.

## Kurulum
Bu projeyi çalıştırabilmek için aşağıdaki adımları takip edebilirsiniz:

### Gereksinimler
- Python 3.x
- OpenCV
- NumPy

### Adımlar
1. Depoyu klonlayın:
   ```bash
   git clone https://github.com/FaruksImageProcessing/PCB-Defect-Detection-and-Alignment-using-ORB-and-Homography.git
