from django.shortcuts import render, HttpResponse

import logging

logger = logging.getLogger(__name__)


# Create your views here.
def loggertest(request):
    logger.error("Error logger")
    logger.info("Info logger")
    logger.critical("critical logger")
    logger.debug("debug logger")
    logger.warning("warning logger")
    return HttpResponse("Please check your server console")