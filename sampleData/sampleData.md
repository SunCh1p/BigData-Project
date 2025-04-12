# Sample Data Directory
- Will have very large (200k entries), large (1k entries), and small (20 entries) CSVs for :
	- Input (to-be anonymized)
	- Reference (For attacker to associate with) - see notes below

* Reference file will exclude some pre-selected 'sensitive' column which will attempt to be used for the attack.

* Data Note:

	* Reference file will also include ADDITIONAL entries which are not stored in our client's database. 

	* Input file will include ADDITIONAL entries which are not stored in our attacker's database. 

	* This offers a 'realistic' scenario, where the attacker does not already know who may be contained within the database.

1. UIDs kept for validation - allows definite way of verifying whether or not two users are equivalent across databases. 
	* NOTE: will generate 2 versions of data - with/without uid. 

---
## Dataset info: 
Available data columns:
* "uid","name","age","gender","zip","disease"
	- Attacker has: "uid" (1), "name", "age", "gender", "zip"
	- Client has: "uid" (1),"name","age","gender","zip","disease"
	- Client publishes: "uid" (1),"age","gender","zip","disease"

* uid ONLY for verification of attack success/fail. It would not be published in a real scenario.

### **Attacker goal**: associate "name" with "disease".
---
## File info:
* sampleData.md 
	* this file
* sampleDataGen.py
	* Script to generate datasets depending on in-file configuration. Depends on 'random, time, namemaker*, string, pandas, sys' libraries
		* namemaker is a non-standard library. Installable with pip, see: https://github.com/Rickmsd/namemaker/tree/main
* files with *_nouid : drops uid column

* files with attackerData* / clientData* : self-explanatory

* Values \*\_a-b\_\* : the a stands for the 'target' datasize, ie. the number of rows in attacker/client data. The b stands for how many rows will be randomly dropped when forming the attacker and client data - from the debug dataset size of a+b

* debug_fullDataset* : full dataset used per-parameter configuration, ignore in trials.
---
(for v1.0.1)
* Exec time for 200,000 target, 20,000 drop : real    8m19.779s | user    8m18.940s | sys     0m0.114s
* Exec time for 200,000 target, 100,000 drop : real    15m52.145s | user    15m50.856s | sys     0m0.115s