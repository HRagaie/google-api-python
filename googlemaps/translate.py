import os
from google.cloud import translate_v2 as translate

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "D:\Bachelor\google-maps-services-python\google-maps-services-python-master\googlemaps\igneous-river-310512-373a899234a0.json"

translate_client = translate.Client()
result = translate_client.translate("شارع عبد الله نور", target_language="en")

print(result)
