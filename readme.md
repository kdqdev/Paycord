
<br />
<p align="center">
  <a href="https://github.com/kdqdev/Paycord">
    <img src="images/discordlogo.png" alt="Logo" width="70" height="50">
  </a>

  <h1 align="center">Paycord</h1>

<p align="center">
  Amazon Giftcard and Cryptocurrencies Payment Gateway for Discord
</p>





## About The Project

<p align="center">
  <a href="https://github.com/kdqdev/Paycord">
    <img src="images/amazcrypto.jpeg" alt="Logo" width="200" height="200">
  </a>


  
</p>

Paycord was created to allow discord server owner to monetize and receive payment from users in return for a digital service or good. Discord server owner is able to set the price of their good/service. With a price for their good/service set, server owner can accept either Amazon Gift Card or Cryptocurrencies(2,215+ different types), such as Bitcoin. The Amazon Giftcard program was developed with Selenium and cryptocurrency program was created with CoinPayments API.
<br /><br /><br />

## Commands

</br>
Discord Bot command/paramters

> **!redeemRole** - bot will assign user with a 'Redeeming' role and will remove role within 30 seconds so other user can use the bot as well.  Required role to use command !redeem.

> **!redeem** - verify that user has the 'Redeeming' role. Will provide next instruction on how to redeem Amazon giftcard. If  captcha exist, user will be prompted to solve it.

> **!verifyCode** - user will enter their captcha(if provided) or AMAZON and their gift card code. Ex: !verifyCode AMAZON MYCODE123

> **!helpme** - guides user to where to find help with bot commands

> **!cryptoPay** - creates a crypto payment gateway using CoinPayments API and user can click on link given by the bot to pay in a cryptocurrency

### Hidden Command and Function(has to be uncommented to work)

> **!getRole** - only users with "GetRole" role is able to use this command to get the "Premium" role, only to be used in a special scenario 

> **my_background_task(function)**  - bot will send an advertisement about the product/service it is offering every 5 minutes


<br>
</br>


## Video Example

Video Link: [https://drive.google.com/file/d/10v1MJscQQNK0W8ucWT36UcG9g_BEtM-N/view?usp=sharing](https://drive.google.com/file/d/10v1MJscQQNK0W8ucWT36UcG9g_BEtM-N/view?usp=sharing)

<br>
</br>
<br>
</br>


<!-- GETTING STARTED -->
## Getting Started

To get started, just download the the .zip file of the repository or clone it. 

### Important Notes
1. After running the program on the same computer, Amazon will disable the captcha. So after a couple  of captcha input from user, the captcha will disappear.
2. To get coinpayment private/public key, you have to create an account on CoinPayment and create an these keys.
3. Amazon login information(email and password) will have to changed in config.json. Also, you can change the subscriptionValue for the price of your product/service.
4. If there is problem with chromedriver, make sure to put it in the same path as the program and download the chromedriver with respect to the Chrome version that is installed on your computer.

### Installation

1. Click on "Code" and then "Download Zip" and unzip the files
   ```sh
   https://github.com/kdqdev/Paycord
   ```
2. Open the files in an IDE environment
3. For macos, go onto terminal and redirect to the file directory of where chromedriver is located(it should be in the same file with the unzipped files)
4. Use 'xattr -d com.apple.quarantine chromedriver' command without the single quotation mark
5. Now, you won't have the problem with trusting the chromedriver developer 

<br>


<!-- CONTACT -->
## Contact


Project Link: [https://github.com/kdqdev/Paycord](https://github.com/kdqdev/Paycord)
<br>





