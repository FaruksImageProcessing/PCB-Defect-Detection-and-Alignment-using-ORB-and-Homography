import cv2
import numpy as np
import os

# Gerekli yollar
reference_image_path = "./PCB_DATASET/Reference/01.jpg"
test_images_base_path = "./PCB_DATASET/rotation/"
output_path = "./PCB_DATASET/Results/"

# Çıkış klasörü oluştur
if not os.path.exists(output_path):
    os.makedirs(output_path)

# Referans görüntüsü kontrolü
reference_image = cv2.imread(reference_image_path, cv2.IMREAD_GRAYSCALE)
if reference_image is None:
    print("Referans görüntü bulunamadı. Programdan çıkılıyor.")
    exit()

# Test görüntülerini işle
for folder in os.listdir(test_images_base_path):
    folder_path = os.path.join(test_images_base_path, folder)

    if os.path.isdir(folder_path):
        # Her görüntü için işlemleri yap
        for image_name in os.listdir(folder_path):
            image_path = os.path.join(folder_path, image_name)
            test_image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

            if test_image is None:
                print(f"Görüntü yüklenemedi: {image_path}")
                continue

            # Görüntü çakıştırma (İmage Registration) ORB ile
            orb = cv2.ORB_create()
            kp1, des1 = orb.detectAndCompute(reference_image, None)
            kp2, des2 = orb.detectAndCompute(test_image, None)

            if des1 is None or des2 is None:
                print(f"Özellik bulunamadı: {image_name}")
                continue

            # Özellik eşleme
            bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
            matches = bf.match(des1, des2)
            matches = sorted(matches, key=lambda x: x.distance)

            if len(matches) < 4:
                print(f"Yeterli eşleşme yok: {image_name}")
                continue

            # Homografi hesaplama
            src_pts = np.float32([kp1[m.queryIdx].pt for m in matches[:10]]).reshape(-1, 1, 2)
            dst_pts = np.float32([kp2[m.trainIdx].pt for m in matches[:10]]).reshape(-1, 1, 2)

            try:
                M, mask = cv2.findHomography(dst_pts, src_pts, cv2.RANSAC, 5.0)
            except:
                print(f"Homografi bulunamadı: {image_name}")
                continue

            if M is None:
                print(f"Homografi başarısız: {image_name}")
                continue

            # Görüntüyü hizalama
            h, w = reference_image.shape
            aligned_test_image = cv2.warpPerspective(test_image, M, (w, h))

            # Fark hesaplama
            diff = cv2.absdiff(reference_image, aligned_test_image)
            _, thresh = cv2.threshold(diff, 50, 255, cv2.THRESH_BINARY)

            # Kusur tespiti
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # Kusurları çiz
            result_image = cv2.cvtColor(reference_image, cv2.COLOR_GRAY2BGR)
            for cnt in contours:
                if cv2.contourArea(cnt) > 50: 
                    x, y, w, h = cv2.boundingRect(cnt)
                    cv2.rectangle(result_image, (x, y), (x + w, y + h), (0, 0, 255), 2)

            # Sonuçları kaydet
            save_folder = os.path.join(output_path, folder)
            if not os.path.exists(save_folder):
                os.makedirs(save_folder)

            result_path = os.path.join(save_folder, f"result_{image_name}")
            cv2.imwrite(result_path, result_image)
            print(f"Kaydedildi: {result_path}")

print("Tüm dosyalar Results klasörüne kaydedildi.")