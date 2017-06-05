#!/usr/bin/env python3

import os
import json
import requests
import click
from hearthstone.deckstrings import Deck

db_url = "https://api.hearthstonejson.com/v1/19506/jaJP/cards.collectible.json"
db_path = "./db.json"
hs_format = {
    1: "ワイルド",
    2: "スタンダード",
}
masters_serif = "このデッキを使うには、あんたのクリップボードにコピーして、ハースストーンで新しいデッキを作ってくれ"


if os.path.exists(db_path):
    with open(db_path, "r") as f:
        db = json.loads(f.read())
else:
    response = requests.get(db_url)
    if response.status_code == 200:
        with open(db_path, "w") as f:
            f.write(response.text)
            db = response.json()
    else:
        raise RuntimeError("Couldn't download cards database: %s"
                           % response.text)


@click.group()
def hsd():
    return

def get_carddata(id):
    for data in db:
        if data["dbfId"] == id:
            return data

def sort_cards(cards):
    cards_data = []
    for id, count in cards:
        card = get_carddata(id)
        if count == 1:
            card["amount"] = 1
        else:
            card["amount"] = 2
        cards_data.append(card)
    cards = sorted(cards_data,
        key=lambda card: (card["amount"], card["cost"], card["name"]),
        )
    return cards

def write_deck(deck, name):
    click.echo("### {}".format(name))
    click.echo("# クラス: {}".format(get_carddata(deck.heroes[0])["cardClass"]))
    click.echo("# フォーマット: {}".format(hs_format[deck.format]))
    click.echo("# マンモス年\n#")
    cards = sort_cards(deck.cards)
    for card in cards:
        click.echo("# {amount}x ({cost}) {name}".format(**card))
    click.echo("#\n{}".format(deck.as_deckstring))
    click.echo("#\n# {}".format(masters_serif))
    return

@hsd.command()
@click.argument("code", type=str)
@click.argument("name", type=str, default="Great Deck!")
def decode(code, name):
    deck = Deck.from_deckstring(code)
    return write_deck(deck, name)

if __name__ == "__main__":
    hsd()
