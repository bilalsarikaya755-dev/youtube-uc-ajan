# YouTube için üç ajanlı üretim paketi

Hazır örnek: **İnternette konuştuğun herkes insan mı?**

İçerik: 4 dakikalık mini belgesel, 60 saniyelik Shorts, kaynak kapsamı,
seslendirmeler, görüntü/ekran yazısı/ses tablosu ve yayın metinleri.

## Hazır senaryoyu kullan

`example/uretim_paketi.md` dosyasını aç. `example/seslendirme.txt` ana videonun,
`example/shorts_seslendirme.txt` Shorts'un okunacak metnidir.
Bu metinler hazırdır; incelemek için API anahtarına ihtiyacın yok.
Paket bir senaryo ve kurgu planıdır. Video, ses kaydı veya lisanslı stok materyal
üretilmiş değildir. Süreler planlıdır; kayıttan sonra kurguya göre ayarlanır.

Konu seçimi, herkesin internet kullanması ve tanıdık bir sese güvenme sorusu üzerine
kurulmuş editoryal değerlendirmedir. Türkiye/kanal için doğrulanmış arama hacmi
veya birinci sıra iddiası yoktur. Kaynaklar 4 Ekim 2026'da kontrol edilmiştir.

## Windows'ta hazır örneği çalıştır

Python 3.12 kurulu olsun. ZIP'i bir klasöre çıkar ve o klasörde PowerShell aç.

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install "pydantic>=2.11,<3"
.\.venv\Scripts\python.exe main.py --demo
```

Aktivasyon komutu gerekmez. Linux/macOS için `python3 -m venv .venv`, ardından
`.venv/bin/python -m pip install "pydantic>=2.11,<3"` ve
`.venv/bin/python main.py --demo` kullan.

Demo kaydedilmiş örneği okur, doğrular ve dosyaları yeniden oluşturur.
**Model çalıştırmaz, araştırma yapmaz ve API ücreti oluşturmaz.**
Yeni konu seçmek için canlı modu kullan.

## GPT -> Claude -> Gemini ile yeni içerik üret

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
```

`.env` dosyasındaki üç anahtarı kendi bilgisayarında doldur. Model kimlikleri
değiştirilebilir; hesabında erişilebilir olmalı. Anahtarları sohbetlere veya ZIP'e
ekleme. Bu projede gerçek anahtar bulunmaz.

```powershell
.\.venv\Scripts\python.exe main.py --live
```

Başka konu:

```powershell
.\.venv\Scripts\python.exe main.py --live --topic "İnternet 24 saat kesilirse ne olur?"
```

Canlı mod üç sağlayıcıya ücretli API çağrıları yapar. Araştırmacı OpenAI Responses
API'nin web aramasını kullanır; ayrıca bir arama hizmeti anahtarı gerekmez.
API kullanımı ve web araması sağlayıcı tarifesine göre ücretlenebilir.
Model erişimi, bakiye ve kota koşulları sağlayıcı hesabına bağlıdır.

## Akış nasıl çalışır?

1. **Araştırmacı / OpenAI:** Birincil kaynakları arar; tarih, ölçüm dönemi,
   kapsam ve belirsizliklerle birlikte yapılandırılmış araştırma üretir.
2. **Senarist / Anthropic:** Araştırma görevini `context` olarak alır. Yalnız
   bu olgularla seslendirmeleri, bölüm sürelerini ve yayın metinlerini yazar.
3. **Yönetmen / Gemini:** Araştırma ve senaryoyu alır; her bölüme görüntü ve ses
   planı ekler. Seslendirmeyi yeniden yazmaz.

`Process.sequential` kullanılır. Hiyerarşik yönetici yoktur; üç görev sırayla
çalışır. Crew nesnesi tek başına kalıcı bir kara tahta değildir. Her tamamlanan
görevin callback'i `blackboard.json` dosyasını atomik olarak günceller.
Kaynak, senaryo ve yönetmen çıktıları böylece aynı çalışma dosyasında birleşir.

