from django.conf import settings


def site_settings(request):
    return {
        "CLUB_NAME": "Unión de Radioaficionados de Vigo - Val Miñor",
        "CLUB_SHORT_NAME": "URV EA1RKV",
        "CLUB_CALLSIGN": "EA1RKV",
        "CLUB_ADDRESS": "c/ Galindra, 16, 36213 Vigo (Pontevedra)",
        "CLUB_PHONE": "986 290 249",
        "CLUB_MOBILE": "600 088 937",
        "CLUB_EMAIL": "seccion.vigo@ure.es",
        "CLUB_FACEBOOK": "URE VIGO VAL MIÑOR EA1RKV",
    }
