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

        # Prepare the response data
        if employee_id == "0":
            response_data = []
            for entry in employee_data:
                response_data.append(
                    {
                        "EmployeeID": entry[0],
                        "Name": entry[1],
                        "DOB": entry[2],
                        "Position": entry[3],
                    }
                )
        else:
            found = False
            response_data = {}
            for entry in employee_data:
                if entry[0] == employee_id:
                    found = True
                    response_data = {
                        "EmployeeID": entry[0],
                        "Name": entry[1],
                        "DOB": entry[2],
                        "Position": entry[3],
                    }
                    break

            if not found:
                return func.HttpResponse(
                    f"No entry found for EmployeeID: {employee_id}", status_code=404
                )

        # Return the JSON response
        return func.HttpResponse(
            json.dumps(response_data), status_code=200, mimetype="application/json"
        )

    except Exception as e:
        return func.HttpResponse(f"An error occurred: {str(e)}", status_code=500)