`expected_output` yalnız bir talimattır. Bu projede ayrıca Pydantic şemaları,
kaynak/olgu kimliği kontrolü, süre toplamı ve çekim eşleşmesi kontrolü vardır.
Kurgu tablosunun zamanları ve Markdown biçimi Python tarafından oluşturulur;
modelin tablo biçimini tutturmasına bağlı değildir. Başarısız kontrol en fazla
iki düzeltme denemesinden sonra akışı durdurur.

Kontroller biçimi ve ilişkileri denetler; bir kaynağın anlattığı olgunun gerçekten
doğru olduğunu otomatik olarak kanıtlamaz. Yayından önce kaynakları ve iddiaların
kapsamını gözden geçir. Güncel talep verisi yoksa araştırma bunu açıkça belirtir.

## Çıktılar

Her çalıştırma `output/TARIH-SAAT-KIMLIK/` içinde yeni bir klasör açar:

| Dosya | İçerik |
|---|---|
| `uretim_paketi.md` | Senaryo, kaynaklar, kurgu tablosu ve yayın metinleri |
| `seslendirme.txt` | Ana videonun düz seslendirme metni |
| `shorts_seslendirme.txt` | Shorts'un düz seslendirme metni |
| `blackboard.json` | Üç aşamanın birleşik durumu |
| `research.json` | Olgular ve kaynak kapsamları |
| `script.json` | Senaryo bölümleri |
| `direction.json` | Görüntü ve ses planı |
| `crew_log.json` | Canlı çalıştırmanın ilerleme kaydı |

Canlı çalıştırma yarıda kalırsa biten aşamalar dosyada kalır. Otomatik devam
özelliği bu şablonda yoktur; yeni çalıştırma yeni klasör açar.

## Kontrol ve test sınırı

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Teslim edilen sürümde hazır örnek, kaynak ilişkileri, süre hataları, eksik/çift
çekim planları ve dosya üretimi yerel olarak kontrol edilmiştir.
**Gerçek OpenAI, Anthropic veya Gemini API çağrıları bu hazırlama oturumunda
çalıştırılmamıştır.** Canlı mod resmi CrewAI belgelerine göre hazırlanmış bir
şablondur; sağlayıcı hesaplarınla entegrasyon kontrolü gerekir.

## Başvurulan teknik belgeler

- CrewAI LLM ve yerel sağlayıcı entegrasyonları:
  https://docs.crewai.com/en/concepts/llms
- Görev bağlamları, çıktı şemaları, callback ve guardrail:
  https://docs.crewai.com/en/concepts/tasks
- Crew ve ardışık süreç:
  https://docs.crewai.com/en/concepts/crews
- OpenAI model kataloğu: https://developers.openai.com/api/docs/models
- Anthropic model kataloğu: https://platform.claude.com/docs/en/models/overview
- Gemini model kataloğu: https://ai.google.dev/gemini-api/docs/models

Kod LangChain sarmalayıcılarına ihtiyaç duymaz; güncel CrewAI `LLM` sınıfıyla
sağlayıcıların yerel SDK entegrasyonlarını kullanır.

## Açık kaynak başlangıcı

Bu paket MIT lisansıyla hazırlanmıştır; koşullar için `LICENSE` dosyasını oku.
Katkı verme adımları `CONTRIBUTING.md`, doğrulanmış test ve entegrasyon durumu
`PROJECT_STATUS.md`, değişiklikler ise `CHANGELOG.md` içindedir.

Ücretsiz demo ve mevcut 8 test 5 Ekim 2026'da yeniden çalıştırıldı.
Canlı sağlayıcı entegrasyonu hâlâ denenmeyi bekliyor. Kamuya açık depo ve
kullanıcı topluluğu henüz oluşmadı.

### English summary

An early-stage Python workflow for Turkish video production: evidence research,
script writing, and shot planning. A saved, offline demo requires no API key.
Pydantic contracts check source references, narration timing, and shot coverage.
The existing eight tests pass. Live provider integrations have not yet been
verified. This project produces scripts and production plans, not finished videos.
See `LICENSE` for the MIT license and `CONTRIBUTING.md` for contribution steps.
