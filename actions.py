# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
# from rasa_sdk import Action, Tracker #type: ignore
# from rasa_sdk.executor import CollectingDispatcher #type: ignore


# class ActionSayData(Action):

#     def name(self) -> Text:
#         return "action_say_data"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
#         name = tracker.get_slot("name")
#         city = tracker.get_slot("city")
#         phone = tracker.get_slot("phone")

#         dispatcher.utter_message(text=f"Hey {name}, {city} is a vey beautiful place. Your phone number is {phone}")
        

       

#         return []

# import pandas as pd
# from typing import Any, Text, Dict, List
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher

# # Load CSV once at startup
# df = pd.read_csv(r"C:\Users\KIIT\Downloads\RASA\actions\IIT_NIT.csv")

# class ActionSayIITResult(Action):

#     def name(self) -> Text:
#         return "action_say_iit_result"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         name= tracker.get_slot("name")
#         city = tracker.get_slot("city")
#         rank = tracker.get_slot("rank")

#         try:
#             rank_int = int(rank)
#         except:
#             dispatcher.utter_message(text="Please enter a valid rank.")
#             return []
        

#         # Filter rows where the rank is within opening-closing range
#     eligible = df[
#         (df["opening_rank"] <= rank_int) &
#         (df["closing_rank"] >= rank_int)
#         ] 

#     if eligible.empty:
#         dispatcher.utter_message(
#             text=f"Hey {name}! With rank {rank}, no matching IIT/NIT branch was found."
#             )
#             return []

#     best_row = eligible.sort_values(by="closing_rank").iloc[0]

#     institute = best_row["institute_short"]
#     branch = best_row["program_name"]

#     dispatcher.utter_message(
#         text=f"Hey {name}! With rank {rank} from {city}, "
#             f"you can get **{branch}** at **{institute}**."
#         )

#            return []




# import pandas as pd
# from typing import Any, Text, Dict, List
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
# from rasa_sdk.events import AllSlotsReset 


# CSV_PATH = r"C:\Users\KIIT\Downloads\RASA\actions\IIT_NIT.csv"

# # Load CSV
# try:
#     df = pd.read_csv(CSV_PATH)
# except Exception as e:
#     print(f"[ERROR] Could not read CSV: {e}")
#     df = pd.DataFrame(columns=["institute_short", "program_name", "opening_rank", "closing_rank"])

# # Clean institute names
# def trim_institute(name: Any) -> str:
#     if isinstance(name, str):
#         return name.replace("IIT-", "").replace("NIT-", "").strip()
#     return ""

# df["institute_trimmed"] = df["institute_short"].astype(str).apply(trim_institute)

# # ======================================================
# # FALLBACK ACTION: FORCE CAPTURE NUMERIC RANK
# # ======================================================
# class ActionResetSlots(Action):

#     def name(self) -> Text:
#         return "action_reset_slots"

#     def run(self, dispatcher, tracker, domain):
#      dispatcher.utter_message(
#             text=" All details have been reset. Let's start again.\nPlease tell me your JEE rank."
#         )
#         return [AllSlotsReset()]

# # ======================================================
# # MAIN RESULT ACTION
# # ======================================================
# class ActionSayIITResult(Action):

#     def name(self) -> Text:
#         return "action_say_iit_result"

#     def run(
#         self,
#         dispatcher: CollectingDispatcher,
#         tracker: Tracker,
#         domain: Dict[Text, Any]
#     ) -> List[Dict[Text, Any]]:

#         rank = tracker.get_slot("rank")
#         name = tracker.get_slot("name") or "there"
#         city = tracker.get_slot("city") or ""

#         if not rank:
#             dispatcher.utter_message(text="Please provide your rank.")
#             return []

#         try:
#             rank = int(rank)
#         except:
#             dispatcher.utter_message(text="Please enter a valid numeric rank.")
#             return []

#         city_clean = city.lower().strip()

#         df_temp = df.copy()
#         df_temp["opening"] = pd.to_numeric(df_temp["opening_rank"], errors="coerce")
#         df_temp["closing"] = pd.to_numeric(df_temp["closing_rank"], errors="coerce")

#         eligible = df_temp[
#             (df_temp["opening"] <= rank) &
#             (df_temp["closing"] >= rank)
#         ]

#         if eligible.empty:
#             dispatcher.utter_message(
#                 text=f"Hey {name}, no IIT/NIT branch found for rank {rank}."
#             )
#             return []

#         eligible["city_match"] = eligible["institute_trimmed"].str.lower() == city_clean

#         if not eligible[eligible["city_match"]].empty:
#             best = eligible[eligible["city_match"]].iloc[0]
#         else:
#             best = eligible.sort_values(by="closing").iloc[0]

#         dispatcher.utter_message(
#             text=f"Hey {name}! With rank {rank} and city {city}, "
#                  f"you can get **{best['program_name']}** at **{best['institute_short']}**."
#         )

#         return []
    

import pandas as pd
import os
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, AllSlotsReset, FollowupAction
import re

# ================= FOLDER PATH =================
FOLDER_PATH = r"C:\Users\KIIT\Downloads\RASA\actions"

