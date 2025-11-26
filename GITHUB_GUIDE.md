# GitHub Kullanım Kılavuzu

Bu proje artık GitHub üzerinde barındırılıyor: [https://github.com/UtBird/Turkey_Earthquake_Project](https://github.com/UtBird/Turkey_Earthquake_Project)

İleride bu işlemleri kendiniz yapmak isterseniz, aşağıdaki adımları takip edebilirsiniz.

## 1. Değişiklikleri Kaydetme ve Yükleme (Günlük Kullanım)

Kodlarınızda değişiklik yaptıktan sonra bunları GitHub'a yüklemek için terminalde şu 3 komutu sırasıyla çalıştırın:

```bash
# 1. Tüm değişiklikleri "sahneye" (stage) ekle
git add .

# 2. Değişiklikleri bir mesajla kaydet (commit)
# Tırnak içindeki mesajı yaptığınız değişikliğe göre güncelleyin
git commit -m "Yeni özellikler eklendi"

# 3. Değişiklikleri GitHub'a gönder (push)
git push
```

## 2. Sıfırdan Yeni Bir Proje Yükleme (İlk Kurulum)

Eğer gelecekte **yepyeni** bir proje klasörünü GitHub'a yüklemek isterseniz:

1.  GitHub web sitesinde yeni bir **boş** repository oluşturun.
2.  Proje klasörünüzün içinde terminali açın.
3.  Şu komutları sırasıyla girin:

```bash
# Git'i başlat
git init

# (Opsiyonel) Gereksiz dosyaları engellemek için .gitignore dosyası oluşturun

# Tüm dosyaları ekle
git add .

# İlk kaydı oluştur
git commit -m "İlk yükleme"

# Ana dal ismini 'main' olarak ayarla (bazen 'master' olur, 'main' güncel standarttır)
git branch -M main

# Uzak sunucu adresini ekle (URL'yi kendi reponuzla değiştirin)
git remote add origin https://github.com/KULLANICI_ADI/REPO_ADI.git

# Yükle
git push -u origin main
```

## 3. Sık Karşılaşılan Sorunlar

*   **"Authentication failed"**: Şifre yerine "Personal Access Token" kullanmanız gerekebilir veya `gh` (GitHub CLI) aracını kurarak daha kolay giriş yapabilirsiniz.
*   **"Updates were rejected"**: Başkası (veya siz başka bilgisayardan) repoya bir şey yüklediyse, önce `git pull` yaparak güncellemeleri almanız gerekir.
