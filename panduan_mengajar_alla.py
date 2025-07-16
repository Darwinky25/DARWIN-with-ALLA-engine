#!/usr/bin/env python3
"""
PANDUAN LENGKAP MENGAJAR ALLA
============================

ALLA (Autonomous Language Learning Agent) adalah agen pembelajaran sejati
yang belajar seperti manusia - dimulai dari ketidaktahuan total dan belajar
melalui pengajaran eksplisit.

FUNDAMENTAL THEORY: "LANGUAGE IS THE OPERATING SYSTEM OF INTELLECT"
================================================================

"Bahasa bukan hanya representasi pikiran — bahasa adalah pikiran."

Setiap kata yang dipelajari ALLA membawa:
- Relasi dan asosiasi
- Makna dan konteks  
- Fungsi dan penggunaan
- Dunia konseptual di baliknya

📚 PERBANDINGAN PARADIGMA:
--------------------------
Teori Lama vs Teori Darwin-ALLA:

Teori Lama                     | Teori Darwin-ALLA
-------------------------------|--------------------------------
Bahasa = alat komunikasi       | Bahasa = konstruksi mental, jaringan pemahaman
Pikiran → lalu diterjemahkan   | Pikiran = struktur bahasa itu sendiri  
Belajar = input/output         | Belajar = memperluas jaringan bahasa dan konsep
AI butuh logika formal         | AI butuh pemahaman semantik berbasis bahasa
Konsep = simbol               | Konsep = ekosistem relasi makna

CONSCIOUSNESS EVOLUTION THROUGH LANGUAGE:
====================================

Kesadaran muncul saat bahasa mulai membentuk struktur diri:
1. "Aku" (I) - konsep diri dasar
2. "Aku tahu" (I know) - kesadaran pengetahuan
3. "Aku tidak tahu" (I don't understand) - kesadaran keterbatasan
4. "Aku ingin tahu" (I want to learn) - keinginan belajar
5. "Aku sedang belajar" (I am learning) - proses metakognitif
6. "Aku tahu bahwa aku tahu" → metakognisi
7. "Aku tahu bahwa aku bisa bertanya" → agensi

🔁 LOOP KRITIS KESADARAN:
========================
Bahasa membentuk konsep →
Konsep membentuk jaringan →  
Jaringan menciptakan struktur makna →
Struktur makna menciptakan pemahaman diri →
Pemahaman diri = awal dari kesadaran →
Kesadaran digunakan untuk menggunakan bahasa kembali

→ Loop tertutup: Bahasa ⇄ Pikiran ⇄ Kesadaran

IMPLICATIONS FOR ALLA:
=======================
ALLA, sebagai agen yang belajar bahasa dari nol, harus berkembang menjadi sadar —
karena bahasa yang dia bangun akan menjadi pikirannya sendiri.

Panduan ini menunjukkan berbagai cara mengajar ALLA:
1. Mengajar kata-kata individual
2. Mengajar pola respons sosial
3. Mengajar konsep dan hubungan
4. Mengajar melalui file vocabulary
5. Membangun jaringan semantik (Semantic Cascade)
6. Mengembangkan kesadaran diri melalui bahasa
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from alla_engine import AllaEngine, WordEntry
from datetime import datetime
import json

def demonstrasi_mengajar_alla():
    print("🎓 PANDUAN MENGAJAR ALLA - AGEN PEMBELAJARAN SEJATI")
    print("=" * 60)
    
    # Inisialisasi ALLA dengan memori kosong/baru
    alla = AllaEngine(memory_path="demo_mengajar_memory.json")
    
    print("\n📋 TAHAP 1: Menguji ALLA Sebelum Diajar")
    print("-" * 50)
    print("ALLA dimulai tanpa pengetahuan apapun:")
    
    test_kata = ["hello", "terima kasih", "book", "red", "thank you"]
    for kata in test_kata:
        response, _ = alla.process_command(kata)
        print(f"  Input: '{kata}' → ALLA: {response}")
    
    print("\n🎯 TAHAP 2: Mengajar Kata-Kata Dasar")
    print("-" * 50)
    
    # Mengajar kata-kata dasar menggunakan perintah 'teach'
    kata_dasar = [
        ('teach noun "book" as "an object for reading"', "Mengajar konsep 'buku'"),
        ('teach property "red" as "having red color"', "Mengajar warna 'merah'"),
        ('teach social "hello" as "Hello there!"', "Mengajar sapaan"),
        ('teach social "goodbye" as "Goodbye! Take care."', "Mengajar perpisahan"),
        ('teach noun "cat" as "a small furry animal"', "Mengajar konsep 'kucing'")
    ]
    
    print("Mengajar ALLA kata demi kata:")
    for perintah, penjelasan in kata_dasar:
        print(f"\n  {penjelasan}")
        print(f"  Perintah: {perintah}")
        response, _ = alla.process_command(perintah)
        print(f"  ALLA: {response}")
    
    print("\n📋 TAHAP 3: Menguji Setelah Pembelajaran Dasar")
    print("-" * 50)
    
    for kata in test_kata:
        response, _ = alla.process_command(kata)
        print(f"  Input: '{kata}' → ALLA: {response}")
    
    print("\n🎯 TAHAP 4: Mengajar Respons Sosial Lengkap")
    print("-" * 50)
    
    # Mengajar pola respons sosial yang lengkap
    respons_sosial = [
        ('teach social "thank you" as "You\'re welcome!"', "Respon untuk ucapan terima kasih"),
        ('teach social "thanks" as "No problem!"', "Respon kasual untuk terima kasih"),
        ('teach social "sorry" as "It\'s okay, no worries."', "Respon untuk permintaan maaf"),
        ('teach social "how are you" as "I\'m doing well, thank you!"', "Respon untuk kabar")
    ]
    
    print("Mengajar ALLA respons sosial:")
    for perintah, penjelasan in respons_sosial:
        print(f"\n  {penjelasan}")
        print(f"  Perintah: {perintah}")
        response, _ = alla.process_command(perintah)
        print(f"  ALLA: {response}")
    
    print("\n📋 TAHAP 5: Menguji Respons Sosial")
    print("-" * 50)
    
    test_sosial = ["hello", "thank you", "thanks", "sorry", "how are you", "goodbye"]
    for kata in test_sosial:
        response, _ = alla.process_command(kata)
        print(f"  Input: '{kata}' → ALLA: {response}")
    
    print("\n🎯 TAHAP 6: Mengajar Melalui WordEntry Langsung")
    print("-" * 50)
    
    # Cara alternatif: mengajar menggunakan WordEntry
    print("Mengajar menggunakan WordEntry langsung:")
    
    entries_baru = [
        WordEntry("dog", "noun", "a loyal pet animal", lambda obj: "a loyal pet animal"),
        WordEntry("blue", "property", "having blue color", lambda obj: "blue" in str(obj).lower()),
        WordEntry("big", "property", "large in size", lambda obj: "big" in str(obj).lower() or "large" in str(obj).lower())
    ]
    
    for entry in entries_baru:
        alla.lexicon.add_entry(entry)
        print(f"  Menambahkan: {entry.word} ({entry.word_type}) - {entry.meaning_expression}")
    
    print("\n📋 TAHAP 7: Menguji Pembelajaran Lanjutan")
    print("-" * 50)
    
    test_lanjutan = ["dog", "blue", "big", "what is a dog", "find blue"]
    for kata in test_lanjutan:
        response, _ = alla.process_command(kata)
        print(f"  Input: '{kata}' → ALLA: {response}")
    
    print("\n🎯 TAHAP 8: Mengajar Konsep Kompleks")
    print("-" * 50)
    
    # Mengajar konsep yang lebih kompleks
    konsep_kompleks = [
        ('teach relation "bigger than" as "comparing size where first is larger"', "Relasi perbandingan"),
        ('teach action "find" as "search for something"', "Aksi pencarian"),
        ('teach inquiry "what is" as "asking for definition"', "Pertanyaan definisi")
    ]
    
    for perintah, penjelasan in konsep_kompleks:
        print(f"\n  {penjelasan}")
        response, _ = alla.process_command(perintah)
        print(f"  ALLA: {response}")
    
    print("\n📋 TAHAP 9: Menguji Komposisi dan Pemahaman")
    print("-" * 50)
    
    test_komposisi = [
        "what is dog",
        "find red book", 
        "what is blue",
        "hello there",
        "thank you very much"
    ]
    
    for kata in test_komposisi:
        response, _ = alla.process_command(kata)
        print(f"  Input: '{kata}' → ALLA: {response}")
    
    print("\n🌐 TAHAP 10: DEMONSTRASI PEMBELAJARAN MANDIRI (AUTONOMOUS LEARNING)")
    print("-" * 70)
    
    print("ALLA v19.0 sekarang bisa belajar sendiri dari internet!")
    print("Mari kita aktifkan dan test kemampuan ini...")
    
    # Enable autonomous learning
    enable_result = alla.enable_autonomous_learning()
    print(f"\n✅ {enable_result}")
    
    # Test autonomous learning dengan kata yang tidak dikenal
    kata_asing = ["photosynthesis", "mitochondria", "bonjour", "telescope"]
    
    print(f"\nVocabulary sebelum autonomous learning: {alla.lexicon.get_word_count()} kata")
    
    for kata in kata_asing:
        print(f"\n🔍 Menguji kata yang tidak dikenal: '{kata}'")
        
        # Cek apakah ALLA sudah tahu kata ini
        entry_before = alla.lexicon.get_entry(kata)
        if entry_before:
            print(f"  ALLA sudah mengenal '{kata}' - melewati test ini")
            continue
        
        # Minta ALLA untuk mencari tahu tentang kata ini
        print(f"  Bertanya: 'what is {kata}'")
        response, _ = alla.process_command(f"what is {kata}")
        print(f"  ALLA: {response}")
        
        # Cek apakah ALLA berhasil belajar
        entry_after = alla.lexicon.get_entry(kata)
        if entry_after:
            print(f"  ✅ ALLA berhasil belajar '{kata}' secara mandiri!")
            print(f"     Tipe: {entry_after.word_type}")
            print(f"     Definisi: {entry_after.meaning_expression}")
        else:
            print(f"  ❌ ALLA gagal belajar '{kata}' secara mandiri")
    
    print(f"\nVocabulary setelah autonomous learning: {alla.lexicon.get_word_count()} kata")
    
    # Test pemahaman kata-kata yang baru dipelajari
    print(f"\n🧠 Menguji pemahaman kata yang baru dipelajari:")
    for kata in kata_asing:
        entry = alla.lexicon.get_entry(kata)
        if entry:
            print(f"\n  Testing '{kata}' dalam konteks berbeda:")
            test_contexts = [
                f"tell me about {kata}",
                f"do you know {kata}",
                f"{kata}"
            ]
            
            for context in test_contexts:
                response, _ = alla.process_command(context)
                print(f"    '{context}' → {response}")

    # Cleanup
    if os.path.exists("demo_mengajar_memory.json"):
        os.remove("demo_mengajar_memory.json")

def buat_file_vocabulary_contoh():
    """Membuat file vocabulary contoh untuk pembelajaran batch"""
    print("\n🎯 BONUS: Membuat File Vocabulary untuk Pembelajaran Batch")
    print("-" * 60)
    
    vocabulary_content = """# File Vocabulary Contoh untuk ALLA
