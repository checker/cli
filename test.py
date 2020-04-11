import requests

possibleCharacters = []
possibleCharacters[:0] = 'abcdefghijklmnopqrstuvwxyz0123456789'
print(possibleCharacters)
finalString = ""

for character in possibleCharacters:
    finalString = 