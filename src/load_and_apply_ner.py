#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import csv
import datetime
import os
import pysolr
import spacy
from spacy import displacy


# In[ ]:


INPUT_MODEL = os.getenv("input_model")
OUTPUT_CSV_FILE = os.getenv("output_csv_file")
INPUT_SOLR_CORE_URL = os.getenv("input_solr_core_url")
print(f"INPUT_SOLR_CORE_URL: {INPUT_SOLR_CORE_URL}")
print(f"INPUT_MODEL: {INPUT_MODEL}")
print(f"OUTPUT_CSV_FILE: {OUTPUT_CSV_FILE}")


# In[ ]:


nlp = spacy.load(INPUT_MODEL)


# In[ ]:


# helper function to display inferenced ner data and its text
def print_with_ner(doc):
    displacy.render(doc, style="ent", jupyter=True)


# In[ ]:


def fetch(pagination_limit=999999):
    solr = pysolr.Solr(INPUT_SOLR_CORE_URL, always_commit=True)
    solr_data = list(solr.search("*:*", rows=pagination_limit))
    solr_id_set = set(sd["id"] for sd in solr_data)
    assert len(solr_data) == len(solr_id_set)
    print(f"length solr_data: {len(solr_data)}")
    return solr_data


# In[ ]:


def parse_persist(solr_data, break_step):
    with open(OUTPUT_CSV_FILE, "w") as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(("id", "start_char", "end_char", "text", "label"))
        data_tmp = []
        for i, entry in enumerate(solr_data):
            # verify
            entry_id = entry["id"]
            text_good = entry["ocrtext_good"]
            assert len(text_good) == 1
            text_good = text_good[0]
            text = entry["ocrtext"]
            assert len(text) == 1
            text = text[0]
            if text_good != text:
                print(f"different texts at {entry_id}")
            # parse
            doc = nlp(text_good)
            for ent in doc.ents:
                assert text_good[ent.start_char:ent.end_char] == ent.text
                data_tmp.append((entry_id, ent.start_char, ent.end_char, ent.text, ent.label_))
            # persist
            if i != 0 and (i % break_step == 0 or i == len(solr_data) - 1):
                print(f"persisting at index: {i}, current id: {entry_id}, {datetime.datetime.now()}")
                for data_row in data_tmp:
                    csv_writer.writerow(data_row)
                data_tmp = []


# In[ ]:


solr_data2 = fetch()


# In[ ]:


# quick helper function to show samples
#for i, sd in enumerate(solr_data2):
#    print(i, sd["id"])


# In[ ]:


parse_persist(solr_data2, 50)

