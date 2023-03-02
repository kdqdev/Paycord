import discord
import datetime
from selenium import webdriver
import asyncio
import os, sys, re
from discord.ext import commands
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import urllib.request, urllib.parse, urllib.error
import urllib.request, urllib.error, urllib.parse
import hmac
import time
import hashlib
import json
import requests

if not os.path.isfile("config.json"):
    sys.exit("config.json not found, please add a config.json file in the same directory")
else:
    with open("config.json") as file:
        config = json.load(file)

subscriptionValue = config["subscriptionValue"]

# class for crypto payments
class CryptoPay:
    def __init__(self):
        self.publicKey = '' # coinpayments public key
        self.privateKey = '' # coinpayments private key
        self.version = 1
        self.format = json
        self.url = 'https://www.coinpayments.net/api.php'

    # creates HMAC(authentication code) to check with CoinPayments API server side if transcation is valid
    def createHmac(self, **params):
        encoded = urllib.parse.urlencode(params).encode('utf-8')
        return encoded, hmac.new(bytearray(self.privateKey, 'utf-8'), encoded, hashlib.sha512).hexdigest()

    # creates the transcation with buyer email/currency/amount
    def create_transactions(self, amount, buyeremail, currency2):
        dict2 = {
            'cmd': 'create_transaction',
            'version': self.version,
            'key': self.publicKey,
            'amount': f'{amount}',
            'currency1': 'USD',
            'currency2': f'{currency2}',
            'buyer_email': f'{buyeremail}',
            'format': self.format
        }
        encoded, hmacvalue = self.createHmac(**dict2)
        headers = {
            'hmac': hmacvalue,
            'Content-Type': 'application/x-www-form-urlencoded'

        }
        res = requests.post(self.url, data=encoded, headers=headers)
        json_value = res.json()
        return json_value['result']['checkout_url']



# use  'xattr -d com.apple.quarantine chromedriver' command where chromedriver is located
# to bypass the trusting a developer error


# urls to visit
loginURL = "https://www.amazon.com/gp/css/gc/balance"
redeemURL = "https://www.amazon.com/gc/redeem?ref_=gcui_b_e_r_c_d"

q = []
crypto_obj = CryptoPay()


# channel for bot to send the messages in certain interval(use developer setting to get channelid)
# channelIDInterval = 849655674371178506
bot = commands.Bot(command_prefix='!', description="Paycord", intents=discord.Intents.all())
driverInstance = None

def startInstance():

    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    DRIVER_BIN = os.path.join(PROJECT_ROOT, "chromedriver")
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(executable_path=DRIVER_BIN, chrome_options=chrome_options)
    driver.get(loginURL)
    time.sleep(2)

    # deprecated version
    # driver.find_element_by_id('ap_email').send_keys(config["email"])
    # driver.find_element_by_id('ap_password').send_keys(config["password"])  # password of amazon account
    # driver.find_element_by_id('signInSubmit').click()
    # time.sleep(2)
    # driver.find_element_by_id('a-autoid-1-announce').click()
    # except:
    #     print("Error: unable to start a selenium instance, Amazon website element id might have changed.")
    #     exit(-1)
    driver.find_element(By.ID, 'ap_email').send_keys(config["email"])
    driver.find_element(By.ID, 'ap_password').send_keys(config["password"])
    driver.find_element(By.ID, 'signInSubmit').click()
    time.sleep(2)
    driver.find_element(By.ID, 'a-autoid-1-announce').click()
    return driver

# my_background_task sends a message every interval to advertise to the users of the server

# async def my_background_task():
#     channel = bot.get_channel(channelIDInterval)
#     while True:
#         embed = discord.Embed(title=f"Guide to get Premium Role",
#                               description="Get whatever is offered",
#                               timestamp=datetime.datetime.utcnow(), color=discord.Color.dark_gold())
#         embed.add_field(name="Instructions?", value=f"Check get-started channel")
#         embed.set_thumbnail(
#             url="") # url can be set to any thumbnail you like
#         await channel.send(embed=embed)
#         await asyncio.sleep(300)  # task runs every 5 minutes

@bot.command()
async def redeemRole(ctx):
    if q:
        await ctx.send("Please wait. Someone is currently redeeming their giftcard. After 30 seconds, you can use this command to redeem.")
    else:
        try:
            q.append(ctx.author.id)
            redeemingRole = discord.utils.get(ctx.guild.roles, name='Redeeming')
            await ctx.author.add_roles(redeemingRole)
            await asyncio.sleep(30)
            await ctx.author.remove_roles(redeemingRole)
        except:
            print("The 'Redeeming' role does not exist in your server")


