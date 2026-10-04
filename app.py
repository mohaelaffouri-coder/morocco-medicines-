import streamlit as st
import database as db
import scraper

db.init_database()

st.set_page_config(
    page_title="نظام إدارة الأدوية المغربية",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #c1272d;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.3rem;
        color: #006233;
        margin-top: 1rem;
    }
    @media (max-width: 768px) {
        .main-header { font-size: 1.8rem !important; }
        .sub-header { font-size: 1.1rem !important; }
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-header">🇦 نظام إدارة الأدوية المغربية</h1>', unsafe_allow_html=True)

expiring_soon, expired = db.check_expiry_alerts()

st.sidebar.title("⚙️ القائمة")
page = st.sidebar.radio(
    "اختر الوظيفة",
    ["🔍 البحث عن دواء", "➕ إضافة دواء جديد", "🤖 استخراج تلقائي", 
     "✏️ تعديل دواء", " الإحصائيات", "🔔 التنبيهات"]
)

if len(expired) > 0 or len(expiring_soon) > 0:
    st.sidebar.warning(f"⚠️ {len(expired)} منتهي، {len(expiring_soon)} قريب الانتهاء")

# ===== البحث =====
if page == "🔍 البحث عن دواء":
    st.markdown('<h2 class="sub-header">🔍 البحث عن الأدوية</h2>', unsafe_allow_html=True)
    
    search_query = st.text_input("ابحث بالاسم أو المادة الفعالة", "")
    categories = db.get_all_categories()
    selected_category = st.selectbox("فئة المرض", ["الكل"] + categories)
    lab_filter = st.text_input("المختبر", "")
    
    if st.button("🔎 بحث", type="primary"):
        results = db.search_medicines(
            query=search_query,
            disease_category=selected_category if selected_category != "الكل" else "",
            laboratory=lab_filter
        )
        
        if results:
            st.success(f"✅ تم العثور على {len(results)} دواء")
            for med in results:
                with st.expander(f"💊 {med[1]} - {med[3]}"):
                    st.markdown(f"**المادة الفعالة:** {med[2]}")
                    st.markdown(f"**طريقة الاستعمال:** {med[4]}")
                    st.markdown(f"**موانع الاستعمال:** {med[5]}")
                    st.markdown(f"**المختبر:** {med[6]}")
                    st.markdown(f"**السعر:** {med[7]}")
                    st.markdown(f"**تاريخ الانتهاء:** {med[11]}")
        else:
            st.warning("️ لم يتم العثور على نتائج")

# ===== الإضافة =====
elif page == "➕ إضافة دواء جديد":
    st.markdown('<h2 class="sub-header">➕ إضافة دواء جديد</h2>', unsafe_allow_html=True)
    
    with st.form("add_form"):
        name = st.text_input("اسم الدواء *", "")
        active_ingredient = st.text_input("المادة الفعالة *", "")
        disease_category = st.text_input("فئة المرض *", "")
        usage = st.text_area("طريقة الاستعمال *", "")
        contraindications = st.text_area("موانع الاستعمال *", "")
        laboratory = st.text_input("المختبر", "")
        price = st.text_input("السعر", "")
        
        submitted = st.form_submit_button("💾 حفظ", type="primary")
        
        if submitted:
            if name and active_ingredient and disease_category:
                db.add_medicine(name, active_ingredient, disease_category, usage, contraindications, laboratory, price, "يدوي")
                st.success(f"✅ تم إضافة '{name}' بنجاح")
            else:
                st.error("❌ يرجى ملء الحقول المطلوبة (*)")

# ===== الاستخراج التلقائي =====
elif page == " استخراج تلقائي":
    st.markdown('<h2 class="sub-header">🤖 استخراج من medbase.ma</h2>', unsafe_allow_html=True)
    
    medicine_name = st.text_input("اسم الدواء", "")
    disease_category = st.text_input("فئة المرض", "")
    
    if st.button(" استخراج", type="primary"):
        if medicine_name:
            with st.spinner("جاري البحث..."):
                result = scraper.scrape_medbase(medicine_name)
                if result and "error" not in result:
                    st.success("✅ تم العثور على بيانات")
                    st.json(result)
                else:
                    st.error("❌ لم يتم العثور على الدواء")

# ===== التعديل =====
elif page == "️ تعديل دواء":
    st.markdown('<h2 class="sub-header">✏️ تعديل دواء</h2>', unsafe_allow_html=True)
    
    all_medicines = db.search_medicines()
    medicine_options = {f"{med[1]} ({med[3]})": med[0] for med in all_medicines}
    
    if medicine_options:
        selected = st.selectbox("اختر الدواء", list(medicine_options.keys()))
        if selected:
            medicine_id = medicine_options[selected]
            medicine = [m for m in all_medicines if m[0] == medicine_id][0]
            
            with st.form("edit_form"):
                new_name = st.text_input("الاسم", medicine[1])
                new_usage = st.text_area("الاستعمال", medicine[4])
                new_contra = st.text_area("موانع الاستعمال", medicine[5])
                new_price = st.text_input("السعر", medicine[7])
                
                if st.form_submit_button("💾 حفظ التعديلات", type="primary"):
                    db.update_medicine(medicine_id, name=new_name, usage=new_usage, 
                                      contraindications=new_contra, price=new_price)
                    st.success("✅ تم التحديث")
    else:
        st.info("لا توجد أدوية للتعديل")

# ===== الإحصائيات =====
elif page == "📊 الإحصائيات":
    st.markdown('<h2 class="sub-header">📊 إحصائيات</h2>', unsafe_allow_html=True)
    
    all_medicines = db.search_medicines()
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("إجمالي الأدوية", len(all_medicines))
    with col2:
        st.metric("فئات الأمراض", len(set([m[3] for m in all_medicines])))
    
    st.markdown("###  توزيع حسب الفئة")
    category_counts = {}
    for med in all_medicines:
        cat = med[3]
        category_counts[cat] = category_counts.get(cat, 0) + 1
    
    for cat, count in category_counts.items():
        st.write(f"**{cat}:** {count} دواء")

# ===== التنبيهات =====
elif page == "🔔 التنبيهات":
    st.markdown('<h2 class="sub-header">🔔 التنبيهات</h2>', unsafe_allow_html=True)
    
    if expired:
        st.markdown("### ❌ أدوية منتهية الصلاحية")
        for med in expired:
            st.error(f"💊 {med[1]} - منتهي في: {med[2]}")
    
    if expiring_soon:
        st.markdown("### ⚠️ قريبة الانتهاء")
        for med in expiring_soon:
            st.warning(f"💊 {med[1]} - ينتهي في: {med[2]}")
    
    if not expired and not expiring_soon:
        st.success("✅ لا توجد تنبيهات")

st.markdown("---")
st.markdown("<div style='text-align: center; color: gray;'>⚠️ لأغراض تنظيمية فقط - استشر طبيباً أو صيدلياً</div>", unsafe_allow_html=True)
