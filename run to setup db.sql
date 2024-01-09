CREATE SCHEMA 'Clinic';
USE Clinic;

CREATE TABLE Clinic.StaffLog(
    Date VARCHAR(255),
    Name VARCHAR(255),
    TimeIn VARCHAR(255),
    TimeOut VARCHAR(255)
);

CREATE TABLE Clinic.MedicineLog(
    Date VARCHAR(255),
    Name VARCHAR(255),
    Quantity INT
);

CREATE TABLE Clinic.NameToID (
    Name VARCHAR(255) PRIMARY KEY,
    ID VARCHAR(255)
);


CREATE TABLE PatientInfoJson (
    ID INT PRIMARY KEY,
    Json JSON
);


CREATE TABLE Clinic.RolesPayment (
    Roles VARCHAR(255) PRIMARY KEY,
    WeekdayDollarPerHour INT,
    WeekendDollarPerHour INT,
    OvertimeWeekdayDollarPerHour INT,
    OvertimeWeekendDollarPerHour INT
);



CREATE TABLE Clinic.StaffRoles (
    Name VARCHAR(255) PRIMARY KEY,
    Role VARCHAR(255)
);




CREATE TABLE Clinic.MedicineTreatmentPrices (
    Name VARCHAR(255) Primary Key,
    Price INT
);

CREATE TABLE Clinic.Barcode (
    Code VARCHAR(255) Primary Key,
    MedicineName VARCHAR(255),
    QuantityPerScan INT,
);
