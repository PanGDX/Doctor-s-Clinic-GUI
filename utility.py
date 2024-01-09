import os, json,socket,openpyxl
from datetime import datetime
import pymysql
from concurrent.futures import ThreadPoolExecutor
def find_file(file_name):
    """
    Search through the root_folder and all its subfolders for a file named file_name.
    Returns a list of full paths to the file if found, otherwise returns False.
    """
    matches = []
    for root, dirs, files in os.walk(os.getcwd()):
        if file_name in files:
            matches.append(os.path.join(root, file_name))

    print(matches)
    try:
        return matches[0]
    except:
        return False
    # must include the extension
    # returns full path


def make_file(dir, name, list_to_append: list = []):
    if find_file(name) == False:
        print(f"Making file: {name}")
        with open(f"{dir}\\{name}", "w") as file:
            if ".json" in name:
                json.dump({}, file, indent=4)
            elif ".xlsx" in name:
                file.close()
                wb = openpyxl.Workbook()
                if list != []:
                    wb.active.append(list_to_append)
                wb.save(f"{dir}\\{name}")
            else:
                pass  # Creates an empty file

def json_loading(file_name):
    """
    searches and loads the json file or else return empty json
    """
    file_path = find_file(file_name)
    if file_path:
        textfile = open(file_path, "r")

        json_file = json.loads(textfile.read())
        return json_file
    else:
        return {}
    



# for calculations





def time_difference(timein: str, timeout: str):
    """
    calculates the time difference using string formatting, 24 hours
    """
    timeinlist = timein.split(":")
    timeoutlist = timeout.split(":")

    hourdifference = int(timeoutlist[0]) - int(timeinlist[0])
    minutedifference = int(timeoutlist[1]) - int(timeinlist[1])
    return hourdifference * 60 + minutedifference





def load_and_check():
    """
    checks and creates all the necessary files
    """


    if find_file("final_app.exe") == False:
        print("Missing app.exe")
    if find_file("computer name.txt") == False:
        print("Missing computer name.txt (for identification)")
    if find_file("database.json") == False:
        print("Missing database.json")








# functions for calculation.py
def remove_blank_rows(excel_file):
    """
    removes all blank rows and saves the file
    """

    # Load the workbook and select the active worksheet
    workbook = openpyxl.load_workbook(excel_file)
    sheet = workbook.active

    # Iterate backwards through the rows
    for row in range(sheet.max_row, 0, -1):
        if all(
            sheet.cell(row=row, column=col).value is None
            for col in range(1, sheet.max_column + 1)
        ):
            sheet.delete_rows(row)

    # Save the modified workbook
    workbook.save(excel_file)
    workbook.close()
def calculate_costs(quantity_json, connection):
    """
    calculates the cost

    specifically made for date. eliminates any (type):"str" elements from calculation
    """
    cursor = connection.cursor()

        # SQL query to select all names and prices from the table
    query = "SELECT Name, Price FROM MedicineTreatmentPrices"

    # Executing the SQL command
    cursor.execute(query)

    # Fetching all results
    results = cursor.fetchall()
    print(results)
    # Close the cursor
    cursor.close()

    # Converting results to a list of dictionaries
    medicine_json = {}
    for json_key in results:
        medicine_json[json_key['Name']] = json_key['Price']


    total_cost = 0
    for med_name in quantity_json:
        if type(quantity_json[med_name]) == int:

            total_cost += (medicine_json[med_name] * quantity_json[med_name])

    return total_cost