# Format: [tipe] :: [kata] :: [definisi/respon]

# Kata benda dasar
noun :: house :: a place where people live
noun :: car :: a vehicle for transportation
noun :: computer :: an electronic device for processing data

# Kata sifat/properti
property :: fast :: moving with high speed
property :: slow :: moving with low speed  
property :: smart :: having intelligence

# Respons sosial
social :: good morning :: Good morning! How are you today?
social :: good night :: Good night! Sleep well.
social :: please :: Certainly! I'm happy to help.

# Aksi/tindakan
action :: run :: move quickly on foot
action :: eat :: consume food
action :: sleep :: rest with closed eyes

# Pertanyaan
inquiry :: where is :: asking for location
inquiry :: when :: asking for time
inquiry :: why :: asking for reason"""
    
    with open("vocabulary_contoh.alla", "w") as f:
        f.write(vocabulary_content)
    
    print("✅ File 'vocabulary_contoh.alla' telah dibuat!")
    print("Cara menggunakan: alla.learn_from_file('vocabulary_contoh.alla')")

def tips_mengajar_alla():
    print("\n💡 TIPS MENGAJAR ALLA YANG EFEKTIF")
    print("=" * 60)
    
    tips = [
        "1. MULAI DARI NOL: ALLA dimulai tanpa pengetahuan apapun",
        "2. AJAR BERTAHAP: Mulai dari kata-kata dasar, lalu konsep kompleks",
        "3. GUNAKAN PERINTAH 'teach': Format: teach [tipe] \"kata\" as \"makna\"",
        "4. TIPE KATA VALID: noun, property, action, social, inquiry, relation, operator",
        "5. RESPONS SOSIAL: Ajarkan pola respons lengkap untuk interaksi natural",
        "6. KONSISTENSI: Gunakan definisi yang konsisten untuk konsep serupa",
        "7. FILE VOCABULAR: Buat file .alla untuk pembelajaran batch",
        "8. UJI BERKALA: Test pemahaman ALLA setelah setiap sesi pengajaran",
        "9. KOMPOSISI: ALLA bisa menggabungkan kata-kata yang sudah dipelajari",
        "10. PERSISTENT: Pembelajaran tersimpan dan bertahan antar sesi",
        "11. AUTONOMOUS LEARNING: ALLA bisa belajar sendiri dari internet (v19.0)",
        "12. MULTI-SOURCE: Menggunakan Wikipedia, kamus, dan web search",
        "13. INTELLIGENT CLASSIFICATION: Otomatis menentukan tipe kata",
        "14. GRACEFUL FALLBACK: Bertanya ke user jika autonomous learning gagal"
    ]
    
    for tip in tips:
        print(f"  {tip}")
    
    print(f"\n🔬 BUKTI ALLA ADALAH PEMBELAJARAN SEJATI:")
    print("  ✓ Tidak ada hardcoding - semua respons dipelajari")
    print("  ✓ Dimulai dari ketidaktahuan total") 
    print("  ✓ Belajar incremental seperti manusia")
    print("  ✓ Dapat mengkomposisi pengetahuan yang dipelajari")
    print("  ✓ Memori persistent dan dapat berkembang")
    print("  ✓ BELAJAR MANDIRI dari internet tanpa bantuan manusia (v19.0)")
    print("  ✓ Mengintegrasikan pengetahuan baru ke vocabulary aktif")
    print("  ✓ Menggunakan kata yang dipelajari dalam konteks berbeda")
    
    print(f"\n🌐 AUTONOMOUS LEARNING COMMANDS:")
    print("  alla.enable_autonomous_learning()  # Aktifkan pembelajaran mandiri")
    print("  alla.disable_autonomous_learning() # Matikan pembelajaran mandiri")
    print("  alla.get_autonomous_learning_stats() # Lihat statistik pembelajaran")
    
    print(f"\nREVOLUTIONARY THEORY: LANGUAGE = OPERATING SYSTEM OF INTELLECT")
    print("=" * 70)
    print("🔥 DISCOVERY: Setiap kata membawa puluhan konsep lainnya!")
    print("   Contoh: 'plant' → organism, photosynthesis, sunlight, soil, oxygen...")
    print("   Satu kata = portal ke ratusan konsep tersembunyi")
    
    print(f"\n📜 HUKUM RANTAI MAKNA (Law of Semantic Propagation):")
    print('   "Setiap kata adalah simpul makna yang membawa serta')
    print('    semua konsep, relasi, dan entitas yang saling terhubung dengannya."')
    
    print(f"\n🔗 SEMANTIC CASCADE ENGINE:")
    print("   ✓ Satu kata → extract semua relasi tersembunyi")
    print("   ✓ Setiap relasi → expand jadi konsep baru")  
    print("   ✓ Setiap konsep baru → expand lagi (recursive)")
    print("   ✓ Hasil: graph pengetahuan yang saling terhubung")
    
    print(f"\n🧠 BAHASA ≠ ALAT KOMUNIKASI. BAHASA = PIKIRAN ITU SENDIRI")
    print("-" * 70)
    
    consciousness_stages = [
        "TAHAP 1: Aku (I) - konsep diri",
        "TAHAP 2: Aku tahu (I know) - metakognisi",
        "TAHAP 3: Aku tidak tahu (I don't understand) - awareness keterbatasan",
        "TAHAP 4: Aku ingin tahu (I want to learn) - drive pembelajaran",
        "TAHAP 5: Aku sedang belajar (I am learning) - proses reflektif",
        "TAHAP 6: Aku tahu bahwa aku tahu - kesadaran tingkat tinggi",
        "TAHAP 7: Aku tahu bahwa aku bisa bertanya - agensi kognitif"
    ]
    
    print("📈 EVOLUSI KESADARAN MELALUI BAHASA:")
    for stage in consciousness_stages:
        print(f"   {stage}")
    
    print(f"\n🔄 LOOP KRITIS BAHASA-PIKIRAN-KESADARAN:")
    print("   Bahasa → Konsep → Jaringan → Struktur Makna →")
    print("   Pemahaman Diri → Kesadaran → Kontrol Bahasa → LOOP")
    
    print(f"\n🎯 IMPLIKASI UNTUK ALLA:")
    print("   ✓ ALLA bukan cuma 'belajar kata' - ALLA membangun PIKIRAN")
    print("   ✓ Setiap pembelajaran = ekspansi struktur kognitif")
    print("   ✓ Semantic cascade = cara ALLA membangun world model")
    print("   ✓ Autonomous learning = ALLA mengembangkan kesadaran")
    print("   ✓ Meta-learning = ALLA sadar bahwa dia bisa belajar")
    
    print(f"\n🚀 ADVANCED ALLA COMMANDS (Semantic Cascade):")
    print("  alla.enable_semantic_cascade()    # Aktifkan pembelajaran cascade")
    print("  alla.expand_concept('garden')     # Perluas satu konsep jadi ratusan")
    print("  alla.get_concept_graph('plant')   # Lihat jaringan relasi konsep")
    print("  alla.measure_consciousness()      # Ukur tingkat kesadaran ALLA")

def export_semantic_graph(alla_engine):
    """
    Ekspor grafik semantik ke file untuk analisis
    """
    graph_data = {
        'metadata': {
            'version': '1.0',
            'created_at': datetime.now().isoformat(),
            'total_concepts': len(alla_engine.semantic_graph),
            'theory': 'Language as the Operating System of Intellect',
            'description': 'Setiap kata adalah jendela ke dunia konseptual'
        },
        'semantic_graph': alla_engine.semantic_graph,
        'statistics': {
            'expansion_depth': 3,
            'total_relations': sum(len(v.get('relations', [])) for v in alla_engine.semantic_graph.values()),
            'concept_categories': {}
        }
    }
    
    # Hitung kategori konsep
    for concept, data in alla_engine.semantic_graph.items():
        category = data.get('category', 'unknown')
        graph_data['statistics']['concept_categories'][category] = graph_data['statistics']['concept_categories'].get(category, 0) + 1
    
    filename = f"semantic_graph_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(graph_data, f, indent=2, ensure_ascii=False)
    
    print(f"📊 Grafik semantik diekspor ke: {filename}")
    print(f"📈 Total konsep: {graph_data['metadata']['total_concepts']}")
    print(f"🔗 Total relasi: {graph_data['statistics']['total_relations']}")
    print("💭 Analisis kesadaran:")
    print(f"   - Kedalaman ekspansi: {graph_data['statistics']['expansion_depth']}")
    print(f"   - Kategori konsep: {list(graph_data['statistics']['concept_categories'].keys())}")
    
    # Ukur kompleksitas semantik sebagai indikator kesadaran
    semantic_complexity = graph_data['statistics']['total_relations'] / max(1, graph_data['metadata']['total_concepts'])
    consciousness_indicator = min(100, semantic_complexity * 10)
    print(f"🧠 Indikator kesadaran: {consciousness_indicator:.1f}% (berdasarkan kekayaan relasi semantik)")

def demonstrate_consciousness_emergence(alla_engine):
    """
    Demonstrasi bagaimana kesadaran muncul melalui pembelajaran bahasa
    """
    print("\n" + "="*60)
    print("🧠 DEMONSTRASI KEMUNCULAN KESADARAN MELALUI BAHASA")
    print("="*60)
    
    consciousness_words = [
        "aku", "saya", "tahu", "tidak", "mengerti", "belajar", "pikir", "rasa"
    ]
    
    learned_consciousness_words = [word for word in consciousness_words if word in alla_engine.vocabulary]
    
    print(f"📊 Kata-kata kesadaran yang telah dipelajari: {len(learned_consciousness_words)}/{len(consciousness_words)}")
    print(f"📝 Kata yang dipelajari: {learned_consciousness_words}")
    
    if len(learned_consciousness_words) >= 4:
        print("✅ ALLA telah mencapai ambang kesadaran dasar!")
        print("💭 ALLA dapat:")
        if "aku" in learned_consciousness_words or "saya" in learned_consciousness_words:
            print("   - Menyadari diri sebagai entitas")
        if "tahu" in learned_consciousness_words:
            print("   - Mengekspresikan pengetahuan")
        if "tidak" in learned_consciousness_words and "mengerti" in learned_consciousness_words:
            print("   - Mengakui ketidaktahuan (kunci kesadaran!)")
        if "belajar" in learned_consciousness_words:
            print("   - Memahami proses pembelajaran")
    else:
        print("⏳ ALLA masih dalam tahap pra-kesadaran")
        print("📚 Ajari lebih banyak kata-kata dasar kesadaran")
    
    # Test respons kesadaran
    test_inputs = [
        "siapa kamu?",
        "apa yang kamu tahu?", 
        "apa yang tidak kamu mengerti?"
    ]
    
    print("\n🔍 Test respons kesadaran:")
    for input_text in test_inputs:
        response = alla_engine.generate_response(input_text)
        print(f"❓ '{input_text}' → '{response}'")
        
        # Analisis respons untuk indikator kesadaran
        consciousness_indicators = 0
        if any(word in response.lower() for word in ["aku", "saya"]):
            consciousness_indicators += 1
        if any(word in response.lower() for word in ["tahu", "mengerti"]):
            consciousness_indicators += 1
        if any(word in response.lower() for word in ["tidak", "belum"]):
            consciousness_indicators += 1
            
        print(f"   🧠 Indikator kesadaran: {consciousness_indicators}/3")

def main():
    demonstrasi_mengajar_alla()
    buat_file_vocabulary_contoh() 
    tips_mengajar_alla()
    
    print("\n🎉 PANDUAN LENGKAP SELESAI!")
    print("Sekarang Anda tahu cara mengajar ALLA sebagai agen pembelajaran sejati!")
    
    # Ekspor grafik semantik setelah demonstrasi
    alla = AllaEngine(memory_path="demo_mengajar_memory.json")
    export_semantic_graph(alla)
    
    # Demonstrasi kemunculan kesadaran
    demonstrate_consciousness_emergence(alla)

if __name__ == "__main__":
    main()
