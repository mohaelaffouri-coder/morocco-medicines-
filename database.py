import sqlite3
from datetime import datetime

DB_NAME = "medicines_database.db"

def init_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS medicines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            active_ingredient TEXT,
            disease_category TEXT NOT NULL,
            usage TEXT,
            contraindications TEXT,
            laboratory TEXT,
            price TEXT,
            source TEXT,
            ammps_status TEXT,
            last_updated TEXT,
            expiry_date TEXT,
            notes TEXT
        )
    ''')
    
    conn.commit()
    
    if get_medicines_count() == 0:
        add_initial_data()
    
    conn.close()

def get_medicines_count():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM medicines")
    count = cursor.fetchone()[0]
    conn.close()
    return count

def add_initial_data():
    initial_medicines = [
        ("توبلكسيل شراب (Toplexil)", "أوكسوميميزين 0.03%", "السعال الجاف", 
         "الكبار +15 سنة: 15 مل 3 مرات يومياً", "الربو، الزرق، الأطفال تحت 15 سنة، الحمل",
         "Sanofi", "35-45 درهم", "medbase.ma", "معتمد", "2026-10-05", "2028-12-31", ""),
        
        ("هليسيدين شراب (Hélicidine)", "هيلاسولفاتي", "السعال الجاف",
         "حسب الوزن، 3-4 مرات يومياً", "فرط الحساسية",
         "Sanofi", "30-40 درهم", "medbase.ma", "معتمد", "2026-10-05", "2028-06-30", ""),
        
        ("أملور (Amlor)", "أملوديبين 5 أو 10 ملغ", "ارتفاع ضغط الدم",
         "قرص واحد يومياً", "صدمة قلبية، ضيق الأبهر الشديد، حمل",
         "Pfizer", "40-60 درهم", "medbase.ma", "معتمد", "2026-10-05", "2027-12-31", ""),
        
        ("كوفيرام (Coveram)", "بيريندوبريل + أملوديبين", "ارتفاع ضغط الدم",
         "قرص واحد صباحاً قبل الأكل", "الحمل، تاريخ وذمة وعائية، تضيق كلوي",
         "Servier", "120-180 درهم", "medbase.ma", "معتمد", "2026-10-05", "2027-09-30", ""),
        
        ("غلوكوفاج (Glucophage)", "ميتفورمين 500-1000 ملغ", "داء السكري نوع 2",
         "قرص واحد 2-3 مرات يومياً مع الوجبات", "فشل كلوي، حماض كيتوني، فشل كبدي",
         "Merck", "40-80 درهم", "medbase.ma", "معتمد", "2026-10-05", "2028-03-31", ""),
        
        ("إينكسيوم (Inexium)", "إيزوميبرازول 20 أو 40 ملغ", "حموضة المعدة والارتجاع",
         "قرص واحد يومياً قبل الأكل بساعة", "فرط الحساسية، بحذر مع كلوبيدوجريل",
         "AstraZeneca", "100-180 درهم", "medbase.ma", "معتمد", "2026-10-05", "2027-11-30", ""),
        
        ("دوليبران 1000 ملغ (Doliprane)", "باراسيتامول 1000 ملغ", "مسكنات خفيفة إلى متوسطة",
         "قرص واحد كل 6 ساعات (حد أقصى 4 غرام يومياً)", "فشل كبدي، فرط الحساسية",
         "Sanofi", "30-50 درهم", "medbase.ma", "معتمد", "2026-10-05", "2028-08-31", ""),
        
        ("أوجومين (Augmentin)", "أموكسيسيلين + حمض كلافولانيك", "عدوى بكتيرية",
         "قرص 1 غرام 2-3 مرات يومياً", "حساسية للبنسلين، يرقان مرتبط بالأموكسيسيلين",
         "GSK", "80-120 درهم", "medbase.ma", "معتمد", "2026-10-05", "2027-07-31", ""),
        
        ("فنتولين بخاخ (Ventoline)", "سالبوتامول 100 ميكروغرام", "الربو",
         "1-2 بخة عند الحاجة، حد أقصى 8 بخات يومياً", "فرط الحساسية، بحذر في فرط الدرقية",
         "GSK", "45-55 درهم", "medbase.ma", "معتمد", "2026-10-05", "2028-01-31", ""),
        
        ("كلاريتين 10 ملغ (Claritine)", "لوراتادين", "الحساسية",
         "قرص واحد يومياً", "فرط الحساسية، أطفال تحت 2 سنة",
         "Bayer", "50-70 درهم", "medbase.ma", "معتمد", "2026-10-05", "2028-05-31", ""),
    ]
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.executemany('''
        INSERT INTO medicines 
        (name, active_ingredient, disease_category, usage, contraindications, 
         laboratory, price, source, ammps_status, last_updated, expiry_date, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', initial_medicines)
    conn.commit()
    conn.close()

def add_medicine(name, active_ingredient, disease_category, usage, contraindications, 
                 laboratory, price, source, expiry_date="", notes=""):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO medicines 
        (name, active_ingredient, disease_category, usage, contraindications, 
         laboratory, price, source, ammps_status, last_updated, expiry_date, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (name, active_ingredient, disease_category, usage, contraindications,
          laboratory, price, source, "معتمد", datetime.now().strftime("%Y-%m-%d"),
          expiry_date, notes))
    medicine_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return medicine_id

def search_medicines(query="", disease_category="", laboratory=""):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    sql = "SELECT * FROM medicines WHERE 1=1"
    params = []
    
    if query:
        sql += " AND (name LIKE ? OR active_ingredient LIKE ?)"
        params.extend([f"%{query}%", f"%{query}%"])
    
    if disease_category:
        sql += " AND disease_category = ?"
        params.append(disease_category)
    
    if laboratory:
        sql += " AND laboratory LIKE ?"
        params.append(f"%{laboratory}%")
    
    sql += " ORDER BY name"
    
    cursor.execute(sql, params)
    results = cursor.fetchall()
    conn.close()
    return results

def get_all_categories():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT disease_category FROM medicines ORDER BY disease_category")
    categories = [row[0] for row in cursor.fetchall()]
    conn.close()
    return categories

def update_medicine(medicine_id, **kwargs):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    set_clause = ", ".join([f"{k} = ?" for k in kwargs.keys()])
    values = list(kwargs.values()) + [datetime.now().strftime("%Y-%m-%d"), medicine_id]
    cursor.execute(f"UPDATE medicines SET {set_clause}, last_updated = ? WHERE id = ?", values)
    conn.commit()
    conn.close()

def delete_medicine(medicine_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM medicines WHERE id = ?", (medicine_id,))
    conn.commit()
    conn.close()

def check_expiry_alerts():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, name, expiry_date FROM medicines 
        WHERE expiry_date != '' AND expiry_date <= date('now', '+3 months')
        AND expiry_date >= date('now')
    ''')
    expiring_soon = cursor.fetchall()
    
    cursor.execute('''
        SELECT id, name, expiry_date FROM medicines 
        WHERE expiry_date != '' AND expiry_date < date('now')
    ''')
    expired = cursor.fetchall()
    
    conn.close()
    return expiring_soon, expired
