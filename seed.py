import os
from supabase import create_client, Client
from dotenv import load_dotenv

# .env file load karna taaki keys mil sakein
load_dotenv()

url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

if not url or not key:
    print("Error: Supabase URL ya Service Role Key missing hai. Kripya .env file check karein.")
    exit(1)

# Supabase Admin Client setup
supabase: Client = create_client(url, key)

def seed_data():
    print("🌱 Database mein sample data dalna shuru kar rahe hain...\n")

    # 1. Wards Insert Karna (Lucknow)
    print("➡️ Wards (Areas) seed kar rahe hain...")
    wards_data = [
        {"ward_number": "LKO-01", "ward_name": "Hazratganj", "zone": "Central", "latitude": 26.8500, "longitude": 80.9499},
        {"ward_number": "LKO-02", "ward_name": "Gomti Nagar", "zone": "East", "latitude": 26.8600, "longitude": 81.0000},
        {"ward_number": "LKO-03", "ward_name": "Alambagh", "zone": "South", "latitude": 26.8143, "longitude": 80.9015}
    ]
    
    try:
        ward_res = supabase.table("wards").insert(wards_data).execute()
        ward_ids = [w['id'] for w in ward_res.data]
        print(f"✅ {len(ward_ids)} Wards successfully add ho gaye.")
    except Exception as e:
        print(f"❌ Wards insert error: {e}")
        return

    # 2. Users Insert Karna
    print("➡️ Users seed kar rahe hain...")
    users_data = [
        {"name": "Amit Sharma", "email": "amit@cleancity.ai", "role": "citizen", "ward_id": ward_ids[0]},
        {"name": "Priya Singh", "email": "priya@cleancity.ai", "role": "citizen", "ward_id": ward_ids[1]},
        {"name": "Admin Sir", "email": "admin@cleancity.ai", "role": "admin", "ward_id": ward_ids[0]}
    ]
    
    try:
        user_res = supabase.table("users").insert(users_data).execute()
        user_ids = [u['id'] for u in user_res.data]
        print(f"✅ {len(user_ids)} Users successfully add ho gaye.")
    except Exception as e:
        print(f"❌ Users insert error: {e}")
        return

    # 3. Waste Reports Insert Karna
    print("➡️️ Waste Reports seed kar rahe hain...")
    reports_data = [
        {
            "user_id": user_ids[0],
            "ward_id": ward_ids[0],
            "image_url": "https://images.unsplash.com/photo-1605600659908-0ef719419d41", # Dummy image
            "description": "Sarak par plastic kachra pada hai.",
            "latitude": 26.8505,
            "longitude": 80.9500,
            "waste_type": "Plastic",
            "confidence": 0.92,
            "status": "pending",
            "priority": "medium",
            "severity": "medium"
        },
        {
            "user_id": user_ids[1],
            "ward_id": ward_ids[1],
            "image_url": "https://images.unsplash.com/photo-1532996122724-e3c354a0b15b", # Dummy image
            "description": "Purane TV aur electronic parts feke gaye hain.",
            "latitude": 26.8610,
            "longitude": 81.0010,
            "waste_type": "E-Waste",
            "confidence": 0.88,
            "status": "pending",
            "priority": "high",
            "severity": "high"
        }
    ]
    
    try:
        supabase.table("waste_reports").insert(reports_data).execute()
        print("✅ Waste Reports successfully add ho gayi.")
    except Exception as e:
        print(f"❌ Reports insert error: {e}")
        return

    print("\n🎉 Seeding process complete! Ab aapka Dashboard data dikhayega.")

if __name__ == "__main__":
    seed_data()
