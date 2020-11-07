import xml.etree.cElementTree as ET


data_file = 'bank_data.xml'
error_opening_file = 'File may not exist or error opening file.'

 
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
	for field_values in root.findall('account'):
		record_id = field_values.find(field_variables[0]).text
		if record_id == user_input_id:
			is_record_exist = True
	return is_record_exist

def new_id():
    maxid = 0
    for field_values in root.findall('account'):
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
		newrecord = ET.SubElement(root, "account",id=new_record_id)
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
	count_records = 0
	count_of_active_records = 0
	try:
		for field_values in root.findall('account'):
			count_records = count_records + 1
			status =root[field_counter][1].text
			field_counter = field_counter + 1
			if status == 'active':
				count_of_active_records = count_of_active_records + 1
				for counter in range(0,count_of_fields):
					print(fields[counter] + ":", end="")
					print(root[count_records - 1][counter + 2].text)
					counter = counter + 1
				print("----------------------")
	except Exception:
		print("No xml data present in file.")
	print("Count of records: " + str(count_of_active_records))


def search_record():
	print("Enter", fields[0] + ":", end = "")
	user_input_id = input()
	is_record_exist = search_if_record_exists(user_input_id)
	for field_values in root.findall('account'):
		record_id = field_values.find(field_variables[0]).text
		if record_id == user_input_id:
			count_records = field_values.find("id").text
			status = field_values.find('status').text
			if status == 'active':
				for counter in range(0,count_of_fields):
					print(fields[counter] + ":", end="")
					print(root[int(count_records) - 1][int(counter) + 2].text)
					counter = counter + 1
				




def deactivate_record():
	print("Enter", fields[0] + ":", end = "")
	user_input_id = input()
	is_record_exist = search_if_record_exists(user_input_id)
	for field_values in root.findall('account'):
		record_id = field_values.find(field_variables[0]).text
		if record_id == user_input_id:
			count_records = field_values.find("id").text
			status = field_values.find('status').text
			if status == 'active':
				field_values.find('status').text = 'inactive'
	try:		
		myroot.write(data_file)
		print("Record deactivated successfully.")
	except Exception:
		print("Error deactivating record.")




def update_record():
	print("Enter", fields[0] + ":", end = "")
	user_input_id = input()
	is_record_exist = search_if_record_exists(user_input_id)
	for field_values in root.findall('account'):
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
	try:
		myroot.write(data_file)
		print("Record updated successfully.")
	except Exception:
		print("Error updating record.")


functions_list = [create_record, show_all_records, search_record, update_record, deactivate_record, exit]


while True:
	print(menu)
	user_option = int(input("Enter option: "))
	functions_list[user_option - 1]()
