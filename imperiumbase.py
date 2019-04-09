import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os

ROOT = os.path.dirname(__file__)

# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name(os.path.join(ROOT, 'config/client_secret.json'), scope)

class ImperiumSheet:
    SPREADSHEET_ID = "1t5IoiIjPAS2CD63P6xI4hWwx9c1SEzW9AL1LJ4LK6og"
    ALL_CARDS_SHEET = "All Cards"
    TRAINING_CARDS_SHEET = "Training Cards"
    STARTER_PACK_SHEET="Starter Pack"

    with open(os.path.join(ROOT, 'config/MASTERSHEET_ID'), 'r') as file:
        MASTERSHEET_ID=file.read()

    MASTER_NAME = "Master List"

    CARD_HEADER = [
        "Rarity",
        "Type",
        "Subtype",
        "Card Name",
        "Race",
        "Description",
        "Notes"
    ]
    MASTER_LIST_HEADER = ["Coach"] + CARD_HEADER


    @classmethod
    def cards(cls):
        if hasattr(cls,"_cards"):
            return cls._cards
        # if they are not leaded yet do it
        client = gspread.authorize(creds)
        sheet = client.open_by_key(cls.SPREADSHEET_ID).worksheet(cls.ALL_CARDS_SHEET)
        cls._cards = sheet.get_all_records()
        return cls._cards

    @classmethod
    def starter_cards(cls):
        if hasattr(cls,"_starter_cards"):
            return cls._starter_cards
        # if they are not loaded yet do it
        client = gspread.authorize(creds)
        sheet = client.open_by_key(cls.SPREADSHEET_ID).worksheet(cls.STARTER_PACK_SHEET)
        cls._starter_cards = sheet.get_all_records()
        return cls._starter_cards

    
    @classmethod
    def start_pack_with_count(cls):
        new_collection = {}
        for card in cls.starter_cards():
            if card["Card Name"] in new_collection:
                new_collection[card["Card Name"]]["Quantity"] += 1
            else:
                new_collection[card["Card Name"]] = deepcopy(card)
                new_collection[card["Card Name"]]["Quantity"] = 1
        return list(new_collection.values())


    # TODO needs retesting when/if it will be needed again
    @classmethod
    def store_coach(cls,coach):
        client = gspread.authorize(creds)
        ws = client.open_by_key(cls.MASTERSHEET_ID)

        try:
            sheet = ws.worksheet(coach.name)
        except gspread.exceptions.WorksheetNotFound:
            sheet = ws.add_worksheet(title=coach.name,rows=300, cols=7)

        sheet.clear()

        COACH_CARD_HEADER = [
            "Rarity",
            "Type",
            "Subtype",
            "Card Name",
            "Race",
            "Description",
            "Quantity"
        ]

        cards = []
        cards.append(COACH_CARD_HEADER)

        for card in cls.start_pack_with_count() + coach.collection_with_count():
            cards.append(card)

        cards_amount, keys_amount = len(cards), len(COACH_CARD_HEADER)

        cell_list = sheet.range(f"A1:{gspread.utils.rowcol_to_a1(cards_amount, keys_amount)}")

        for cell in cell_list:
            if cell.row==1:
                cell.value = cards[cell.row-1][cell.col-1]
            else:
                cell.value = cards[cell.row-1][COACH_CARD_HEADER[cell.col-1]]
        sheet.update_cells(cell_list)


    @classmethod
    def store_cards(cls,cards):
        client = gspread.authorize(creds)
        ws = client.open_by_key(cls.MASTERSHEET_ID)
        try:
            sheet = ws.worksheet(cls.MASTER_NAME)
        except gspread.exceptions.WorksheetNotFound:
            sheet = ws.add_worksheet(title=cls.MASTER_NAME,rows=100, cols=15)

        sheet.clear()

        cards.insert(0,cls.MASTER_LIST_HEADER)
        cards_amount, keys_amount = len(cards), len(cls.MASTER_LIST_HEADER)

        cell_list = sheet.range(f"A1:{gspread.utils.rowcol_to_a1(cards_amount, keys_amount)}")

        for cell in cell_list:
            if cell.row==1:
                cell.value = cards[cell.row-1][cell.col-1]
            else:
                cell.value = cards[cell.row-1][cls.MASTER_LIST_HEADER[cell.col-1]]
        sheet.update_cells(cell_list)



#if __name__ == "__main__":