# allows redeeming role user to redeem
@bot.command(name="redeem")
@commands.has_role('Redeeming')
async def redeem(ctx):
    try:
        element2 = driverInstance.find_element_by_id('gc-captcha-image')
        screenshot = element2.screenshot_as_png
        with open('canvas.png', 'wb') as f:
            f.write(screenshot)
        await ctx.send(
            "Please enter the CAPTCHA below. Use command ***!verifyCode <enter captcha answer here> <enter giftcard code here>***")
        with open('canvas.png', 'rb') as f:
            picture = discord.File(f)
            await ctx.send(file=picture)
    except:
        await ctx.send(
            "Please enter your code. Use command ***!verifyCode AMAZON <enter giftcard code here>*** ")
@redeem.error
async def redeem_error(ctx, error):
    if isinstance(error, (commands.MissingRole, commands.MissingAnyRole)):
        await ctx.send("*You don't have the role to use this command.*")

# only people with redeeming role can redeem their amazon gift card
@bot.command(name="verifyCode")
@commands.has_role('Redeeming')
async def verifyCode(ctx, capCode: str, giftCode:str):
    if capCode == None or giftCode == None:
        await ctx.send("Use the command !verifyCode CAPTCHA_CODE GIFT_CODE")
    submission = False
    while (not submission):
        try:
            if capCode == 'AMAZON':
                driverInstance.find_element_by_id('gc-redemption-input').send_keys(giftCode)
                driverInstance.find_element_by_id('gc-redemption-apply-button').click()
            else:
                driverInstance.find_element_by_id('gc-captcha-code-input').send_keys(capCode)
                driverInstance.find_element_by_id('gc-redemption-input').send_keys(giftCode)
                driverInstance.find_element_by_id('gc-redemption-apply-button').click()
        except:
            print("Error: unable to start a selenium instance, Amazon website element id might have changed.")
            exit(-1)
        html_source = driverInstance.page_source
        submission = True
        cardValue = 0
        if "this gift card claim code is invalid" in html_source or "redeemed in another account" in html_source:
            await ctx.send("Sorry, the code that you entered was invalid.")
        elif "has been added to your":
            pattern = "\$(.*?) has been applied successfully to your account"
            try:
                substring = re.search(pattern, html_source).group(1)
                cardValue = float(substring)
                print(cardValue)
            except:
                await ctx.send("Something went wrong. Please contact owner.")
                break
            if cardValue >= subscriptionValue:
                await ctx.send("Success! You have been assigned Premium role!")
                memberRole = discord.utils.get(ctx.guild.roles, name='Premium')
                await ctx.author.add_roles(memberRole)
            else:
                await ctx.send("Sorry, but your the giftcard that was redeemed value was not enough.")
        else:
            await ctx.send("Something went wrong. Please contact the owner.")


# assigning role test
#@bot.command()
#@commands.has_role('GetRole')
# async def getRole(ctx):
#     await ctx.send("Success! You have been assigned Premium role!")
#     memberRole = discord.utils.get(ctx.guild.roles, name='Premium')
#     await ctx.author.add_roles(memberRole)

# a help command for users to use if they get lost
@bot.command()
async def helpme(ctx):
    embed = discord.Embed(title=f"Guide to get Premium Role",
                          description="Unlock whatever is offered.",
                          timestamp=datetime.datetime.utcnow(), color=discord.Color.dark_gold())
    embed.add_field(name="Instructions?", value=f"Please check the channel #get-started channel")
    embed.set_thumbnail(
        url="") # set url to any thumbnail for helpme command
    await ctx.send(embed=embed)

@bot.command(name="cryptoPay")
async def cryptoPay(ctx, paying_curr=None, buyer_email=None):
    if paying_curr == None or buyer_email == None:
        await ctx.send("Use the command !cryptoPay CURRENCY EMAIL")
        return
    try:
        await ctx.send(crypto_obj.create_transactions(subscriptionValue, buyer_email, paying_curr))
        await ctx.send("After completing the transaction, provide the payment ID to receive role.")
    except:
        print("!cryptoPay command error")

@verifyCode.error
async def on_command_error(ctx, error):
    if isinstance(error, commands.NoPrivateMessage):
        await ctx.send("*Private messages.* ")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("*Command is missing an argument:* ")
    elif isinstance(error, commands.DisabledCommand):
        await ctx.send("*This command is currenlty disabled. Please try again later.* ")
    elif isinstance(error, commands.CheckFailure):
        await ctx.send("*You do not have the permissions to do this.* ")
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send("*This command is not listed in my dictionary.*")
    elif isinstance(error, (commands.MissingRole, commands.MissingAnyRole)):
        await ctx.send("*You don't have the role to use this command.*")


# event to check if bot is ready
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Streaming(name="Amazon GC", url="http://www.twitch.tv/accountname"))
    print('Bot is Ready.')

driverInstance = startInstance()



bot.run(config["token"])
