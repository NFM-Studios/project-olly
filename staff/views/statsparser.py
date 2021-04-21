from django.shortcuts import render, HttpResponseRedirect, reverse
from django.contrib import messages
from profiles.models import UserProfile
from matches.models import StatsPlayer
import logging


def upload_parse(request):
    messages.success(request, 'Your partner has been created')
    try:
        csv_file = request.FILES["csv_file"]
        if not csv_file.name.endswith('.csv'):
            messages.error(request,'File is not CSV type')
            return HttpResponseRedirect(reverse("staff:upload_parse"))

        #if file is too large, return message
        if csv_file.multiple_chunks():
            messages.error(request,"Uploaded file is too big (%.2f MB)." % (csv_file.size/(1000*1000),))
            return HttpResponseRedirect(reverse("staff:upload_parse"))

        file_data = csv_file.read().decode("utf-8")

        lines = file_data.split("\n")
        #loop over the lines and save them in db. If error shows up , store as string and then display
        for line in lines:
            row = line.split(",")
            data_dict = {}
            data_dict["Name"], data_dict["Rating"], data_dict["Kills"], data_dict["Assists"], \
                            data_dict["Deaths"], data_dict["K_R"], data_dict["ADR"], data_dict["UD"], data_dict["EF"], data_dict["F_Assists"], data_dict["HS"], \
                            data_dict["KAST"], data_dict["AWP_K"],data_dict["two_k"], data_dict["three_k"], data_dict["four_k"], data_dict["five_k"], \
                            data_dict["oneV"], data_dict["twoV"], data_dict["threeV"], data_dict["fourV"], data_dict["fiveV"], data_dict["F_Kills"], data_dict["F_Deaths"], \
                            data_dict["Entries"], data_dict["Trades"],data_dict["Rounds"], data_dict["RF"], data_dict["RA"], data_dict["Damage"] \
                            = row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[1], row[12],\
                              row[13], row[14], row[15], row[16], row[17], row[18], row[19], row[20], row[21], row[22], row[23], row[24], row[25],\
                              row[26], row[27], row[28], row[29], row[30], row[31], row[32]
            try:
                form = StatsPlayer(data_dict)
                if form.is_valid():
                    form.save()
                else:
                    logging.getLogger("error_logger").error(form.errors.as_json())
            except Exception as e:
                logging.getLogger("error_logger").error(repr(e))
                pass

    except Exception as e:
        logging.getLogger("error_logger").error("Unable to upload file. "+repr(e))
        messages.error(request,"Unable to upload CVS file. "+repr(e))

    return HttpResponseRedirect(reverse("staff:upload_parse"))