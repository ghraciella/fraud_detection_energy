# Data Card: Overview of the Dataset



## __Fraud Detection Energy Dataset:__


> Dataset containing information about client and billing (invoice) information for a Tunisian electricity and gas company.


---
---


### Data Overview : Client data

| feature column | description | data type  |
|:--------|:------------------------| :--------------| 
| Client_id | Unique id for client. |  object  |
| District | District where the client is. |   object |
| Client_catg  | Category client belongs to. |  string |
| Region | Area where the client is. |object |
| Creation_date  |  Date client joined. |  int64  | 
| Target   |   fraud:1 , not fraud: 0.  | int64 | 


---
---

### Data Overview : Invoice data

| feature column | description | data type  |
|:--------|:------------------------| :--------------| 
| Client_id | Unique id for the client. |  object  |
| Invoice_date | Date of the invoice. |   object |
| Tarif_type  | Type of tax. |  object |
| Counter_number | id number for reading meter/counter for electricity and gas. |object |
| Counter_statue  | Status of the reading meter/counter; takes up to 5 values such as working fine, not working, on hold statue, etc. |  object  | 
| Counter_code   |  code for the reading meter/counter. | object | 
| Reading_remarque  | Reading remark/notes the STEG agent takes during visit client (e.g: If the counter shows something wrong, the agent gives a bad score).  | int | 
| Counter_coefficient  | An additional coefficient to be added when standard consumption is exceeded. | - | 
| Consommation_level_1 | The threshold level of energy consumption to which a certain price is attributed (1). | - | 
| Consommation_level_2 | second threshold level of energy consumption to which a certain price is attributed (2). | - | 
| Consommation_level_3 | third threshold level of energy consumption to which a certain price is attributed (3). | -  | 
| Consommation_level_4 | fourth threshold level of energy consumption to which a certain price is attributed (4). | - | 
| Old_index   | Old_index. |  -  | 
| New_index   | New_index. |  -  | 
| Months_number | Month number. |  - | 
| Counter_type| Type of counter. |  - | 


