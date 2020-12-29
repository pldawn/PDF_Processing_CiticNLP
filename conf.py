
environment = "standard"  # standard, customized

if environment == "standard":
    from conf_standard import *

if environment == "customized":
    from conf_customized import *
