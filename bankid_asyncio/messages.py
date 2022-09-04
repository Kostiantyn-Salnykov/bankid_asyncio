import enum

RFA1 = "Start your BankID app."
RFA2 = "The BankID app is not installed. Please contact your internet bank."
RFA3 = "Action cancelled. Please try again."
RFA4 = "An identification or signing for this personal number is already started. Please try again."
RFA5 = "Internal error. Please try again."
RFA6 = "Action cancelled."
RFA8 = """The BankID app is not responding. Please check that the program is started and that you have internet access. 
If you don’t have a valid BankID you can get one from your bank. Try again."""
RFA9 = "Enter your security code in the BankID app and select Identify or Sign."
RFA13 = "Trying to start your BankID app."
RFA14_A = """
Searching for BankID:s, it may take a little while… If a few seconds have passed and still no BankID has been found, 
you probably don’t have a BankID which can be used for this identification/signing on this computer. 
If you have a BankID card, please insert it into your card reader. 
If you don’t have a BankID you can order one from your internet bank. 
If you have a BankID on another device you can start the BankID app on that device.
"""
RFA14_B = """
Searching for BankID:s, it may take a little while… If a few seconds have passed and still no BankID has been found, 
you probably don’t have a BankID which can be used for this identification/signing on this device. 
If you don’t have a BankID you can order one from your internet bank. 
If you have a BankID on another device you can start the BankID app on that device.
"""
RFA15_A = """
Searching for BankID:s, it may take a little while… If a few seconds have passed and still no BankID has been found, 
you probably don’t have a BankID which can be used for this identification/signing on this computer. 
If you have a BankID card, please insert it into your card reader. 
If you don’t have a BankID you can order one from your internet bank.
"""
RFA15_B = """
Searching for BankID:s, it may take a little while… If a few seconds have passed and still no BankID has been found, 
you probably don’t have a BankID which can be used for this identification/signing on this device. 
If you don’t have a BankID you can order one from your internet bank.
"""
RFA16 = """The BankID you are trying to use is revoked or too old. Please use another BankID or order a new one from 
your internet bank."""
RFA17_A = """
The BankID app couldn’t be found on your computer or mobile device. 
Please install it and order a BankID from your internet bank. 
Install the app from your app store or https://install.bankid.com.
"""
RFA17_B = """
Failed to scan the QR code. Start the BankID app and scan the QR code. Check that the BankID app is up to date. 
If you don't have the BankID app, you need to install it and order a BankID from your internet bank. 
Install the app from your app store or https://install.bankid.com.
"""
RFA18 = "Start the BankID app."
RFA19 = "Would you like to identify yourself or sign with a BankID on this computer or with a Mobile BankID?"
RFA20 = "Would you like to identify yourself or sign with a BankID on this device or with a BankID on another device?"
RFA21 = "Identification or signing in progress."
RFA22 = "Unknown error. Please try again."


class Messages(str, enum.Enum):
    RFA1 = RFA1
    RFA2 = RFA2
    RFA3 = RFA3
    RFA4 = RFA4
    RFA5 = RFA5
    RFA6 = RFA6
    RFA8 = RFA8
    RFA9 = RFA9
    RFA13 = RFA13
    RFA14_A = RFA14_A
    RFA14_B = RFA14_B
    RFA15_A = RFA15_A
    RFA15_B = RFA15_B
    RFA16 = RFA16
    RFA17_A = RFA17_A
    RFA17_B = RFA17_B
    RFA18 = RFA18
    RFA19 = RFA19
    RFA20 = RFA20
    RFA21 = RFA21
    RFA22 = RFA22
