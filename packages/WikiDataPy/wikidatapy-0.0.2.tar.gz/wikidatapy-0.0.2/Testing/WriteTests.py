
from WikiDataPy.writer import WikiWriter
import sys
import os

# Add the parent directory to the system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def write_test(w):

    # create / edit entity

    labels = {
        "en": "New Sample Entity by Aryan",
        "fr": "Nouvel exemple d'entité par Aryan"
    }
    descriptions = {
        "en": "This is a newly created sample entity by Aryan",
        "fr": "Il s'agit d'un exemple d'entité nouvellement créé par Aryan"
    }
    res = w.createOrEditEntity(labels=labels, descriptions=descriptions)
    WikiWriter.dumpResult(res, "test_createEntity.json")


def claim_test(w: WikiWriter):
    # create / edit claim
    e = "Q130532046"
    p = "P31"  # instance of
    v = "Q5"  # human
    res = w.addClaim(e, p, v)
    WikiWriter.dumpResult(res, "test_addClaim.json")


def label_test(w: WikiWriter, f):

    ent = "Q130532046"
    lang = "hi"  # hindi
    val = "मैं आर्यन हूं ha"

    data = w.setLabel(ent, lang, val)
    WikiWriter.dumpResult(data, f)


def desc_test(w: WikiWriter, f):

    ent = "Q130532046"
    lang = "hi"  # hindi
    val = "यह एक विवरण है"

    data = w.setDescription(ent, lang, val)
    WikiWriter.dumpResult(data, f)


def set_alias_test(w: WikiWriter, f):

    ent = "Q130532046"
    lang = "en"  # hindi
    # val = "MyEntity_1"
    val = ["MyEntity_1", "MyEntity_2"]

    data = w.setAliases(ent, val, lang)
    WikiWriter.dumpResult(data, f)


def addRem_alias_test(w: WikiWriter, f):

    ent = "Q130532046"
    lang = "en"
    add = ["E2", "E1"]
    remove = ["MyEntity_1"]

    data = w.addRemoveAliases(ent, add, remove, lang)
    WikiWriter.dumpResult(data, f)


print("Hi")