def modify_medicine_log(medicine_treatment_name="", quantity=0):
    """
    assumes existence of sheet in excel file
    for current date only
    if current date exist, add/subtract
    note that it does NOT STACK -> add/subtract separated!

    quantity can be negative!!

    if current date does not exist, add new entry.
    KEY:sign included

    WORKS
    """

    excel_location = find_file("medicine-log.xlsx")
    now = datetime.now()
    date = now.strftime("%d/%m/%Y")

    workbook = openpyxl.load_workbook(excel_location)
    worksheet = workbook[f"{medicine_treatment_name}"]

    modified = False
    for i, row in enumerate(worksheet.iter_rows(min_row=2, values_only=True), start=2):
        if row[0] == date:  # date exists
            if row[1] != None:
                if row[1] < 0 and quantity <= 0:
                    modified = True
                    # index 1 for cell modification
                    worksheet.cell(row=i, column=2, value=row[1] + quantity)
                if row[1] > 0 and quantity > 0:
                    modified = True
                    # index 1 for cell modification
                    worksheet.cell(row=i, column=2, value=row[1] + quantity)
    if not modified:
        worksheet.append([date, quantity])

    workbook.save(excel_location)


def create_medicine_sheet(connection):
    """
    creates a new sheet if name does not exist
    If it does exist, ignore

    file does always exist (presumed)

    WORKS
    """
    cursor = connection.cursor()
    query = "SELECT Name FROM MedicineTreatmentPrices"
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    medicine_treatment_list = [name['Name'] for name in results]

    make_file(os.getcwd(), 'medicine-log.xlsx')
    excel_location = find_file("medicine-log.xlsx")
    workbook = openpyxl.load_workbook(excel_location)
    for key in medicine_treatment_list:
        if key not in workbook.sheetnames:
            workbook.create_sheet(key)
            worksheet = workbook[key]
            worksheet.append(["Date", "Quantity"])

    workbook.save(excel_location)





# connection and socket stuff

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception as e:
        return "Could not determine local IP: " + str(e)

def find_open_ports(port=65432):
    
    def scan_port(ip, port):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                s.connect((ip, port))
                return ip
        except (socket.timeout, ConnectionRefusedError, OSError):
            return None

    def get_local_network_ip_range():
        """ Get the local network's IP range based on the host's IP address. """
        host_ip = get_local_ip()
        ip_parts = host_ip.split('.')
        base_ip = '.'.join(ip_parts[:3]) + '.'
        return [base_ip + str(i) for i in range(1, 255)]
    

    ip_range = get_local_network_ip_range()
    print(ip_range)
    open_ips = []

    with ThreadPoolExecutor(max_workers=50) as executor:
        futures = [executor.submit(scan_port, ip, port) for ip in ip_range]
        for future in futures:
            result = future.result()
            if result:
                open_ips.append(result)
    

    print(open_ips)
    return open_ips

def return_connection():
    """
    run to return connection to the mysql service. 
    connection only
    Can be used to run connection.cursur(), etc
    """
    timeout = 10
    json_database = json_loading('database.json')

    connection = pymysql.connect(
        charset="utf8mb4",
        connect_timeout=timeout,
        cursorclass=pymysql.cursors.DictCursor,
        db=json_database['db'], #defaultdb??
        host=json_database['host'],
        password=json_database['password'],
        read_timeout=timeout,
        port= json_database['port'],
        user= json_database['user'],
        write_timeout=timeout,
        )
    return connection






# all the sql query and update stuff

def query_id_from_name(name:str, connection):
    """
    Queries the NameToID table to find the ID associated with a given name.

    Parameters:
    name (str): The name to query for.
    connection: An established MySQL database connection object.

    Returns:
    str: The ID associated with the given name, or None if not found.
    """
    if name == "" or name == None:
        return None

    cursor = connection.cursor()
    query = "SELECT ID FROM Clinic.NameToID WHERE Name = %s"
    cursor.execute(query, (name,))
    result = cursor.fetchone()
    cursor.close()
    print(result)
    if result:
        return result['ID']
    else:
        return None
    
    

def query_staff_roles(connection):
    """
    Queries staff-roles. Dictionary in truple
    """


    cursor = connection.cursor()
    query = "SELECT * FROM Clinic.StaffRoles"
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    print(result)
    if result:
        return result
    else:
        return None

