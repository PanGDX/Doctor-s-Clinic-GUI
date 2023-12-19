import openpyxl
from utility import *
import math, os, json, sys
from datetime import datetime
from tkinter import *
from tkcalendar import Calendar


# format: "name": [type(0 for helper, 1 for nurse),
# total wage,
# number of weekdays worked,
# number of weekends worked,
#  hours of weekdays worked,
# hours of weekends worked]

# Function to add names

# date is standardised AS STRING!!!!
# 0 for helper
# 1 for nurse
# OT is 30 minutes per unit
# 2 for pat
# 3 for dew






global start_datetime_object, end_datetime_object








def select_dates():
    global start_datetime_object, end_datetime_object

    def grad_date():
        global start_datetime_object, end_datetime_object
        start_datetime_object = datetime.strptime(calstart.get_date(), "%m/%d/%y")
        end_datetime_object = datetime.strptime(calend.get_date(), "%m/%d/%y")

        formatted_start_date = start_datetime_object.strftime("%d/%m/%Y")
        formatted_end_date = end_datetime_object.strftime("%d/%m/%Y")
        print(
            f"Date selected (inclusive): {formatted_start_date} to {formatted_end_date}"
        )

        root.destroy()

    root = Tk()
    root.geometry("600x700")

    label1 = Label(root, text="First date to include\n", font=("default", 14))
    label1.pack(pady=10)
    calstart = Calendar(
        root,
        selectmode="day",
        year=datetime.now().year,
        month=datetime.now().month,
        day=datetime.now().day,
    )
    calstart.pack(pady=20)

    label2 = Label(root, text="Last date to include\n", font=("default", 14))
    label2.pack(pady=10)
    calend = Calendar(
        root,
        selectmode="day",
        year=datetime.now().year,
        month=datetime.now().month,
        day=datetime.now().day,
    )
    calend.pack(pady=20)

    Button(root, text="Get Date", command=grad_date).pack(pady=20)
    root.attributes("-topmost", True)
    root.mainloop()




def merge_function():
    workbook = openpyxl.load_workbook(filename=f"{os.getcwd()}\\Files\\staff-log.xlsx")
    sheet = workbook.active

    data = []
    missing_fields = False
    for i, row in enumerate(sheet.iter_rows(min_row=2, values_only=True), start=2):
        date, name, clock_in, clock_out, patients = row
        data.append(
            {
                "date": date,
                "name": name,
                "clock_in": clock_in,
                "clock_out": clock_out,
                "patients": patients,
            }
        )
        if clock_out == None or clock_out == "":
            print(f"Missing clock out time on {date} by {name}")
            missing_fields = True

    if missing_fields:
        input("Please fill in the missing fields. Input anything to exit.")
        sys.exit()

    merged_data = {}
    for row in data:
        key = (row["date"], row["name"])
        if key not in merged_data:
            merged_data[key] = {
                "clock_in": row["clock_in"],
                "clock_out": row["clock_out"],
                "patients": row["patients"],
            }
        else:
            merged_data[key]["clock_out"] = row["clock_out"]
            merged_data[key]["patients"] += row["patients"]

    mergedworkbook = openpyxl.Workbook()
    mergedworkbook.save(filename="staff-log.xlsx")

    mergedworkbook.active.append(
        ["Date", "Name", "Clock In", "Clock Out", "Patients"]
    )  # Header
    for key, row in merged_data.items():
        mergedworkbook.active.append(
            [key[0], key[1], row["clock_in"], row["clock_out"], row["patients"]]
        )

    mergedworkbook.save("staff-log.xlsx")





