
###################################################################

import logging

from lxf.ai.ocr.ocr import doOcr_from_pdf
from lxf import settings



logger = logging.getLogger('iban extractor')
fh = logging.FileHandler('./logs/iban_extractor.log')
fh.setLevel(settings.get_logging_level())
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.setLevel(settings.get_logging_level())
logger.addHandler(fh)
#################################################################
from lxf.extractors.finance.ibans.iban_analyzer import IbanAnalyzer
from lxf.services.try_safe import try_safe_execute_async


async def extract_data(file_path:str)->str:
    """
    Extrait les données d'un iban 
    """
    result = await try_safe_execute_async(logger,doOcr_from_pdf, path_filename=file_path)
    if result!=None :
        analyzer:IbanAnalyzer= IbanAnalyzer(result)
        return await try_safe_execute_async(logger,analyzer.do_analyze)
    return result