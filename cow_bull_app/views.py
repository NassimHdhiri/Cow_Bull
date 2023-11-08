from spyne.service import ServiceBase
from spyne.decorator import rpc
from spyne.model.primitive import Unicode, Integer
from spyne.application import Application
from spyne.protocol.soap import soap11
from spyne.server.django import DjangoApplication
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import random


# Create your views here.
class GameServices(ServiceBase):

    _result = ""
    _playerName = ""
    _hiddenNumber = ""
    _nbrOfAttemps = ""

    # AboutGame
    def AboutGame():  # Add self parameter to all instance methods
        GameDescription = """Welcome to the Number Guessing Game!    
        We will generate a random 4-digit number.
        Your task is to guess this number.

        There are three possible outcomes:

        1. If you guess the number correctly, you will receive the message "4B CONGRATULATIONS!"

        2. If some of the digits are in the correct positions, you will receive a message with the number of correct digits (Bulls) and the number of incorrect digits (Cows). Unfortunately, you lose.

        3. If you run out of attempts without guessing the correct number, you will also lose. You will be provided with the number of Bulls and Cows for the final attempt.

        Good luck with your guesses!"""

        return GameDescription

    # StartGame
    @rpc(Unicode(nillable=False), Integer(nillable=False))
    def StartGame(self,PlayerName="Guess player", NbrOfAttemps=10):  # Add self parameter
        # Assignment of name's player
        GameServices._playerName = PlayerName

        # Assignment of proposition's player
        GameServices._nbrOfAttemps = NbrOfAttemps

        # handle random number
        firstDigit = random.randint(1, 9)

        if firstDigit == 0:
            firstDigit = 1 + random.randint(1, 8)

        otherDigits = random.sample(range(10), 3)  # Use range(10) to get a list of digits
        random.shuffle(otherDigits)

        GameServices._hiddenNumber = str(firstDigit) + "".join(map(str, otherDigits))  # Convert to a string

        return f" Go Go Go !!! The game is started {GameServices._playerName} secret number is {GameServices._hiddenNumber}"

    # PlayGame
    @rpc(Integer(nullable=False))  # Add return type
    def PlayGame(self,playerProposition):
        if GameServices._nbrOfAttemps == 1 and GameServices._result != "4C":
            return f'Oops! Unfortunately, you lose!'

        if GameServices._nbrOfAttemps >= 1 and GameServices._nbrOfAttemps <= 10 and GameServices._result != "4B":
            return "You win!!!"

        proposition = str(playerProposition)

        result = GameServices.evaluate_proposition(proposition)

        if result == '4B':
            result += " " + GameServices._playerName + " Congratulations! You have won the game"

        return result

    @staticmethod
    def evaluate_proposition(proposition):
        try:
            if len(proposition) < 4:
                raise ValueError("You must enter a proposition of 4 digits!")

            hidden_number = list(GameServices._hiddenNumber)
            _nbrCow = 0
            _nbrBull = 0

            for i in range(4):
                if int(proposition[i]) == int(GameServices._hiddenNumber[i]):  # Convert to int for comparison
                    _nbrBull += 1
                elif int(proposition[i]) in map(int, hidden_number):  # Convert to int for comparison
                    _nbrCow += 1

            GameServices._nbrOfAttemps -= 1

            if _nbrBull == 0 and _nbrCow > 0:
                return f"{_nbrCow}C"
            elif _nbrBull > 0 and _nbrCow == 0:
                return f"{_nbrBull}B"
            else:
                return f"{_nbrBull}B-{_nbrCow}C"

        except Exception as e:
            return str(e)

# Create a SOAP application
spyne_app = Application(
    [GameServices],
    tns="http.soa.tn",
    in_protocol=soap11(validator='lxml'),
    out_protocol=soap11()
)

# Create a Django application with SOAP architecture
django_app = DjangoApplication(spyne_app)

# Create a Django app without CSRF protection
cb_game = csrf_exempt(django_app)
