from supabase_client import supabase

def verify_doctor(full_name: str, registration_number: str):
    response = supabase.table("doctors") \
        .select("*") \
        .eq("full_name", full_name) \
        .eq("registration_number", registration_number) \
        .execute()

    if not response.data:
        print("❌ Doctor not found. Verification failed.")
        return None

    doctor = response.data[0]
    print(f"✅ Doctor found: {doctor['full_name']} (Reg#: {doctor['registration_number']})")

    supabase.table("doctors") \
        .update({"is_verified": True}) \
        .eq("doctor_id", doctor["doctor_id"]) \
        .execute()

    print("🎉 Doctor successfully verified!")
    return doctor["doctor_id"]

def collect_and_store_details(doctor_id: str):
    try:
        experience = int(input("Enter your years of experience: "))
    except ValueError:
        experience = 0
        print("Invalid input. Defaulting experience to 0.")

    speciality_id = input("Enter your speciality ID (from Supabase): ")

    supabase.table("doctors") \
        .update({"experience_years": experience}) \
        .eq("doctor_id", doctor_id) \
        .execute()

    supabase.table("doctor_specialities") \
        .insert({"doctor_id": doctor_id, "speciality_id": int(speciality_id)}) \
        .execute()

    print("✅ Additional details saved successfully.")

if __name__ == "__main__":
    name = input("Enter your full name: ")
    reg_no = input("Enter your registration number: ")

    doctor_id = verify_doctor(name, reg_no)
    if doctor_id:
        collect_and_store_details(doctor_id)
