BEGIN TRANSACTION;
CREATE TABLE inventory(ID INT PRIMARY KEY NOT NULL, Item CHAR(25) NOT NULL, Price, Units_Sold INT NOT NULL, Marginal_Cost,  AVG_Value_of_Item_Inventory, Turnover, Profitability, Physical_Volume);
COMMIT;
