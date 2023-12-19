# Data Card: Overview of the Dataset



## __Fraud Detection Energy Dataset:__


> Dataset containing information about client and billing (invoice) information for a Tunisian electricity and gas company.


---
---


### Data Overview : Client data

| feature column | description | data type  |
|:--------|:------------------------| :--------------| 
| Client_id | Unique id for client. |  object  |
| District |  District area where the client resides/ services was provided. |   object |
| Client_catg  | Category client belongs to (residential, business - commercial, industrial). |  string |
| Region | Regional area where the client is or where utility service is provided. |object |
| Creation_date  |  Date client joined or clients account was created. |  int64  | 
| Target   |   fraud:1 , not fraud: 0.  | int64 | 


<br>

---
---

### Data Overview : Invoice data

| feature column | description | data type  |
|:--------|:------------------------| :--------------| 
| Client_id | Unique id for the client. |  object  |
| Invoice_date | Date the invoice was issued to client for utility service. |   object |
| Tarif_type  | Type of price tariff for clients account. |  object |
| Counter_number | id number for reading meter/counter for utility (electricity and gas). |object |
| Counter_statue  | Status/condition of the reading meter/counter; takes up to 5 values such as working fine, not working, on hold statue, maintenance etc. |  object  | 
| Counter_code   |  id code for the reading meter/counter. | object | 
| Reading_remarque  | Reading remark/notes the STEG agent takes during visit client to indicate specific observation during reading.  | int | 
| Counter_coefficient  | An additional coefficient (adjustment factor) to be added when standard consumption is exceeded. | - | 
| Consommation_level_1 | The threshold level of energy consumption to which a certain price is attributed (1). | - | 
| Consommation_level_2 | second threshold level of energy consumption to which a certain price is attributed (2). | - | 
| Consommation_level_3 | third threshold level of energy consumption to which a certain price is attributed (3). | -  | 
| Consommation_level_4 | fourth threshold level of energy consumption to which a certain price is attributed (4). | - | 
| Old_index   | Old counter reading index recorded for previous billing cycle. |  -  | 
| New_index   | New counter reading index recorded for current billing cycle. |  -  | 
| Months_number | Number of months covered by the invoice for billing period. |  - | 
| Counter_type| Type of counter installed for client. |  - | 


<br>


---
---

### Assumptions : based on features


---

Assuming the company's internal codes for representing different meter reading is as follows

| feature column | description |
|:--------|:------------------------|
| 5 | Anomalies or exceptional situations. |
| 6 | Reading due to change of address. |
| 7 | Special reading (for irregular situations). |
| 8 | Normal reading. |
| 9  | Estimated reading. |
| 203   |  Reading after meter replacement. |
| 207   |  Different meter size or capacity. |
| 413   |  Reading after maintenance or repair. |


<br>
<br>

Assumption on cost of fraudlent activity, where total amount declared as lost for STEG = $200,000,000$:

---

* total number of clients in dataset = $135,493$
* total fraudulent clients in dataset = $7566$
* assumed loss per client = $26,434.047$
    - calculated as such: assumed loss per client = total amount lost divided by total fraudulent clients


<br>
<br>

Assumption on cost of fraudlent activity per client based on their computed fraudulent transactions, where total amount declared as lost for STEG = $200,000,000$:

---
* total number of clients in dataset = $135,493$
* total fraudulent clients in dataset = $7566$
* assumed fraudulent rtransactions per client :
    - calculated as such: fraudulent transactions per client = count of fraudulent transactions per client when target == 1 else fraudlent transactions = 0.
    - 
* assumed loss per client:
    - calculated as such: assumed loss per client = fraud transactions per client multiplied by the total amount declared to be lost divided by sum of all fraud transactions
    - amount_lost_per_client = (fraudulent_transactions_per_client) * (total_amount_lost / sum of fraudulent transactions) 



<br>
<br>


Assuming the company's internal codes for representing counter status is as follows

---

| feature column | description |
|:--------|:------------------------|
| operational status | 0 - functioning normally <br> 1 - minor issue  <br>  2 - warning for issue higher than 1?  <br> 3 - warning for issue hhigher than 2?.  <br> 4 - critical issue  <br> 5 - special issue? anomaly? | 
|  anomaly - irregular status | A - anomaly (like 5?) |
| ---? status  | 46 - ? <br> 420 - ? <br>  618 - ?  <br> 769 - ?  <br> 269375 - ? |


<br>
<br>


Assuming the company's internal codes for representing the pricing tarrif type is as follows

---

| feature column | description |
|:--------|:------------------------|
|   ?---- tarrifs (seasonal, government etc) |  8  - ? <br> 9 - ? <br>  10 - ?  <br> 18 - ?  <br> 21 - ?  <br> 24 - ? <br>  27 - ?  <br> 29 - ?  <br> 30 - ?  <br> 42 - ?|
| tarrifs (standard, residential, commercial , etc)  | 11 - ? <br> 12 - ?commercial <br>  13 - ?standard  <br> 14 - ?standard  <br> 15 - ?standard |
| ?---- tarrifs (promotional, unique contract, industrial, etc) | 40 - ?  <br> 45 - ? | 
|  anomaly - irregular status | A - anomaly (like 5?) |





<br>

---
---



