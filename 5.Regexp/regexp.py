import csv
import re

with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)


def process_name(contact):
    full_name = ' '.join(contact[:3])

    name_parts = full_name.split()

    if len(name_parts) >= 1:
        contact[0] = name_parts[0]
    if len(name_parts) >= 2:
        contact[1] = name_parts[1]
    if len(name_parts) >= 3:
        contact[2] = name_parts[2]
    elif len(name_parts) == 2:
        contact[2] = ''

    return contact


def process_phone(phone):
    if not phone:
        return ''

    addon_match = re.search(r'доб\.?\s*(\d+)', phone)
    addon = addon_match.group(1) if addon_match else ''

    phone_without_addon = re.sub(r'доб\.?\s*\d+', '', phone)

    digits = re.findall(r'\d', phone_without_addon)
    digits_str = ''.join(digits)

    if digits_str.startswith('8') and len(digits_str) >= 11:
        digits_str = '7' + digits_str[1:]

    if len(digits_str) >= 10:
        base_digits = digits_str[-10:]
    else:
        base_digits = digits_str

    if len(base_digits) >= 10:
        formatted = f"+7({base_digits[:3]}){base_digits[3:6]}-{base_digits[6:8]}-{base_digits[8:10]}"
    else:
        formatted = phone

    if addon:
        formatted += f" доб.{addon}"

    return formatted


for contact in contacts_list[1:]:
    process_name(contact)

    if len(contact) > 5:
        contact[5] = process_phone(contact[5])


def merge_contacts(contact1, contact2):
    """Объединяет два контакта в один"""
    result = contact1.copy()

    for i in range(len(contact1)):
        if not contact1[i] and i < len(contact2) and contact2[i]:
            result[i] = contact2[i]

    return result


contacts_dict = {}

for contact in contacts_list[1:]:
    if len(contact) < 2:
        continue

    key = (contact[0], contact[1])

    if key in contacts_dict:
        contacts_dict[key] = merge_contacts(contacts_dict[key], contact)
    else:
        contacts_dict[key] = contact

merged_contacts = [contacts_list[0]]

for contact in contacts_dict.values():
    merged_contacts.append(contact)

with open("phonebook.csv", "w", encoding="utf-8", newline='') as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(merged_contacts)
