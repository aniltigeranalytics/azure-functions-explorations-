import azure.functions as func
import csv
import json
import os


def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        # Parse the request body as JSON

        req_body = req.get_json()

        # Extract the required parameters``
        employee_id = req_body.get("EmployeeID")
        name = req_body.get("Name")
        dob = req_body.get("DOB")
        position = req_body.get("Position")

        # Check if any required parameter is missing
        if not employee_id or not name or not dob or not position:
            return func.HttpResponse(
                "Missing required parameters. Please provide EmployeeID, Name, DOB, and Position.",
                status_code=400,
            )

        # Append the entry to the CSV file
        with open(r"../employee_details.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([employee_id, name, dob, position])

        # Prepare the response JSON
        response_data = {
            "EmployeeID": employee_id,
            "Name": name,
            "DOB": dob,
            "Position": position,
        }

        # Return the JSON response
        return func.HttpResponse(
            json.dumps(response_data), status_code=200, mimetype="application/json"
        )

    except Exception as e:
        return func.HttpResponse(f"An error occurred: {str(e)}", status_code=500)
