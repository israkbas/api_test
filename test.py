import os
import json
import requests

def perform_http_requests(endpoints_directory):
    headers = {'Authorization': 'Bearer [YOUR_TOKEN_ACCESS]'}

    with open("all_tests_results.txt", "w") as result_file, \
            open("pass.txt", "w") as pass_file:
        
        for filename in os.listdir(endpoints_directory):
            if filename.endswith('.json'):
                result_file.write(f"\n***********\nProcessing file: {filename}\n")

                with open(os.path.join(endpoints_directory, filename), 'r') as file:
                    try:
                        json_data = json.load(file)
                    except json.JSONDecodeError as json_error:
                        result_file.write(f"Error: JSON decoding failed for {filename}\n")
                        result_file.write(f"Error Details: {json_error}\n")
                        continue

                    category_name = filename[:-5]
                    result_file.write(f"Category: {category_name}\n")

                    for endpoint in json_data.get(category_name, []):
                        result_file.write(f"\nProcessing endpoint: {endpoint}\n")

                        method = endpoint.get("method", "")
                        url = endpoint.get("url", "")
                        response_code = endpoint.get("response_code", "")
                        proceed = endpoint.get("proceed", False)

                        if 'url_parameters' in endpoint:
                            url_parameters = endpoint.get('url_parameters', {})
                            url = url.format(**url_parameters)

                        if proceed:
                            url += "?proceed=true"

                        data = endpoint.get("data", {})

                        response = None

                        try:
                            if method == 'GET':
                                response = requests.get(url, headers=headers)
                            elif method == 'POST':
                                response = requests.post(url, json=data, headers=headers)
                            elif method == 'PUT':
                                response = requests.put(url, json=data, headers=headers)
                            elif method == 'PATCH':
                                response = requests.patch(url, headers=headers)
                            elif method == 'DELETE':
                                response = requests.delete(url, headers=headers)

                            if response is not None:
                                result_file.write(f"URL: {url}\n")
                                result_file.write(f"Expected Status Code: {response_code}\n")
                                result_file.write(f"Actual Status Code: {response.status_code}\n")

                                if response.status_code == response_code:
                                    result_file.write("Result: PASS\n")
                                    pass_file.write(f"Endpoint: {url} \nMethod: {method}\n")
                                    pass_file.write(f"Expected Status Code: {response_code}\n")
                                    pass_file.write(f"Actual Status Code: {response.status_code}\n \n")
                                else:
                                    result_file.write("Result: FAIL\n")
                                    result_file.write(f"Error Message: {response.text}\n")

                                    failed_file_path = f"failed_{response.status_code}_tests.txt"
                                    if not os.path.isfile(failed_file_path):
                                        with open(failed_file_path, "w"):
                                            pass

                                    with open(failed_file_path, "r") as failed_file:
                                        error_exists = any(f"Category: {category_name}" in line for line in failed_file)
                                        if not error_exists:
                                            with open(failed_file_path, "a") as failed_file_append:
                                                failed_file_append.write(f"Category: {category_name} \nEndpoint: {url} \nMethod: {method}\n")
                                                failed_file_append.write(f"Expected Status Code: {response_code}\n")
                                                failed_file_append.write(f"Actual Status Code: {response.status_code}\n")
                                                failed_file_append.write(f"Error Message: {response.text}\n \n")

                            else:
                                result_file.write(f"Unsupported method: {method}\n")
                        except requests.RequestException as req_error:
                            result_file.write(f"An error occurred during the request: {req_error}\n")
                            result_file.write("Result: FAIL\n")

                        
                            failed_file_path = f"failed_{response.status_code}_tests.txt"
                            if not os.path.isfile(failed_file_path):
                                with open(failed_file_path, "w"):
                                    pass

                            with open(failed_file_path, "r") as failed_file:
                                error_exists = any(f"Category: {category_name}" in line for line in failed_file)
                                if not error_exists:
                                    with open(failed_file_path, "a") as failed_file_append:
                                        failed_file_append.write(f"Category: {category_name} \nEndpoint: {url}\n")
                                        failed_file_append.write(f"Error Message: {req_error}\n")

    print("All tests completed.")

endpoints_directory = r"C:/Users/pc_name/Desktop/new_folder/test_json" //YOUR JSON FOLDER PATH 
perform_http_requests(endpoints_directory)
