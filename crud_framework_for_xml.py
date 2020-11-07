import xml.etree.cElementTree as ET

data_file = 'data.xml'
error_opening_file = 'File may not exist or error opening file.'
record_not_found = 'Record not found'
invalid_input = "INVALID INPUT"
 
myroot = ET.parse(data_file)
root = myroot.getroot()

try:
	with open("menu.cfg") as f_menu:
		menu = f_menu.read()
	f_menu.close()
except Exception:
	print(error_opening_file)

try:
	with open("fields_file.cfg") as f_fields:
		field = f_fields.read()
	f_fields.close()
except Exception:
	print(error_opening_file)

fields = eval(field)

try:
	with open("field_variables_file.cfg") as f_variables:
		field_variable = f_variables.read()
	f_variables.close()
except Exception:
	print(error_opening_file)

field_variables = eval(field_variable)

def get_count_of_fields():
	count_of_fields = 0
	for field in fields:
		count_of_fields = count_of_fields + 1
	return count_of_fields

count_of_fields = get_count_of_fields()

def search_if_record_exists(user_input_id):
	is_record_exist = False
	for field_values in root.findall('record'):
		record_id = field_values.find(field_variables[0]).text
		if record_id == user_input_id:
			is_record_exist = True
	return is_record_exist

def new_id():
    maxid = 0
    for field_values in root.findall('record'):
        id= int(field_values.find('id').text)
        if id>maxid:
            maxid=id
    return maxid+1

def create_record():
	print("Enter", fields[0] + ":", end = "")
	user_input_id = input()
	is_record_exist = search_if_record_exists(user_input_id)
	if is_record_exist == True:
		print("Record already exist")
	else:
		new_record_id = str(new_id())
		status = 'active'
		newrecord = ET.SubElement(root, "record",id=new_record_id)
		ET.SubElement(newrecord, "id", name = "id").text = new_record_id
		ET.SubElement(newrecord, "status", name = "status").text = status
		ET.SubElement(newrecord, "account_number", name = "account_number").text = user_input_id

		for field_counter in range(1, count_of_fields):
			print("Enter " , fields[field_counter] + ":" ,end = "")
			field_value = input()
			ET.SubElement(newrecord, field_variables[field_counter], name = field_variables[field_counter]).text = field_value
		print("Record saved successfully.")
		myroot.write(data_file)
		
def show_all_records():
	field_counter = 0
	count_of_active_records = 0
	count_of_records = 0
	try:
		for field_values in root.findall('record'):
			count_of_records = count_of_records + 1
			status =root[field_counter][1].text
			field_counter = field_counter + 1
			if status == 'active':
				count_of_active_records = count_of_active_records + 1
				show_record(count_of_records)
				print("----------------------")
	except Exception:
		print("No XML data present in file.")
	print("Count of records: " + str(count_of_active_records))

def search_record():
	print("Enter", fields[0] + ":", end = "")
	user_input_id = input()
	is_record_exist = search_if_record_exists(user_input_id)
	for field_values in root.findall('record'):
		record_id = field_values.find(field_variables[0]).text
		if record_id == user_input_id:
			count_of_record = field_values.find("id").text
			status = field_values.find('status').text
			if status == 'active':
				show_record(count_of_record)
	if is_record_exist == False:
		print(record_not_found)		

def show_record(count_of_record):
	for counter in range(0,count_of_fields):
		print(fields[counter] + ":", end="")
		print(root[int(count_of_record) - 1][int(counter) + 2].text)
		counter = counter + 1

def deactivate_record():
	print("Enter", fields[0] + ":", end = "")
	user_input_id = input()
	is_record_exist = search_if_record_exists(user_input_id)
	for field_values in root.findall('record'):
		record_id = field_values.find(field_variables[0]).text
		if record_id == user_input_id:
			count_records = field_values.find("id").text
			status = field_values.find('status').text
			if status == 'active':
				field_values.find('status').text = 'inactive'
		else:
			print("Record not found.")
	try:		
		myroot.write(data_file)
		print("Record deactivated successfully.")
	except Exception:
		print(record_not_found)

def update_record():
	print("Enter", fields[0] + ":", end = "")
	user_input_id = input()
	is_record_exist = search_if_record_exists(user_input_id)
	for field_values in root.findall('record'):
		record_id = field_values.find(field_variables[0]).text
		if record_id == user_input_id:
			count_records = field_values.find("id").text
			status = field_values.find('status').text
			if status == 'active':
				for counter in range(1, count_of_fields):
					print(str(counter) + ". Update "+ fields[counter])
			user_option = int(input("Enter option: "))
			if user_option >= 1 and user_option < count_of_fields:
				print("Enter new " + fields[user_option] + ": ", end="")
				updated_data = input()
				field_values.find(field_variables[user_option]).text = updated_data
		else:
			print(record_not_found)
	try:
		myroot.write(data_file)
		print("Record updated successfully.")
	except Exception:
		print("Error updating record.")

functions_list = [create_record, show_all_records, search_record, update_record, deactivate_record, exit]

while True:
	print(menu)
	try:
		user_option = int(input("Enter option: "))
	except Exception:
		print(invalid_input)
		continue
	if user_option >=1 and user_option <= 6:
		functions_list[user_option - 1]()
	else:
		print(invalid_input)
	
