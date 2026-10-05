# Doğrulanmış proje durumu

Kontrol tarihi: 5 Ekim 2026.

## Çalışan bölüm

Python kodu, kaydedilmiş örneği okuyup Pydantic şemalarıyla doğruluyor; ana video
ve Shorts seslendirme metinlerini, kaynak ilişkilerini ve çekim planı tablolarını
dosyaya yazıyor. Demo API anahtarı gerektirmiyor ve ücretli çağrı yapmıyor.

## Bu kontrolde çalıştırılan testler

Komut: `python3 -m unittest discover -s tests -v`

Sonuç: 8 test, 8 başarılı.

Testler tam üretim paketi, tanımsız kaynak, tanımsız olgu, yanlış süre,
eksik çekim, çift çekim, Markdown tablo hücresi ve boşluk içeren klasörde
demo dosyası üretimini kapsıyor.

## Henüz doğrulanmayan bölüm

- OpenAI, Anthropic ve Gemini ile canlı üretim akışı.
- Bağımsız bir kullanıcının temiz Windows kurulumunda çalıştırması.
- Kamuya açık GitHub deposu, sürümler ve dış katkılar.
- Dış kullanıcı sayısı, indirmeler ve bakım geçmişi.

Bu alanlar için ölçüm veya başarı iddiası yoktur. GitHub'da yayımlanmadan ve
düzenli bakım başlamadan proje için kurulmuş bir topluluk veya geniş kullanım
iddia edilmemelidir.

## Lisans

Bu başlangıç paketi MIT lisansıyla hazırlanmıştır. Lisans dosyası yazılımın
kullanımı, değiştirilmesi ve dağıtılması için izin koşullarını içerir.
Bağımlılıkların kendi lisansları geçerlidir.

