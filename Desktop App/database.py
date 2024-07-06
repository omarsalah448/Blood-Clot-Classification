import sqlite3

def create_database():
    # Connect to SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect('app_database.db', timeout=20)
    c = conn.cursor()
    
    # Create a Hospital Doctor table if it doesn't exist
    c.execute('''CREATE TABLE IF NOT EXISTS hospital_doctor (
                    EmployeeID INTEGER PRIMARY KEY AUTOINCREMENT,
                    Name VARCHAR NOT NULL,
                    NationalID INTEGER NOT NULL UNIQUE,
                    Email TEXT NOT NULL UNIQUE,
                    PhoneNumber TEXT NOT NULL UNIQUE,
                    Department TEXT NOT NULL
                 )''')
    
    # Create a User table if it doesn't exist
    c.execute('''CREATE TABLE IF NOT EXISTS user (
                    UserID INTEGER PRIMARY KEY AUTOINCREMENT,
                    EmployeeID INTEGER NOT NULL UNIQUE,
                    Name TEXT NOT NULL,
                    Email TEXT NOT NULL UNIQUE,
                    Password TEXT NOT NULL,
                    FOREIGN KEY (EmployeeID) REFERENCES hospital_doctor(EmployeeID)
                 )''')
    
    # Create a Ischemic Stroke Patient table if it doesn't exist
    c.execute('''CREATE TABLE IF NOT EXISTS ischemic_stroke_patient (
                    PatientID INTEGER PRIMARY KEY AUTOINCREMENT,
                    Name TEXT NOT NULL,
                    NationalID INTEGER NOT NULL UNIQUE,
                    BloodClotImg TEXT NOT NULL,
                    Diagnosis TEXT,
                    DateOfDiagnosis TEXT NOT NULL,
                    EmployeeID INTEGER,
                    FOREIGN KEY (EmployeeID) REFERENCES hospital_doctor(EmployeeID)
                 )''')
    
    # Add records to Hospital Doctor
    sql_insert = "INSERT INTO hospital_doctor (Name, NationalID, Email, PhoneNumber, Department) VALUES (?, ?, ?, ?, ?)"
    records = [('Habiba Khaled', 30109200203603, 'habibaelmazahy20@gmail.com', '01234567899', 'Laboratory'),
               ('Mohamed Abdelaty', 30203203211703, 'm.abdelaty@gmail.com', '01173855921', 'Internal Medicine'),
               ('Abdelaziz Khalil', 30110010208275, 'khalil.abdelazizm@gmail.com', '01098515811', 'Laboratory'),
               ('Ahmed Mohsen', 28912203231703, 'mohsen.ahmed@gmail.com', '01552883739', 'Intensive Care Unit'),
               ('Omar Salah', 27302303231703, 'omaarsalah522@gmail.com', '01178337443', 'Laboratory'),
               ('Khaled Tarek', 27607178273467, 'khaledtarek@hotmail.com', '01557765322', 'Emergency'),
               ('Aly Nasr', 26702158766512, 'aly.nasr.l190@gmail.com', '01097652211', 'Laboratory'),
               ('Salma Mohamed', 26409200203603, 'salma.mk@yahoo.com', '01209934884', 'Emergency'),
               ('Logine Magdy', 27503120877676, 'loginemagdy777@gmail.com', '01109776333', 'Laboratory'),
               ('Mahmoud ElSheemy', 25501028873765, 'sheemy.mahm@hotmail.com', '01009872233', 'Oncology'),
               ('Youssef Yosry', 25311078734212, 'youssefyosry58@gmail.com', '01022834544', 'Laboratory'),
               ('Ahmed Ali', 21093456789012, 'ahmedali@example.com', '01123456789', 'Surgery'),
               ('Fatma Mohamed', 22012178901234, 'fatmamohamed@example.com', '01012345678', 'Pediatrics'),
               ('Salma Mahmoud', 23031234567890, 'salmamahmoud@example.com', '01234567890', 'Internal Medicine'),
               ('Khaled Hassan', 24051234567890, 'khaledhassan@example.com', '01111111111', 'Obstetrics and Gynecology'),
               ('Laila Ali', 25070345678901, 'lailaali@example.com', '01000000000', 'Radiology'),
               ('Mohamed Youssef', 26090456789012, 'mohamedyoussef@example.com', '01001111111', 'Anesthesia'),
               ('Sara Ahmed', 27110567890123, 'saraahmed@example.com', '01233567890', 'Emergency'),
               ('Omar Mahmoud', 28120678901234, 'omarmahmoud@example.com', '01512345678', 'Physical Therapy'),
               ('Nour Hassan', 29140789012345, 'nourhassan@example.com', '01123556789', 'Oncology'),
               ('Aya Mohamed', 30160890123456, 'ayamohamed@example.com', '01234567810', 'Psychiatry'),
               ('Karim Ali', 31180901234567, 'karimali@example.com', '01121111111', 'Nutrition and Dietetics'),
               ('Lina Ahmed', 32201012345678, 'linaahmed@example.com', '01000010000', 'Pharmacy'),
               ('Amr Youssef', 33221123456789, 'amryoussef@example.com', '01111011111', 'Internal Medicine'),
               ('Nada Hassan', 34241234567890, 'nadahassan@example.com', '01234067890', 'Surgery'),
               ('Sami Mahmoud', 35261345678901, 'samimahmoud@example.com', '01012445678', 'Pediatrics'),
               ('Yara Mohamed', 36281456789012, 'yaramohamed@example.com', '01023456789', 'Radiology'),
               ('Yousef Ali', 37301567890123, 'yousefali@example.com', '01987654321', 'Emergency'),
               ('Lina Mohamed', 38321678901234, 'linamohamed@example.com', '01765432109', 'Radiology'),
               ('Adham Amr', 37301667890123, 'amradham@example.com', '01298734434', 'Intensive Care Unit')]
    
    c.executemany(sql_insert, records)

    # Commit changes and close the connection
    conn.commit()
    conn.close()
    
create_database()