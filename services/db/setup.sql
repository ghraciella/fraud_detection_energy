CREATE SCHEMA IF NOT EXISTS fraudschema;

DROP TABLE IF EXISTS fraudschema.client_data;

CREATE TABLE fraudschema.client_data (
        district  TEXT,
        client_id INT,
        client_catg  TEXT,
        region TEXT,
        creation_date DATE,
        target DECIMAL,
);

COPY fraudschema.client_data
FROM '/data/raw/client_data.csv' DELIMETER ',' CSV HEADER;


DROP TABLE IF EXISTS fraudschema.invoice_data;

CREATE TABLE fraudschema.invoice_data (
        client_id INT,
        invoice_date DATE,
        tarif_type TEXT,
        counter_number INT,
        counter_statue TEXT,
        counter_code TEXT,
        reading_remarque TEXT,
        counter_coefficient DECIMAL,
        consommation_level_1 DECIMAL,
        consommation_level_2 DECIMAL,
        consommation_level_3 DECIMAL,
        consommation_level_4 DECIMAL,
        old_index DECIMAL,
        new_index DECIMAL,
        months_number INT,
        counter_type TEXT
);

COPY fraudschema.invoice_data
FROM '/data/raw/invoice_data.csv' DELIMETER ',' CSV HEADER;









