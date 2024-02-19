import requests
import random
import string
import time

# Discord webhook URL
discord_webhook_url = "https://discord.com/api/webhooks/1208546726768541766/6VMGGQCc0NNQIEd-ODSkBYsakNGuO4mxFb0V2B5-7LJuiKRqPEmSlmHYPMQDIhGbqGFI"

def send_webhook(message):
    payload = {"content": message}
    requests.post(discord_webhook_url, json=payload)

def generate_random_string(length):
    num_digits = random.randint(1, length)  # Ensure at least one digit in the string
    num_letters = length - num_digits
    digits = ''.join(random.choices(string.digits, k=num_digits))
    letters = ''.join(random.choices(string.ascii_letters, k=num_letters))
    return ''.join(random.sample(digits + letters, len(digits + letters)))

def generate_gift_link(code):
    return f"https://discord.gift/{code}"

def log_generated_code(code):
    print(f"Generated Code: {code}")

def check_gift_code(code):
    url = f"https://discordapp.com/api/v9/entitlements/gift-codes/{code}?with_application=false&with_subscription_plan=true"
    response = requests.get(url)
    if response.status_code == 200:
        gift_link = generate_gift_link(code)
        send_webhook(f"Valid Gift Code Found: {gift_link}")

def main():
    while True:
        generated_code = generate_random_string(16)
        log_generated_code(generated_code)
        check_gift_code(generated_code)
        time.sleep(0.1)  # Adjust this delay as needed, here set to 0.1 seconds

if __name__ == "__main__":
    main()
