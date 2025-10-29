from app.db.connectdb import connect, disconnect

def create_table():
    conn, cursor = connect()
    if not conn:
        print("Failed Connect")
        return
    
    queries = [
        '''
        CREATE TABLE IF NOT EXISTS health_insurance(
            citizen_id VARCHAR(12) PRIMARY KEY,
            fullname VARCHAR(50) NOT NULL,
            gender BOOLEAN NOT NULL,
            dob DATE NOT NULL,
            phone_number CHAR(10) NOT NULL,
            registration_place TEXT NOT NULL,
            valid_from DATE NOT NULL,
            expired DATE NOT NULL
        );
        ''',
        '''
        CREATE TABLE IF NOT EXISTS patient(
            citizen_id VARCHAR(12) PRIMARY KEY,
            fullname VARCHAR(50) NOT NULL,
            gender BOOLEAN NOT NULL,
            dob DATE NOT NULL,
            address VARCHAR(80) NOT NULL,
            phone_number CHAR(10) NOT NULL,
            ethnic VARCHAR(30),
            job VARCHAR(30),
            create_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            is_insurance BOOLEAN
        );
        ''',
        '''
        CREATE TABLE IF NOT EXISTS clinic(
            clinic_id INT AUTO_INCREMENT PRIMARY KEY,
            fullname VARCHAR(50) NOT NULL,
            clinic_status BOOLEAN DEFAULT 0,
            address_room VARCHAR(30) NOT NULL
        );
        ''',
        '''
        CREATE TABLE IF NOT EXISTS staff(
            staff_id INT AUTO_INCREMENT PRIMARY KEY,
            fullname VARCHAR(30) NOT NULL,
            staff_position ENUM('DOCTOR', 'NURSE'),
            clinic_id INT NULL,
            FOREIGN KEY (clinic_id) REFERENCES clinic(clinic_id) ON DELETE SET NULL
        );
        ''',
        '''
        CREATE TABLE IF NOT EXISTS service(
            service_id INT AUTO_INCREMENT PRIMARY KEY,
            service_name VARCHAR(50) NOT NULL,
            service_description TEXT NOT NULL,
            price DECIMAL(8,2) NOT NULL,
            price_insurance DECIMAL(8,2) NOT NULL
        );
        ''',
        '''
        CREATE TABLE IF NOT EXISTS clinic_service(
            clinic_service_id INT AUTO_INCREMENT PRIMARY KEY,
            clinic_id INT,
            service_id INT,
            service_status BOOLEAN DEFAULT 1,
            FOREIGN KEY (clinic_id) REFERENCES clinic(clinic_id) ON DELETE CASCADE,
            FOREIGN KEY (service_id) REFERENCES service(service_id) ON DELETE CASCADE
        );
        ''',
        '''
        CREATE TABLE IF NOT EXISTS orders(
            order_id INT AUTO_INCREMENT PRIMARY KEY,
            queue_number INT NOT NULL,
            citizen_id VARCHAR(12),
            clinic_service_id INT,
            create_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            order_status BOOLEAN DEFAULT 0,
            payment_method ENUM('CASH', 'CARD', 'INSURANCE', 'BANKING'),
            payment_status ENUM('PAID', 'UNPAID', 'PENDING', 'CANCELLED'),
            price DECIMAL(8,2) NOT NULL,
            FOREIGN KEY (citizen_id) REFERENCES patient(citizen_id) ON DELETE CASCADE,
            FOREIGN KEY (clinic_service_id) REFERENCES clinic_service(clinic_service_id) ON DELETE CASCADE
        );
        ''',
    ]
    for query in queries:
        cursor.execute(query)

    conn.commit()
    return conn, cursor