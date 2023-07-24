import azure.functions as func
import csv
import json


def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        req_body = req.get_json()

        # Extract the required parameters``
        employee_id = req_body.get("EmployeeID")
        # Parse the query parameters

        # Check if EmployeeID is provided
        if employee_id is None:
            return func.HttpResponse(
                "Missing required parameter. Please provide EmployeeID.",
                status_code=400,
            )

        # Read the CSV file
        with open(r"../employee_details.csv", "r") as file:
            reader = csv.reader(file)
            employee_data = list(reader)

        # Find the entry with the specified EmployeeID
        entry_found = False
        deleted_entry = {}
        updated_employee_data = []

        for entry in employee_data:
            if entry[0] == employee_id:
                entry_found = True
                deleted_entry = {
                    "EmployeeID": entry[0],
                    "Name": entry[1],
                    "DOB": entry[2],
                    "Position": entry[3],
                }
            else:
                updated_employee_data.append(entry)

        # Check if the entry was found
        if not entry_found:
            return func.HttpResponse(
                f"No entry found for EmployeeID: {employee_id}", status_code=404
            )

        # Write the updated data back to the CSV file
        with open(r"../employee_details.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(updated_employee_data)

        # Return the JSON response of the deleted entry
        return func.HttpResponse(
            json.dumps(deleted_entry), status_code=200, mimetype="application/json"
        )

    except Exception as e:
        return func.HttpResponse(f"An error occurred: {str(e)}", status_code=500)
