from datetime import datetime
from typing import Any
from http import HTTPStatus

from ..interfaces.presenter_interface import PresenterInterface
from ...application.dto.customer_dto import CustomerResponse, CustomerListResponse


class XMLPresenter(PresenterInterface):
    """
    XML presenter for XML API responses.

    In Clean Architecture:
    - This is part of the Interface Adapters layer
    - It formats data for XML responses
    - It demonstrates how to implement different presentation formats
    - It provides consistent XML API response structure
    """

    def present(self, data: Any) -> dict:
        """Present single data item as XML"""
        if isinstance(data, CustomerResponse):
            return self._present_customer_xml(data)
        elif isinstance(data, CustomerListResponse):
            return self._present_customer_list_xml(data)
        else:
            return self._present_generic_xml(data)

    def present_list(self, data_list: list) -> dict:
        """Present list of data as XML"""
        if not data_list:
            return {
                "xml": f"""<?xml version="1.0" encoding="UTF-8"?>
<response>
    <data></data>
    <total_count>0</total_count>
    <timestamp>{self._get_timestamp()}</timestamp>
</response>"""
            }

        # Handle different types of lists
        if all(isinstance(item, CustomerResponse) for item in data_list):
            return self._present_customer_list_xml_from_list(data_list)
        else:
            return self._present_generic_list_xml(data_list)

    def present_error(self, error: Exception) -> dict:
        """Present error as XML"""
        status_code = self._get_error_status_code(error)

        error_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<error>
    <message>{str(error)}</message>
    <type>{type(error).__name__}</type>
    <status_code>{status_code}</status_code>
    <timestamp>{self._get_timestamp()}</timestamp>
</error>"""

        return {"xml": error_xml}

    def _present_customer_xml(self, customer: CustomerResponse) -> dict:
        """Present customer data in XML format"""
        xml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<customer>
    <id>{customer.id or ""}</id>
    <first_name>{customer.first_name}</first_name>
    <last_name>{customer.last_name}</last_name>
    <email>{customer.email}</email>
    <document>{customer.document}</document>
    <full_name>{customer.full_name}</full_name>
    <is_anonymous>{str(customer.is_anonymous).lower()}</is_anonymous>
    <is_registered>{str(customer.is_registered).lower()}</is_registered>
    <created_at>{self._get_timestamp()}</created_at>
</customer>"""

        return {"xml": xml_content}

    def _present_customer_list_xml(self, customer_list: CustomerListResponse) -> dict:
        """Present customer list data in XML format"""
        customers_xml = ""
        for customer in customer_list.customers:
            customers_xml += f"""
    <customer>
        <id>{customer.id or ""}</id>
        <first_name>{customer.first_name}</first_name>
        <last_name>{customer.last_name}</last_name>
        <email>{customer.email}</email>
        <document>{customer.document}</document>
        <full_name>{customer.full_name}</full_name>
        <is_anonymous>{str(customer.is_anonymous).lower()}</is_anonymous>
        <is_registered>{str(customer.is_registered).lower()}</is_registered>
    </customer>"""

        xml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<response>
    <data>{customers_xml}
    </data>
    <total_count>{customer_list.total_count}</total_count>
    <timestamp>{self._get_timestamp()}</timestamp>
</response>"""

        return {"xml": xml_content}

    def _present_customer_list_xml_from_list(self, customers: list) -> dict:
        """Present customer list from list in XML format"""
        customers_xml = ""
        for customer in customers:
            customers_xml += f"""
    <customer>
        <id>{customer.id or ""}</id>
        <first_name>{customer.first_name}</first_name>
        <last_name>{customer.last_name}</last_name>
        <email>{customer.email}</email>
        <document>{customer.document}</document>
        <full_name>{customer.full_name}</full_name>
        <is_anonymous>{str(customer.is_anonymous).lower()}</is_anonymous>
        <is_registered>{str(customer.is_registered).lower()}</is_registered>
    </customer>"""

        xml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<response>
    <data>{customers_xml}
    </data>
    <total_count>{len(customers)}</total_count>
    <timestamp>{self._get_timestamp()}</timestamp>
</response>"""

        return {"xml": xml_content}

    def _present_generic_xml(self, data: Any) -> dict:
        """Present generic data in XML format"""
        if hasattr(data, "__dict__"):
            xml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<response>
    <data>{str(data.__dict__)}</data>
    <timestamp>{self._get_timestamp()}</timestamp>
</response>"""
        else:
            xml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<response>
    <data>{str(data)}</data>
    <timestamp>{self._get_timestamp()}</timestamp>
</response>"""

        return {"xml": xml_content}

    def _present_generic_list_xml(self, data_list: list) -> dict:
        """Present generic list in XML format"""
        items_xml = ""
        for item in data_list:
            items_xml += f"""
    <item>{str(item)}</item>"""

        xml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<response>
    <data>{items_xml}
    </data>
    <total_count>{len(data_list)}</total_count>
    <timestamp>{self._get_timestamp()}</timestamp>
</response>"""

        return {"xml": xml_content}

    def _get_timestamp(self) -> str:
        """Get current timestamp in ISO format"""
        return datetime.utcnow().isoformat() + "Z"

    def _get_error_status_code(self, error: Exception) -> int:
        """Get HTTP status code for error"""
        if hasattr(error, "status_code"):
            return error.status_code
        elif isinstance(error, ValueError):
            return HTTPStatus.BAD_REQUEST
        elif isinstance(error, FileNotFoundError):
            return HTTPStatus.NOT_FOUND
        else:
            return HTTPStatus.INTERNAL_SERVER_ERROR
