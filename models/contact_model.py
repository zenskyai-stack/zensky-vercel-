from database.db import insert_contact


class Contact:
    @staticmethod
    def save_contact(name, company, email, phone, service, message):
        insert_contact(name, company, email, phone, service, message)
