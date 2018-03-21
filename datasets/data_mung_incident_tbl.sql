/*
This script will clean up our terrorism event table.  
It will then create a tableby reading from the referenced csv file. 
The csv file had minor datamunging done in excel as well, including:
    -- eliminating columns we were not interested in.  
    -- adding a date column
    -- no edits appear needed to the column titles. 
-- data munging starts from the incidents_raw csv import.  
-- Certain columns were already eliminated prior to import.  The target table will be incidents_tbl.  
-- datatypes were explicitly mapped to mysql datatypes upon csv import.  
-- The structure will be defined now, then populated with the cleaned data.  

-- MySQL Connection Details:  
-- user:  gtdb_admin
-- password: ktjljmjj (team member initials)
-- host: gtdb-insta.csuho8dvfguv.us-east-1.rds.amazonaws.com
-- port:  3306
-- database: gtdb

@author: joelee
*/ 

USE gtdb;

DROP TABLE IF EXISTS incidents_tbl;

CREATE TABLE incidents_tbl(
    incident_id int NOT NULL AUTO_INCREMENT,
    iyear int,
    icountry_id int,
    icountry_txt varchar(50), 
    ilatitude float, 
    ilongitude float, 
    attacktype_id int, 
    attacktype_txt varchar(50), 
    targtype_id int, 
    targtype_txt varchar(50), 
    gname varchar(100), 
    weaptype_id int, 
    weaptype_txt varchar(100), 
    nkill int, 
    nwound int, 
    property int,
    PRIMARY KEY (incident_id)
);

-- The raw table has some know clean up tasks required.  
-- Need to handle the blanks/nulls in nkill, and nwound values.  
-- It will be assumed that they have 0 impact on results, therefore transform to 0
-- Also, the dba managing the source data used '-9' for unknown property damage.  
-- This should be handled to zero for the purposes of tracking known property damage flag.  
-- create a temp table to perform transform 1
DROP TABLE IF EXISTS tmp_inc_x1;
CREATE TEMPORARY TABLE IF NOT EXISTS tmp_inc_x1 AS (SELECT * FROM incidents_raw);
UPDATE tmp_inc_x1 
SET nkill = 0 
WHERE nkill = '' OR nkill IS  NULL; 

UPDATE tmp_inc_x1 
SET nwound = 0 
WHERE nwound = '' OR nkill IS  NULL; 

-- Incidents that do not have a known lat/long cannot be factored into our maps.  
-- Delete rows where ilatitude is blank or null
SELECT * FROM tmp_inc_x1 
WHERE 
ilatitude IS NULL 
OR ilatitude = ''  
OR ilongitude IS NULL 
OR ilongitude = ''
;
 
 DELETE FROM tmp_inc_x1 
 WHERE 
ilatitude IS NULL 
OR ilatitude = ''  
OR ilongitude IS NULL 
OR ilongitude = ''
;

SELECT * FROM tmp_inc_x1;

INSERT INTO incidents_tbl (incident_id, iyear, icountry_id, icountry_txt, ilatitude, ilongitude
, attacktype_id, attacktype_txt, targtype_id, targtype_txt, gname, weaptype_id, weaptype_txt, nkill
, nwound, property 
)
    SELECT tmp_inc_x1.incident_id, 
    tmp_inc_x1.iyear, 
    tmp_inc_x1.icountry_id, 
    tmp_inc_x1.icountry_txt, 
    tmp_inc_x1.ilatitude, 
    tmp_inc_x1.ilongitude, 
    tmp_inc_x1.attacktype_id, 
    tmp_inc_x1.attacktype_txt, 
    tmp_inc_x1.targtype_id, 
    tmp_inc_x1.targtype_txt, 
    tmp_inc_x1.gname, 
    tmp_inc_x1.weaptype_id, 
    tmp_inc_x1.weaptype_txt, 
    tmp_inc_x1.nkill, 
    tmp_inc_x1.nwound, 
    tmp_inc_x1.property
    FROM tmp_inc_x1 
    ORDER BY tmp_inc_x1.incident_id;


