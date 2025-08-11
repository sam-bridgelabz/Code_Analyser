import json
import requests

# Your raw Java code
java_code = """package Arrays;

import java.util.Scanner;

public class Even_Postion_Array {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        System.out.println("Enter the Size of Array");
        int size = sc.nextInt();

        int[] arr = new int[size];

        for (int i = 0; i < arr.length; i++) {
            System.out.println("Enter the Array " + (i + 1) + " :");
            arr[i] = sc.nextInt();
        }

        for (int i = 0; i < arr.length; i += 2) {
            System.out.println("Even Position " + i + " Arrays is :" + arr[i]);
        }
    }
}"""

# Create the request body
payload = {
    "content": java_code,
    "type": "text"
}

# Convert to JSON-safe format
json_safe_string = json.dumps(payload, ensure_ascii=False)

print(json_safe_string)


# Create request body
payload = {
    "content": java_code,
    "type": "text"
}

# Send POST request
url = "http://localhost:8000/github/multi-quality-check"  # Change to your server URL
headers = {"Content-Type": "application/json"}
response = requests.post(url, data=json.dumps(payload), headers=headers)

# Print response
print(response.status_code)
print(response.json())
