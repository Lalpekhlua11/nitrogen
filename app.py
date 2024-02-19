import aiohttp
import asyncio
import random
import string
import time

# Discord webhook URL
discord_webhook_url = "https://discord.com/api/webhooks/1208546726768541766/6VMGGQCc0NNQIEd-ODSkBYsakNGuO4mxFb0V2B5-7LJuiKRqPEmSlmHYPMQDIhGbqGFI"

async def send_webhook(message):
    async with aiohttp.ClientSession() as session:
        payload = {"content": message}
        async with session.post(discord_webhook_url, json=payload) as response:
            pass

async def generate_and_check_codes():
    generated_codes = 0
    start_time = time.time()
    while True:
        generated_code = generate_random_string(16)
        log_generated_code(generated_code)
        await check_gift_code(generated_code)
        generated_codes += 1
        current_time = time.time()
        elapsed_time = current_time - start_time
        if elapsed_time >= 1:  # Check every second
            print(f"Generated {generated_codes} codes in {elapsed_time:.2f} seconds")
            start_time = current_time
            generated_codes = 0

async def check_gift_code(code):
    url = f"https://discordapp.com/api/v9/entitlements/gift-codes/{code}?with_application=false&with_subscription_plan=true"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                gift_link = generate_gift_link(code)
                await send_webhook(f"Valid Gift Code Found: {gift_link}")

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

async def main():
    tasks = [generate_and_check_codes() for _ in range(100)]  # Adjust the number of tasks as needed
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
