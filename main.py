import functools
import os.path

import numpy as np
import yaml
import pandas as pd
import zipfile

from messsage import generate_message
from send_emails import santa_emails

PARTECIPANTS_FILE = "participants.csv"
EXCLUSION_FILE = "exclusions.yaml"
OUTFOLDER = "out"
ATTEMPTS = 100
MAIL_SUBJECT = "SSID 2022"


def load_exclusions(file):
    with open(file, 'r') as f:
        exclusions = yaml.safe_load(f)
    return exclusions


def load_participants(csv):
    parts = pd.read_csv(csv)
    return parts[['email', 'name']]


def secret_santa(names, exclusions):
    integrity_checks(names, exclusions)

    # santa loop
    i = 0
    santa_fail = True
    while santa_fail and i < ATTEMPTS:
        print(f"Attempt {i + 1}...", end=" ")
        # shuffle
        shuffled = names.sample(frac=1).reset_index(drop=True)
        # shift
        shifted = shuffled.reindex(index=np.roll(shuffled.index, -1)).reset_index(drop=True)
        santa_table = pd.DataFrame({"santa": shuffled, "child": shifted})
        santa_fail = not check_exclusions(santa_table, exclusions)
        print("failed" if santa_fail else "succeeded!!")
        i += 1
    if santa_fail:
        print("Generation failed\n"
              "Maybe you were unlucky\n"
              "Or maybe you added so many exclusions that there are no solutions!!!")
    else:
        generate_files(santa_table, OUTFOLDER)


def integrity_checks(names, exclusions):
    duplicates = names.duplicated()
    if duplicates.any():
        msg = f"Duplicates in names!!\n" \
              f"{names[duplicates]}"
        raise ValueError(msg)
    excluded_set = functools.reduce(set.union, (map(set, exclusions.values())))
    if not excluded_set.issubset(set(names)):
        msg = f"Set of exclusions:\n" \
              f"{excluded_set}\n" \
              f"Set of names:\n" \
              f"{set(names)}\n" \
              f"Missing:\n" \
              f"{excluded_set - set(names)}\n"
        raise ValueError(msg)


def check_exclusions(table, exclusions):
    for name, excluded in exclusions.items():
        child = table[table['santa'] == name]["child"].item()
        if child in excluded:
            return False
    return True


def generate_files(table, path):
    os.makedirs(path, exist_ok=True)
    os.chdir(path)

    def get_message(table_row):
        i, (santa, child) = table_row
        return generate_message(santa, child)

    def generate_file(table_row):
        i, (santa, child, message) = table_row
        fname = santa + ".txt"
        with open(fname, "w") as f:
            f.write(message)
        return fname

    def generate_zip(santa, txt):
        fname = santa + ".zip"
        with zipfile.ZipFile(fname, "w") as zip_txt:
            zip_txt.write(txt)

    table['message'] = list(map(get_message, table.iterrows()))
    table['txt'] = list(map(generate_file, table.iterrows()))
    for i, (santa, child, messages, txt) in table.iterrows():
        generate_zip(santa, txt)

    for i, (santa, child, message, txt) in table.iterrows():
        os.remove(txt)
        # hash check
        print(f"{hash(santa)} -> {hash(child)}")

    os.chdir("..")


if __name__ == '__main__':
    participants = load_participants(PARTECIPANTS_FILE)
    exclusions = load_exclusions(EXCLUSION_FILE)
    secret_santa(participants['name'], exclusions)
    santa_emails(participants, OUTFOLDER, MAIL_SUBJECT)