df_list = []

# Load ALL CSV files automatically
for file in os.listdir(FOLDER_PATH):
    if file.endswith(".csv"):
        try:
            full_path = os.path.join(FOLDER_PATH, file)
            temp = pd.read_csv(full_path)

            # Remove first 2 rows (title rows)
            temp = temp.iloc[2:].reset_index(drop=True)

            # Rename columns dynamically
            temp = temp.rename(columns={
                temp.columns[0]: "institute_short",
                temp.columns[1]: "program_name",
                temp.columns[5]: "opening_rank",
                temp.columns[6]: "closing_rank"
            })

            temp = temp[["institute_short","program_name","opening_rank","closing_rank"]]

            temp["opening_rank"] = pd.to_numeric(temp["opening_rank"], errors="coerce")
            temp["closing_rank"] = pd.to_numeric(temp["closing_rank"], errors="coerce")

            df_list.append(temp)

            print(f"Loaded file: {file}")

        except Exception as e:
            print(f"Error loading {file}: {e}")

# Combine all CSVs
if df_list:
    df = pd.concat(df_list, ignore_index=True)
else:
    print("No CSV files loaded!")
    df = pd.DataFrame(columns=["institute_short","program_name","opening_rank","closing_rank"])

# Clean institute name
def trim_institute(name: Any) -> str:
    if isinstance(name, str):
        return name.strip()
    return ""

df["institute_trimmed"] = df["institute_short"].astype(str).apply(trim_institute)

# ======================================================
# ACTION 1: FORCE CAPTURE NUMERIC RANK
# ======================================================
class ActionSetRankFromText(Action):

    def name(self) -> Text:
        return "action_set_rank_from_text"

    def run(self, dispatcher, tracker, domain):
        text = tracker.latest_message.get("text", "")
        match = re.search(r"\b\d+\b", text)
        if match:
            return [SlotSet("rank", match.group())]
        return []





# class ActionSayIITResult(Action):

#     def name(self) -> Text:
#         return "action_say_iit_result"

#     def run(self, dispatcher, tracker, domain):

#         name = tracker.get_slot("name") or "Student"
#         city = tracker.get_slot("city")
#         rank = tracker.get_slot("rank")

#         if not rank:
#             dispatcher.utter_message(text="Please provide your rank.")
#             return []

#         try:
#             rank = int(rank)
#         except:
#             dispatcher.utter_message(text="Please enter a valid numeric rank.")
#             return []

#         city_clean = city.lower().strip() if city else ""

#         df_temp = df.copy()

#         eligible = df_temp[
#             (df_temp["opening_rank"] <= rank) &
#             (df_temp["closing_rank"] >= rank)
#         ]

#         if eligible.empty:
#             dispatcher.utter_message(
#                 text=f"Sorry {name}, no suitable college found for rank {rank}."
#             )
#             return []

#         eligible = eligible.copy()
#         eligible["city_match"] = eligible["institute_trimmed"].str.lower() == city_clean

#         if not eligible[eligible["city_match"]].empty:
#             best = eligible[eligible["city_match"]].iloc[0]
#         else:
#             best = eligible.sort_values(by="closing_rank").iloc[0]

#         dispatcher.utter_message(
#             text=f"Hey {name}! With rank {rank}, you can get {best['program_name']} at {best['institute_short']}."
#         )

#         return []

class ActionSayIITResult(Action):

    def name(self) -> Text:
        return "action_say_iit_result"

    def run(self, dispatcher, tracker, domain):

        name = tracker.get_slot("name") or "Student"
        city = tracker.get_slot("city")
        rank = tracker.get_slot("rank")

        if not rank:
            dispatcher.utter_message(text="Please provide your rank.")
            return []

        try:
            rank = int(rank)
        except:
            dispatcher.utter_message(text="Please enter a valid numeric rank.")
            return []

        df_temp = df.copy()

        # Find all colleges where student rank fits
        eligible = df_temp[
            (df_temp["opening_rank"] <= rank) &
            (df_temp["closing_rank"] >= rank)
        ].copy()

        if eligible.empty:
            dispatcher.utter_message(
                text=f"Sorry {name}, no suitable college found for rank {rank}."
            )
            return []

        # Calculate probability score
        eligible["score"] = eligible["closing_rank"] - rank

        # Sort by best probability
        eligible = eligible.sort_values(by="score")

        # Select Top 5
        top5 = eligible.head(5)

        message = f"🎓 Top 5 Colleges for Rank {rank}:\n\n"

        for i, row in enumerate(top5.itertuples(), 1):
            message += f"{i}. {row.program_name} at {row.institute_short}\n"

        dispatcher.utter_message(text=message)

        return []  



class ActionResetSlots(Action):

    def name(self) -> Text:
        return "action_reset_slots"

    def run(self, dispatcher, tracker, domain):

        dispatcher.utter_message(
            text="🔄 Chat reset. Starting again."
        )
   
        return [
            AllSlotsReset(),               
            SlotSet("requested_slot", None),            
            FollowupAction("admission_form")  
        ]

    

        

 


