from django.apps import AppConfig
from django.apps import AppConfig
from watson import search as watson



class DatabaseConfig(AppConfig):
    name = 'database'

    def ready(self):
        Vendor = self.get_model("Vendor")
        watson.register(Vendor)

        Employee = self.get_model("Employee")
        watson.register(Employee)

        GoogleGroup = self.get_model("GoogleGroup")
        watson.register(GoogleGroup)

        Partner = self.get_model("Partner")
        watson.register(Partner)

        Customer = self.get_model("Customer")
        watson.register(Customer)

        Contract = self.get_model("Contract")
        watson.register(Contract)

        Department = self.get_model("Department")
        watson.register(Department)

        POC = self.get_model("POC")
        watson.register(POC)