def query_name_from_id(patient_id:str, connection):
    """
    Queries the NameToID table to find the ID associated with a given name.

    Parameters:
    name (str): The name to query for.
    connection: An established MySQL database connection object.

    Returns:
    str: The ID associated with the given name, or None if not found.
    """
    cursor = connection.cursor()
    query = "SELECT Name FROM Clinic.NameToID WHERE ID = %s"
    cursor.execute(query, (patient_id,))
    result = cursor.fetchone()
    cursor.close()
    print(result)
    if result:
        return result['Name']
    else:
        return None

def update_name_2_id(name:str, new_id:str, connection):
    """
    Checks if a name exists in the NameToID table. If it does, updates the ID.
    If not, inserts a new row with the name and ID.

    Parameters:
    name (str): The name to check.
    new_id (str): The new ID to associate with the name.
    connection: An established MySQL database connection object.
    """
    cursor = connection.cursor()

    # Check if the name exists
    check_query = "SELECT ID FROM Clinic.NameToID WHERE Name = %s"
    cursor.execute(check_query, (name,))
    result = cursor.fetchone()

    if result:
        # Name exists, update the ID
        update_query = "UPDATE Clinic.NameToID SET ID = %s WHERE Name = %s"
        cursor.execute(update_query, (new_id, name))
        print(f"Updated ID for {name}")
    else:
        # Name does not exist, insert new row
        insert_query = "INSERT INTO Clinic.NameToID (Name, ID) VALUES (%s, %s)"
        cursor.execute(insert_query, (name, new_id))
        print(f"Inserted new name and ID: {name}, {new_id}")

    # Commit changes and close cursor
    connection.commit()
    cursor.close()
    


def update_patient_json_using_id(patient_id, connection, 
                                 medicine_or_treatment:str = "",
                                 quantity:int = 0,
                                 doctor_note:str=""):
    patient_json = query_patient_info_json_using_id(patient_id,connection)
    cursor = connection.cursor()

    now = datetime.now()
    date = now.strftime("%d/%m/%Y")

    if patient_json!=None:

        patient_json = json.loads(patient_json)
        if patient_json.get(date) == None:
            
            patient_json[date] = {}

            if medicine_or_treatment != "":
                patient_json[date][medicine_or_treatment] = quantity
            if doctor_note != "":
                patient_json[date]["doctor note"] = doctor_note
        else:
            
            if medicine_or_treatment != "":
                if patient_json[date].get(medicine_or_treatment) == None:
                    patient_json[date][medicine_or_treatment] = quantity
                else:
                    patient_json[date][medicine_or_treatment] += quantity
            if doctor_note != "":
                if patient_json[date].get("doctor note") == None:
                    patient_json[date]["doctor note"] = doctor_note
                else:
                    patient_json[date]["doctor note"] = (
                        patient_json[date]["doctor note"] + "\n" + doctor_note
                    )
        



        update_query = "UPDATE PatientInfoJson SET Json = %s WHERE ID = %s"

        output_json_str = json.dumps(patient_json)
        print(output_json_str)
        print(type(output_json_str))
        # Executing the SQL command
        cursor.execute(update_query, (output_json_str, patient_id))

        # Commit the changes to the database
        connection.commit()

        

    else:
        output_json = {}
        output_json["ID"] = str(patient_id)
        if output_json.get(date) == None:
            # new date
            output_json[date] = {}

            if medicine_or_treatment != "":
                output_json[date][medicine_or_treatment] = quantity
            if doctor_note != "":
                output_json[date]["doctor note"] = doctor_note
        else:
            # append to that
            if medicine_or_treatment != "":
                if output_json[date].get(medicine_or_treatment) == None:
                    output_json[date][medicine_or_treatment] = quantity
                else:
                    output_json[date][medicine_or_treatment] += quantity
            if doctor_note != "":
                if output_json[date].get("doctor note") == None:
                    output_json[date]["doctor note"] = doctor_note
                else:
                    output_json[date]["doctor note"] = (
                        output_json[date]["doctor note"] + "\n" + doctor_note
                    )




        output_json_str = json.dumps(output_json)

        print(output_json_str)
        print(type(output_json_str))
        insert_query = "INSERT INTO PatientInfoJson (ID, Json) VALUES (%s, %s)"

        # Executing the SQL command
        cursor.execute(insert_query, (patient_id, output_json_str))

        # Commit the changes to the database
        connection.commit()

        

    cursor.close()
    


    

