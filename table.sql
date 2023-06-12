CREATE TABLE Devices (
  `ID` INT PRIMARY KEY AUTO_INCREMENT,
  `Name` VARCHAR(255),
  `Description` TEXT,
  `ConnectionType` VARCHAR(255),
  `Period` INT,
  `TimeCountStart` TIME,
  `TimeCountEnd` TIME,
  `Weight` INT,
  `Status` TEXT
);
