import re

def unify_characters(text, select_resemblings=True)->str:
    """Unify different representations of the same characters.\n
    Parameters:
        text (str): The input text.
        select_resemblings (bool): If True, unify characters that are similar in shape but not identical. Useful in OCR generated text post-processing.
    
    Reference: https://en.wikipedia.org/wiki/List_of_Unicode_characters#Semitic_languages"""
     
    text = re.sub(r'[ۃةہەۀۂھۿ]', 'ه', text)
    text = re.sub(r'[ڵڶڷڸ]', 'ل', text)			
    text = re.sub(r'[ڰ-ڴ]', 'گ', text)
    text = re.sub(r'[ىيؿؾؽێۍۑېےۓؠ]', 'ی', text)  					
    text = re.sub(r'[ۋۄۅۆۇۈۊۉۏٷؤٶ]', 'و', text)
    text = re.sub(r'[ػؼكڪګڬڭڮكﻙ]', 'ک', text)
    text = re.sub(r'[إأٱٲٳٵ]', 'ا', text)
    text = re.sub(r'[ڹںڻڼ]', 'ن', text)
    text = re.sub(r'[ړڔڕږڒۯ]', 'ر', text)
    text = re.sub(r'[ٺټ]', 'ت', text) 
    text = re.sub(r'[ٻ]', 'ب', text)  
    text = re.sub(r'[ۺ]', 'ش', text)
    text = re.sub(r'[ۼ]', 'غ', text)
    text = re.sub(r'[ۻ]', 'ض', text)
    text = re.sub(r'[ڝ]', 'ص', text)
    text = re.sub(r'[ڛښ]', 'س', text)
    text = re.sub(r'[ڇڿ]', 'چ', text)
    text = re.sub(r'[ډڊڍ]', 'د', text)
    text = re.sub(r'[ڣ]', 'ف', text)

    text = re.sub(r'[?]', '؟', text)
    text = re.sub(r'[,٬]', '،', text)

					
    arabic_digits = '٠١٢٣٤٥٦٧٨٩'
    persian_digits = '۰۱۲۳۴۵۶۷۸۹'
    translation_table = str.maketrans(arabic_digits, persian_digits)
    text = text.translate(translation_table)
 
 
    if select_resemblings:
        
        text = re.sub(r'[ڃڄ]', 'چ', text)
        text = re.sub(r'[ځڂ]', 'خ', text)
        text = re.sub(r'[ڗڙۋ]', 'ژ', text)
        text = re.sub(r'[ڒۯ]', 'ز', text)
        text = re.sub(r'[ٽٿٹڽ]', 'ث', text)
        text = re.sub(r'[ڜ]', 'ش', text)
        text = re.sub(r'[ڠ]', 'غ', text)
        text = re.sub(r'[ڥ]', 'پ', text)
        text = re.sub(r'[ڤڦڨ]', 'ق', text)
        text = re.sub(r'[ڞ]', 'ض', text)
        text = re.sub(r'[ڋڌڈڎڏڐ]', 'ذ', text)
        text = re.sub(r'[؋]', 'ف', text)
        text = re.sub(r'[ڟ]', 'ظ', text)
         	
    return text