def query_info_using_barcode(barcode:str, connection):
    """
    Queries the Barcode table to find the MedicineName and QuantityPerScan associated with a given barcode.

    Parameters:
    barcode (str): The barcode to query for.
    connection: An established MySQL database connection object.

    Returns:
    tuple: A tuple containing (MedicineName, QuantityPerScan), or None if not found.
    """
    barcode = int(barcode)

    cursor = connection.cursor()

    # SQL query to find the MedicineName and QuantityPerScan for a given barcode
    query = "SELECT MedicineName, QuantityPerScan FROM Clinic.Barcode WHERE Code = %s"

    # Executing the SQL command
    cursor.execute(query, (barcode,))

    # Fetching the result
    result = cursor.fetchone()

    # Close the cursor
    cursor.close()

    # Return the result if found, otherwise None
    return result if result else None
    

def update_medicine_log_sql(medicine_name:str, quantity:int, connection):
    """
    Appends a new record to the MedicineLog table with the current date, 
    given medicine name, and quantity.

    Parameters:
    medicine_name (str): The name of the medicine.
    quantity (int): The quantity of the medicine.
    connection: An established MySQL database connection object.
    """
    now = datetime.now()
    today_date = now.strftime("%d/%m/%Y")

    # Create a cursor object
    cursor = connection.cursor()

    # SQL query to insert data
    insert_query = """
    INSERT INTO Clinic.MedicineLog (Date, Name, Quantity) 
    VALUES (%s, %s, %s)
    """

    # Data tuple
    data = (today_date, medicine_name, quantity)

    # Executing the SQL command
    cursor.execute(insert_query, data)

    # Commit the changes to the database
    connection.commit()

    # Close the cursor
    cursor.close()

    print(f"New record added for {medicine_name} with quantity {quantity} on {today_date}")

    return

  
def query_patient_info_json_using_id(patient_id, connection):
    """
    Queries the PatientInfoJson table to find the JSON data associated with a given patient ID.

    Parameters:
    patient_id (int): The patient ID to query for.
    connection: An established MySQL database connection object.

    Returns:
    dict: The JSON data associated with the given patient ID, or None if not found.
    """

    # Create a cursor object
    cursor = connection.cursor()

    # SQL query to find the JSON data for a given patient ID
    query = "SELECT Json FROM PatientInfoJson WHERE ID = %s"

    # Executing the SQL command
    cursor.execute(query, (patient_id,))

    # Fetching the result
    result = cursor.fetchone()

    # Close the cursor
    cursor.close()

    print(result)

    # Return the JSON data if found, otherwise None
    if result:
        return result['Json']
    else:
        return None
    

def query_price_from_med_name(medicine_name,connection):
    """
    THIS IS NOT FOR BARCODE. THIS IS FOR MedicineTreatmentPrices
    """ 

    cursor = connection.cursor()

    # SQL query to find the MedicineName and QuantityPerScan for a given barcode
    query = "SELECT Price FROM Clinic.MedicineTreatmentPrices WHERE Name = %s"

    # Executing the SQL command
    cursor.execute(query, (medicine_name,))

    # Fetching the result
    result = cursor.fetchone()

    # Close the cursor
    cursor.close()

    # Return the result if found, otherwise None
    return result['Price'] if result else None