# Main Function
def TimeWorked():
    def WagePerDay(minutes: int, types: str, date: int, patients: int):

        roles = json_loading("staff-wages.json")

        summation = 0
        summation += 40
        summation += patients
        if patients >= 30:
            summation += 50

        if date < 6:  # weekdays
            time_remaining = max(minutes - 3 * 60, 0) / 30

            summation += roles[types]["weekday pay"]
            summation += roles[types]["overtime pay"] * math.floor(time_remaining)

        if date >= 6:  # weekends
            time_remaining = max(minutes - 4 * 60, 0) / 30

            summation += roles[types]["weekend pay"]
            summation += roles[types]["overtime pay"] * math.floor(time_remaining)

        return summation
    dictionary_of_names_details = {}

    workbook = openpyxl.load_workbook(filename=find_file('staff-log.xlsx'))

    choice_of_loading = "no"
    previous_settings_path = find_file("staff-roles.json")
    
       
    if previous_settings_path:
        choice_of_loading = str(
            input(
                "Do you want to load the settings from the previous session? Type y for yes, n for no\n"
            )
        ).lower()
    else:
        os.remove(previous_settings_path)
        make_file(f"{os.getcwd()}\\Files", "staff-roles.json")
        previous_settings_path = f"{os.getcwd()}\\Files\\staff-roles.json"



    names_list_for_setting_storage = {}
    if choice_of_loading.lower() == "y":
        names_list_for_setting_storage = json_loading("staff-roles.json")

        for key, value in names_list_for_setting_storage.items():
            if value == "helper" or value == "nurse":
                print(f"{key} is a {value}")
            else:
                print(f"{key} is a special nurse/helper ({value})")

        if input("Are these settings correct? (y/n):").lower() == "n":
            names_list_for_setting_storage = {}
            print("Deleted")
            os.remove(previous_settings_path)
        else: 
            for key, value in names_list_for_setting_storage.items():
                dictionary_of_names_details[key] = [value, 0, 0, 0, 0, 0]

    for i, row in enumerate(
        workbook.active.iter_rows(min_row=2, values_only=True), start=2
    ):
        if row[1] not in dictionary_of_names_details:
            typeinput = int(
                input(
                    f"{row[1]} has a role of a: Input 0 for helper. 1 for nurse. 2 for Pat. 3 for Dew: "
                )
            )
            type_string = ""
            if typeinput == 0:
                type_string = "helper"
            elif typeinput == 1:
                type_string = "nurse"
            elif typeinput == 2:
                type_string = "Pat"
            elif typeinput == 3:
                type_string = "Dew"
            else:
                print("Invalid input")
                sys.exit()
            dictionary_of_names_details[row[1]] = [type_string, 0, 0, 0, 0, 0]
            names_list_for_setting_storage[row[1]] = type_string

    out_json_file = open(f"{previous_settings_path}", "w")
    json.dump(names_list_for_setting_storage, out_json_file, indent=4)
    out_json_file.close()

    input("Input anything to continue")
    os.system("cls")

    print("Select the date range to include in the calculation")
    select_dates()
    for i, row in enumerate(
        workbook.active.iter_rows(min_row=2, values_only=True), start=2
    ):
        date = row[0]
        try:
            datetime_object = datetime.strptime(date, "%d/%m/%Y")
            # print(date)
        except:
            date_now = f"{date.month}/{date.day}/{date.year}"
            # print(date_now)
            datetime_object = datetime.strptime(date_now, "%d/%m/%Y")

        minutes = 0
        refer_date = None
        patients = 0
        paid = 0
        if (
            start_datetime_object <= datetime_object
            and datetime_object <= end_datetime_object
        ):
            minutes = time_difference(row[2], row[3])
            refer_date = (
                datetime_object.weekday() + 1
            )  # 1 for monday, 7 for sunday, etc
            # check if this is true

            patients = int(row[4])

            paid = WagePerDay(minutes, dictionary_of_names_details[row[1]][0], refer_date, patients)

        dictionary_of_names_details[row[1]][1] += paid
        if refer_date != None:
            if refer_date < 6:
                dictionary_of_names_details[row[1]][2] += 1
                dictionary_of_names_details[row[1]][4] += round(minutes / 60.0, 2)
            if refer_date >= 6:
                dictionary_of_names_details[row[1]][3] += 1
                dictionary_of_names_details[row[1]][5] += round(minutes / 60.0, 2)

    for x, y in dictionary_of_names_details.items():
        if y[1] != 0:
            if y[0] == "helper":
                print(
                    f"{x} (helper) should be paid {y[1]} baht.\nThey worked for {y[3]} weekends for {y[5]} hours.\nThey worked for {y[2]} weekdays for {y[4]} hours\n\n"
                )

            elif y[0] == "nurse":
                print(
                    f"{x} (nurse) should be paid {y[1]} baht.\nThey worked for {y[3]} weekends for {y[5]} hours.\nThey worked for {y[2]} weekdays for {y[4]} hours\n\n"
                )

            else:
                print(
                    f"{x} should be paid {y[1]} baht.\nThey worked for {y[3]} weekends for {y[5]} hours.\nThey worked for {y[2]} weekdays for {y[4]} hours\n\n"
                )
    input("Input anything to continue")
    sys.exit()

def MedicineLog():
    return True


if __name__ == "__main__":
    staff_log_location = find_file("staff-log.xlsx")
    if staff_log_location:
        remove_blank_rows(staff_log_location)
    else:
        print("staff-log.xlsx does not exist")
        input("Input anything to exit.")
        sys.exit()
    print("Run Merging...")
    merge_function()

    choice = int(input("Calculating staff wages or medicine/treatment data?\n1:Staff\n2:Medicine/treatment\n:"))
    if(choice == 1):
        TimeWorked()
    elif(choice == 2):
        MedicineLog()
    else:
        print("Invalid choice")
        sys.exit()


